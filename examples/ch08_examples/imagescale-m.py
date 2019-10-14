#!/usr/bin/env python3
"""
Image scaling example from 'Python in Practice' by Mark Summerfield

Implemented with concurrent.future.ProcessPoolExecutor
"""

# Copyright © 2012-13 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version. It is provided for
# educational purposes and is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import sys
import argparse
import collections
import concurrent.futures
import math
import multiprocessing
import os
from Image import Image, Error
import Qtrac
from concurrent.futures import ProcessPoolExecutor

Result = collections.namedtuple("Result", "copied scaled name")
Summary = collections.namedtuple("Summary", "todo copied scaled canceled")


def scale(size, smooth, src_dir, dest_dir, num_procs):
    futures = set()  # create empty set
    with ProcessPoolExecutor(max_workers=num_procs) as executor:
        for src_image, dest_image in get_jobs(src_dir, dest_dir):
            future = executor.submit(scale_one, size, smooth,
                                     src_image, dest_image)
            futures.add(future)

        summary = wait_for(futures)
        return summary
    # When 'with' block completes, it calls ProcessPoolExecutor.showdown()

    # if we caught the KeyboardInterrupt in this function we'd lose the
    # accumulated todo, copied, scaled counts.


def wait_for(futures):
    canceled = False
    copied = scaled = 0
    try:
        for future in concurrent.futures.as_completed(futures):
            err = future.exception()
            if err is None:
                result = future.result()
                copied += result.copied
                scaled += result.scaled
                Qtrac.report("{} {}".format(
                    "copied" if result.copied else "scaled",
                    os.path.basename(result.name)))
            elif isinstance(err, Error):
                Qtrac.report(str(err), True)
            else:
                raise err  # Unanticipated
    except KeyboardInterrupt:  # Ctrl-C
        Qtrac.report("cancelling...")
        canceled = True
        for future in futures:
            future.cancel()
    return Summary(len(futures), copied, scaled, canceled)


def scale_one(size, smooth, src_image, dest_image):
    try:
        old_image = Image.from_file(src_image)
        if old_image.width <= size and old_image.height <= size:
            old_image.save(dest_image)
            return Result(1, 0, dest_image)
        else:
            if smooth:
                img_scale = min(size / old_image.width, size / old_image.height)
                new_image = old_image.scale(img_scale)
            else:
                stride = int(math.ceil(max(old_image.width / size,
                                           old_image.height / size)))
                new_image = old_image.subsample(stride)
            new_image.save(dest_image)
            return Result(0, 1, dest_image)
    except Exception as e:
        Qtrac.report("Problem scaling " +
                     os.path.basename(src_image), error=True)
        Qtrac.report(str(e), error=True)
        return Result(0, 0, src_image)


def get_jobs(src_dir, dest_dir):
    for file_name in os.listdir(src_dir):
        src_file_path = os.path.join(src_dir, file_name)
        dest_file_path = os.path.join(dest_dir, file_name)
        yield src_file_path, dest_file_path


def summarize(summary, concurrency):
    message = "copied {} scaled {} ".format(summary.copied, summary.scaled)
    difference = summary.todo - (summary.copied + summary.scaled)
    if difference:
        message += "skipped {} ".format(difference)
    message += "using {} processes".format(concurrency)
    if summary.canceled:
        message += " [canceled]"
    Qtrac.report(message)
    print()


def main():
    size, smooth, source, target, concurrency = handle_commandline()
    Qtrac.report("starting...")
    summary = scale(size, smooth, source, target, concurrency)
    summarize(summary, concurrency)


def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--concurrency", type=int,
                        default=multiprocessing.cpu_count(),
                        help="specify the concurrency (for debugging and "
                             "timing) [default: %(default)d]")
    parser.add_argument("-s", "--size", default=45, type=int,
                        help="make a scaled image that fits the given dimension "
                             "[default: %(default)d]")
    parser.add_argument("-S", "--smooth", action="store_true",
                        help="use smooth scaling (slow but good for text)")
    parser.add_argument("source",
                        help="the directory containing the original .xpm images")
    parser.add_argument("target",
                        help="the directory for the scaled .xpm images")
    args = parser.parse_args()
    source = os.path.abspath(args.source)
    target = os.path.abspath(args.target)
    if source == target:
        args.error("source and target must be different")
    if not os.path.exists(args.target):
        os.makedirs(target)
    return args.size, args.smooth, source, target, args.concurrency


if __name__ == "__main__":
    main()
