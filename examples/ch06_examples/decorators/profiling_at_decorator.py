from decorators.profiling_decorator import profile_call

@profile_call
def nsum(n):
    """Return the sum of the first n numbers"""
    assert(n >= 0), "n must be >= 0"
    sum = 0
    for i in range(n+1):
        sum += i
    return sum

@profile_call
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


@profile_call
def simple():
    """Function has no arguments and returns no value"""
    print("printed in simple()")

# Profiling decorator applied with '@profile_call', no need for monkey patching

if __name__ == "__main__":

    fib_result = fibonacci(20, debug=True)
    print(f"in main, fibonacci(20, debug=True) = {fib_result}\n")

    nsum_result = nsum(1000000)
    print(f"in main, nsum(1000000) = {nsum_result}\n")

    simple_result = simple()
    print(f"in main, simple() = {simple_result}\n")
