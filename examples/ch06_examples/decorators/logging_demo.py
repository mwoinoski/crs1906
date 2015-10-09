from decorators.logging_decorator import log_call
from decorators.profiling_decorator import profile_call


@log_call
def nsum(n):
    """Return the sum of the first n numbers"""
    assert(n >= 0), "n must be >= 0"
    sum = 0
    for i in range(n+1):
        sum += i
    return sum

@log_call
def fibonacci(n, debug=False):
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
def simple():
    """Function has no arguments and returns no value"""
    print("printed in simple()")

if __name__ == "__main__":

    fib_result = fibonacci(20, debug=True)
    print("\nin main, fibonacci(20, debug=True) = {}\n".format(fib_result))

    nsum_result = nsum(1000000)
    print("\nin main, nsum(1000000) = {}\n".format(nsum_result))

    simple_result = simple()
    print("\nin main, simple() = {}\n".format(simple_result))


