"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description = "Data Processing Pipeline"
    )
    
    parser.add_argument(
        "--input", "-i",
        required = True,
        help = "Input file to process"
    )

    parser.add_argument(
        "--config", "-c",
        required = True,
        help = "Configuration file for data processing"
    )
    
    parser.add_argument(
        "--output", "-o",
        required = True,
        help = "Output file name"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action = "store_true",
        help = "Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    setup_logging(verbose=args.verbose)
    
    logger.debug(f"Arguments parsed: input={args.input}, output={args.output}, config={args.config}")
    
    return args



def main():
    """Main pipeline function."""
    
    args = parse_arguments()
    
    if validate_input(args.input) == False:
        logger.error("Invalid input file: %s", args.input)
        sys.exit(1)

    if validate_input(args.config) == False:
        logger.error("Invalid config file: %s", args.config)
        sys.exit(1)

    # load data
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        logger.error("Failed to load input or config file")
        sys.exit(1)

    original_data = data.copy()
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    # Validate data before processing.
    try:
        data = validate_dataframe(original_data, required_columns, numeric_columns)
    except ValueError:
        logger.error("Data validation failed")
        sys.exit(1)
    logger.info(
        "Validation complete: %s -> %s rows",
        original_data.shape[0],
        data.shape[0],
    )

    # Process the validated data.
    processing_input = data.copy()
    try:
        processed_data = process_data(data, config)
    except ValueError:
        logger.error("Data processing failed")
        sys.exit(1)

    logger.info(
        "Processing complete: %s -> %s rows",
        processing_input.shape[0],
        processed_data.shape[0],
    )

    # save processed data to the output file
    save_data(processed_data, args.output)
    logger.info("Saved cleaned data to %s", args.output)
    
    print("\nCleaning report:")
    print(create_cleaning_report(processing_input, processed_data))


if __name__ == "__main__":
    main()
