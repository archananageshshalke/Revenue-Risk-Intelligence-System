-- =========================================
-- 1. MISSING PAYMENTS (FULL LEAKAGE)
-- =========================================

SELECT 
    i.invoice_id,
    i.customer_id,
    i.amount AS invoice_amount
FROM invoice_data i
LEFT JOIN payment_data p
ON i.invoice_id = p.invoice_id
WHERE p.invoice_id IS NULL;


-- =========================================
-- 2. PARTIAL PAYMENTS (UNDER PAYMENT CASE)
-- =========================================

SELECT 
    i.invoice_id,
    i.customer_id,
    i.amount AS invoice_amount,
    SUM(p.amount_paid) AS total_paid,
    (i.amount - SUM(p.amount_paid)) AS leakage_amount
FROM invoice_data i
JOIN payment_data p
ON i.invoice_id = p.invoice_id
GROUP BY i.invoice_id, i.customer_id, i.amount
HAVING SUM(p.amount_paid) < i.amount;


-- =========================================
-- 3. TOTAL REVENUE LEAKAGE SUMMARY
-- =========================================

WITH missing AS (
    SELECT 
        i.invoice_id,
        i.amount AS leakage
    FROM invoice_data i
    LEFT JOIN payment_data p
    ON i.invoice_id = p.invoice_id
    WHERE p.invoice_id IS NULL
),

partial AS (
    SELECT 
        i.invoice_id,
        (i.amount - SUM(p.amount_paid)) AS leakage
    FROM invoice_data i
    JOIN payment_data p
    ON i.invoice_id = p.invoice_id
    GROUP BY i.invoice_id, i.amount
    HAVING SUM(p.amount_paid) < i.amount
)

SELECT 
    (SELECT SUM(leakage) FROM missing) AS missing_leakage,
    (SELECT SUM(leakage) FROM partial) AS partial_leakage,
    (SELECT SUM(leakage) FROM missing) +
    (SELECT SUM(leakage) FROM partial) AS total_leakage;