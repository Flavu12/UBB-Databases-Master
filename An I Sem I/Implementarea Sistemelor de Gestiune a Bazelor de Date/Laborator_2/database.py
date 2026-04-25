database = {
    "owners": {
        "columns": {
            "owner_id": "int",
            "full_name": "string",
            "city": "string",
            "age": "int",
            "created_at": "date",
        },
        "primary_key": ["owner_id"]
    },

    "pets": {
        "columns": {
            "pet_id": "int",
            "owner_id": "int",
            "name": "string",
            "species": "string",
            "breed": "string",
            "birth_year": "int",
        },
        "primary_key": ["pet_id"],
        "foreign_keys": {
            "owner_id": ("owners", "owner_id"),
        }
    },

    "vets": {
        "columns": {
            "vet_id": "int",
            "full_name": "string",
            "specialty": "string",
            "hire_date": "date",
        },
        "primary_key": ["vet_id"]
    },

    "visits": {
        "columns": {
            "visit_id": "int",
            "pet_id": "int",
            "vet_id": "int",
            "visit_date": "date",
            "reason": "string",
        },
        "primary_key": ["visit_id"],
        "foreign_keys": {
            "pet_id": ("pets", "pet_id"),
            "vet_id": ("vets", "vet_id"),
        }
    },

    "prescriptions": {
        "columns": {
            "prescription_id": "int",
            "visit_id": "int",
            "drug": "string",
            "dose_mg": "int",
            "days": "int",
        },
        "primary_key": ["prescription_id"],
        "foreign_keys": {
            "visit_id": ("visits", "visit_id"),
        }
    }
}
