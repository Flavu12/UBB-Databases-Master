from plan import ExecutionPlan, ExecutionStep


def reorder_joins(query, catalog, base_rows):
    remaining_joins = query.joins[:]
    ordered_joins = []

    current_tables = {query.from_table}
    current_rows = base_rows

    while remaining_joins:
        best_join = None
        best_result_rows = float("inf")

        for join in remaining_joins:
            # join valid: un tabel e deja in rezultat
            if join.left_table in current_tables and join.right_table not in current_tables:
                left_table = catalog.get_table(join.left_table)
                right_table = catalog.get_table(join.right_table)
                next_table = join.right_table

            elif join.right_table in current_tables and join.left_table not in current_tables:
                left_table = catalog.get_table(join.right_table)
                right_table = catalog.get_table(join.left_table)
                next_table = join.left_table

            else:
                continue  # evitam produs cartezian

            FR = estimate_join_selectivity(
                left_table,
                right_table,
                join.left_column,
                join.right_column
            )

            estimated_result = current_rows * right_table.n_tuples * FR

            if estimated_result < best_result_rows:
                best_result_rows = estimated_result
                best_join = join
                best_next_table = next_table

        if best_join is None:
            break

        ordered_joins.append(best_join)
        remaining_joins.remove(best_join)

        current_tables.add(best_next_table)
        current_rows = best_result_rows

    return ordered_joins


def estimate_selectivity(condition, table_catalog):
    stats = table_catalog.column_stats.get(condition.column)
    if stats is None:
        return 0.3

    if condition.operator == "=":
        if stats.n_keys and stats.n_keys > 0:
            return 1 / stats.n_keys
        return 0.1

    if stats.low is None or stats.high is None:
        return 0.5

    val = condition.value

    if condition.operator in (">", ">="):
        return max(0.0, (stats.high - val) / (stats.high - stats.low))

    if condition.operator in ("<", "<="):
        return max(0.0, (val - stats.low) / (stats.high - stats.low))

    if condition.operator == "!=":
        if stats.n_keys and stats.n_keys > 0:
            return 1 - (1 / stats.n_keys)
        return 0.9

    return 0.5


def estimate_join_selectivity(left_table, right_table, left_col, right_col):
    stats_left = left_table.column_stats.get(left_col)
    stats_right = right_table.column_stats.get(right_col)

    if stats_left is None or stats_right is None:
        return 0.1

    if stats_left.n_keys and stats_right.n_keys:
        return 1 / max(stats_left.n_keys, stats_right.n_keys)

    return 0.1


def find_join_index(table, column):
    for idx in table.indexes:
        if column in idx.columns:
            return idx
    return None


def estimate_snlj_cost(outer_rows, inner_table):
    return outer_rows * inner_table.n_pages


def expected_matches(inner_table, inner_index):
    if inner_index and inner_index.n_keys > 0:
        return max(1.0, inner_table.n_tuples / inner_index.n_keys)
    return 1.0


def record_lookup_cost(inner_table, inner_index):
    # index search cost
    index_search = inner_index.height if (inner_index and inner_index.height) else 3  # fallback 2-4

    # record read cost dep de clusterizare
    if inner_index and inner_index.clustered:
        record_read = 1.0
    else:
        record_read = expected_matches(inner_table, inner_index)

    return index_search + record_read


def estimate_inlj_cost(outer_rows, inner_table, inner_index):
    lookup = record_lookup_cost(inner_table, inner_index)
    cost = outer_rows * lookup
    return cost


def optimizer(query, catalog):
    plan = ExecutionPlan()

    # Alege tipul de scanare
    table_obj = catalog.get_table(query.from_table)

    # Calc factorul de reductie
    fr_prod = 1.0
    for cond in query.where:
        if cond.table == table_obj.name:
            fr_prod *= estimate_selectivity(cond, table_obj)

    # Estimare randuri dupa selectie
    estimated_rows = max(1, int(table_obj.n_tuples * fr_prod))

    # Cost Table scan
    best_method = "Table Scan"
    best_index = None
    best_cost = table_obj.n_pages

    # Cost Unclustered index scan
    for idx in table_obj.indexes:
        if any(cond.table == table_obj.name and cond.column in idx.columns for cond in query.where):
            index_cost = (idx.n_pages + table_obj.n_tuples) * fr_prod
            if index_cost < best_cost:
                best_cost = index_cost
                best_method = "Unclustered Index Scan"
                best_index = idx

    # Adauga pas la plan
    details = {"estimated_rows": estimated_rows}
    if best_index:
        details["index"] = best_index.name

    plan.add_step(ExecutionStep(
        best_method,
        table_obj.name,
        details=details,
        cost=int(best_cost)
    )
)

    # Ordonare joinuri

    ordered_joins = reorder_joins(query, catalog, estimated_rows)

    current_rows = estimated_rows
    current_tables = {query.from_table}

    for join in ordered_joins:
        if join.left_table in current_tables:
            outer_table = catalog.get_table(join.left_table)
            inner_table = catalog.get_table(join.right_table)
            join_col_inner = join.right_column
            next_table = join.right_table
        else:
            outer_table = catalog.get_table(join.right_table)
            inner_table = catalog.get_table(join.left_table)
            join_col_inner = join.left_column
            next_table = join.left_table

        join_FR = estimate_join_selectivity(
            outer_table,
            inner_table,
            join.left_column,
            join.right_column
        )

        join_rows = current_rows * inner_table.n_tuples * join_FR

        # Cost SNLJ
        cost_nlj = estimate_snlj_cost(current_rows, inner_table)

        # Cost INLJ (daca exista index)
        index = find_join_index(inner_table, join_col_inner)
        cost_inlj = float("inf")

        if index:
            cost_inlj = estimate_inlj_cost(
                outer_rows=current_rows,
                inner_table=inner_table,
                inner_index=index
            )

        # Alegem algoritmul
        if cost_inlj < cost_nlj:
            plan.add_step(
                ExecutionStep(
                    "Index Nested Loop Join",
                    table=f"{outer_table.name} ⋈ {inner_table.name}",
                    details={
                        "index": index.name,
                        "on": f"{join.left_column}={join.right_column}",
                        "estimated_rows": int(join_rows)
                    },
                    cost=int(cost_inlj)
                )
            )
        else:
            plan.add_step(
                ExecutionStep(
                    "Simple Nested Loop Join",
                    table=f"{outer_table.name} ⋈ {inner_table.name}",
                    details={
                        "on": f"{join.left_column}={join.right_column}",
                        "estimated_rows": int(join_rows)
                    },
                    cost=int(cost_nlj)
                )
            )

        current_tables.add(next_table)
        current_rows = join_rows

    return plan
