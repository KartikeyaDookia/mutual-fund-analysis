import requests, pandas as pd, json

url = "https://api.mfapi.in/mf/125497"
data = requests.get(url, timeout=10).json()

with open("data/raw/hdfc_top100_raw.json", "w") as f:
    json.dump(data, f, indent=2)

df = pd.DataFrame(data["data"])
df.columns = ["date", "nav"]
df["scheme_code"] = 125497
df["scheme_name"] = data["meta"]["scheme_name"]
df.to_csv("data/raw/hdfc_top100_nav.csv", index=False)
print(f"Saved {len(df)} records — {df['scheme_name'][0]}")

schemes = {
    119551: "SBI Bluechip",
    120503: "ICICI Bluechip",
    118632: "Nippon Large Cap",
    119092: "Axis Bluechip",
    120841: "Kotak Bluechip"
}
all_dfs = []
for code, name in schemes.items():
    d = requests.get(f"https://api.mfapi.in/mf/{code}", timeout=10).json()
    df = pd.DataFrame(d["data"])
    df.columns = ["date", "nav"]
    df["scheme_code"] = code
    df["scheme_name"] = name
    all_dfs.append(df)
    print(f"✓ {name}: {len(df)} records")

pd.concat(all_dfs).to_csv("data/raw/bluechip_schemes_nav.csv", index=False)
print("Saved bluechip_schemes_nav.csv")