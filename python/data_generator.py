import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# SETTINGS
num_invoices = 1000
customers = [f"CUST_{i:03d}" for i in range(1, 201)]
regions = ["North", "South", "East", "West"]

# CREATE INVOICE DATA
invoice_data = []

start_date = datetime(2025, 1, 1)

for i in range(1, num_invoices + 1):
    invoice_date = start_date + timedelta(days=random.randint(0, 150))

    invoice_data.append({
        "invoice_id": f"INV_{i:05d}",
        "customer_id": random.choice(customers),
        "date": invoice_date,
        "region": random.choice(regions),
        "amount": round(random.uniform(500, 20000), 2)
    })

invoice_df = pd.DataFrame(invoice_data)

# CREATE PAYMENT DATA
payment_data = []

payment_id = 1

for _, row in invoice_df.iterrows():
    rand = random.random()

    if rand < 0.10:
        continue

    elif rand < 0.30:
        paid_amount = round(row["amount"] * random.uniform(0.3, 0.9), 2)
        status = "Partial"

    else:
        paid_amount = row["amount"]
        status = "Completed"

    payment_data.append({
        "payment_id": f"PAY_{payment_id:06d}",
        "invoice_id": row["invoice_id"],
        "date_paid": row["date"] + timedelta(days=random.randint(0, 10)),
        "amount_paid": paid_amount,
        "status": status
    })

    payment_id += 1

invoice_df.to_csv("invoice_data.csv", index=False)
payment_df = pd.DataFrame(payment_data)
payment_df.to_csv("payment_data.csv", index=False)

print("Dataset created successfully!")
print("Invoice rows:", len(invoice_df))
print("Payment rows:", len(payment_df))