# %%
<<<<<<< HEAD
from quant_trading.data.load_data import load_excel
=======
from quant_trading.data.load_excel import load_excel
>>>>>>> 18f731c854db396daaeaf75461f10dab49a853c8
from quant_trading.strategies.run_pairs_strategy  import run_pairs_strategy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

<<<<<<< HEAD
# %% Pair trading example with GLD and GDX 
=======
# % Pair trading example with GLD and GDX 
>>>>>>> 18f731c854db396daaeaf75461f10dab49a853c8
df1 = load_excel("GLD.xls")
df2 = load_excel("GDX.xls")
# Merge dataframes on Date
df=pd.merge(df1, df2, on='Date', suffixes=('_GLD', '_GDX')) # inner join on Date
df.set_index('Date', inplace=True) # set Date as index
df.sort_index(inplace=True) # sort by Date

trainset=np.arange(0, 252) # first year as training set (252 trading days ~ 1 year)
testset=np.arange(trainset.shape[0], df.shape[0]) # rest as test set
df, pnl, positions, hr, sharpeTrainset, sharpeTestset, spreadmean, spreadstd = run_pairs_strategy(df, trainset, testset);
#
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
print(f"Spread Mean: {spreadmean:.6f}, Spread Std Dev: {spreadstd:.4f}")
# %  Standard Z-score logic
plt.close('all')
df['zscore'].plot(figsize=(12,4), title="Z-Score of GLD/GDX Spread")
plt.axhline(2, color='red', linestyle='--')   # Upper threshold
plt.axhline(-2, color='green', linestyle='--') # Lower threshold
plt.axhline(0, color='black')                 # Mean
plt.show()

# 4. Calculate Sharpe Ratios
# Note: we skip the first row of trainset because pct_change() makes it NaN
print(f"Sharpe Ratio (Train): {sharpeTrainset:.4f}")
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
<<<<<<< HEAD
# %%

startDate = 20060101
endDate=20061231
df = pd.read_table('C:\\Users\\espg\\Documents\\GitHub\\quantitative-trading\\data\\SPX_20071123.txt')
df['Date'] = df['Date'].astype(int) # Convert Date to integer
df.set_index('Date', inplace=True) # Set Date as index
df.sort_index(inplace=True) # Sort by Date
# %%

daily_returns = df.pct_change() # Calculate daily returns
marketDailyReturns = daily_returns.mean(axis=1) # Average across all stocks to get market return
weights = - (np.array(daily_returns)-np.array(marketDailyReturns).reshape((daily_returns.shape[0], 1))) # Calculate weights as negative of excess returns
wtsum = np.nansum(abs(weights), axis=1) # Sum of absolute weights for normalization
weights[wtsum == 0,]=0 # Avoid division by zero
wtsum[wtsum == 0] = 1   # Set sum to 1 where it was zero to prevent division by zero

weights = weights / wtsum.reshape((daily_returns.shape[0], 1)) # Normalize weights
dailypnl = np.nansum(np.array(pd.DataFrame(weights).shift()) * np.array(daily_returns), axis=1) # Calculate daily PnL
dailypnl = dailypnl[np.logical_and(df.index >= startDate, df.index <= endDate)] # Filter by date range
sharperatio = np.mean(dailypnl) / np.std(dailypnl) * np.sqrt(252) # Annualized Sharpe Ratio
print(f"Annualized Sharpe Ratio: {sharperatio:.4f}")
=======
>>>>>>> 18f731c854db396daaeaf75461f10dab49a853c8
