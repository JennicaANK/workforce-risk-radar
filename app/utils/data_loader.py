from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"

def load_final_predictions():
    path = DATA_DIR / "final_predictions.csv"
    df = pd.read_csv(path)
    if "month" in df.columns:
        df["month"] = pd.to_datetime(df["month"])
    return df

def load_final_risk_scores():
    path = DATA_DIR / "final_risk_scores.csv"
    df = pd.read_csv(path)
    if "month" in df.columns:
        df["month"] = pd.to_datetime(df["month"])
    return df

def load_regression_metrics():
    path = DATA_DIR / "regression_metrics.csv"
    return pd.read_csv(path)

def load_classification_metrics():
    path = DATA_DIR / "classification_metrics.csv"
    return pd.read_csv(path)

def load_final_model_coefficients():
    path = DATA_DIR / "final_model_coefficients.csv"
    return pd.read_csv(path)


def load_master_monthly():
    path = DATA_DIR / "master_monthly.csv"
    df = pd.read_csv(path)
    if "month" in df.columns:
        df["month"] = pd.to_datetime(df["month"])
    return df