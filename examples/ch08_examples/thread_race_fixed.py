#!/usr/bin/env python3
"""
thread_race_fixed.py - Demo of the use of locks to prevent a race condition
between threads

IMPORTANT: this program runs only with Python 3.7.
"""


# Copyright 2014 Brett Slatkin, Pearson Education Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import subprocess
from threading import Thread, Lock


# This program needs to run under Python 3.7. In newer versions of Python,
# many more operations are atomic, so race conditions are much less likely.
if f'{sys.version_info.major}.{sys.version_info.minor}' != '3.7':
    subprocess.run(['py', '-3.7', sys.argv[0]])
    exit()


class Counter:
    """A single instance of Counter will be shared by all worker threads
       to accumulate sensor reading counts"""
    def __init__(self):
        self.count = 0

    def increment(self, offset=1):
        self.count += offset


class SampleSensors:
    counter = Counter()  # single shared instance of Counter
    counter_lock = Lock()

    def sample_one_sensor(self, how_many):
        """Action for each work thread.

        Each sensor has its own worker thread. After each measurement,
        a worker increments the count in the shared Counter instance.
        :param how_many number of measurements the worker thread will take
        """

        for i in range(how_many):
            self.read_from_sensor()
            # acquire the lock before incrementing
            with SampleSensors.counter_lock:
                SampleSensors.counter.increment()

    def sample_sensors(self):
        threads = []
        for i in range(5):
            thread = Thread(target=SampleSensors.sample_one_sensor,
                            args=(self, 100_000))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

        print(f'Counter should be 500000, found {SampleSensors.counter.count}')

    def read_from_sensor(self):
        """ Dummy method """


def main():
    sampler = SampleSensors()
    sampler.sample_sensors()


if __name__ == '__main__':
    from timeit import timeit
    main_time = timeit('main()', setup="from __main__ import main", number=1)
    print(f'\nTime to run main with locking: {main_time:.2f} seconds')
