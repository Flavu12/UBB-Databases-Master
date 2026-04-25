-- index pentru cautarea tratamentelor dupa nume
CREATE INDEX idx_treatments_name ON treatments(treatment_name);

-- index pentru cautarea animalelor unui anumit proprietar
CREATE INDEX idx_pets_owner_id ON pets(owner_id);

-- index pentru cautarea proprietarilor dupa nume
CREATE INDEX idx_owners_name ON owners(owner_name);

-- index pentru a cauta toate animalele care au primit un tratament
CREATE INDEX idx_pet_treatments ON pet_treatments(treatment_id);