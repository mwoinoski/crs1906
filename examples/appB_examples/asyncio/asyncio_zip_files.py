#!/usr/bin/python3.7
# asyncio_zip_files.py
# pip install aiofiles
# Example: py asyncio_zip_files.py *.txt

import sys, asyncio, aiofiles, gzip, glob
from typing import List


async def read_file(file: str) -> bytes:
    print(f"starting to read {file}")
    async with aiofiles.open(file, "rb") as f:
        contents = await f.read()
    print(f"    done reading {file}")
    return contents


def compress(data: bytes) -> bytes:
    return gzip.compress(data)


async def write_file(file: str, contents: bytes) -> None:
    print(f"starting to write {file}")
    async with aiofiles.open(file, "wb") as f:
        await f.write(contents)
    print(f"    done writing {len(contents)} bytes to {file}")


async def zip_file(file: str) -> None:
    contents = await read_file(file)  # read a file asynchronously
    zipped_contents = compress(contents)  # zipping is CPU-bound, so asyncio won't help
    await write_file(file + ".gzip", zipped_contents)  # write a file asynchronously


async def main(files: List[str]) -> None:
    tasks = []
    for file in files:
        # calling an async function doesn't actually run the function; instead,
        # it creates a Task object that can be scheduled to run the function later
        task_obj = zip_file(file)
        tasks.append(task_obj)

    # Now schedule all the tasks to run asynchronously
    await asyncio.gather(*tasks)

    # The cool kids use a generator:
    # await asyncio.gather(*(zip_file(file_path) for file_path in file_paths))


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        print(f"Usage: {sys.argv[0]} file-name-pattern")
        sys.exit()

    paths = glob.glob(f"{sys.argv[1]}")
    if sys.version_info >= (3, 7):

        asyncio.run(main(paths))

    else:
        # Prior to Python 3.7, use the low-level AsyncIO API
        # to manage the event loop yourself:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(main(paths))
        finally:
            loop.close()
