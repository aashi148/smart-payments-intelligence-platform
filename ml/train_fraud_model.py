import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from feature_engineering import prepare_features

df = pd.read_csv("data/payments.csv")

X, _, y_fraud = prepare_features(df)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_fraud, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Fraud Detection Report:")
print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, "ml/fraud_model.pkl")
print("✅ Fraud model saved")
