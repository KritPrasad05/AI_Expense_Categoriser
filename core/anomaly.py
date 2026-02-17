import pandas as pd
import numpy as np


# def detect_global_outliers(df: pd.DataFrame):
#     df = df.copy()

#     q1 = df["amount"].quantile(0.25)
#     q3 = df["amount"].quantile(0.75)
#     iqr = q3 - q1

#     upper_bound = q3 + 1.5 * iqr

#     df["high_amount_flag"] = df["amount"] > upper_bound

#     return df

def detect_high_absolute_amount(df: pd.DataFrame):
    df = df.copy()

    global_mean = df["amount"].mean()
    global_std = df["amount"].std()

    if global_std == 0:
        df["high_absolute_flag"] = False
        return df

    z_scores = (df["amount"] - global_mean) / global_std

    df["high_absolute_flag"] = z_scores > 3  # extreme global

    return df


def detect_category_outliers(df: pd.DataFrame, z_threshold: float = 2.5):
    df = df.copy()
    df["category_zscore"] = 0.0
    df["category_outlier_flag"] = False

    for category in df["category"].unique():
        subset = df[df["category"] == category]

        if len(subset) < 5:
            continue

        mean = subset["amount"].mean()
        std = subset["amount"].std()

        if std == 0:
            continue

        z_scores = (subset["amount"] - mean) / std

        df.loc[subset.index, "category_zscore"] = z_scores
        df.loc[subset.index, "category_outlier_flag"] = z_scores.abs() > z_threshold

    return df

def detect_duplicates(df: pd.DataFrame):
    df = df.copy()

    df["duplicate_flag"] = df.duplicated(
        subset=["date", "amount", "description"],
        keep="first"
    )

    return df

def generate_anomaly_explanations(df: pd.DataFrame):
    df = df.copy()
    df["anomaly_reason"] = ""

    df.loc[df["category_outlier_flag"], "anomaly_reason"] += \
        "Unusual amount compared to typical spending in this category. "

    df.loc[df["duplicate_flag"], "anomaly_reason"] += \
        "Potential duplicate transaction detected. "

    df.loc[df["high_absolute_flag"], "anomaly_reason"] += \
        "Transaction amount is significantly high compared to overall spending. "

    return df

def apply_anomaly_detection(df: pd.DataFrame):
    df = detect_category_outliers(df)
    df = detect_high_absolute_amount(df)
    df = detect_duplicates(df)

    df["anomaly_flag"] = (
        df["category_outlier_flag"] |
        df["duplicate_flag"]
    )

    df = generate_anomaly_explanations(df)

    return df
