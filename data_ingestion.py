import pandas as pd
import os

CSV_DIR = "data/raw"
for fname in [f for f in os.listdir(CSV_DIR) if f.endswith(".csv")]:
    df = pd.read_csv(os.path.join(CSV_DIR, fname))
    print(f"\n{'='*40}\nFile: {fname}")
    print(f"Shape: {df.shape}")
    print(df.dtypes)
    print(df.head(3))
    nulls = df.isnull().sum()
    if nulls.any():
        print(f"Nulls found:\n{nulls[nulls>0]}")

        fund_master = pd.read_csv("data/raw/fund_master.csv")

# Check actual column names first
print("Columns:", fund_master.columns.tolist())

print("\nUnique fund houses:", fund_master["fund_house"].nunique())
print(fund_master["fund_house"].unique())
print("\nCategories:", fund_master["category"].unique())
print("\nSub-categories:", fund_master["sub_category"].unique())
print("\nRisk grades:\n", fund_master["risk_grade"].value_counts())
print("\nScheme code range:",
      fund_master["scheme_code"].min(), "–",
      fund_master["scheme_code"].max())

nav_history = pd.read_csv("data/raw/nav_history.csv")
master_codes = set(fund_master["scheme_code"].astype(str))
nav_codes    = set(nav_history["scheme_code"].astype(str))
missing = master_codes - nav_codes
extra   = nav_codes - master_codes

summary = f"""
DATA QUALITY SUMMARY
====================
Fund master records : {len(fund_master)}
NAV history records : {len(nav_history)}
Codes in master     : {len(master_codes)}
Codes in NAV hist   : {len(nav_codes)}
Missing from NAV    : {len(missing)} {list(missing)[:5]}
Extra in NAV        : {len(extra)} {list(extra)[:5]}
Null NAV values     : {nav_history['nav'].isnull().sum()}
"""
print(summary)
with open("reports/data_quality_summary.txt", "w") as f:
    f.write(summary)