# data_processor.py
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""

    original_size = df.shape[0]
    df = df.drop_duplicates()
    new_size = df.shape[0]

    logger.debug("remove_duplicates: %s -> %s rows", original_size, new_size)

    return df


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""

    
    original_size = df.shape[0] if axis == "rows" else df.shape[1]

    if axis == "rows":
        df = df.dropna(axis=0)
    elif axis == "columns":
        df = df.dropna(axis=1)
    else:
        logger.error("Invalid axis: %s", axis)
        raise ValueError("axis must be 'rows' or 'columns'")

    new_size = df.shape[0] if axis == "rows" else df.shape[1]
    unit = "rows" if axis == "rows" else "columns"
    logger.debug("handle_missing: %s -> %s %s", original_size, new_size, unit)

    return df


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""

    if method not in {"iqr", "zscore"}:
        logger.error("Unsupported outlier method: %s", method)
        raise ValueError("method must be 'iqr' or 'zscore'")

    for col in columns:
        if col not in df.columns:
            logger.warning("Column not found: %s", col)
            continue

        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning("Column is not numeric: %s", col)
            continue

        original_size = df.shape[0]
        if method == "iqr":
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        else:  # method == "zscore"
            mean = df[col].mean()
            std = df[col].std()
            lower_bound = mean - threshold * std
            upper_bound = mean + threshold * std
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

        logger.debug(
            "%s: method=%s, threshold=%s, removed=%s",
            col,
            method,
            threshold,
            original_size - df.shape[0],
        )

    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""

    if config["processing"]["remove_duplicates"]:
        df = remove_duplicates(df)

    if config["processing"]["missing"]["enabled"]:
        axis = config["processing"]["missing"]["axis"]
        df = handle_missing(df, axis=axis)

    if config["processing"]["outliers"]["enabled"]:
        columns = config["processing"]["outliers"]["columns"]
        method = config["processing"]["outliers"]["method"]
        threshold = config["processing"]["outliers"]["threshold"]
        df = remove_outliers(df, columns=columns, method=method, threshold=threshold)

    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    
    report = {
        "rows_before": df_before.shape[0],
        "rows_after": df_after.shape[0],
        "rows_removed": df_before.shape[0] - df_after.shape[0],
        "columns_before": df_before.shape[1],
        "columns_after": df_after.shape[1],
        "columns_removed": df_before.shape[1] - df_after.shape[1],
    }

    return report
