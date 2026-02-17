import pandas as pd

REQUIRED_COLUMNS = ["date", "amount", "description"]

class CSVValidationError(Exception):
    pass


def validate_columns(df: pd.DataFrame):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise CSVValidationError(
            f"Missing required columns: {', '.join(missing)}"
        )


def validate_and_load(file):
    try:
        df = pd.read_csv(file)
    except Exception as e:
        raise CSVValidationError(f"Invalid CSV file: {str(e)}")

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    validate_columns(df)

    return df
