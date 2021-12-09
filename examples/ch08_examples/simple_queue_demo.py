r"""
Demo of interprocess communication using synchronized queues.
"""

from multiprocessing import Process, SimpleQueue

# The SimpleQueue class handles all synchronization, 
# so there's no danger of deadlocks between processes

def produce(queue):
    """ Function executed by producer process """
    data = ('image.xpm', 'scaled_image.xpm')
    queue.put(data)  # producer adds data to the queue

def consume(queue):
    """ Function executed by consumer process """
    result = queue.get()  # consumer removes data from the queue
    # if there is no data on the queue, get() blocks, and
    # the consumer process waits
    
    print(result)    # prints "('image.jpg', 'scaled_image.jpg')"

# Must have a guard condition because the main module will be imported
# by each of the child processes. See "Safe importing of main module" at
# https://docs.python.org/3/library/multiprocessing.html#windows
if __name__ == '__main__':

    queue = SimpleQueue()  # create a synchronized queue

    # start producer and consumer child processes
    producer = Process(target=produce, args=(queue,)) 
    producer.start()  # calls produce(queue)

    consumer = Process(target=consume, args=(queue,))
    consumer.start()  # calls consume(queue)

    # wait for child processes to complete
    producer.join()
    consumer.join()
