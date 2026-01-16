def evaluate_alerts(metrics):
    alerts = []

    if metrics["failure_rate_pct"] > 20:
        alerts.append(" High transaction failure rate detected")

    if metrics["fraud_rate_pct"] > 5:
        alerts.append(" Fraud rate spike detected")

    if metrics["avg_refund_time_hrs"] > 48:
        alerts.append(" Refund SLA breach risk")

    return alerts
