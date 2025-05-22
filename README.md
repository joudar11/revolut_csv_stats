
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
