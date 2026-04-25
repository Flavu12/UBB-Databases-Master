from database import database


class IndexCatalog:
    def __init__(self, name, columns, clustered=False, n_keys=0, n_pages=0, height=None, low=None, high=None):
        self.name = name
        self.columns = columns
        self.clustered = clustered
        self.n_keys = n_keys        # nr de val distincte ale cheilor
        self.n_pages = n_pages      # nr de pag pentru index
        self.height = height        # inaltime arbore
        self.low = low              # val min a cheii
        self.high = high            # val max a cheii

    def __repr__(self):
        return (f"IndexCatalog({self.name}, columns={self.columns}, clustered={self.clustered}, "
                f"NKeys={self.n_keys}, NPages={self.n_pages}, Height={self.height}, Low={self.low}, High={self.high})")


class ColumnStats:
    def __init__(self, n_keys=None, low=None, high=None):
        self.n_keys = n_keys      # nr val distincte
        self.low = low            # min val
        self.high = high          # max val

    def __repr__(self):
        return f"ColumnStats(NKeys={self.n_keys}, Low={self.low}, High={self.high})"


class TableCatalog:
    def __init__(self, name, columns, primary_key, foreign_keys=None, indexes=None, n_tuples=0, n_pages=0, column_stats=None):
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        self.foreign_keys = foreign_keys or {}
        self.indexes = indexes or []
        self.n_tuples = n_tuples    # nr inregistrari 
        self.n_pages = n_pages      # nr pagini 
        self.column_stats = column_stats or {}

    def add_index(self, index):
        self.indexes.append(index)

    def __repr__(self):
        return (f"TableCatalog({self.name}, NTuples={self.n_tuples}, NPages={self.n_pages}, "
                f"PrimaryKey={self.primary_key}, Indexes={self.indexes})")


class DatabaseCatalog:
    def __init__(self):
        self.tables = {}

    def add_table(self, table):
        self.tables[table.name] = table

    def get_table(self, table_name):
        return self.tables.get(table_name)

    def __repr__(self):
        return f"DatabaseCatalog(tables={list(self.tables.keys())})"


# Initializare catalog DB

db_catalog = DatabaseCatalog()

# Tabel: owners
owners = TableCatalog(
    name="owners",
    columns=database["owners"]["columns"],
    primary_key=database["owners"]["primary_key"],
    n_tuples=50_000,
    n_pages=2_500,
    column_stats={
        "owner_id": ColumnStats(n_keys=50_000, low=1, high=50_000),
        "city": ColumnStats(n_keys=200),     # ex: ~200 orase
        "age": ColumnStats(n_keys=80, low=1, high=100)
    }
)
owners.add_index(IndexCatalog(
    name="idx_owners_city",
    columns=["city"],
    clustered=False,
    n_keys=200,
    n_pages=80,
    height=3,
    low=1,
    high=200
))
db_catalog.add_table(owners)

# Tabel: pets
pets = TableCatalog(
    name="pets",
    columns=database["pets"]["columns"],
    primary_key=database["pets"]["primary_key"],
    foreign_keys=database["pets"].get("foreign_keys", {}),
    n_tuples=120_000,
    n_pages=6_000,
    column_stats={
        "pet_id": ColumnStats(n_keys=120_000, low=1, high=120_000),
        "owner_id": ColumnStats(n_keys=50_000, low=1, high=50_000),
        "species": ColumnStats(n_keys=12),
        "breed": ColumnStats(n_keys=300),
        "birth_year": ColumnStats(n_keys=40, low=1985, high=2025)
    }
)
pets.add_index(IndexCatalog(
    name="idx_pets_owner",
    columns=["owner_id"],
    clustered=False,
    n_keys=50_000,
    n_pages=300,
    height=3,
    low=1,
    high=50_000
))
db_catalog.add_table(pets)

# Tabel: vets
vets = TableCatalog(
    name="vets",
    columns=database["vets"]["columns"],
    primary_key=database["vets"]["primary_key"],
    n_tuples=1_000,
    n_pages=80,
    column_stats={
        "vet_id": ColumnStats(n_keys=1_000, low=1, high=1_000),
        "specialty": ColumnStats(n_keys=40),
    }
)
db_catalog.add_table(vets)

# Tabel: visits
visits = TableCatalog(
    name="visits",
    columns=database["visits"]["columns"],
    primary_key=database["visits"]["primary_key"],
    foreign_keys=database["visits"].get("foreign_keys", {}),
    n_tuples=900_000,
    n_pages=55_000,
    column_stats={
        "visit_id": ColumnStats(n_keys=900_000, low=1, high=900_000),
        "pet_id": ColumnStats(n_keys=120_000, low=1, high=120_000),
        "vet_id": ColumnStats(n_keys=1_000, low=1, high=1_000),
        "visit_date": ColumnStats(n_keys=3_650, low=1, high=3_650)  # ~10 ani zile (aprox)
    }
)
# index compus 
visits.add_index(IndexCatalog(
    name="idx_visits",
    columns=["pet_id", "visit_date"],
    clustered=False,
    n_keys=900_000,
    n_pages=4_000,
    height=4,
    low=1,
    high=900_000
))
db_catalog.add_table(visits)

# Tabel: prescriptions
prescriptions = TableCatalog(
    name="prescriptions",
    columns=database["prescriptions"]["columns"],
    primary_key=database["prescriptions"]["primary_key"],
    foreign_keys=database["prescriptions"].get("foreign_keys", {}),
    n_tuples=1_800_000,
    n_pages=120_000,
    column_stats={
        "prescription_id": ColumnStats(n_keys=1_800_000, low=1, high=1_800_000),
        "visit_id": ColumnStats(n_keys=900_000, low=1, high=900_000),
        "drug": ColumnStats(n_keys=5_000),
    }
)
db_catalog.add_table(prescriptions)
