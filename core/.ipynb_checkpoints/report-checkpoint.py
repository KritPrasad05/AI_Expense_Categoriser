import pandas as pd


def generate_summary_metrics(df: pd.DataFrame):
    total_spend = df["amount"].sum()
    total_transactions = len(df)
    total_anomalies = df["anomaly_flag"].sum()

    return {
        "total_spend": total_spend,
        "total_transactions": total_transactions,
        "total_anomalies": total_anomalies
    }


def spend_by_category(df: pd.DataFrame):
    summary = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    summary["percentage"] = (
        summary["amount"] / summary["amount"].sum() * 100
    )

    return summary


def top_5_largest_transactions(df: pd.DataFrame):
    return df.sort_values("amount", ascending=False).head(5)


def anomaly_breakdown(df: pd.DataFrame):
    return {
        "category_anomalies": df["category_outlier_flag"].sum(),
        "duplicate_anomalies": df["duplicate_flag"].sum(),
        "high_absolute_risk": df["high_absolute_flag"].sum()
    }


def monthly_spend_trend(df: pd.DataFrame):
    df_copy = df.copy()
    df_copy["month"] = df_copy["date"].dt.to_period("M")

    monthly = (
        df_copy.groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    monthly["month"] = monthly["month"].astype(str)

    return monthly


def average_spend_per_category(df: pd.DataFrame):
    return (
        df.groupby("category")["amount"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
