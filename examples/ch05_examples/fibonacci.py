"""
fibonacci.py -
"""

def fib(n):
    # from http://en.literateprograms.org/Fibonacci_numbers_(Python)
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def fib_seq(n):
    seq = []
    if n > 0:
        seq.extend(fib_seq(n-1))
    seq.append(fib(n))
    return seq


def main():
    for i in range(20):
        fib_seq(i)

if __name__ == '__main__':
    print("Starting fibonacci...")
    main()
    # from timeit import timeit
    # loops = 100
    # best_time = timeit("main()",
    #                    setup="from __main__ import main",
    #                    number=loops)
    # print('Called main() {} times in {:.3} seconds'
    #       .format(loops, best_time))
    print("Done.")
