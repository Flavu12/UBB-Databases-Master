-- popularea tabelei owners
INSERT INTO owners (owner_id, owner_name, email, phone_number)
VALUES (1, 'Ana Popescu', 'ana.popescu@gmail.com', '0711111111');

INSERT INTO owners (owner_id, owner_name, email, phone_number)
VALUES (2, 'Mihai Ionescu', 'mihai.ionescu@gmail.com', '0722222222');

INSERT INTO owners (owner_id, owner_name, email)
VALUES (3, 'Elena Georgescu', 'elena.georgescu@gmail.com');

--popularea tabelei pets

INSERT INTO pets (pet_id, owner_id, pet_name, weight, birth_date, pet_description)
VALUES (10, 1, 'Rex', 12.5, DATE '2020-05-10', pet_description_t('dog', 'M'));

INSERT INTO pets (pet_id, owner_id, pet_name, weight, birth_date, pet_description)
VALUES (11, 1, 'Luna', 4.2, DATE '2022-03-01', pet_description_t('CAT', 'F'));

INSERT INTO pets (pet_id, owner_id, pet_name, weight, birth_date, pet_description)
VALUES (12, 2, 'Pufulet', 2, DATE '2025-01-12', pet_description_t('Rabbit', 'F'));

INSERT INTO pets (pet_id, owner_id, pet_name, weight, birth_date)
VALUES (13, 2, 'Max', 18.7, DATE '2019-11-20');


--Popularea tabelei treatments
INSERT INTO treatments (treatment_id, treatment_name, treatment_price, treatment_duration)
VALUES (100, 'Vaccin', 150, 1);

INSERT INTO treatments (treatment_id, treatment_name, treatment_price, treatment_duration)
VALUES (101, 'Consultatie', 100, 1);

INSERT INTO treatments (treatment_id, treatment_name, treatment_price, treatment_duration)
VALUES (102, 'Deparazitare', 80, 1);

INSERT INTO treatments VALUES (1, 'Vaccin', 100, 1);
INSERT INTO treatments VALUES (2, 'Vaccin', 120, 1);
INSERT INTO treatments VALUES (3, 'Vaccin', 150, 1);

INSERT INTO treatments VALUES (4, 'Consultatie', 80, 1);
INSERT INTO treatments VALUES (5, 'Consultatie', 100, 1);
INSERT INTO treatments VALUES (6, 'Consultatie', 130, 1);

--Popularea tabelei pet_treatments
INSERT INTO pet_treatments (pet_id, treatment_id, notes)
VALUES (10, 100, 'vaccinare anuala');

INSERT INTO pet_treatments (pet_id, treatment_id, notes)
VALUES (10, 101, 'control general');

INSERT INTO pet_treatments (pet_id, treatment_id, notes)
VALUES (11, 102, 'tratament preventiv');


-- Inserturi invalide 
-- cheie primara duplicata
INSERT INTO owners (owner_id, owner_name, email, phone_number)
VALUES (1, 'Test', 'test1@gmail.com', '0700000000');

-- cheie unica duplicata pe email
INSERT INTO owners (owner_id, owner_name, email, phone_number)
VALUES (4, 'Test', 'ana.popescu@gmail.com', '0744444444');

-- cheie unica duplicata pe telefon
INSERT INTO owners (owner_id, owner_name, email, phone_number)
VALUES (5, 'Test', 'test@gmail.com', '0711111111');

-- foreign key invalid: owner_id nu exista
INSERT INTO pets (pet_id, owner_id, pet_name, weight, birth_date)
VALUES (20, 999, 'Fluffy', 5.5, DATE '2022-01-01');

-- weight <= 0
INSERT INTO pets (pet_id, owner_id, pet_name, weight, birth_date)
VALUES (21, 1, 'Zero', 0, DATE '2022-01-01');

--treatment_price negativ
INSERT INTO treatments (treatment_id, treatment_name, treatment_price, treatment_duration)
VALUES (103, 'Tratament gresit', -10, 2);

-- treatment_duration <= 0
INSERT INTO treatments (treatment_id, treatment_name, treatment_price, treatment_duration)
VALUES (104, 'Tratament invalid', 50, 0);

-- foreign key la stergere: owner folosit in pets
DELETE FROM owners
WHERE owner_id = 1;

-- Modificare Date
UPDATE pets
SET weight = 13.2
WHERE pet_id = 10;

UPDATE pets
SET pet_description = pet_description_t('Hamster', 'M')
WHERE pet_id = 13;

UPDATE treatments
SET treatment_price = 120
WHERE treatment_id = 101;

--Delete
DELETE FROM pet_treatments
WHERE pet_id = 11
  AND treatment_id = 102;

DELETE FROM pets
WHERE pet_id = 13;