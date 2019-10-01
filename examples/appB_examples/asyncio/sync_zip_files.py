#!/usr/bin/python3.7
# sync_zip_files.py
# Example: py sync_zip_files.py *.txt

import sys, gzip, glob
from typing import List


def read_file(file: str) -> bytes:
    print(f"starting to read {file}")
    with open(file, "rb") as f:
        contents = f.read()
    print(f"    done reading {file}")
    return contents


def compress(data: bytes) -> bytes:
    return gzip.compress(data)


def write_file(file: str, contents: bytes) -> None:
    print(f"starting to write {file}")
    with open(file, "wb") as f:
        f.write(contents)
    print(f"    done writing {len(contents)} bytes to {file}")


def zip_file(file: str) -> None:
    contents = read_file(file)
    zipped_contents = compress(contents)
    write_file(file + ".gzip", zipped_contents)


def main(files: List[str]) -> None:
    for file in files:
        zip_file(file)


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        paths = glob.glob(f"{sys.argv[1]}")
        main(paths)
    else:
        print(f"Usage: {sys.argv[0]} file-name-pattern")
