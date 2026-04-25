SELECT * FROM STUDENTI;

--creati un view ce contine, pentru fiecare student: nume, prenume, cod_sectia, denumire_sectia, an_studiu, grupa, media

CREATE OR REPLACE VIEW info_studenti AS 
    SELECT nume, prenume, cod_sectia, denumire_sectia, an_studiu, grupa, media
    FROM studenti;
    
SELECT * FROM info_studenti;

/* Folosind acest view, se cer view-uri pentru urmatoarele probleme (se rezolva usor cu functiile analitice): 
a) Pentru fiecare student se cere: nume, prenume, grupa, media, media sectiei din care face parte, 
distanta fata de medie (varianta), pozitia studentului in anul din care face parte (in ordonarea 
studentilor descrescator dupa medie). */

CREATE OR REPLACE VIEW medie_studenti AS
    SELECT nume, prenume, grupa, media,
        AVG(media) OVER (PARTITION BY cod_sectia) AS media_sectiei,
        VARIANCE(media) OVER (PARTITION BY cod_sectia) as varianta,
        ROW_NUMBER() OVER (PARTITION BY an_studiu ORDER BY media DESC) AS poz_student
    FROM info_studenti;
    
SELECT * FROM medie_studenti;

-- b) Studentii care au primele 3 medii cele mai mari din fiecare grupa. 
CREATE OR REPLACE VIEW top_medii AS
SELECT nume, prenume, grupa, media
FROM (
    SELECT nume, prenume, grupa, media,
           ROW_NUMBER() OVER (PARTITION BY grupa ORDER BY media DESC) AS poz_student_grupa
    FROM info_studenti
)
WHERE poz_student_grupa <= 3;
    
SELECT * FROM top_medii;