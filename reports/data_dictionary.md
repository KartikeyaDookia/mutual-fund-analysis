# Data Dictionary

## nav_history
| Column     | Type     | Description                        | Source            |
|------------|----------|------------------------------------|-------------------|
| amfi_code  | TEXT     | Unique AMFI scheme identifier      | fund_master.csv   |
| date       | DATETIME | NAV date (parsed to datetime)      | nav_history.csv   |
| nav        | FLOAT    | Net Asset Value on that date (>0)  | nav_history.csv   |

## investor_transactions
| Column           | Type     | Description                               | Source                       |
|------------------|----------|-------------------------------------------|------------------------------|
| date             | DATETIME | Transaction date                          | investor_transactions.csv    |
| transaction_type | TEXT     | One of: SIP / Lumpsum / Redemption        | investor_transactions.csv    |
| amount           | FLOAT    | Transaction amount in INR (>0)            | investor_transactions.csv    |
| kyc_status       | TEXT     | KYC_VERIFIED / KYC_PENDING / KYC_REJECTED | investor_transactions.csv    |

## scheme_performance
| Column        | Type  | Description                             | Source                   |
|---------------|-------|-----------------------------------------|--------------------------|
| scheme_code   | TEXT  | AMFI scheme code                        | scheme_performance.csv   |
| return_1y     | FLOAT | 1-year return %                         | scheme_performance.csv   |
| return_3y     | FLOAT | 3-year return %                         | scheme_performance.csv   |
| return_5y     | FLOAT | 5-year return %                         | scheme_performance.csv   |
| expense_ratio | FLOAT | Annual expense ratio % (valid: 0.1–2.5) | scheme_performance.csv   |