import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/processed/mutual_funds.db")

files = {
    "nav_history":           "data/processed/nav_history_clean.csv",
    "investor_transactions": "data/processed/investor_transactions_clean.csv",
    "scheme_performance":    "data/processed/scheme_performance_clean.csv",
}

for table, path in files.items():
    df = pd.read_csv(path)
    df.to_sql(table, engine, if_exists="replace", index=False)
    count = pd.read_sql(f"SELECT COUNT(*) as n FROM {table}", engine)["n"][0]
    src   = len(df)
    match = "✓" if count == src else "✗ MISMATCH"
    print(f"{match} {table}: source={src}, db={count}")