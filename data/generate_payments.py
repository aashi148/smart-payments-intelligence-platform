import pandas as pd
import numpy as np

np.random.seed(42)

rows = 5000

data = {
    "transaction_id": [f"TXN{i}" for i in range(1, rows + 1)],
    "user_id": np.random.randint(1000, 2000, rows),
    "amount": np.random.randint(50, 10000, rows),
    "status": np.random.choice(
        ["success", "failed", "pending"],
        rows,
        p=[0.8, 0.15, 0.05]
    ),
    "failure_reason": np.random.choice(
        ["network", "bank", "user", "fraud", "NA"],
        rows
    ),
    "refund_time_hrs": np.random.choice(
        [0, 2, 6, 12, 24, 48],
        rows,
        p=[0.5, 0.15, 0.15, 0.1, 0.07, 0.03]
    ),
    "hour_of_day": np.random.randint(0, 24, rows),
    "fraud_flag": np.random.choice([0, 1], rows, p=[0.95, 0.05])
}

df = pd.DataFrame(data)

#logic
df.loc[df["status"] == "success", "failure_reason"] = "NA"
df.loc[df["status"] != "failed", "refund_time_hrs"] = 0

df.to_csv("data/payments.csv", index=False)

print(" payments.csv generated successfully")
