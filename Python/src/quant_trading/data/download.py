# %% Downloading data from Yahoo Finance
# Anders Dyhr Sandgaard
import matplotlib.pyplot as plt
import yfinance as yf
# %%
def GetMarketDataYahoo(symbols, start_dt, end_dt, interval):

    # You can download all at once in one line!
    print(">> Fetching data...")
    data = yf.download(symbols, start=start_dt, end=end_dt, group_by='ticker', interval=interval)
    
    for symbol in symbols:
        print(f"\n--- {symbol} ---")
        # Accessing data for each ticker
        if len(symbols) > 1:
            ticker_data = data[symbol]
        else:
            ticker_data = data
            
        print(ticker_data.head())
        return data