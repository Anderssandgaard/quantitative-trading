# %%
import pandas as pd
import numpy as np
# %%
def CalcSharpeRatio(data, price_col='Close'):
    """
    Calculates annualized Sharpe Ratios across Daily, Hourly, and Minute timeframes.
    df: DataFrame with a DatetimeIndex
    price_col: The name of the column to use (e.g., 'Close' or 'Adj Close')
    """
    # 1. Configuration & Data Heartbeat
    # Calculate the median gap in minutes
    diffs = data.index.to_series().diff().dt.total_seconds() / 60
    base_gap = diffs.median()
    
    # Identify Market Type (Crypto = weekends exist)
    # df.index.dayofweek > 4 checks for Saturday (5) and Sunday (6)
    is_crypto = data.index.dayofweek.max() > 4
    daily_min = 1440 if is_crypto else 390
    base_gap = daily_min if base_gap > 390 else base_gap

    # Setup Tiers
    tiers = [
        {'name': 'Daily',  'mins': daily_min, 'freq': 'D'},
        {'name': 'Hourly', 'mins': 60,        'freq': 'h'},
        {'name': 'Minute', 'mins': 1,         'freq': 'min'}
    ]
    
    results = {}
    rf_annual = 0.04

    # 2. Processing Tiers
    for tier in tiers:
        # Check if the requested tier is larger than our data granularity
        if tier['mins'] >= (base_gap - 0.1):
            
            # --- SAMPLING (Like MATLAB's dateshift 'last') ---
            # Resample takes the last price in every bucket (Day, Hour, or Minute)
            tiered_prices = data['IGE'][price_col].resample(tier['freq']).last().dropna()
            
            # --- MATH EXECUTION ---
            # Annualization Factor (N)
            if is_crypto:
                N = (365 * 1440) / tier['mins']
            else:
                N = (252 * 390) / tier['mins']
            
            # Simple Returns
            returns = tiered_prices.pct_change().dropna()
            
            if len(returns) < 2:
                results[tier['name']] = np.nan
                continue
            
            # Risk-Adjusted Return
            rf_period = rf_annual / N
            excess_returns = returns - rf_period
            
            # Compute Annualized Sharpe
            sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(N)
            results[tier['name']] = round(sharpe, 4)
        else:
            results[tier['name']] = np.nan
    return results
