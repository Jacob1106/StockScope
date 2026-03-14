import yfinance as yf
import pandas as pd


def get_stock_data(tick_sym: list, time_period: str = "5d", interval_between: str = "1d"):

        # API call 
    data = {}

    for i in range(len(tick_sym)):
        stockCall = yf.Ticker(tick_sym[i])

        # Open close etc 
        price_his = stockCall.history(period = time_period, interval = interval_between)

        gen_info = stockCall.info

        income = stockCall.income_stmt

        balance = stockCall.balance_sheet

        cash = stockCall.cash_flow

        
        sub_data = {"price_his": price_his, "gen_info": gen_info,
                    "income": income, "balance": balance, "cash": cash}

        
        data[tick_sym[i]] = sub_data

    return data
















p = get_stock_data(tick_sym = ["NVDA", "GOOGL", "AAPL"], time_period = "3mo", interval_between="5d")

