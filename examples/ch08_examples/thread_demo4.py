"""
threading_demo2.py - threading demo from Chapter 8

Creates a Thread instance directly, calls a method.
"""

from threading import Thread
import shutil


class DiskUsage(Thread):
    def __init__(self, target_dir):
        super().__init__()
        self.target_dir = target_dir
        self.results = None

    def run(self):
        print('Getting disk usage for "{}"'.format(self.target_dir))
        total, used, free = shutil.disk_usage('/')
        self.results = used / total

disk_usage_thread = DiskUsage('/')
disk_usage_thread.start()  # start the Thread executing
print('Main thread is running while DiskUsage thread is running')

disk_usage_thread.join()  # Wait for the child_process task to finish
disk_usage = disk_usage_thread.results  # Main thread gets child thread results

print('Root dir is {:.1f}% full'.format(100 * disk_usage))
