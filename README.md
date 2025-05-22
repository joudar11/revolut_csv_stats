# revolut_csv_stats

A Python app to **analyze your Revolut investment statement**. It automatically parses the `.csv` file, calculates buys, sells, dividends, fees, deposits, withdrawals, the current value of held stocks, and the profit/loss in CZK. The output includes per-year breakdowns and total summaries.

---

## Features

- Automatic calculation of:
  - Buys, sells, and dividends
  - Fees and net deposits/withdrawals
  - Current value of held stocks
- Currency conversion using **live CZK rates from CNB** (for EUR and USD)
- Multi-currency transaction support
- Ticker correction for Yahoo Finance (e.g., `BRK.B â†’ BRK-B`)
- Console output grouped by year and total

---

## Sample Output

```
========================================
EUR to CZK rate used: 24.570
USD to CZK rate used: 22.980
========================================

CZK [NOW] Invested: 58240.320
CZK [NOW] Value: 61221.270
CZK [NOW] Profit/loss: 2980.950

========================================
CZK [ALL TIME] Sells: 11986.620
CZK [ALL TIME] Buys: 10584.180
CZK [ALL TIME] Balance: -1402.440
CZK [ALL TIME] Dividends: 120.900
CZK [ALL TIME] Fees: 98.400
CZK [ALL TIME] Topups: 57700.000
CZK [ALL TIME] Withdrawals: 540.320
...
```

---

## Requirements

- Python 3.10+
- Libraries:
  - `requests`
  - `yfinance`
  - `decimal` (built-in)
  - `csv`, `datetime`, `os` (built-in)

---

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/joudar11/revolut_csv_stats.git
    cd revolut_csv_stats
    ```

2. **Create a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Place your Revolut CSV**:
    - Export your statement from Revolut
    - Rename it to `statement.csv` and place it in the project root (or enter a different name at launch)

---

## Usage

```bash
python main.py
```

---

## Notes

- The expected CSV format is:
  ```
  Date,Ticker,Type,Quantity,Price per share,Total Amount,Currency,FX Rate
  ```
- If the file is not found, the app will prompt for a different filename.
- Some tickers are auto-corrected for compatibility with Yahoo Finance (e.g., `BRK.B â†’ BRK-B`)

---

## Author

Created by **[joudar11](https://github.com/joudar11)**  
Feel free to open an issue or pull request for suggestions or fixes.

---

## License

MIT License
