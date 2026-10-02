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
from data_loaders import load_data
from data_processor import process_data, create_cleaning_report


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    
    logging.basicConfig(
        level = logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt = "%H:%M:%S"
    )


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


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    
    if not Path(filepath).is_file():
        logger.error(f"Input file not found: {filepath}")
        return False
    
    logger.info(f"Input file validated: {filepath}")
    return True


def main():
    """Main pipeline function."""
    
    args = parse_arguments()
    
    if validate_input(args.input) == False:
        logger.error("Invalid input file: %s", args.input)
        sys.exit(1)

    if validate_input(args.config) == False:
        logger.error("Invalid config file: %s", args.config)
        sys.exit(1)
        
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        logger.error("Failed to load input or config file")
        sys.exit(1)

    original_data = data.copy()

    try:
        processed_data = process_data(data, config)
    except ValueError:
        logger.error("Data processing failed")
        sys.exit(1)

    

    logger.info("Processing complete: %s → %s rows", original_data.shape[0], processed_data.shape[0])

    # save processed data to the output file
    processed_data.to_csv(args.output, index=False)
    logger.info(f"Processed data saved to {args.output}")
    
    print(create_cleaning_report(original_data, processed_data))


if __name__ == "__main__":
    main()
