UPDATE treatments
SET treatment_price = treatment_price + 50
WHERE treatment_id = 100;

COMMIT;