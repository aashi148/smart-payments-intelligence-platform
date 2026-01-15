from flask import Flask, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load payment data
df = pd.read_csv("data/payments.csv")

# Load models
failure_model = joblib.load("ml/failure_model.pkl")
fraud_model = joblib.load("ml/fraud_model.pkl")

@app.route("/")
def home():
    return jsonify({
        "message": "Smart Payments Intelligence Platform API running"
    })

@app.route("/metrics")
def metrics():
    total_txns = len(df)
    success_rate = round((df["status"] == "success").mean() * 100, 2)
    failure_rate = round((df["status"] == "failed").mean() * 100, 2)
    pending_rate = round((df["status"] == "pending").mean() * 100, 2)

    avg_refund_time = round(
        df[df["refund_time_hrs"] > 0]["refund_time_hrs"].mean(), 2
    )

    fraud_rate = round((df["fraud_flag"] == 1).mean() * 100, 2)

    return jsonify({
        "total_transactions": total_txns,
        "success_rate_pct": success_rate,
        "failure_rate_pct": failure_rate,
        "pending_rate_pct": pending_rate,
        "avg_refund_time_hrs": avg_refund_time,
        "fraud_rate_pct": fraud_rate
    })


@app.route("/failures/breakdown")
def failure_breakdown():
    failed = df[df["status"] == "failed"]
    breakdown = (
        failed["failure_reason"]
        .value_counts()
        .to_dict()
    )

    return jsonify({
        "failure_reason_breakdown": breakdown
    })

@app.route("/failures/hourly")
def hourly_failures():
    failed = df[df["status"] == "failed"]
    hourly = (
        failed.groupby("hour_of_day")
        .size()
        .to_dict()
    )

    return jsonify({
        "hourly_failure_distribution": hourly
    })

@app.route("/fraud/insights")
def fraud_insights():
    fraud = df[df["fraud_flag"] == 1]

    high_value_fraud = fraud[fraud["amount"] > 5000]
    low_value_fraud = fraud[fraud["amount"] <= 5000]

    return jsonify({
        "total_fraud_cases": len(fraud),
        "high_value_fraud_cases": len(high_value_fraud),
        "low_value_fraud_cases": len(low_value_fraud)
    })

@app.route("/predict", methods=["POST"])
def predict():
    from flask import request

    data = request.json

    features = [[
        data["amount"],
        data["hour_of_day"],
        data["refund_time_hrs"]
    ]]

    failure_prob = failure_model.predict_proba(features)[0][1]
    fraud_prob = fraud_model.predict_proba(features)[0][1]

    return jsonify({
        "failure_probability": round(float(failure_prob), 3),
        "fraud_probability": round(float(fraud_prob), 3)
    })

if __name__ == "__main__":
    app.run(debug=True)