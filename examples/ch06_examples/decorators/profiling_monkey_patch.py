from decorators.profiling_decorator import profile_call


def nsum(n):
    """Return the sum of the first n numbers"""
    assert(n >= 0), "n must be >= 0"
    total = 0
    for i in range(n+1):
        total += i
    return total


def fibonacci(n, debug=False):
    """Returns the nth number of the Fibonacci sequence"""
    assert(n >= 1), "n must be >= 1"
    prev_num = 0
    next_num = 1
    fib = 0
    for i in range(0, n):
        fib = prev_num + next_num
        prev_num = next_num
        next_num = fib
    if debug:
        print(f'fibonacci({n} returned {fib}')
    return fib


def simple():
    """Function has no arguments and returns no value"""
    print("printed in simple()")


# Monkey patch functions to apply profiling decorator
nsum = profile_call(nsum)
fibonacci = profile_call(fibonacci)
simple = profile_call(simple)

if __name__ == "__main__":

    fib_result = fibonacci(20, debug=True)
    print(f"in main, fibonacci(20, debug=True) = {fib_result}\n")

    nsum_result = nsum(1000000)
    print(f"in main, nsum(1000000) = {nsum_result}\n")

    simple_result = simple()
    print(f"in main, simple() = {simple_result}\n")
