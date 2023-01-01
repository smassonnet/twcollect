import dataclasses
import logging
import time
from typing import ClassVar, Dict, Generator, Optional

import requests

_logger = logging.getLogger(__name__)


class FilteredStreamWithNoRulesException(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(
            "Attempting to connect to a stream with no defined rules. "
            "Check that you have created at least one rule on the "
            "stream you are connecting to.",
            *args,
        )


@dataclasses.dataclass
class TwitterStreamReader:
    twitter_token: str
    parameters: Optional[Dict[str, str]] = None

    url_streams: ClassVar[str] = "https://api.twitter.com/2/tweets/search/stream"

    def authorization_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.twitter_token}"}

    def _open_stream(self) -> Generator[bytes, None, None]:
        requests_call = requests.get(
            self.url_streams,
            headers=self.authorization_header(),
            params=self.parameters,
            stream=True,
        )
        with requests_call as response:
            if response.status_code == 409:
                raise FilteredStreamWithNoRulesException()
            if not response.ok:
                _logger.error(
                    "Error returned by Twitter stream API:"
                    f"{response.status_code=},"
                    f"{response.text=},"
                )
                response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    _logger.info(f"Received a tweet {line}")
                    yield line + b"\n"

    def read(self) -> Generator[bytes, None, None]:
        """Reads and restart connection on failures

        Returns:
            Generator[str, None, None]: Each string returned
                is a JSON response from Twitter
        """
        retry_delays = [2, 10, 100]
        retry_idx = 0
        while True:
            try:
                for tweet_bytes in self._open_stream():
                    retry_idx = 0
                    yield tweet_bytes
            except requests.HTTPError:
                # Getting and incrementing retry delay
                delay = retry_delays[retry_idx]
                retry_idx = min(len(retry_delays) - 1, retry_idx + 1)
                # Logging error
                _logger.error(
                    "Error when reading stream from Twitter."
                    f"Retrying in {delay} seconds"
                )
                time.sleep(delay)
