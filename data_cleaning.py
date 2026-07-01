import pandas as pd

nav = pd.read_csv("data/raw/nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"], dayfirst=True)
nav = nav.sort_values(["amfi_code", "date"]).reset_index(drop=True)

nav["nav"] = pd.to_numeric(nav["nav"], errors="coerce")
nav = nav.set_index("date")
nav["nav"] = nav.groupby("amfi_code")["nav"].transform(
    lambda x: x.resample("D").asfreq().ffill()
)
nav = nav.reset_index()

nav = nav.drop_duplicates(subset=["amfi_code", "date"])
nav = nav[nav["nav"] > 0]

nav.to_csv("data/processed/nav_history_clean.csv", index=False)
print(f"nav_history cleaned: {len(nav)} rows saved")

txn = pd.read_csv("data/raw/investor_transactions.csv")

type_map = {
    "sip": "SIP", "lumpsum": "Lumpsum", "redemption": "Redemption",
    "SIP": "SIP", "LUMPSUM": "Lumpsum", "REDEMPTION": "Redemption"
}
txn["transaction_type"] = txn["transaction_type"].str.strip().map(type_map)

txn["date"] = pd.to_datetime(txn["date"], dayfirst=True)
txn = txn[txn["amount"] > 0]

valid_kyc = ["KYC_VERIFIED", "KYC_PENDING", "KYC_REJECTED"]
invalid_kyc = txn[~txn["kyc_status"].isin(valid_kyc)]
if len(invalid_kyc):
    print(f"Invalid KYC values:\n{invalid_kyc['kyc_status'].value_counts()}")

txn.to_csv("data/processed/investor_transactions_clean.csv", index=False)
print(f"transactions cleaned: {len(txn)} rows saved")

perf = pd.read_csv("data/raw/scheme_performance.csv")

return_cols = ["1y_return","3y_return","5y_return"]
for col in return_cols:
    perf[col] = pd.to_numeric(perf[col], errors="coerce")
    anomalies = perf[(perf[col] < -100) | (perf[col] > 500)]
    if len(anomalies):
        print(f"Anomalies in {col}:\n{anomalies[['scheme_code', col]]}")

perf["expense_ratio"] = pd.to_numeric(perf["expense_ratio"], errors="coerce")
out_of_range = perf[
    (perf["expense_ratio"] < 0.1) | (perf["expense_ratio"] > 2.5)
]
if len(out_of_range):
    print(f"Expense ratio out of range (0.1–2.5%):\n{out_of_range[['scheme_code','expense_ratio']]}")

perf.to_csv("data/processed/scheme_performance_clean.csv", index=False)
print(f"scheme_performance cleaned: {len(perf)} rows saved")