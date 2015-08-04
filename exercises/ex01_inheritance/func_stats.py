"""
func_stats.py - example for list comprehensions
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

# Dictionary for accumulated function statistics.
# Each key is a function name.
# Each value is a two-item list of the total number of calls to the function
# and the total execution time of all calls.
_function_stats = {}


def add_stats(func_name, number_of_calls, total_time):
    _function_stats[func_name] = [number_of_calls, total_time]


def get_function_stats():
    """
    Returns list of 3-tuple:
        (function-name, number-of-calls, average-time-per-call)
    """
    # BONUS TODO: convert the following loop into a list comprehension
    # stat_list = []
    # sorted_stat_list = sorted(_function_stats.items(),
    #                           key=lambda stats: stats[0])
    # for name, [calls, total_time] in sorted_stat_list:
    #     avg_time = total_time/calls if calls > 0 else 0
    #     stat_list.append((name, calls, avg_time))

    sorted_stat_list = sorted(_function_stats.items(),
                              key=lambda stats: stats[0])

    stat_list = [(name, calls, total_time/calls if calls > 0 else 0)
                 for name, (calls, total_time) in sorted_stat_list]

    return stat_list


def clear_stats():
    global _function_stats
    _function_stats = {}


def main():
    add_stats('ccc_func', 20, 400)
    add_stats('aaa_func', 40, 200)
    add_stats('ddd_func', 0, 0)
    add_stats('bbb_func', 30, 300)

    for stats in get_function_stats():
        print(stats)


if __name__ == '__main__':
    main()
