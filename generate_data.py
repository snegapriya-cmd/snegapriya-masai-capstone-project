"""Generate reproducible synthetic Instamart-style customer, order and ticket data.
All records are synthetic and are not real Swiggy customer data.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = np.random.default_rng(42)

n_customers = 250
cities = ["Bengaluru", "Chennai", "Hyderabad", "Mumbai", "Pune"]
genders = ["Female", "Male", "Other"]
customers = pd.DataFrame({
    "customer_id": [f"C{i:04d}" for i in range(1, n_customers + 1)],
    "city": rng.choice(cities, n_customers),
    "gender": rng.choice(genders, n_customers, p=[0.46, 0.50, 0.04]),
    "signup_date": pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 900, n_customers), unit="D"),
})
customers.to_csv(DATA / "customers.csv", index=False)

rows = []
order_no = 1
for cid in customers["customer_id"]:
    count = int(rng.integers(1, 28))
    dates = pd.Timestamp("2026-10-31") - pd.to_timedelta(rng.integers(0, 240, count), unit="D")
    for d in dates:
        status = rng.choice(["Completed", "Cancelled"], p=[0.91, 0.09])
        rows.append({
            "order_id": f"O{order_no:06d}", "customer_id": cid,
            "order_date": d, "order_status": status,
            "order_amount": round(float(rng.uniform(100, 2500)), 2)
        })
        order_no += 1
orders = pd.DataFrame(rows)
# Add a few intentionally imperfect records for the cleaning exercise.
if len(orders) > 10:
    orders.loc[3, "order_amount"] = -50
    orders.loc[7, "customer_id"] = None
orders.to_csv(DATA / "orders.csv", index=False)

issues = [
    "My order is delayed and has not arrived",
    "I was charged twice for one order",
    "The vegetables arrived damaged",
    "I received the wrong product",
    "Please help me get a refund for my cancelled order",
    "The payment failed but money was deducted",
]
labels = ["Delivery", "Payment", "Product Quality", "Wrong Item", "Refund", "Payment"]
ticket_rows = []
for i in range(1, 401):
    idx = int(rng.integers(0, len(issues)))
    ticket_rows.append({
        "ticket_id": f"T{i:05d}",
        "customer_id": str(rng.choice(customers["customer_id"])),
        "ticket_text": issues[idx],
        "issue_type": labels[idx],
        "ticket_status": rng.choice(["Open", "Closed", "Pending"], p=[0.35, 0.5, 0.15])
    })
pd.DataFrame(ticket_rows).to_csv(DATA / "tickets.csv", index=False)

policies = pd.DataFrame([
    ["Refunds", "Refund eligibility and processing time depend on payment method and order status. Check the order record before promising a date."],
    ["Delivery", "For delayed or missing orders, verify live order status and escalate unresolved cases to delivery support."],
    ["Product Quality", "For damaged or poor-quality items, request order details and supporting photos, then route to quality support."],
    ["Payments", "For duplicate charges or failed payments, verify the transaction before initiating a payment investigation."]
], columns=["policy_topic", "policy_text"])
policies.to_csv(DATA / "policy_evaluation.csv", index=False)
print(f"Generated {len(customers)} customers, {len(orders)} orders and {len(ticket_rows)} tickets in {DATA}")
