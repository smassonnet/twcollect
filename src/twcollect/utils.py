import argparse
import logging
import pathlib


def folder_type(path: str) -> pathlib.Path:
    """Parse a path and makes sure it is a folder"""
    output = pathlib.Path(path)
    if output.exists() and not output.is_dir():
        raise argparse.ArgumentTypeError("The path should be a folder.")
    return output


def valid_file_type(path: str) -> pathlib.Path:
    output = pathlib.Path(path)
    if (output.exists() and not output.is_file()) or not output.exists():
        raise argparse.ArgumentTypeError("The path should be a valid file.")
    return output


def add_credentials_file_argument(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--credentials-file",
        "-c",
        dest="credentials",
        type=valid_file_type,
        default="credentials.yml",
        help="A yaml file with mapping between credential name and value",
    )


def add_log_level_argument(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        help="Logging level",
    )


def setup_logging(log_level: str):
    logging.basicConfig(level=getattr(logging, log_level))
