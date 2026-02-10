# %%
from quant_trading.metrics.PerformanceMetrics import CalcHedgeratio 
import numpy as np
# %% Pair trading example with GLD and GDX 

def run_pairs_strategy (df, trainset, testset):
    
    hr = CalcHedgeratio(df['Adj Close_GLD'].iloc[trainset], df['Adj Close_GDX'].iloc[trainset]);
    df['spread'] = df['Adj Close_GLD'] - df['Adj Close_GDX']*hr;

    spreadmean = df['spread'].iloc[trainset].mean();
    spreadstd  = df['spread'].iloc[trainset].std();

    # %  Standard Z-score logic
    df['zscore'] = (df['spread'] - spreadmean) / spreadstd
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
    # %
    # 1. Consolidate positions into a single DataFrame
    # We use .copy() to ensure we aren't working on a "View" of the original df
    positions = df[['pos_GLD', 'pos_GDX']].copy()

    # 2. Calculate daily returns for our two assets
    # Using the specific columns from your merged df
    dailyret = df[['Adj Close_GLD', 'Adj Close_GDX']].pct_change()

    # 3. Calculate PnL
    # Today's PnL is yesterday's position * today's return
    pnl = (positions.shift().values * dailyret.values)
    pnl = np.sum(pnl, axis=1) # Sum the GLD and GDX PnL into a single strategy PnL

    # 4. Calculate Sharpe Ratios
    # Note: we skip the first row of trainset because pct_change() makes it NaN
    sharpeTrainset = np.sqrt(252) * np.mean(pnl[trainset[1:]]) / np.std(pnl[trainset[1:]])
    sharpeTestset = np.sqrt(252) * np.mean(pnl[testset]) / np.std(pnl[testset])

    return df, pnl, positions, hr, sharpeTrainset, sharpeTestset, spreadmean, spreadstd
    
    
    












