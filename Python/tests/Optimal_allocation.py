# %% --- Imports ---
import pandas as pd
import numpy as np
from quant_trading.strategies.calculate_kelly_allocation import calculate_kelly_allocation

# %% --- Configuration ---
# List of ticker files to process
assets = ["OIH.xls", "RKH.xls", "RTH.xls"]
RF_RATE = 0.04  # 4% Annual Risk-Free Rate

# %% --- Execution ---
# Calculate the Kelly Optimal Portfolio weights and metrics
# This handles data merging, return calculation, and matrix inversion internally.
results = calculate_kelly_allocation(assets, rf_annual=RF_RATE)

# %% --- Output Summary ---
print("-" * 30)
print("KELLY PORTFOLIO ANALYSIS")
print("-" * 30)

# Display weights as a readable list
print("Optimal Allocation (F):")
for ticker, weight in results["weights"].items():
    print(f"  {ticker:8}: {weight:10.4f}")

print("-" * 30)

# Display key performance indicators
print(f"Annualized Expected Return (M): {results['expected_returns'].mean():.4f}")
print(f"Expected Growth Rate (g):       {results['growth_rate']:.4f}")
print(f"Portfolio Volatility (S):       {results['portfolio_vol']:.4f}")
print(f"Estimated Sharpe Ratio:         {results['expected_returns'].mean() / results['portfolio_vol']:.4f}")

print("-" * 30)