#!/usr/bin/env python3
"""
thread_lock_demo.py - Demo of use of Lock to prevent race condition
among threads
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
from random import random

from threading import Barrier, Thread


def read_from_sensor():
    pass


# I have a barrier in here so the workers synchronize
# when they start counting, otherwise it's hard to get a race
# because the overhead of starting a thread is high.
barrier = Barrier(5)  # required to artificially force race conditions


class Counter:
    """A single instance of Counter will be shared by all worker threads
       to accumulate sensor reading counts"""
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


def worker(sensor_index, how_many, counter):
    """Action for each work thread.

    Each sensor has its own worker thread. After each measurement,
    a worker increments the count in the shared Counter instance.
    :param how_many number of measurements the worker thread will take
    :param counter shared Counter instance
    """
    barrier.wait()  # forces the race condition to manifest more often

    for i in range(how_many):
        read_from_sensor()  # Get the measurement
        counter.increment(1)  # Bump the number of measurements so far


how_many_measurements = 10**5

counter = Counter()  # single shared instance of Counter

threads = []
for i in range(5):
    thread = Thread(target=worker,
                    args=(i, how_many_measurements, counter))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

print('Counter should be {}, found {}'
      .format(5 * how_many_measurements, counter.count))
