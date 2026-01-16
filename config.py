class Config:
    DEBUG = True

    # CSV 
    DATA_PATH = "data/payments.csv"

    # PostgreSQL
    DATABASE_URL = "postgresql://postgres:5432@localhost:5432/payments_db"

    FAILURE_MODEL_PATH = "ml/failure_model.pkl"
    FRAUD_MODEL_PATH = "ml/fraud_model.pkl"
