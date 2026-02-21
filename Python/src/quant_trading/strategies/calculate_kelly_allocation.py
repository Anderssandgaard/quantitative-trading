# %% --- Imports ---
import pandas as pd
import numpy as np
from quant_trading.data.load_data import load_and_merge
def calculate_kelly_allocation(filenames, rf_annual=0.04):
    """
    Calculates the optimal Kelly allocation (F), Expected Growth (g), 
    and Portfolio Volatility (S) for a list of assets.
    """
    
    # 1. Internal helper to load and prep data
    df_merged = load_and_merge(filenames)

    # 3. Calculate Daily and Excess Returns
    daily_rf = rf_annual / 252
    daily_ret = df_merged.filter(like='Adj Close_').pct_change().dropna()
    
    # Rename to keep clean tickers from the start
    daily_ret.columns = [c.replace('Adj Close_', '') for c in daily_ret.columns]
    excess_ret = daily_ret.sub(daily_rf, axis=0)

    # 4. Annualized Expected Return (M) and Covariance (C)
    M = excess_ret.mean() * 252
    C = excess_ret.cov() * 252

    # 5. Matrix Inversion and Kelly Weights (F)
    # Using .values for the math to avoid alignment errors, 
    # then wrapping back in a Series for labels.
    C_inv = np.linalg.inv(C.values)
    F_values = C_inv.dot(M.values)
    F = pd.Series(F_values, index=C.index)

    # 6. Performance Metrics
    # Growth rate g = rf + 0.5 * (F^T * C * F)
    # Portfolio Volatility S = sqrt(F^T * C * F)
    variance_p = F.dot(C.values).dot(F.values)
    g = rf_annual + 0.5 * variance_p
    S = np.sqrt(variance_p)

    return {
        "weights": F,
        "growth_rate": g,
        "portfolio_vol": S,
        "expected_returns": M,
        "cov_matrix": C
    }