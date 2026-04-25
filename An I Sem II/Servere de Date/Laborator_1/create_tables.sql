-- Creare tabele 

CREATE TABLE owners (
    owner_id NUMBER PRIMARY KEY,
    owner_name VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) NOT NULL,
    phone_number VARCHAR2(15),
    CONSTRAINT owners_email UNIQUE (email),
    CONSTRAINT owners_phone UNIQUE (phone_number)
);

CREATE TABLE pets (
    pet_id NUMBER PRIMARY KEY,
    owner_id NUMBER NOT NULL,
    pet_name VARCHAR2(50) NOT NULL,
    weight NUMBER CHECK(weight > 0),
    birth_date DATE,
    CONSTRAINT fk_pets_owner FOREIGN KEY (owner_id) REFERENCES owners(owner_id)
);

CREATE TABLE treatments (
    treatment_id NUMBER PRIMARY KEY,
    treatment_name VARCHAR2(100) NOT NULL,
    treatment_price NUMBER NOT NULL,
    treatment_duration NUMBER NOT NULL,
    CONSTRAINT treatment_price_const CHECK (treatment_price >= 0),
    CONSTRAINT treatment_duration_const CHECK (treatment_duration > 0)
);

CREATE TABLE pet_treatments (
    pet_id NUMBER,
    treatment_id NUMBER,
    notes VARCHAR2(200),
    CONSTRAINT pk_pet_treatments PRIMARY KEY (pet_id, treatment_id),
    CONSTRAINT fk_pet FOREIGN KEY (pet_id) REFERENCES pets(pet_id),
    CONSTRAINT fk_treatment FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id)
);

-- Comentarii 
COMMENT ON TABLE owners IS 'Tabela cu proprietarii animalelor';
COMMENT ON COLUMN owners.email IS 'Adresa de email, unica pentru fiecare proprietar';
COMMENT ON COLUMN owners.phone_number IS 'Numar de telefon, unic daca este completat';

COMMENT ON TABLE pets IS 'Tabela cu animalele de companie';
COMMENT ON COLUMN pets.pet_id IS 'Identificator unic al animalului';
COMMENT ON COLUMN pets.weight IS 'Greutatea animalului in kilograme';

COMMENT ON TABLE treatments IS 'Tabela cu tipurile de tratamente';
COMMENT ON COLUMN treatments.treatment_duration IS 'Durata tratamentului in zile';

-- Tip definit de utilizator 
CREATE TYPE pet_description_t AS OBJECT (
    pet_type VARCHAR2(10),
    gender CHAR(1)
);

-- Adaugare coloana noua 
ALTER TABLE pets ADD(pet_description pet_description_t);