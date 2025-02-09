"""
func_stats.py - example for comparing performance of "for" loops and
list comprehensions.
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
    Returns list of 3-tuples:
        (function-name, number-of-calls, average-time-per-call)
    """

    # BONUS TODO: version 1: note how we create a list of function stats with a 
    #             `for` loop. After reviewing this code, profile this program
    #             using either cProfile or timeit.
    stat_list = []
    sorted_stat_list = sorted(_function_stats.items(),
                              key=lambda stats: stats[0])
    for name, [calls, total_time] in sorted_stat_list:
        avg_time = total_time/calls if calls > 0 else 0
        stat_list.append((name, calls, avg_time))

    # BONUS TODO: version 2: note how the following code creates the function
    #             stats using a list comprehension. After profiling version 1, 
    #             comment out the code above, uncomment the following code, 
    #             and profile this program again.
    # sorted_stat_list = sorted(_function_stats.items(),
    #                           key=lambda stats: stats[0])
    #
    # stat_list = [(name, calls, total_time/calls if calls > 0 else 0)
    #              for name, (calls, total_time) in sorted_stat_list]

    return stat_list


def clear_stats():
    global _function_stats
    _function_stats = {}


def main():
    for i in range(10**5):
        add_stats('func'+str(i), 20, 400)

    all_stats = get_function_stats()
    print(f'got stats for {len(all_stats)} functions')


if __name__ == '__main__':
    main()

