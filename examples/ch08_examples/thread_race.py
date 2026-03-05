"""
Demo of a race condition.

Depending on the performance of your VM, you may need either to increase or
decrease the value of the global `goal` variable to get interesting results.
"""

from threading import Thread
import time, os

buffer = []

sentinel = object()  # value that means "end of data"
produced = 0
consumed = 0

goal = 500  # you may need to tweak this value
expected = 2 * goal  # two producers should produce this many items

def producer(pid):
    global produced
    for i in range(goal):
        buffer.append((pid, i))
        produced += 1
        time.sleep(0)   # hack to increase the chance of a race condition
    buffer.append(sentinel)  # add sentinel to end of buffer


def consumer(cid):
    global consumed, expected
    while True:
        if len(buffer) > 0:  # check that there is an item to pop
            time.sleep(0)    # hack to increase the chance of a race condition
            try:
                item = buffer.pop(0)
                if item is sentinel:
                    return
                else:
                    consumed += 1
            except IndexError:
                print("pop failed because buffer was empty", flush=True)
                print("race detected by consumer", cid, flush=True)
                print_stats(expected, produced, consumed)
                os._exit(1)  # hard exit
        else:
            time.sleep(0) # yield the CPU so another thread has a chance


def print_stats(expected, produced, consumed):
    print("expected:", expected)
    print("produced:", produced)
    print("consumed:", consumed)


threads = [
    Thread(target=producer, args=(1,)),
    Thread(target=producer, args=(2,)),
    Thread(target=consumer, args=(1,)),
    Thread(target=consumer, args=(2,))
]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("No race condition detected", flush=True)
print_stats(expected, produced, consumed)
