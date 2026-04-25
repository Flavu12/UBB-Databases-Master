from catalog import db_catalog
from optimizer import optimizer
from query import SelectQuery, Join, Condition



q1 = SelectQuery(
    select_columns=["*"],
    from_table="owners",
    where=[
        Condition("owners", "city", "=", "Bucharest")
    ]
)

plan1 = optimizer(q1, db_catalog)
#plan1.explain()


q2 = SelectQuery(
    select_columns=["*"],
    from_table="owners",
    joins=[
        Join("owners", "pets", "owner_id", "owner_id")
    ],
    where=[
        Condition("owners", "city", "=", "Bucharest")
    ]
)

plan2 = optimizer(q2, db_catalog)
#plan2.explain()



q3 = SelectQuery(
    select_columns=["*"],
    from_table="pets",
    joins=[
        Join("pets", "visits", "pet_id", "pet_id"),
        Join("visits", "prescriptions", "visit_id", "visit_id")
    ],
    where=[
        Condition("visits", "visit_date", ">=", "2024-01-01")
    ]
)

plan3 = optimizer(q3, db_catalog)
#plan3.explain()

q4 = SelectQuery(
    select_columns=["*"],
    from_table="owners",
    joins=[
        Join("owners", "pets", "owner_id", "owner_id"),
        Join("pets", "visits", "pet_id", "pet_id"),
        Join("visits", "prescriptions", "visit_id", "visit_id"),
        Join("visits", "vets", "vet_id", "vet_id"),
    ],
    where=[
        Condition("owners", "city", "=", "Bucharest"),
        Condition("visits", "visit_date", ">=", "2024-01-01")
    ]
)

plan4 = optimizer(q4, db_catalog)
plan4.explain()
