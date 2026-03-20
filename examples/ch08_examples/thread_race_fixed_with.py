"""
Demo of how to fix a race condition using a lock using a `with` statement to
handle the lock acquisition and release.
"""

from threading import Thread, Lock
import time, os, random

RACE_CHANCE = 0.10  # widen the dangerous check-then-pop gap 10% of the time
PRODUCER_DELAY = 0.0005  # slow down the producer

buffer = []
buffer_lock = Lock()  # create a Lock

sentinel = object()  # value that means "end of data"
produced = 0
consumed = 0
expected = 1000
stop = False

def producer(pid):
    global produced
    for i in range(expected):
        # attempt to acquire the lock. If another thread is holding the lock,
        # wait until the other thread releases it.
        with buffer_lock:
            buffer.append((pid, i))
            produced += 1
        time.sleep(PRODUCER_DELAY)  # hack to increase the chance of a race condition

    # now add the sentinel to the end of the buffer.
    with buffer_lock:
        buffer.append(sentinel)


def consumer(cid):
    global consumed, stop
    while not stop:
        with buffer_lock:
            if len(buffer) > 0:  # check that there is an item to pop
                if random.random() < RACE_CHANCE:  # widen the race window only sometimes
                    time.sleep(0)
                try:
                    item = buffer.pop(0)
                    if item is sentinel:
                        stop = True
                        return
                    else:
                        consumed += 1
                except IndexError:
                    print("\npop failed because buffer was empty", flush=True)
                    print("race detected by consumer", cid, flush=True)
                    print_stats(expected, produced, consumed)
                    os._exit(1)  # hard exit, kills all threads
            else:
                time.sleep(0)  # yield the CPU so another thread has a chance


def print_stats(items_expected, items_produced, items_consumed):
    print("expected:", items_expected)
    print("produced:", items_produced)
    print("consumed:", items_consumed)

threads = [
    Thread(target=producer, args=(1,)),
    Thread(target=consumer, args=(1,)),
    Thread(target=consumer, args=(2,))
]

for t in threads:  # start producer and consumer threads
    t.start()
for t in threads:  # wait for all child threads to complete
    t.join()

print("\nNo race condition detected", flush=True)
print_stats(expected, produced, consumed)
