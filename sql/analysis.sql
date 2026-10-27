-- Run against outputs/phase1/banking.db after main.py --phase 1.
-- Read-only descriptive analysis of cleaned synthetic transactions.
-- These full-period aggregates are not model features.

SELECT customer_id, COUNT(*) AS transaction_count,
       ROUND(SUM(amount), 2) AS total_spent
FROM transactions
GROUP BY customer_id
HAVING SUM(amount) > 2000
ORDER BY total_spent DESC
LIMIT 5;

-- Daily volume by merchant category.
SELECT DATE(date) AS transaction_date, merchant_category,
       COUNT(*) AS transaction_count,
       ROUND(SUM(amount), 2) AS total_volume
FROM transactions
GROUP BY DATE(date), merchant_category
ORDER BY transaction_date, merchant_category;

-- WHERE filters rows before GROUP BY, HAVING filters aggregate groups.
SELECT customer_id, COUNT(*) AS validation_transactions,
       ROUND(SUM(amount), 2) AS validation_volume
FROM transactions
WHERE date >= '2026-09-15' AND date < '2026-09-21'
GROUP BY customer_id
HAVING COUNT(*) >= 2
ORDER BY validation_volume DESC;
