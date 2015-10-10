"""
string_cat_demo.py - Run timings of string concatenation strategies,
from chapter 7
"""

from simple_profiler import measure


@measure
def concatenate1(lines):
    """Using string concatenation"""
    r = ''
    for line in lines:
        r += line
    return len(r)


@measure
def concatenate2(lines):
    """Using join in a loop"""
    r = ''
    for line in lines:
        r = ''.join((r, line))
    return len(r)


@measure
def concatenate3(lines):
    """Much faster appending strings to a list and then joining them"""
    r = []
    for line in lines:
        r.append(line)
    r = ''.join(r)
    return len(r)


if __name__ == '__main__':
    with open('big_input_file.html') as f:
        all_lines = f.read().split(sep='\n')

    input_lines = all_lines[1:20000]

    concatenate1(input_lines)
    concatenate2(input_lines)
    concatenate3(input_lines)
