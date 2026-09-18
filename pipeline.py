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


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    
    logging.basicConfig(
        level = logging.DEBUG if verbose else logging.INFO,
        format = "%(asctime)s %(levelname)-8s %(message)s",
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
        "--output", "-o",
        required = True,
        help = "Output file name"
    )
    
    parser.add_argument(
        "--format",
        choices = ["json", "csv"],
        default = "csv",
        help = "Output format"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action = "store_true",
        help = "Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    setup_logging(verbose=args.verbose)
    
    logger.debug(f"Arguments parsed: input = {args.input}, output = {args.output}, format = {args.format}")
    
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
        sys.exit(1)
    
    pass  # TODO: implement


if __name__ == "__main__":
    main()
