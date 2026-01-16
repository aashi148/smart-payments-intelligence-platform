from flask import Flask, jsonify, request
import pandas as pd
import joblib

from config import Config
from backend.logger import logger

app = Flask(__name__)

# LOAD DATA & MODELS 
logger.info("Loading data and models...")

df = pd.read_csv(Config.DATA_PATH)
failure_model = joblib.load(Config.FAILURE_MODEL_PATH)
fraud_model = joblib.load(Config.FRAUD_MODEL_PATH)

logger.info("Startup completed successfully")

# ROUTES 

@app.route("/")
def home():
    return jsonify({"message": "Smart Payments Intelligence Platform API running"})


@app.route("/metrics")
def metrics():
    return jsonify({
        "total_transactions": len(df),
        "success_rate_pct": round((df["status"] == "success").mean() * 100, 2),
        "failure_rate_pct": round((df["status"] == "failed").mean() * 100, 2),
        "pending_rate_pct": round((df["status"] == "pending").mean() * 100, 2),
        "avg_refund_time_hrs": round(
            df[df["refund_time_hrs"] > 0]["refund_time_hrs"].mean(), 2
        ),
        "fraud_rate_pct": round((df["fraud_flag"] == 1).mean() * 100, 2)
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
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

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": "Invalid input"}), 400

@app.route("/failures/breakdown")
def failure_breakdown():
    failed = df[df["status"] == "failed"]
    breakdown = failed["failure_reason"].value_counts().to_dict()
    return jsonify(breakdown)


@app.route("/failures/hourly")
def hourly_failures():
    failed = df[df["status"] == "failed"]
    hourly = failed.groupby("hour_of_day").size().to_dict()
    return jsonify(hourly)


@app.route("/fraud/insights")
def fraud_insights():
    fraud = df[df["fraud_flag"] == 1]
    return jsonify({
        "total_fraud_cases": len(fraud),
        "high_value_fraud_cases": len(fraud[fraud["amount"] > 5000]),
        "low_value_fraud_cases": len(fraud[fraud["amount"] <= 5000])
    })

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
