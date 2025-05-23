"""
fibonacci.py - Fibonacci sequence generator
"""

from argparse import ArgumentParser

usage_msg = 'python fibonacci.py [-h|-v]'
verbose = False

def get_command_line_args():
    parser = ArgumentParser(description='Fibonacci sequence generator',
                            usage=usage_msg)
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='enable verbose output')
    return parser.parse_args()


def fib(n):
    # from http://en.literateprograms.org/Fibonacci_numbers_(Python)
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def fib_seq(n):
    seq = []
    if n > 0:
        seq.extend(fib_seq(n - 1))
    seq.append(fib(n))
    return seq


def main():
    values = 20
    for i in range(1, values + 1):  # noqa
        next_fib_seq = fib_seq(i)
    if verbose and i == values:  # noqa
        print(f'First {values} Fibonacci numbers: {next_fib_seq}')  # noqa


if __name__ == '__main__':
    verbose = get_command_line_args().verbose

    main()

    # from timeit import timeit
    # loops = 100
    # total_time = timeit("main()",
    #                    setup="from __main__ import main",
    #                    number=loops)
    # avg_time_per_call = total_time / loops
    # print(f'Called main() {loops} times,',
    #       f'average time per call was {avg_time_per_call:.3f} seconds')  # noqa
