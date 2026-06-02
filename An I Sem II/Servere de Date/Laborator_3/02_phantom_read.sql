-- second transaction
INSERT INTO treatments (
    treatment_id,
    treatment_name,
    treatment_price,
    treatment_duration
)
VALUES (
    999,
    'Tratament Phantom',
    150,
    1
);

COMMIT;