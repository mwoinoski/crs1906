"""
Demo of a race condition.

Depending on the performance of your VM, you may need either to increase or
decrease the values of the global RACE_CHANCE and PRODUCER_DELAY variables to
get interesting results.
"""

from threading import Thread
import time, os, random

# Because this code is so simple, the race condition will rarely occur unless
# we hack the code a bit. The following values introduce processing delays
# that increase the chance of the race condition. But in production code,
# race conditions happen with no additional coaxing :)

# Tweak the following values as needed to get an occasional race condition.
# Make one or both values larger to increase the rate of failure.
# Make them smaller to decrease the rate of failure
RACE_CHANCE = 0.10  # widen the dangerous check-then-pop gap 10% of the time
PRODUCER_DELAY = 0.0005  # slow down the producer

buffer = []

sentinel = object()  # value that means "end of data"
produced = 0
consumed = 0
expected = 100
stop = False

def producer(pid):
    global produced
    for i in range(expected):
        buffer.append((pid, i))
        produced += 1
        time.sleep(PRODUCER_DELAY)  # hack to increase the chance of a race condition

    buffer.append(sentinel)

def consumer(cid):
    global consumed, stop
    while not stop:
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
