# %%
from quant_trading.data.download import GetMarketDataYahoo
from quant_trading.vizualization.showmetrics import show_CalcMaxdrawdur
from quant_trading.metrics.PerformanceMetrics import CalcSharpeRatio, CalcSharpeRatioHedge, CalcMaxdrawdur
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
# %%
symbols  = ['IGE','SPY']
start_dt = '2001-11-26' 
end_dt   = '2007-11-15'
interval = '1d'  # Daily data
data = GetMarketDataYahoo(symbols, start_dt, end_dt, interval);

# % 3. Plotting
ax =data[symbols[0]]['Close'].plot(
    figsize=(20, 10),
    title=f'{symbols[0]} Hourly Close Price', 
    grid=True, color='blue', linewidth=1.5)

data[symbols[1]]['Close'].plot(ax=ax,
    figsize=(20, 10),
    title=f'{symbols[0]} Hourly Close Price', 
    grid=True, color='red', linewidth=1.5)
plt.xlabel('Date/Time')    
 
# %% calculate sharpe ratios
sharpe = CalcSharpeRatio(data[symbols[0]], price_col='Close');
print(sharpe)
sharpe = CalcSharpeRatio(data[symbols[1]], price_col='Close');
print(sharpe)
sharpe_hedge = CalcSharpeRatioHedge(data[symbols[0]],data[symbols[1]], price_col='Close');
print(sharpe_hedge)

# %% Calculate maximum drawdown and maximum drawdown duration

excess_returns = (data[symbols[0]]['Close'].pct_change().dropna() - data[symbols[1]]['Close'].pct_change().dropna())/2;
cumreturns     = excess_returns.add(1).cumprod() - 1;
max_drawdown, max_drawdown_duration, wealth_index, drawdowns, mdd_date = CalcMaxdrawdur(cumreturns);
print(f"Max Drawdown: {max_drawdown:.4f}, Max Drawdown Duration: {max_drawdown_duration} periods", f"Date of MDD: {mdd_date.date()}")
# Show the max drawdown and duration visually
show_CalcMaxdrawdur(cumreturns, max_drawdown, max_drawdown_duration, mdd_date, wealth_index, drawdowns)
