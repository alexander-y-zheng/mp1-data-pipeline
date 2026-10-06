# src/data_validator.py
import logging
import pandas as pd


logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data.

    required_columns: a list of column names that must exist.
    numeric_columns: a list of column names whose values should be numeric.
    """
    original_row_count = df.shape[0]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        for col in missing_columns:
            if col not in df.columns:
                logger.error(f"Missing required column: {col}")
                raise ValueError(f"Missing required column: {col}")

    for col in numeric_columns:
        invalid_rows = []
        for i, value in df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except (TypeError, ValueError):
                    invalid_rows.append(i)

        # Remove the invalid rows.
        if invalid_rows:
            logger.warning(
                "Removed %s rows with invalid numeric values in %s",
                len(invalid_rows),
                col,
            )
            df = df.drop(index=invalid_rows)

        # Convert to a numeric data type.
        df[col] = pd.to_numeric(df[col])

    logger.debug(
        "Validation: %s -> %s rows",
        original_row_count,
        df.shape[0],
    )

    return df