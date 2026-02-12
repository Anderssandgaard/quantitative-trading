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
# %% Pair trading example with GLD and GDX 
from quant_trading.metrics.PerformanceMetrics import CalcHedgeratio, Calcspread


df1=pd.read_excel(r'C:\Users\espg\OneDrive - Aarhus universitet\GitHub\quantitative-trading\data\GLD.xls')
df2=pd.read_excel(r'C:\Users\espg\OneDrive - Aarhus universitet\GitHub\quantitative-trading\data\GDX.xls')

df=pd.merge(df1, df2, on='Date', suffixes=('_GLD', '_GDX')) # inner join on Date
df.set_index('Date', inplace=True) # set Date as index
df.sort_index(inplace=True) # sort by Date

trainset=np.arange(0, 252) # first year as training set (252 trading days ~ 1 year)
testset=np.arange(trainset.shape[0], df.shape[0]) # rest as test set


df['hedgeratio'] = CalcHedgeratio(df['Adj Close_GLD'].iloc[trainset], df['Adj Close_GDX'].iloc[trainset]);
print(f"Hedge Ratio: {df['hedgeratio'].iloc[0]:.6f}")

df['spread'] = df['Adj Close_GLD'] - df['Adj Close_GDX']*df['hedgeratio'];

plt.close('all')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=False)
# 2. Plot Training Set on the first subplot
ax1.plot(df.index[trainset], df['spread'].iloc[trainset], color='blue', label='Training Spread')
ax1.set_title('In-Sample: Training Period')
ax1.set_ylabel('Spread Price')
ax1.grid(True)
ax1.legend()

# 3. Plot Test Set on the second subplot
ax2.plot(df.index[testset], df['spread'].iloc[testset], color='orange', label='Test Spread')
ax2.set_title('Out-of-Sample: Test Period')
ax2.set_ylabel('Spread Price')
ax2.grid(True)
ax2.legend()

# 4. Adjust layout so titles don't overlap
plt.tight_layout()
plt.show()
df['spreadmean'] = df['spread'].iloc[trainset].mean();
df['spreadstd'] = df['spread'].iloc[trainset].std();
print(f"Spread Mean: {df['spreadmean'].iloc[0]:.6f}, Spread Std Dev: {df['spreadstd'].iloc[0]:.4f}")
# %%  Standard Z-score logic
df['zscore'] = (df['spread'] - df['spreadmean'].iloc[0]) / df['spreadstd'].iloc[0]
plt.close('all')
df['zscore'].plot(figsize=(12,4), title="Z-Score of GLD/GDX Spread")
plt.axhline(2, color='red', linestyle='--')   # Upper threshold
plt.axhline(-2, color='green', linestyle='--') # Lower threshold
plt.axhline(0, color='black')                 # Mean
plt.show()

df['pos_GLD'] = np.nan
df['pos_GDX'] = np.nan
# 2. Set Entry/Exit signals
# Long the spread
df.loc[df['zscore'] <= -2, ['pos_GLD', 'pos_GDX']] = [1, -1]
# Short the spread
df.loc[df['zscore'] >= 2, ['pos_GLD', 'pos_GDX']] = [-1, 1]
# Exit signals (Set to 0)
df.loc[(df['zscore'] >= -1) & (df['zscore'] <= 1), ['pos_GLD', 'pos_GDX']] = 0
# 3. Fill the gaps (This carries the position forward)
df.ffill(inplace=True)
# 4. Fill the very first rows (before the first trade) with 0
df.fillna(0, inplace=True)
# %%
# 1. Consolidate positions into a single DataFrame
# We use .copy() to ensure we aren't working on a "View" of the original df
positions = df[['pos_GLD', 'pos_GDX']].copy()

# 2. Calculate daily returns for our two assets
# Using the specific columns from your merged df
dailyret = df[['Adj Close_GLD', 'Adj Close_GDX']].pct_change()

# 3. Calculate PnL
# .shift() is vital: today's PnL is yesterday's position * today's return
# We use .values instead of np.array() for cleaner Pandas-to-Numpy conversion
pnl = (positions.shift().values * dailyret.values)
pnl = np.sum(pnl, axis=1) # Sum the GLD and GDX PnL into a single strategy PnL

# 4. Calculate Sharpe Ratios
# Note: we skip the first row of trainset because pct_change() makes it NaN
sharpeTrainset = np.sqrt(252) * np.mean(pnl[trainset[1:]]) / np.std(pnl[trainset[1:]])
print(f"Sharpe Ratio (Train): {sharpeTrainset:.4f}")

sharpeTestset = np.sqrt(252) * np.mean(pnl[testset]) / np.std(pnl[testset])
print(f"Sharpe Ratio (Test): {sharpeTestset:.4f}")

# 5. Plot Cumulative Returns
plt.close('all') # Prevent freezing!
plt.figure(figsize=(10, 6))
plt.plot(np.cumsum(pnl[testset]), label='Test Set Cumulative Returns', color='green')
plt.title('Out-of-Sample Strategy Performance')
plt.ylabel('Cumulative Return')
plt.xlabel('Days')
plt.grid(True)
plt.legend()
plt.show()
# %%