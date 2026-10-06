# DS 3500 MP1: Data Processing Pipeline

This command-line pipeline loads CSV data and YAML configuration, validates the input, applies configurable cleaning steps, and saves the cleaned data as a CSV file. Run it with the included sample dataset and configuration using the command below. The root `pipeline.py` coordinates the workflow and reports validation and processing results. The `src/data_loaders.py` module loads CSV, JSON, and YAML files, while `src/data_validator.py` checks required columns and converts configured numeric columns. The `src/data_processor.py` module removes duplicates, handles missing values, and filters outliers according to the configuration. The `src/data_output.py` module creates the output directory and writes the cleaned CSV without an index. Shared logging and input-path validation are provided by `src/utils.py`, and `config/config.yaml` specifies the validation and processing settings.

## Run

```powershell
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

## Example output

With the included sample data, the pipeline validates 100 input rows, removes invalid numeric entries, and saves 92 cleaned rows:

```text
INFO     src.data_loaders — Loaded CSV file: fixtures\sample_data.csv (100 rows)
INFO     src.data_loaders — Loaded YAML file: config\config.yaml
WARNING  src.data_validator — Invalid value in column 'rating' at row 94: not_available
WARNING  src.data_validator — Invalid value in column 'rating' at row 95: error
INFO     __main__ — Data validated: 98 rows
INFO     __main__ — Processing complete: 98 → 92 rows
INFO     __main__ — Processed data saved to output/clean.csv

 Cleaning Report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```