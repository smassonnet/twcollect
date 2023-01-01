import gzip
import pathlib
import tempfile
from typing import List, Optional

import pytest

from twcollect.drivers import LocalFileDriver
from twcollect.drivers.local import (
    _FileMaxSizeReached,
    get_index_from_filename,
    get_latest_file_index,
)


def _assert_gzip_file_lines_content(file_path: pathlib.Path, payload: List[bytes]):
    with gzip.open(file_path) as f:
        assert f.readlines() == payload


def test_local_writelines_to_file_raises_max_size():
    with tempfile.TemporaryDirectory() as d:
        directory = pathlib.Path(d)
        driver = LocalFileDriver(path=directory, max_file_size=1)

        with pytest.raises(_FileMaxSizeReached):
            driver._writelines_to_file(directory / "tmp.zip", iter([b"aaaa", b"bbbb"]))


def test_local_writelines_to_file_complete():
    payload = [b"aaaa\n", b"bbbb\n"]
    with tempfile.TemporaryDirectory() as d:
        directory = pathlib.Path(d)
        file_path = directory / "tmp.zip"
        driver = LocalFileDriver(path=directory)

        driver._writelines_to_file(file_path, iter(payload))

        _assert_gzip_file_lines_content(file_path, payload)


@pytest.mark.parametrize(
    ("expected", "filename"),
    [
        (1, "tweets-1.jsonl.gz"),
        (None, "tweets-a.jsonl.gz"),
        (None, "tweets-11jsonl.gz"),
        (None, "tweets-1.jsonlgz"),
    ],
    ids=["ok", "not-number", "bad-ext-1", "bad-ext-2"],
)
def test_local_get_index_from_filename(expected: Optional[int], filename: str):
    assert get_index_from_filename(filename) == expected


def test_local_get_latest_file_index():
    # Multiple files with bad format
    assert (
        get_latest_file_index(
            [
                "tweets-1.jsonl.gz",
                "tweets-10.jsonl.gz",
                "tweets-1-11.jsonl.gz",
                "tweets-a.jsonl.gz",
            ]
        )
        == 10
    )

    # One valid file
    assert (
        get_latest_file_index(
            [
                "tweets-10.jsonl.gz",
                "tweets-1-11.jsonl.gz",
                "tweets-a.jsonl.gz",
            ]
        )
        == 10
    )

    # No files
    assert get_latest_file_index([]) == 0


def test_local_writelines_multi_files():
    a = b"a" * 100 + b"\n"
    b = b"b" * 100 + b"\n"
    c = b"c" * 100 + b"\n"
    with tempfile.TemporaryDirectory() as d:
        directory = pathlib.Path(d)
        driver = LocalFileDriver(path=directory, max_file_size=1)
        driver.writelines([a, b, c])

        files = directory.glob("tweets-*.jsonl.gz")
        filename_set = {f.name for f in files}
        assert filename_set == {
            "tweets-0.jsonl.gz",
            "tweets-1.jsonl.gz",
            "tweets-2.jsonl.gz",
            "tweets-3.jsonl.gz",
        }
        _assert_gzip_file_lines_content(directory / "tweets-0.jsonl.gz", [a])
        _assert_gzip_file_lines_content(directory / "tweets-1.jsonl.gz", [b])
        _assert_gzip_file_lines_content(directory / "tweets-2.jsonl.gz", [c])
        _assert_gzip_file_lines_content(directory / "tweets-3.jsonl.gz", [])


def test_local_writelines_existing_files():
    with tempfile.TemporaryDirectory() as d:
        directory = pathlib.Path(d)

        # Creating an existing indexed file
        (directory / "tweets-0.jsonl.gz").touch()
        (directory / "tweets-4.jsonl.gz").touch()

        driver = LocalFileDriver(path=directory)
        driver.writelines([b"abcdefg"])
        _assert_gzip_file_lines_content(directory / "tweets-0.jsonl.gz", [])
        _assert_gzip_file_lines_content(directory / "tweets-4.jsonl.gz", [b"abcdefg"])
