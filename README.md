# Quantitative Trading Research 📈

Test research environment for quantitative tranding in **Python** and **MATLAB**.

## 📂 Project Structure
* `python_research/`: Data scraping (yfinance), signal processing, and machine learning.
* `matlab_research/`: Financial toolbox analysis, matrix optimizations, and backtesting.
* `data/`: Shared storage for market data (CSV/Parquet).
* `results/`: Language-specific outputs (plots and performance reports).

## 🛠️ Setup & Prerequisites
### Python
* **Version:** 3.10+
* **Libraries:** `pandas`, `yfinance`, `matplotlib`
* Install via: `pip install -r requirements.txt` (once created)

### MATLAB
* **Version:** R2024b+
* **Required Toolboxes:** Financial Toolbox, Optimization Toolbox.

## 🚀 Current Workflow
1.  Run `python_research/scripts/download_data.py` to fetch latest Yahoo Finance data.
2.  Data is saved to `data/raw/`.
3.  Execute MATLAB scripts to perform comparative analysis on the shared datasets.

---


