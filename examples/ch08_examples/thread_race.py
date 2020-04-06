#!/usr/bin/env python3
"""
thread_race.py - Demo of a race condition among threads
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

from threading import Thread


class Counter:
    """A single instance of Counter will be shared by all worker threads
       to accumulate sensor reading counts"""
    def __init__(self):
        self.count = 0

    def increment(self, offset=1):
        self.count += offset


class SampleSensors:
    counter = Counter()  # single shared instance of Counter

    def worker(self, how_many):
        """Action for each work thread.

        Each sensor has its own worker thread. After each measurement,
        a worker increments the count in the shared Counter instance.
        :param how_many number of measurements the worker thread will take
        """

        for i in range(how_many):
            self.read_from_sensor()  # Get the measurement
            SampleSensors.counter.increment()  # Bump number of measurements

    def sample_sensors(self):
        threads = []
        for i in range(5):
            thread = Thread(target=SampleSensors.worker,
                            args=(self, 100_000))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

        print(f'Counter should be 500000, found {SampleSensors.counter.count}')

    def read_from_sensor(self):
        """ Dummy method """
        pass


def main():
    sampler = SampleSensors()
    sampler.sample_sensors()


if __name__ == '__main__':
    from timeit import timeit
    main_time = timeit('main()', setup="from __main__ import main", number=1)
    print(f'\nTime to run main: {main_time:.2f} seconds')
