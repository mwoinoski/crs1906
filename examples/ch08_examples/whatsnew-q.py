#!/usr/bin/env python3
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
import multiprocessing
import os
import queue
import tempfile
from threading import Thread
import webbrowser
import Feed
import Qtrac


def main():
    limit, how_many_threads = handle_commandline()
    Qtrac.report("starting...")
    filename = os.path.join(os.path.dirname(__file__), "whatsnew.dat")

    jobs = queue.Queue()
    results = queue.Queue()
    create_threads(limit, jobs, results, how_many_threads)
    todo = add_jobs(filename, jobs)
    process(todo, jobs, results, how_many_threads)


def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--limit", type=int, default=0,
            help="the maximum items per feed [default: unlimited]")
    parser.add_argument("-c", "--concurrency", type=int,
            default=multiprocessing.cpu_count() * 4,
            help="specify the concurrency (for debugging and "
                "timing) [default: %(default)d]")
    args = parser.parse_args()
    return args.limit, args.concurrency


def create_threads(limit, jobs, results, how_many_threads):
    for _ in range(how_many_threads):
        thread = Thread(target=worker,
                        args=(limit, jobs, results))
        thread.daemon = True
        thread.start()


def worker(limit, jobs, results):
    while True:
        try:
            feed = jobs.get()
            # Feed is a namedtuple of (name, rss_url)
            ok, result = Feed.read(feed, limit)
            if not ok:
                Qtrac.report(result, True)
            elif result is not None:
                Qtrac.report("read {}".format(result[0][4:-6]))
                results.put(result)
        finally:
            jobs.task_done()


def add_jobs(filename, jobs):
    # Feed.iter() yields a Feed instance (name, rss_url)
    for todo, feed in enumerate(Feed.iter(filename), start=1):
        jobs.put(feed)  # add the feed to the input queue
    return todo  # number of feeds added to jobs queue


def process(todo, jobs, results, how_many_threads):
    canceled = False
    try:
        jobs.join() # Wait for all the work to be done
    except KeyboardInterrupt: # May not work on Windows
        Qtrac.report("canceling...")
        canceled = True
    if canceled:
        done = results.qsize()
    else:
        done, filename = output(results)
    Qtrac.report("read {}/{} feeds using {} threads{}".format(done, todo,
                 how_many_threads, " [canceled]" if canceled else ""))
    print()
    if not canceled:
        webbrowser.open(filename)


def output(results):
    done = 0
    filename = os.path.join(tempfile.gettempdir(), "whatsnew.html") 
    with open(filename, "wt", encoding="utf-8") as file:
        file.write("<!doctype html>\n")
        file.write("<html><head><title>What's New</title></head>\n")
        file.write("<body><h1>What's New</h1>\n")
        while not results.empty(): # Safe because all jobs have finished
            result = results.get_nowait()
            done += 1
            for item in result:
                file.write(item)
        file.write("</body></html>\n")
    return done, filename


if __name__ == "__main__":
    main()
