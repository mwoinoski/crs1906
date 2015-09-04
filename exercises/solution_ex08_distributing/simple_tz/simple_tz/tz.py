# TODO: add a docstring that describes this module. This string will be
# displayed when you execute help(tz) from a Python interpreter.
"""
Defines a simple wrapper for pytz functions.
"""

# TODO: set the variable `__author__` to a string with your name. This will
# also be displayed by help(tz)
__author__ = 'Happy Pythonista (hpythonista@python.org)'

import re
import pytz
from datetime import datetime

# Add a few timezone abbreviations missing from pytz
tz_abbrevs = {
    'CDT': 'CST6CDT',
    'CST': 'CST6CDT',
    'EDT': 'EST5EDT',
    'MDT': 'MST7MDT',
    'PDT': 'PST8PDT',
    'PST': 'PST8PDT',
}


# TODO: note the definition of the convert() function. This function will be
# accessible to scripts that import our new package.
# (no code change required)
def convert(time_str, from_tz, to_tz, time_format='%Y-%m-%d %H:%M:%S'):
    """
    Convert date/time from one timezone to another.

    :param time_str string representation of the date/time being converted
    :param from_tz string representation of the timezone of the input string
    :param to_tz string representation of the timezone of the output string
    :param time_format time format string in the same format as the
        datatime.strptime() format string
    :return string representation of the converted datatime
    """
    from_datetime_no_tz = datetime.strptime(time_str, time_format)
    from_timezone = pytz.timezone(tz_abbrevs.get(from_tz, from_tz))
    from_datetime_with_tz = from_timezone.localize(from_datetime_no_tz)
    utc_dt = pytz.utc.normalize(from_datetime_with_tz.astimezone(pytz.utc))

    to_timezone = pytz.timezone(tz_abbrevs.get(to_tz, to_tz))
    to_datetime = to_timezone.normalize(utc_dt.astimezone(to_timezone))
    to_datetime_str_no_tz = re.sub(r'[+-]\d\d:\d\d$', '', str(to_datetime))
    return to_datetime_str_no_tz
