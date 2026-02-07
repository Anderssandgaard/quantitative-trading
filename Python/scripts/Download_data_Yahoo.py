# %%
from utils.GetMarketDataYahoo import GetMarketDataYahoo
import matplotlib.pyplot as plt
# %%
    symbols = ['AAPL']
    start_dt = '2010-09-25' 
    end_dt = '2020-10-02'
    interval = '1h'  # Daily data
    data = GetMarketDataYahoo(symbols, start_dt, end_dt, interval);

# %% 3. Plotting
data[symbols[0]]['Close'].plot(
    figsize=(20, 10),
    title=f'{symbols[0]} Hourly Close Price', 
    grid=True, color='blue', linewidth=1.5)
plt.xlabel('Date/Time')     





