ALTER TABLE pets
ADD pet_xml XMLTYPE;

UPDATE pets p
SET pet_xml =
    XMLELEMENT(
        "Pet",
        XMLFOREST(
            p.pet_id AS "PetID",
            p.owner_id AS "OwnerID",
            p.pet_name AS "PetName",
            p.weight AS "Weight",
            p.birth_date AS "BirthDate"
        )
    );

COMMIT;

SELECT pet_id,
       XMLSERIALIZE(CONTENT pet_xml AS CLOB INDENT SIZE = 2) AS xml_data
FROM pets;