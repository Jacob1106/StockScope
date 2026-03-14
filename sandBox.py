import yfinance as yf



# Last month (default daily interval)
aa = yf.Ticker("AAPL").history(period="1d", interval="5m")