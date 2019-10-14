#!/usr/bin/env python3
"""
Image scaling example from 'Python in Practice' by Mark Summerfield

Implemented with multiprocessing.JoinableQueue and Queue
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

import argparse
import collections
import math
import multiprocessing
import os
from Image import Image
import Qtrac


Result = collections.namedtuple("Result", "copied scaled name")
Summary = collections.namedtuple("Summary", "todo copied scaled canceled")


def main():
    size, smooth, src_dir, dest_dir, num_procs = handle_commandline()
    Qtrac.report("starting...")
    summary = scale(size, smooth, src_dir, dest_dir, num_procs)
    summarize(summary, num_procs)


def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--num_procs", type=int,
        default=multiprocessing.cpu_count(),
        help="specify the concurrency (for debugging and "
             "timing) [default: %(default)d]")
    parser.add_argument(
        "-s", "--size", default=45, type=int,
        help="make a scaled image that fits the given dimension "
             "[default: %(default)d]")
    parser.add_argument(
        "-S", "--smooth", action="store_true",
        help="use smooth scaling (slow but good for text)")
    parser.add_argument(
        "source",
        help="the directory containing the original .xpm images")
    parser.add_argument(
        "dest",
        help="the directory for the scaled .xpm images")
    args = parser.parse_args()
    src_dir = os.path.abspath(args.source)
    dest_dir = os.path.abspath(args.dest)
    if src_dir == dest_dir:
        args.error("source and destination directories must be different")
    if not os.path.exists(args.dest):
        os.makedirs(dest_dir)
    return args.size, args.smooth, src_dir, dest_dir, args.num_procs


def scale(size, smooth, src_dir, dest_dir, num_procs):
    canceled = False
    jobs = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    create_processes(size, smooth, jobs, results, num_procs)
    for src_image, dest_image in get_jobs(src_dir, dest_dir):
        jobs.put((src_image, dest_image))
    try:
        jobs.join()
    except KeyboardInterrupt: # catch Ctrl-C (may not work on Windows)
        Qtrac.report("canceling...")
        canceled = True
    copied = scaled = 0
    todo = results.qsize()
    while not results.empty():  # Safe because all jobs have finished
        result = results.get_nowait()
        copied += result.copied
        scaled += result.scaled
    return Summary(todo, copied, scaled, canceled)


def create_processes(size, smooth, jobs, results, num_procs):
    for _ in range(num_procs):
        process = multiprocessing.Process(
            target=worker,
            args=(size, smooth, jobs, results))
        process.daemon = True
        process.start()


def worker(size, smooth, jobs, results):
    while True:
        try:
            scr_image, dest_image = jobs.get()
            try:
                result = scale_one(size, smooth, scr_image, dest_image)
                Qtrac.report("{} {}".format("copied" if result.copied else
                             "scaled", os.path.basename(result.name)))
                results.put(result)
            except Image.Error as err:
                Qtrac.report(str(err), True)
        finally:
            jobs.task_done()


def get_jobs(src_dir, dest_dir):
    for file_name in os.listdir(src_dir):
        src_file_path = os.path.join(src_dir, file_name)
        dest_file_path = os.path.join(dest_dir, file_name)
        yield src_file_path, dest_file_path


def scale_one(size, smooth, scr_image, dest_image):
    old_image = Image.from_file(scr_image)
    if old_image.width <= size and old_image.height <= size:
        old_image.save(dest_image)
        return Result(1, 0, dest_image)
    else:
        if smooth:
            image_scale = min(size / old_image.width, size / old_image.height)
            new_image = old_image.scale(image_scale)
        else:
            stride = int(math.ceil(max(old_image.width / size,
                                       old_image.height / size)))
            new_image = old_image.subsample(stride)
        new_image.save(dest_image)
        return Result(0, 1, dest_image)


def summarize(summary, num_procs):
    message = "copied {} scaled {} ".format(summary.copied, summary.scaled)
    difference = summary.todo - (summary.copied + summary.scaled)
    if difference:
        message += "skipped {} ".format(difference)
    message += "using {} processes".format(num_procs)
    if summary.canceled:
        message += " [canceled]"
    Qtrac.report(message)
    print()


if __name__ == "__main__":
    main()
