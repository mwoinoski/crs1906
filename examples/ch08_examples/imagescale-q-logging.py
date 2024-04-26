#!/usr/bin/env python3
"""
This is a version of the imaging scaling application that demonstrates a
technique for using a Logger from multiple processes. As mentioned in the
Logging HOWTO, Loggers are thread safe but not process safe, so Processes
that log messages to the same file can overwrite each other's output. The
QueueLogger class defined below can be used as a drop-in replacement for a
standard Logger. When a client Process calls one of QueueLogger's methods,
it adds the message to a Queue, which is processed by a background Process.
That is the only Process that actually writes output to the log file, so there
are no race conditions when writing to the log file.

Relevant section in Logging HOWTO:
https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes

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
from os.path import basename
import logging
import logging.config
from multiprocessing import Process

# The loading of the logging config file must be done in global scope
logging.config.fileConfig('logging.conf')


class QueueLogger:
    """
    The QueueLogger class supports multiple processes writing to the same log
    file. Its interface is similar to the standard Logger class.
    """
    def __init__(self):
        self.msg_queue = multiprocessing.Queue()
        self.logger = logging.getLogger('multiprocess_logger')

    def logging_worker(self):
        while True:
            record = self.msg_queue.get()
            if record is None:
                break
            self.logger.log(*record)

    def debug(self, msg, *args, **kwargs):
        self.msg_queue.put((logging.DEBUG, msg, *args, *kwargs))

    def info(self, msg, *args, **kwargs):
        self.msg_queue.put((logging.INFO, msg, *args, *kwargs))

    def warn(self, msg, *args, **kwargs):
        self.msg_queue.put((logging.WARNING, msg, *args, *kwargs))

    def error(self, msg, *args, **kwargs):
        self.msg_queue.put((logging.ERROR, msg, *args, *kwargs))

    def fatal(self, msg, *args, **kwargs):
        self.msg_queue.put((logging.FATAL, msg, *args, *kwargs))

    def critical(self, msg, *args, **kwargs):
        self.msg_queue.put((logging.CRITICAL, msg, *args, *kwargs))


Result = collections.namedtuple("Result", "copied scaled name")
Summary = collections.namedtuple("Summary", "todo copied scaled canceled")


def main():
    logger = QueueLogger()
    logger_process = Process(target=QueueLogger.logging_worker,
                             args=(logger,))
    # ensure the logger process won't stop the interpreter from exiting
    logger_process.daemon = True
    logger_process.start()

    size, smooth, src_dir, dest_dir, num_procs = handle_commandline()
    logger.info("Starting...")
    summary = scale(logger, size, smooth, src_dir, dest_dir, num_procs)
    summarize(logger, summary, num_procs)
    logger.info("Done")


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


def scale(logger, size, smooth, src_dir, dest_dir, num_procs):
    canceled = False
    jobs = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    create_processes(logger, size, smooth, jobs, results, num_procs)
    for src_image, dest_image in get_jobs(src_dir, dest_dir):
        jobs.put((src_image, dest_image))
    try:
        jobs.join()
    except KeyboardInterrupt: # catch Ctrl-C (may not work on Windows)
        logger.info("canceling...")
        canceled = True
    copied = scaled = 0
    todo = results.qsize()
    while not results.empty():  # Safe because all jobs have finished
        result = results.get_nowait()
        copied += result.copied
        scaled += result.scaled
    return Summary(todo, copied, scaled, canceled)


def create_processes(logger, size, smooth, jobs, results, num_procs):
    for _ in range(num_procs):
        process = multiprocessing.Process(
            target=worker,
            args=(logger, size, smooth, jobs, results))
        process.daemon = True
        process.start()


def worker(logger, size, smooth, jobs, results):
    while True:
        try:
            scr_image, dest_image = jobs.get()
            try:
                result = scale_one(logger, size, smooth, scr_image, dest_image)
                logger.debug("%s %s", "copied" if result.copied else "scaled",
                             basename(result.name))
                results.put(result)
            except Image.Error as err:
                logger.error(str(err))
        finally:
            jobs.task_done()


def get_jobs(src_dir, dest_dir):
    for file_name in os.listdir(src_dir):
        src_file_path = os.path.join(src_dir, file_name)
        dest_file_path = os.path.join(dest_dir, file_name)
        yield src_file_path, dest_file_path


def scale_one(logger, size, smooth, scr_image, dest_image):
    logger.debug('scale_one(%d, %s, %s, %s)',
                 size, smooth, basename(scr_image), basename(dest_image))

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


def summarize(logger, summary, num_procs):
    message = "copied {} scaled {} ".format(summary.copied, summary.scaled)
    difference = summary.todo - (summary.copied + summary.scaled)
    if difference:
        message += "skipped {} ".format(difference)
    message += "using {} processes".format(num_procs)
    if summary.canceled:
        message += " [canceled]"
    logger.info(message)


if __name__ == "__main__":
    main()
