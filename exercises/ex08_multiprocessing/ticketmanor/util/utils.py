"""
Utility functions
"""

# To enable tracing from command line:
#  python -m trace -t --ignore-module=trace,abc,_weakrefset,_bootstrap,cp437 path/to/module.py

import inspect
import json


__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

# Define table that maps characters to HTML entities.
# Use a list of tuples instead of a dictionary to ensure that amp is
# escaped first, to avoid double escaping
html_escape_table = [
    ('&', "&amp;"),
    ('<', "&lt;"),
    ('>', "&gt;"),
    ('"', "&quot;"),
    ('"', "&#34;"),
    ("'", "&apos;"),
    ("'", "&#39;"),
]


def html_escape(text):
    """Converts special characters to HTML entities"""
    for pair in html_escape_table:
        text = text.replace(pair[0], pair[1])
    return text


def html_unescape(text):
    """Converts HTML entities to special characters"""
    for pair in reversed(html_escape_table):
        text = text.replace(pair[1], pair[0])
    return text


def func_name(obj):
    return type(obj).__name__ + "." + \
        inspect.currentframe().f_back.f_code.co_name


class SimpleJsonEncoder(json.JSONEncoder):
    """JSON encoder that leverages an object's __json__() method.

    If the object being encoded defines __json__(), SimpleJsonEncoder uses it.
    Otherwise, it uses the default JSON encoding of json.JSONEncoder

    Usage: json_str = json.dumps(some_object, cls=SimpleJsonEncoder)
    """
    def default(self, obj):
        return obj.__json__() if hasattr(obj, '__json__') \
            else json.JSONEncoder.default(self, obj)


# FIXME: add class name to output of tracefunc
# def tracefunc(frame, event, arg, indent=[0]):
#       if event == "call":
#           indent[0] += 2
#           print(" " * indent[0] + "> call function", frame.f_code.co_name)
#       elif event == "return":
#           print(" " * indent[0] + "< exit function", frame.f_code.co_name)
#           indent[0] -= 2
#       return tracefunc
#
# import sys
# sys.settrace(tracefunc)
