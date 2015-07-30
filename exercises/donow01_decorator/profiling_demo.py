from logging_decorator import log_call
from profiling_decorator import profile_call

@log_call
@profile_call
def nsum(n, *args):
    """Return the sum of the first n numbers"""
    assert(n >= 0), "n must be >= 0"
    sum = 0
    for i in range(n+1):
        sum += i
    return sum

@log_call
@profile_call
def fibonacci(n, *args):
    """Returns the nth number of the Fibonacci sequence"""
    assert(n >= 1), "n must be >= 1"
    prev = 0
    next = 1
    for i in range(0, n):
        fib = prev + next
        prev = next
        next = fib
    return fib

@log_call
@profile_call
def simple():
    """Function has no arguments and returns no value"""
    print("printed in simple()")

if __name__ == "__main__":
    print("\nin main, fibonacci(100) = {}\n".format(fibonacci(100)))
    print("\nin main, nsum(1000000) = {}\n".format(nsum(1000000)))
    print("\nin main, simple() = {}\n".format(simple()))


