"""
string_cat_demo.py - Run timings of string concatenation strategies,
from chapter 5
"""

from simple_profiler import measure

##############################################################################
# String concatenation examples
##############################################################################

@measure
def to_lower_string_concatenation(lines):
    """String concatenation: slow"""
    r = ''
    for line in lines:
        r += line.lower()
    return r


@measure
def to_lower_joining_individual_strings(lines):
    """Joining individual strings: very slow"""
    r = ''
    for line in lines:
        r = ''.join((r, line.lower()))
    return r


@measure
def to_lower_appending_strings_to_list(lines):
    """Appending strings to list, then a single join: fast"""
    r = []
    for line in lines:
        r.append(line.lower())
    return ''.join(r)


##############################################################################
# Examples of passing data aggregates to functions
##############################################################################

@measure
def to_lower_one_call(lines):
    """One call to to_lower(): fast"""
    return to_lower_append_all_lines_in_function(lines)


def to_lower_append_all_lines_in_function(lines):
    r = []
    for line in lines:
        r.append(line.lower())
    return ''.join(r)


@measure
def to_lower_many_calls(lines):
    """Many calls to to_lower_append_line_to_buffer(): slow

    Compare this method's performance with to_lower_append_all_lines_in_function(),
    which uses a similar technique but avoids extra method calls"""
    r = []
    for line in input_lines:
        to_lower_append_line_to_buffer(line, r)
    result = ''.join(r)
    return result


def to_lower_append_line_to_buffer(line, buffer):
    """This method must be called many times to process all lines"""
    buffer.append(line.lower())


if __name__ == '__main__':
    with open('big_input_file.html') as f:
        all_lines = f.read().split(sep='\n')

    input_lines = all_lines[1:10000]

    print("String concatenation demo:")
    to_lower_string_concatenation(input_lines)
    to_lower_joining_individual_strings(input_lines)
    to_lower_appending_strings_to_list(input_lines)

    print("\nFunction call overhead demo:")
    to_lower_one_call(input_lines)
    to_lower_many_calls(input_lines)
