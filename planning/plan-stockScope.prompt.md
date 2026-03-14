# StockScope — Financial Analysis Shiny App

Build a modular Python app: data layer (`yfinance`) → analysis layer → multi-page Shiny UI. Each step is self-contained and testable before moving to the next.

---

## Step 1 — Add Dependencies to `pyproject.toml`

Add to the `dependencies` list: `yfinance`, `shiny`, `pandas`, `polars`, `plotnine`, and `lxml` (needed for Wikipedia table scraping). Your current list is empty. This unlocks everything downstream.

---

## Step 2 — Build `data.py` (Data Fetching Layer)

Create `src/stockscope/data.py` with two core functions:

- **`get_stock_data(ticker, period="1y")`** — wraps `yf.Ticker()` to return a dict containing:
  - Price history DataFrame (from `.history()`)
  - Company info dict (from `.info` — sector, industry, marketCap, PE ratios, etc.)
  - Financial statements (`.income_stmt`, `.balance_sheet`, `.cashflow`)

- **`get_sector_tickers(sector)`** — scrapes the [Wikipedia S&P 500 table](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) using `pandas.read_html()`, filters by `GICS Sector`, and returns a list of ticker symbols. This is more reliable and complete than `yf.Sector()` which only returns "top" companies. Cache the table in a module-level variable so you only fetch it once per session.

Optionally add a **`download_bulk_prices(tickers, period)`** wrapper around `yf.download()` for fetching multiple tickers at once (used later for comparison charts).

---

## Step 3 — Build `analysis.py` (Calculations Layer)

Create `src/stockscope/analysis.py` with pure functions that take DataFrames in and return DataFrames/values out:

- **`daily_returns(history_df)`** — percent change on Close
- **`moving_averages(history_df, windows=[20, 50, 200])`** — SMA columns
- **`volatility(history_df, window=20)`** — rolling standard deviation of returns
- **`compare_performance(tickers_dict)`** — normalize prices to a common start date for relative comparison
- **`key_metrics(info_dict)`** — extract a summary row (P/E, market cap, dividend yield, beta, 52-week range) from the `info` dict

Keep these stateless — no `yfinance` calls here. That separation makes testing trivial.

---

## Step 4 — Build the Shiny App (`src/stockscope/app.py`)

Use **Shiny Core** with `ui.page_navbar` for a multi-page layout. Three pages:

| Page                       | Sidebar Inputs                                          | Main Content                                                                    |
| -------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Stock Overview**         | Ticker input, period selector                           | Value boxes (price, market cap, P/E), price chart with MAs, financials table    |
| **Sector Analysis**        | Sector dropdown (11 GICS sectors)                       | Sector heatmap/bar chart of returns, top/bottom performers table                |
| **Competitor Comparison**  | Multi-select tickers (auto-populated from same sector)  | Normalized performance line chart, side-by-side metrics table                   |

Reactive flow: ticker input → `reactive.calc` calls `get_stock_data()` → downstream renders consume the cached result. Use `reactive.event` on an "Analyze" button to avoid firing on every keystroke.

---

## Step 5 — Write Tests in `tests/`

- **`test_data.py`** — mock `yf.Ticker` and `pandas.read_html` to test `get_stock_data()` and `get_sector_tickers()` without hitting the network.
- **`test_analysis.py`** — feed known DataFrames into each analysis function, assert expected outputs (e.g., moving average length, return values).

---

## Step 6 — Update `README.md`

Add: purpose, install (`pip install -e ".[dev]"`), run command (`shiny run src/stockscope/app.py`), screenshots placeholder, and dependency list.

---

## Open Questions

1. **Wikipedia vs. yfinance for sector data** — Wikipedia gives the full S&P 500 list with GICS sectors; `yf.Sector("technology")` gives only "top companies." Recommend Wikipedia as primary, with `yf.Sector` as an optional enrichment.
2. **Caching strategy** — yfinance calls are slow (~1-3s per ticker). Add a simple `functools.lru_cache` or `diskcache` layer now, or defer until the app feels sluggish?
3. **Charting library** — `plotnine` for static grammar-of-graphics plots, or `plotly` for interactive zoom/hover in the Shiny app? Plotly integrates more naturally with Shiny's `@render.plot` but plotnine produces cleaner static visuals.
