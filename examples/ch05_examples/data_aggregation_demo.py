"""
data_aggregation_demo.py - Run timings of string concatenation strategies,
from chapter 5
"""

from simple_profiler import measure


@measure
def concatenate1(lines, buffer):
    """Using string concatenation"""
    for line in lines:
        buffer = cat1(line, buffer)
    return buffer


def cat1(line, buffer):
    """Using string concatenation"""
    buffer += line
    return buffer


@measure
def concatenate2(lines, buffer):
    """Using join in a loop"""
    for line in lines:
        buffer = cat2(line, buffer)
    return buffer


def cat2(line, buffer):
    """Using join in a loop"""
    buffer = ''.join((buffer, line))
    return buffer


@measure
def concatenate3(lines, buffer):
    """Much faster appending strings to a list and then joining them"""
    for line in lines:
        cat3(line, buffer)


def cat3(line, buffer):
    """Much faster appending strings to a list and then joining them"""
    buffer.append(line)


if __name__ == '__main__':
    with open('big_input_file.html') as f:
        all_lines = f.read().split(sep='\n')

    input_lines = all_lines[1:20000]

    r = ''
    r = concatenate1(input_lines, r)
    print('len(res) =', len(r))

    r = ''
    r = concatenate2(input_lines, r)
    print('len(r) =', len(r))

    r = []
    concatenate3(input_lines, r)
    r = ''.join(r)
    print('len(r) =', len(r))
