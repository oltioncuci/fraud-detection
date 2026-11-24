import time
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
CSV_PATH = next(DATA_DIR.glob("*.csv"))
PARQUET_PATH = DATA_DIR / "paysim.parquet"


DTYPES = {
    "step": "int16",
    "type": "category",
    "amount": "float64",
    "nameOrig": "string",
    "oldbalanceOrg": "float64",
    "newbalanceOrig": "float64",
    "nameDest": "string",
    "oldbalanceDest": "float64",
    "newbalanceDest": "float64",
    "isFraud": "int8",
    "isFlaggedFraud": "int8",
}

def convert():
    t = time.time()
    df = pd.read_csv(CSV_PATH, dtype=DTYPES)
    print(f"read {len(df):,} rows from {CSV_PATH.name} in {time.time() - t:.1f} s")
    df.to_parquet(PARQUET_PATH, index=False)
    print(f"saved {PARQUET_PATH} ({PARQUET_PATH.stat().st_size / 1e6:.0f} MB)")

def load():
    return pd.read_parquet(PARQUET_PATH)

if __name__ == "__main__":
    convert()
    t = time.time()
    df = load()
    print(f"reloaded from Parquet in {time.time() - t:.1f} s")
    print(df.dtypes)
    print(f"memory: {df.memory_usage(deep=True).sum() / 1e6:.0f} MB")