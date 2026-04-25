class SelectQuery:
    def __init__(self, select_columns, from_table, joins=None, where=None):
        self.select_columns = select_columns
        self.from_table = from_table
        self.joins = joins or []  # list of Join objects
        self.where = where or []  # list of Condition objects

    def get_tables(self):
        tables = {self.from_table}
        for join in self.joins:
            tables.add(join.right_table)
        return tables

    def get_conditions_for_table(self, table_name):
        return [c for c in self.where if c.table == table_name]



    def __repr__(self):
        return (f"SelectQuery(select_columns={self.select_columns}, "
                f"from_table={self.from_table}, joins={self.joins}, where={self.where})")


class Join:
    def __init__(self, left_table, right_table, left_column, right_column, join_type="INNER"):
        self.left_table = left_table
        self.right_table = right_table
        self.left_column = left_column
        self.right_column = right_column
        self.join_type = join_type

    def __repr__(self):
        return (f"Join({self.left_table}.{self.left_column} {self.join_type} "
                f"{self.right_table}.{self.right_column})")


class Condition:
    def __init__(self, table, column, operator, value):
        self.table = table
        self.column = column
        self.operator = operator
        self.value = value

    def is_equality(self):
        return self.operator == "="

    def is_range(self):
        return self.operator in (">", ">=", "<", "<=")

    def __repr__(self):
        return f"Condition({self.table}.{self.column} {self.operator} {self.value})"
