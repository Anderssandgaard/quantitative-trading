# %%
from xml.parsers.expat import model
import pandas as pd
import numpy as np
import statsmodels.api as sm
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
    # Identify Market Type (Crypto = weekends exist)
    # df.index.dayofweek > 4 checks for Saturday (5) and Sunday (6)
    is_crypto = data.index.dayofweek.max() > 4
    daily_min = 1440 if is_crypto else 390
    base_gap = diffs.median()
    base_gap = daily_min if base_gap > 390 else diffs.median()

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
        if tier['mins'] >= (base_gap):
            
            # --- SAMPLING (Like MATLAB's dateshift 'last') ---
            # Resample takes the last price in every bucket (Day, Hour, or Minute)
            tiered_prices = data[price_col].resample(tier['freq']).last().dropna()
            
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


def CalcSharpeRatioHedge(data1,data2, price_col='Close'):
    """
    Calculates annualized Sharpe Ratios across Daily, Hourly, and Minute timeframes.
    df: DataFrame with a DatetimeIndex
    price_col: The name of the column to use (e.g., 'Close' or 'Adj Close')
    """
    # 1. Configuration & Data Heartbeat
    # Calculate the median gap in minutes
    diffs = data1.index.to_series().diff().dt.total_seconds() / 60
    base_gap = diffs.median()
    
    # Identify Market Type (Crypto = weekends exist)
    # df.index.dayofweek > 4 checks for Saturday (5) and Sunday (6)
    is_crypto = data1.index.dayofweek.max() > 4
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
            tiered_prices1 = data1[price_col].resample(tier['freq']).last().dropna()
            tiered_prices2 = data2[price_col].resample(tier['freq']).last().dropna()
            
            # --- MATH EXECUTION ---
            # Annualization Factor (N)
            if is_crypto:
                N = (365 * 1440) / tier['mins']
            else:
                N = (252 * 390) / tier['mins']
            
            # Simple Returns
            returns1 = tiered_prices1.pct_change().dropna()
            returns2 = tiered_prices2.pct_change().dropna()
            
            if len(returns1) < 2:
                results[tier['name']] = np.nan
                continue
            
            # Risk-Adjusted Return
            excess_returns = (returns1 - returns2)/2
            
            # Compute Annualized Sharpe
            sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(N)
            results[tier['name']] = round(sharpe, 4)
        else:
            results[tier['name']] = np.nan
    return results
# %%
def CalcMaxdrawdur(cumreturns):
    """
    Calculates max drawdown and duration (time spent underwater).
    Input: Series of cumulative returns (starting from 0)
    """
    # 1. Create a Wealth Index (Starting at $1)
    wealth_index = 1 + cumreturns
    
    # 2. Calculate the Running Maximum (High Water Mark)
    running_max = wealth_index.expanding().max()
    
    # 3. Calculate Drawdowns
    # (Current Value / Highest Value to date) - 1
    drawdowns = (wealth_index / running_max) - 1
    max_drawdown = drawdowns.min()
    
    # 4. Calculate Duration (Vectorized - No Loops)
    # Marks True whenever we are below the last peak
    is_in_dd = drawdowns < 0
    
    # This groups consecutive True values and resets when we hit a new high
    # It measures the time from the start of the drop to a NEW high
    durations = is_in_dd.groupby((~is_in_dd).cumsum()).cumsum()
    max_duration = durations.max()
    mdd_date = drawdowns.idxmin() # Finds the date when MDD happened
    return max_drawdown, max_duration, wealth_index, drawdowns, mdd_date


def CalcHedgeratio(data1, data2):
 
    # Fit the OLS regression model
    model = sm.OLS(data1, data2).fit();
    hedgeRatio = model.params.iloc[0]
    return hedgeRatio

def Calcspread(data1, data2,hedgeRatio):
 
    spread = data1 - hedgeRatio * data2;
   
    return spread
