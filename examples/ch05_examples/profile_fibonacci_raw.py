"""
profile_fibonacci_raw.py - Example from MOTW http://pymotw.com/2/
"""

import cProfile


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
    print('RAW')
    print('=' * 80)
    cProfile.run('main()', sort='ncalls')
    # common sort values: 'calls' 'ncalls' 'tottime' 'cumulative'


