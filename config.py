import os

class Config:
    DATA_PATH = os.getenv("DATA_PATH", "data/payments.csv")
    FAILURE_MODEL_PATH = os.getenv("FAILURE_MODEL_PATH", "ml/failure_model.pkl")
    FRAUD_MODEL_PATH = os.getenv("FRAUD_MODEL_PATH", "ml/fraud_model.pkl")
    DEBUG = os.getenv("DEBUG", "True") == "True"

