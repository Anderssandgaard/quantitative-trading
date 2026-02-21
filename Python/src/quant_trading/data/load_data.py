from pathlib import Path
import pandas as pd
from functools import reduce

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = PROJECT_ROOT / "data"

def load_excel(filename):
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_excel(path)

def load_table(filename):
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_table(path)



def load_and_merge(filenames):   
    
    def load_and_prep(files):
        for f in files:
            suffix = f.split('.')[0]
            temp = load_excel(f).set_index('Date')
            temp.columns = [f"{col}_{suffix}" for col in temp.columns]
            yield temp

    # 2. Merge Data
    df_merged = reduce(
        lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='outer'), 
        load_and_prep(filenames)
    )
    return df_merged