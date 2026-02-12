# %%--- Imports ---
from quant_trading.strategies.statArb_backtest import run_stat_arb_backtest
import pandas as pd
from quant_trading.data.load_data import load_table

# This script executes a Cross-Sectional Mean Reversion (StatArb) strategy backtest.
# The strategy logic is as follows:
# 1. Demarketing: Subtract the market average return from each asset's return
# 2. Mean Reversion: Invert the sign of the excess returns (short winners, buy losers)
# 3. Shift: Use yesterday's signals to trade today's prices (to avoid look-ahead bias)
# The backtest also accounts for transaction costs based on turnover, and calculates both gross and net Sharpe ratios for the specified date range.

# Load Data
df_raw = load_table("SPX_20071123.txt")

# Pre-processing
df_raw['Date'] = pd.to_datetime(df_raw['Date'].astype(int).astype(str), format='%Y%m%d')
df_raw = df_raw.set_index('Date').sort_index()

# Run Function
results = run_stat_arb_backtest(
    df_input=df_raw, 
    start_date='2006-01-01', 
    end_date='2006-12-31', 
    t_cost=0.0005
)

# Output Results
print(f"Analysis Period: 2006-01-01 to 2006-12-31")
print(f"Gross Sharpe Ratio: {results['Gross Sharpe']:.4f}")
print(f"Net Sharpe Ratio (after 5bps cost): {results['Net Sharpe']:.4f}")
print(f"Average Daily Turnover: {results['Avg Daily Turnover']:.2%}")