SET SERVEROUTPUT ON;

-- Procedura care afiseaza codul sursa
CREATE OR REPLACE PROCEDURE proc_show_source (
    p_schema IN VARCHAR2,
    p_proc_name IN VARCHAR2
) IS
BEGIN
    FOR r IN (
        SELECT text
        FROM all_source
        WHERE owner = UPPER(p_schema)
          AND name = UPPER(p_proc_name)
        ORDER BY line
    )
    LOOP
        DBMS_OUTPUT.PUT_LINE(r.text);
    END LOOP;
END;
/

EXECUTE proc_show_source(USER, 'PROCENT_TREATMENTS');

-- Procedura care calculeaza intervalul bazat pe procentul p
CREATE OR REPLACE PROCEDURE procent_treatments(p IN NUMBER) IS

    procent_stanga NUMBER := 50 - p/2;
    procent_dreapta NUMBER := 50 + p/2;

    pozitie_stanga NUMBER;
    pozitie_dreapta NUMBER;

    CURSOR crs_cat IS
        SELECT DISTINCT treatment_name
        FROM treatments;

    total_treat NUMBER;
    poz_crt NUMBER;

BEGIN
    FOR cat_idx IN crs_cat LOOP

        SELECT COUNT(*) INTO total_treat
        FROM treatments
        WHERE treatment_name = cat_idx.treatment_name;

        pozitie_stanga := ROUND(procent_stanga * total_treat / 100);
        pozitie_dreapta := ROUND(procent_dreapta * total_treat / 100);

        DBMS_OUTPUT.PUT_LINE(
            'Categorie: ' || cat_idx.treatment_name ||
            ', Total: ' || total_treat ||
            ', Interval [' || pozitie_stanga || ', ' || pozitie_dreapta || ')'
        );

        poz_crt := 1;

        FOR tr IN (
            SELECT treatment_name, treatment_price
            FROM treatments
            WHERE treatment_name = cat_idx.treatment_name
            ORDER BY treatment_price DESC
        )
        LOOP
            IF poz_crt >= pozitie_stanga AND poz_crt < pozitie_dreapta THEN
                DBMS_OUTPUT.PUT_LINE(
                    tr.treatment_name || ' - ' || tr.treatment_price
                );
            END IF;

            poz_crt := poz_crt + 1;
        END LOOP;

        DBMS_OUTPUT.PUT_LINE(' ');
    END LOOP;

END;
/

EXECUTE procent_treatments(20);