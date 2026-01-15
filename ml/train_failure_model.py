import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from feature_engineering import prepare_features

df = pd.read_csv("data/payments.csv")

X, y_failure, _ = prepare_features(df)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_failure, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print("Failure Prediction Report:")
print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, "ml/failure_model.pkl")
print(" Failure model saved")
