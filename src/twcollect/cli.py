"""CLI to start data collection from Twitter stream"""


import argparse
import urllib.parse

from twcollect.utils import (
    add_credentials_file_argument,
    add_log_level_argument,
    folder_type,
    setup_logging,
)
from twcollect.config import parse_credentials_file
from twcollect.drivers import LocalFileDriver
from twcollect.streams import TwitterStreamReader


def collect_cli():
    parser = argparse.ArgumentParser(
        "python -m twcollect",
        description="Script that connects to a Tweet stream and writes data to disk",
    )

    add_log_level_argument(parser)

    # Get stream query parameters
    parser.add_argument(
        "--parameters",
        "-p",
        default=None,
        type=urllib.parse.parse_qs,
        help="Query-string parameters to pass when getting the stream URL",
    )

    # Credentials
    add_credentials_file_argument(parser)

    # Target folder
    parser.add_argument(
        "output_path",
        type=folder_type,
        help="The path to the output folder to store tweets",
    )

    # Driver options
    parser.add_argument(
        "--max-file-size",
        default=2**30,
        type=int,
        help="Maximum output file size (Defaults to 1 Gigabyte)",
    )

    # Get arguments
    arguments = parser.parse_args()

    # Logging
    setup_logging(arguments.log_level)

    # Getting credentials
    credentials = parse_credentials_file(arguments.credentials)
    twitter_token = credentials.__root__["twitter_token"]

    reader = TwitterStreamReader(
        twitter_token=twitter_token, parameters=arguments.parameters
    )

    tweet_stream = reader.read()
    output_path = arguments.output_path
    driver = LocalFileDriver(output_path, max_file_size=arguments.max_file_size)
    driver.writelines(tweet_stream)
