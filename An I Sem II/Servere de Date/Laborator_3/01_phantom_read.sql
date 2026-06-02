SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- first transaction
SELECT *
FROM treatments
WHERE treatment_price >= 100;

-- second transaction runs and then commit 

-- first transaction read again 
-- phantom read
SELECT *
FROM treatments
WHERE treatment_price >= 100;
COMMIT;