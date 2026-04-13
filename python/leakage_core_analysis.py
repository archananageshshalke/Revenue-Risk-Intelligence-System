import pandas as pd
import sqlite3

# -----------------------------
# LOAD DATA
# -----------------------------
invoice_df = pd.read_csv("invoice_data.csv")
payment_df = pd.read_csv("payment_data.csv")

# -----------------------------
# CREATE SQL DB
# -----------------------------
conn = sqlite3.connect(":memory:")

invoice_df.to_sql("invoice_data", conn, index=False, if_exists="replace")
payment_df.to_sql("payment_data", conn, index=False, if_exists="replace")

print("DATA LOADED INTO SQL SUCCESSFULLY")

# -----------------------------
# 1. MISSING PAYMENTS
# -----------------------------
query_missing = """
SELECT i.invoice_id, i.customer_id, i.amount
FROM invoice_data i
LEFT JOIN payment_data p
ON i.invoice_id = p.invoice_id
WHERE p.invoice_id IS NULL
"""

missing_df = pd.read_sql(query_missing, conn)

print("\n===== MISSING PAYMENTS =====")
print("Count:", len(missing_df))
print(missing_df.head())

# -----------------------------
# 2. PARTIAL PAYMENTS
# -----------------------------
query_partial = """
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
HAVING total_paid < i.amount
"""

partial_df = pd.read_sql(query_partial, conn)

print("\n===== PARTIAL PAYMENTS =====")
print("Count:", len(partial_df))
print(partial_df.head())

# -----------------------------
# 3. TOTAL REVENUE LEAKAGE SUMMARY
# -----------------------------

missing_leakage = missing_df["amount"].sum()

partial_leakage = partial_df["leakage_amount"].sum()

total_leakage = missing_leakage + partial_leakage

total_revenue = invoice_df["amount"].sum()

leakage_percent = (total_leakage / total_revenue) * 100

summary = pd.DataFrame([{
    "total_revenue": total_revenue,
    "missing_payment_leakage": missing_leakage,
    "partial_payment_leakage": partial_leakage,
    "total_leakage": total_leakage,
    "leakage_percent": leakage_percent
}])

print("\n===== REVENUE LEAKAGE SUMMARY =====")
print(summary)

# -----------------------------
# SAVE OUTPUTS (FOR POWER BI)
# -----------------------------
missing_df.to_csv("missing_payments.csv", index=False)
partial_df.to_csv("partial_payments.csv", index=False)
summary.to_csv("leakage_summary.csv", index=False)

print("\nFILES READY FOR POWER BI DASHBOARD")