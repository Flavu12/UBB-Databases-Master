/*1. Scrieti o interogare care sa afiseze toate produsele din categoria "Software" 
(si din toate subcategoriile acesteia)fara a utiliza direct codul/id-ul categoriei 
(se cere folosirea numelui categoriei).*/

SELECT p.cod,
       p.denumire
FROM produse p
WHERE p.cod IN (
    SELECT cod
    FROM structura
    START WITH codp = (
        SELECT cod
        FROM produse
        WHERE denumire = 'Software'
    )
    CONNECT BY PRIOR cod = codp
)
OR p.denumire = 'Software';

/*2. Scrieti o interogare care afiseaza toate nodurile radacina ale structurii si pentru fiecare 
astfel de nod numarul de descendenti directi; adaugati o coloana tablei produse care va stoca 
in format XML informatiile despre descendentii directi (cod, denumire, pozitie). */
SELECT p.cod, 
       p.denumire, 
       COUNT(s.cod) AS nr_descendenti_directi
FROM produse p
LEFT JOIN structura s 
       ON s.codp = p.cod
WHERE p.cod NOT IN (
      SELECT cod FROM structura)
GROUP BY p.cod, p.denumire;

ALTER TABLE produse 
ADD descendenti_xml XMLTYPE;

UPDATE produse p
SET descendenti_xml =
    XMLELEMENT(
        "descendenti",
        (
            SELECT XMLAGG(
                       XMLELEMENT(
                           "descendent",
                           XMLFOREST(
                               c.cod AS "cod",
                               c.denumire AS "denumire",
                               s.pozitia AS "pozitie"
                           )
                       )
                       ORDER BY s.pozitia
                   )
            FROM structura s
            JOIN produse c
              ON c.cod = s.cod
            WHERE s.codp = p.cod
        )
    );

COMMIT;


SELECT cod,
       denumire,
       XMLSERIALIZE(CONTENT descendenti_xml AS CLOB INDENT SIZE = 2) AS xml_descendenti
FROM produse;

/*3. Afisati primele 7 de produse de pe fiecare nivel, care se afla pe nivele 3 si 4 ale ierarhiei
si care au cel putin 2 vocale in denumire, ordonate alfabetic in fiecare nivel (sa fie afisat si nivelul)*/ 

SELECT nivel,
       cod,
       denumire
FROM (
    SELECT
        LEVEL AS nivel,
        p.cod,
        p.denumire,
        ROW_NUMBER() OVER (
            PARTITION BY LEVEL
            ORDER BY p.denumire
        ) AS rn
    FROM produse p
    LEFT JOIN structura s 
           ON p.cod = s.cod
    START WITH p.cod NOT IN (
        SELECT cod
        FROM structura
        WHERE cod IS NOT NULL
    )
    CONNECT BY PRIOR p.cod = s.codp
)
WHERE nivel IN (3, 4)
  AND REGEXP_COUNT(LOWER(denumire), '[aeiouăâî]') >= 2
  AND rn <= 7
ORDER BY nivel, denumire;

/*4. Creati scripturile necesare (INSERT-uri, UPDATE-uri)  pentru a modifica structura astfel incat sa
obtineti in structura ierarhica cel putin un ciclu (ciclu pe care sa-l evidentiati apoi in afisarea 
rezultatului unei interogari; fie cu "DA", fie cu alt string, pentru nodul care induce acel ciclu)*/

INSERT INTO structura (cod, codp) VALUES (1106, 1022);
INSERT INTO structura (cod, codp) VALUES (1115, 1008);
COMMIT;

SELECT
    s.cod,
    s.codp,
    p.denumire,
    SYS_CONNECT_BY_PATH(s.cod, '->') AS cale,
    CASE WHEN CONNECT_BY_ISCYCLE = 1 THEN 'DA' ELSE 'NU' END AS are_ciclu
FROM structura s
JOIN produse p ON p.cod = s.cod
START WITH s.cod IN (1106, 1115)
CONNECT BY NOCYCLE PRIOR s.cod = s.codp;


