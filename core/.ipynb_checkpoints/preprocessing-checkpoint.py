import pandas as pd


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remove rows with invalid dates
    df = df.dropna(subset=["date"])

    # Convert amount to numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Remove invalid amounts
    df = df.dropna(subset=["amount"])

    # Normalize description
    df["description"] = df["description"].astype(str).str.strip()

    # Remove empty descriptions
    df = df[df["description"] != ""]

    return df.reset_index(drop=True)
