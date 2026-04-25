--Views sistem
-- tabelele mele
SELECT table_name FROM user_tables;

-- tabele accesibile
SELECT owner, table_name FROM all_tables;

-- restrictii
SELECT constraint_name, table_name, constraint_type
FROM user_constraints;

-- indexuri
SELECT index_name, table_name
FROM user_indexes;

-- coloane tabel (ex: PETS)
SELECT column_name, data_type
FROM user_tab_columns
WHERE table_name = 'PETS';

--View pt a vedea lista procedurilor
CREATE OR REPLACE VIEW view_procedures AS
SELECT owner, object_name
FROM all_objects
WHERE object_type = 'PROCEDURE';

SELECT * FROM view_procedures;