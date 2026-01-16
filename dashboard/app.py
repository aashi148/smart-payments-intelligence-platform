import streamlit as st
import pandas as pd
import requests

API_BASE = "http://127.0.0.1:5000"

st.set_page_config(page_title="Smart Payments Intelligence", layout="wide")
st.title(" Smart Payments Intelligence Platform")

# KPIs
st.subheader(" Payment KPIs")

try:
    metrics = requests.get(f"{API_BASE}/metrics", timeout=5).json()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Txns", metrics["total_transactions"])
    c2.metric("Success %", metrics["success_rate_pct"])
    c3.metric("Failure %", metrics["failure_rate_pct"])
    c4.metric("Pending %", metrics["pending_rate_pct"])
    c5.metric("Fraud %", metrics["fraud_rate_pct"])
except Exception:
    st.error(" Metrics API not available")
    st.stop()

st.divider()

st.subheader(" Active Alerts")

try:
    alerts = requests.get(f"{API_BASE}/alerts", timeout=5).json()

    if alerts["alert_count"] == 0:
        st.success("No active alerts")
    else:
        for alert in alerts["active_alerts"]:
            st.warning(alert)
except Exception:
    st.error("Alerts service unavailable")


# FAILURE BREAKDOWN
st.subheader(" Failure Reason Breakdown")

try:
    failures = requests.get(f"{API_BASE}/failures/breakdown", timeout=5).json()

    failure_df = pd.DataFrame(
        list(failures.items()),
        columns=["Reason", "Count"]
    )
    st.bar_chart(failure_df.set_index("Reason"))
except Exception:
    st.error("Failure breakdown API not available")

st.divider()

# HOURLY FAILURES 
st.subheader(" Hourly Failure Distribution")

try:
    hourly = requests.get(f"{API_BASE}/failures/hourly", timeout=5).json()

    hourly_df = pd.DataFrame(
        list(hourly.items()),
        columns=["Hour", "Failures"]
    ).astype({"Hour": int}).sort_values("Hour")

    st.line_chart(hourly_df.set_index("Hour"))
except Exception:
    st.error("Hourly failure API not available")

st.divider()

# FRAUD INSIGHTS 
st.subheader(" Fraud Insights")

try:
    fraud = requests.get(f"{API_BASE}/fraud/insights", timeout=5).json()

    st.write(f"**Total Fraud Cases:** {fraud['total_fraud_cases']}")
    st.write(f"**High Value Fraud (>5000):** {fraud['high_value_fraud_cases']}")
    st.write(f"**Low Value Fraud (≤5000):** {fraud['low_value_fraud_cases']}")
except Exception:
    st.error("Fraud insights API not available")

st.divider()

# ML PREDICTION
st.subheader(" Predict Transaction Risk")

with st.form("predict_form"):
    amount = st.number_input("Transaction Amount", min_value=1, value=3000)
    hour = st.slider("Hour of Day", 0, 23, 14)
    refund_time = st.number_input("Refund Time (hrs)", min_value=0, value=0)
    submitted = st.form_submit_button("Predict Risk")

    if submitted:
        try:
            payload = {
                "amount": amount,
                "hour_of_day": hour,
                "refund_time_hrs": refund_time
            }
            response = requests.post(
                f"{API_BASE}/predict",
                json=payload,
                timeout=5
            ).json()

            st.success("Prediction Results")
            st.write(f"**Failure Probability:** {response['failure_probability']}")
            st.write(f"**Fraud Probability:** {response['fraud_probability']}")
        except Exception:
            st.error("Prediction API not available")
