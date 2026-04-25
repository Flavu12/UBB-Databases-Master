indexes = {
    "owners": [
        {
            "name": "idx_owners_city",
            "columns": ["city"],
            "clustered": False
        }
    ],

    "pets": [
        {
            "name": "idx_pets_owner",
            "columns": ["owner_id"],
            "clustered": False
        }
    ],

    "visits": [
        {
            "name": "idx_visits",
            "columns": ["pet_id", "visit_date"], 
            "clustered": False
        }
    ]

}
