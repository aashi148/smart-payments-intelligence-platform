import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:5432@localhost:5432/payments_db"
)

df = pd.read_csv("data/payments.csv")

print(df.head())       
print(len(df))          

df.to_sql("payments", engine, if_exists="replace", index=False)

print(" Data loaded into PostgreSQL")
