"""
ping_threaded.py - Multi-threaded ping example from Chapter 9

author: Noah Gift
"""

__author__ = 'Noah Gift (https://www.linkedin.com/in/noahgift)'

from threading import Thread
import subprocess
from queue import Queue
import platform


# wraps system ping command
def pinger(index, q):
    """Pings a host"""
    while True:
        host = q.get()
        print("Thread {}: Pinging {}".format(index, host))
        is_win = platform.system() == 'Windows'
        try:
            ret = subprocess.call(
                "ping -{} 1 {}".format('n' if is_win else 'c', host),
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                timeout=2)  # timeout after 2 seconds
            if ret == 0:
                print("{}: is alive".format(host))
            else:
                print("{}: did not respond".format(host))
        except subprocess.TimeoutExpired:
            print("{}: did not respond".format(host))

        # notify Queue that this work item has been processed
        q.task_done()


def main():
    hosts = ["google.com", "yahoo.com", "ebay.com", "twitter.com"]
    queue = Queue()

    # Spawn thread pool
    for i, _ in enumerate(hosts, start=1):
        worker = Thread(target=pinger, args=(i, queue))
        worker.setDaemon(True)
        worker.start()

    # Place work in queue
    for host in hosts:
        queue.put(host)

    # Wait until worker threads are done to exit
    queue.join()


if __name__ == '__main__':
    main()
