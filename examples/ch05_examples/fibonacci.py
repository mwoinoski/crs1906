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
    for i in range(1, 20):
        next_fib_seq = fib_seq(i)
        print(f'First {i+1} Fibonacci numbers: {next_fib_seq}')


if __name__ == '__main__':
    print("Starting fibonacci...")
    main()
    # from timeit import timeit
    # loops = 100
    # total_time = timeit("main()",
    #                    setup="from __main__ import main",
    #                    number=loops)
    # avg_time_per_call = total_time / loops
    # print(f'Called main() {loops} times,',
    #       f'average time per call was {avg_time_per_call:.3f} seconds')
    print('Done.')
