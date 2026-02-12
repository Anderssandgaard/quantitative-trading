import pandas as pd
import numpy as np


def run_stat_arb_backtest(df_input, start_date, end_date, t_cost=0.0005):
    """
    Executes a StatArb (Cross-Sectional Mean Reversion) strategy backtest.
    
    Logic:
    1. Demarketing: Subtract market average from individual returns.
    2. Mean Reversion: Inverse the sign (short winners, buy losers).
    3. Shift: Use yesterday's signals to trade today's prices.
    """
    
    # --- 1. Signal Calculation ---
    # Calculate daily returns before filtering to preserve the 'edge' days
    daily_ret = df_input.pct_change()
    
    # Calculate cross-sectional market average
    market_avg = daily_ret.mean(axis=1, skipna=True)
    
    # Raw weights: Negative of excess returns (Mean Reversion)
    weights = -(daily_ret.sub(market_avg, axis=0))
    
    # --- 2. Weight Normalization ---
    # Scale to ensure Gross Exposure = 1.0 (100% of capital)
    abs_sum = weights.abs().sum(axis=1, skipna=True)
    weights = weights.div(abs_sum, axis=0)
    
    # Handle mathematical edge cases (division by zero or missing data)
    weights = weights.replace([np.inf, -np.inf], 0).fillna(0)
    
    # --- 3. PnL Generation ---
    # Shift weights by 1 to avoid look-ahead bias
    shifted_weights = weights.shift(1)
    
    # Calculate Gross PnL (sum of weight * return for all assets)
    daily_pnl = (shifted_weights * daily_ret).sum(axis=1, skipna=True)
    
    # --- 4. Transaction Cost Analysis ---
    # Turnover = the absolute daily change in our positions
    turnover = weights.diff().abs().sum(axis=1, skipna=True)
    daily_t_costs = turnover * t_cost
    
    # Adjusted PnL = Gross PnL - Costs
    net_pnl = daily_pnl - daily_t_costs
    
    # --- 5. Filtering and Metrics ---
    # Slicing the series to our target date range
    pnl_slice = daily_pnl.loc[start_date:end_date]
    net_pnl_slice = net_pnl.loc[start_date:end_date]
    turnover_slice = turnover.loc[start_date:end_date]
    
    def get_sharpe(s):
        # Using Sample Std Dev (ddof=1) annualized by sqrt of 252 trading days
        return (s.mean() / s.std(ddof=1)) * np.sqrt(252) if s.std() != 0 else 0

    return {
        "Gross Sharpe": get_sharpe(pnl_slice),
        "Net Sharpe": get_sharpe(net_pnl_slice),
        "Avg Daily Turnover": turnover_slice.mean(),
        "Total Net Return": net_pnl_slice.sum(),
        "Daily Net Series": net_pnl_slice
    }
