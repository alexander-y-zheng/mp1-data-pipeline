# tests/test_data_validator.py

import pytest

from src import validate_dataframe


def test_validate_dataframe_removes_invalid_ratings(sample_df):
    # Set the required and numeric column names.
    required_columns = ["record_id", "name", "rating", "category", "status"]
    numeric_columns = ["rating"]

    # Call validate_dataframe().
    validated_df = validate_dataframe(sample_df, required_columns, numeric_columns)
    
    # Assert that 98 rows remain and all five columns are preserved.
    assert validated_df.shape[0] == 98
    assert list(validated_df.columns) == required_columns
    

def test_validate_dataframe_with_missing_column(sample_df):
    # Set required_columns to include a nonexistent column.
    required_columns = ["record_id", "name", "rating", "category", "status", "nonexistent_column"]
    numeric_columns = ["rating"]
    
    # Use pytest.raises(ValueError) around validate_dataframe().
    with pytest.raises(ValueError):
        validate_dataframe(sample_df, required_columns, numeric_columns)
