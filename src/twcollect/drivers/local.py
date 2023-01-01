import dataclasses
import gzip
import logging
import pathlib
import re
from typing import Callable, Generator, Iterable, Iterator, List, Optional

_logger = logging.getLogger()


_FILE_PART_RE = re.compile(r"tweets-(\d+)\.jsonl\.gz")


class _FileMaxSizeReached(Exception):
    pass


def get_index_from_filename(filename: str) -> Optional[int]:
    """Extracts file index from filename

    Examples:
        Filename: `tweets-2.jsonl.gz` -> `2`

        Filename: `tweets-a.jsonl.gz` -> `None`
    """
    match = _FILE_PART_RE.fullmatch(filename)
    if match is None:
        # No match
        return None
    return int(match.group(1))


def get_latest_file_index(filenames: List[str]) -> int:
    """The number suffix of the file to write the next documents

    Returns:
        int: Index of next file
    """
    file_indices = list(filter(None, (get_index_from_filename(f) for f in filenames)))
    if len(file_indices) == 0:
        # When no files we start at 0
        return 0
    if len(file_indices) == 1:
        # Only one file
        return file_indices[0]
    # Otherwise multiple files
    return max(file_indices)


@dataclasses.dataclass
class LocalFileDriver:
    """Drivers that writes text in local files

    Attributes:
        path (str): The path to a local folder
        max_file_size (int): The maximum file size before writing to a new file.
            Default to 1G.
    """

    path: pathlib.Path
    max_file_size: int = 2**30

    def __post_init__(self):
        # Must be a valid folder
        try:
            self.path.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            # The path exists and is a not a folder
            raise ValueError("The path should be a folder.")

    def _iterate_line_until_file_max_size(
        self, file_size_fun: Callable[[], int], lines: Iterator[bytes]
    ) -> Generator[bytes, None, None]:
        while True:
            # If the file is already too big, we raise
            if file_size_fun() > self.max_file_size:
                raise _FileMaxSizeReached("Maximum file size reached")

            # Try to get the next element, if we reached the end, we stop
            try:
                line = next(lines)
            except StopIteration:
                break

            yield line

    def _writelines_to_file(
        self, file_path: pathlib.Path, lines: Iterator[bytes]
    ) -> None:
        """Write lines to a file until we reach the max_file_size

        Raises:
            _FileMaxSizeReached: When the file if bigger that the max_file_size
        """
        with gzip.open(file_path, mode="ab") as f:
            for line in self._iterate_line_until_file_max_size(f.tell, lines):
                f.write(line)

    def get_current_file_index(self) -> int:
        """The number suffix of the file to write the next documents

        Returns:
            int: Index of next file
        """
        filenames = [f.name for f in self.path.glob("tweets-*.jsonl.gz") if f.is_file()]
        return get_latest_file_index(filenames)

    def file_index_to_name(self, index: int) -> pathlib.Path:
        return self.path / f"tweets-{index}.jsonl.gz"

    def writelines(self, lines: Iterable[bytes]) -> None:
        lines_iterator = iter(lines)
        file_index = self.get_current_file_index()
        while True:
            file_path = self.file_index_to_name(file_index)
            try:
                _logger.info(f"Starting to write to file {file_path}")
                self._writelines_to_file(file_path, lines_iterator)
            except _FileMaxSizeReached:
                # Move to next file
                file_index += 1
            else:
                # We went reached the end of the stream
                break
