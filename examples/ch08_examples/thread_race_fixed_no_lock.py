#!/usr/bin/env python3
"""
thread_race_fixed_no_lock.py - Re-designed threading code that does not require
a lock because there is no possibility of a race condition.
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
    def __init__(self):
        self.count = 0

    def increment(self, offset=1):
        self.count += offset

class WorkerThread(Thread):
    """Each worker thread will have its own unique Counter instance"""

    def __init__(self, sample_sensor, sensor_index, how_many):
        super().__init__()
        self.counter = Counter()
        self.sample_sensor = sample_sensor
        self.sensor_index = sensor_index
        self.how_many = how_many

    def run(self):
        """Action for each work thread.

        Each sensor has its own worker thread. After each measurement,
        a worker increments the count in the shared Counter instance.
        :param how_many number of measurements the worker thread will take
        """
        for i in range(self.how_many):
            self.sample_sensor.read_from_sensor()  # Get the measurement
            self.counter.increment()  # Bump number of measurements

class SampleSensors:
    def __init__(self, worker_thread_count):
        self.worker_thread_count = worker_thread_count
        
    def sample_sensors(self):
        how_many = 10**5
        threads = []
        for i in range(self.worker_thread_count):
            thread = WorkerThread(self, i, how_many)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

        print('Counter should be {}, found {}'
              .format(self.worker_thread_count*how_many, 
                      sum(thread.counter.count for thread in threads)))

    def read_from_sensor(self):
        pass
        
def main():
    sampler = SampleSensors(5)
    sampler.sample_sensors()

if __name__ == '__main__':
    from timeit import timeit
    print("\nTime to run main: {:.2f} seconds".format(
        timeit('main()', setup="from __main__ import main", number=1)))
