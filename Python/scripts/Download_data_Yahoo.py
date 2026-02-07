# %%
from GetMarketDataYahoo import GetMarketDataYahoo
from PerformanceMetrics import CalcSharpeRatio
import matplotlib.pyplot as plt
# %%
symbols = ['IGE']
start_dt = '2001-11-26' 
end_dt = '2007-11-15'
interval = '1h'  # Daily data
data = GetMarketDataYahoo(symbols, start_dt, end_dt, interval);

# %% 3. Plotting
data[symbols[0]]['Close'].plot(
    figsize=(20, 10),
    title=f'{symbols[0]} Hourly Close Price', 
    grid=True, color='blue', linewidth=1.5)
plt.xlabel('Date/Time')     

# %% calculate sharpe ratio
sharpe = CalcSharpeRatio(data, price_col='Close');
print(sharpe)