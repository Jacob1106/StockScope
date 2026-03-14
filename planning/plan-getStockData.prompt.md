# Plan: `get_stock_data()` — Core Data Fetching Function

Build the first function in `src/stockscope/data.py` that wraps `yf.Ticker()` to extract comprehensive stock data for any company by ticker symbol.

---

## Input Decision

The function accepts a **ticker symbol string** (e.g., `"AAPL"`, `"MSFT"`). This is the universal stock identifier used by yfinance and all downstream analysis. A `period` parameter controls how much price history to pull.

**Signature:**
```
get_stock_data(ticker: str, period: str = "1y") -> dict
```

### Valid `period` values
`1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`, or custom like `2wk`, `10mo`.

---

## What yfinance Methods to Use

| Data Needed | yfinance Method | Returns |
|---|---|---|
| Price history (OHLCV) | `ticker.history(period=period)` | `pd.DataFrame` — columns: Open, High, Low, Close, Volume, Dividends, Stock Splits |
| Company info & metrics | `ticker.info` | `dict` — 100+ keys including sector, marketCap, PE ratios, margins, etc. |
| Income statement | `ticker.income_stmt` | `pd.DataFrame` — annual income statement |
| Balance sheet | `ticker.balance_sheet` | `pd.DataFrame` — annual balance sheet |
| Cash flow | `ticker.cashflow` | `pd.DataFrame` — annual cash flow statement |

---

## Return Structure

A single `dict` with named keys so downstream code can access exactly what it needs:

```
{
    "ticker":           str,              # the symbol passed in
    "history":          pd.DataFrame,     # OHLCV price history
    "info":             dict,             # full .info dict
    "income_stmt":      pd.DataFrame,     # annual income statement
    "balance_sheet":    pd.DataFrame,     # annual balance sheet
    "cashflow":         pd.DataFrame,     # annual cash flow
}
```

---

## Steps to Implement

1. **Create `src/stockscope/data.py`** with the function skeleton and imports (`yfinance`, `pandas`).
2. **Instantiate `yf.Ticker(ticker)`** — store the ticker object locally.
3. **Call `.history(period=period)`** — store the resulting DataFrame. Reset the index so `Date` becomes a regular column (easier for plotting later).
4. **Access `.info`** — store the full dict. This is lazy-loaded by yfinance on first access.
5. **Access `.income_stmt`, `.balance_sheet`, `.cashflow`** — store each DataFrame.
6. **Wrap all calls in a try/except** — if the ticker is invalid or the network fails, raise a clean `ValueError` with a helpful message rather than letting raw yfinance errors bubble up.
7. **Return the dict** with all five data pieces plus the ticker string.

---

## Error Handling

- Invalid ticker → `yf.Ticker("FAKE").history()` returns an empty DataFrame. Check `history.empty` and raise `ValueError(f"No data found for ticker '{ticker}'")`.
- Network errors → catch `Exception` broadly on the yfinance calls, re-raise as `ConnectionError` with context.

---

## Open Questions

1. **Should the function also pull quarterly financials** (`.quarterly_income_stmt`, etc.) or keep it annual-only for now?
2. **Should `.fast_info` be included** as a lightweight alternative to `.info` for quick lookups (current price, market cap, 52-week range)?
3. **Should we add an `interval` parameter** (e.g., `"1d"`, `"1wk"`, `"1mo"`) or default to daily and add it later?


## Syntax for function intial inputs: 

aa = yf.Ticker("AAPL").history(period="1d", interval="5m")'