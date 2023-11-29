#!/usr/bin/env python3
"""
thread_race_fixed.py - Demo of use of Lock to prevent a race condition
between threads
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

from threading import Thread, Lock


class Counter:
    """A single instance of Counter will be shared by all worker threads
       to accumulate sensor reading counts"""
    def __init__(self):
        self.count = 0

    def increment(self, offset=1):
        # self.count += offset  # race condition occurs with Python 3.7 and earlier
        self.count += offset * self.forceRaceCondition()  # race condition always occurs

    def forceRaceCondition(self):
        """Hack to force a race condition in Python 3.10+

        Python 3.10 introduced changes that reduced the chance of race
        conditions. But if we add a method call to the statement, it makes
        a race condition more likely. For an explanation, see
        https://stefan-marr.de/2023/11/python-global-interpreter-lock/
        """
        return 1


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
            self.read_from_sensor()  # Get the measurement
            with SampleSensors.counter_lock:
                SampleSensors.counter.increment()  # Bump number of measurements

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
    # For demo purposes only: wait for two threads to arrive at the Barrier
    # This greatly increases the chance of a race condition
    from threading import Barrier
    barrier = Barrier(2, lambda: barrier.reset())

    from timeit import timeit
    main_time = timeit('main()', setup="from __main__ import main", number=1)
    print(f'\nTime to run main: {main_time:.2f} seconds')
