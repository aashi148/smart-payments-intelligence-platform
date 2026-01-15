import pandas as pd

def prepare_features(df):
    df = df.copy()

    # Binary target for failure
    df["is_failed"] = (df["status"] == "failed").astype(int)

    features = df[[
        "amount",
        "hour_of_day",
        "refund_time_hrs"
    ]]

    return features, df["is_failed"], df["fraud_flag"]
