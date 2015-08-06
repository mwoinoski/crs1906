import sys
import datetime
from optparse import OptionParser
from ctypes import *

from ctypes import cdll, c_int, cast, POINTER
import os

# .dll file is located in the current directory.
# To build the DLL, run:  mingw32-make

library = 'calc_z_ser.dll'

library = os.path.join(*(os.path.split(__file__)[:-1] + (library,)))
print("Loading DLL from " + library)

library_mod = cdll.LoadLibrary(library)

# The type of ctypes.cdll is ctypes.LibraryLoader. If you reference an
# attribute with the same name as a DLL, the LibraryLoader loads the DLL.
# So the following can replace the call to LoadLibrary:
# library_mod = ctypes.cdll.calc_z_ser


class COMPLEX(Structure):
    _fields_ = [("real", c_double), ("imag", c_double)]

# area of space to investigate
x1, x2, y1, y2 = -2.13, 0.77, -1.3, 1.3


def calculate_z_serial(q, maxiter):
    """Calls C function calc_z_ser() for the bulk of the calculation."""
    len_q = len(q)

    # double* calc_z_ser(COMPLEX*, int, int)
    calc_z_ser = library_mod.calc_z_ser
    calc_z_ser.argtypes = (POINTER(COMPLEX), c_int, c_int)
    calc_z_ser.restype = POINTER(c_double) * len_q

    # Convert Python array of complex to ctypes array of COMPLEX structs
    complex_array = (COMPLEX * len_q)()
    for index in range(len_q):
        q_value = q[index]
        complex_array[index].real = q_value.real
        complex_array[index].imag = q_value.imag

    # call the C function
    output = calc_z_ser(complex_array, len_q, maxiter)

    # return array of Python doubles
    return output


def calc(maxiter, w, h, show_output):
    """Make a list of x and y values which will represent q"""
    x_step = (float(x2 - x1) / float(w)) * 2
    y_step = (float(y1 - y2) / float(h)) * 2
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step
    q = []
    for ycoord in y:
        for xcoord in x:
            q.append(complex(xcoord, ycoord))

    output = calculate_z_serial(q, maxiter)

    if show_output:
        try:
            from PIL import Image
            import numpy as nm
            output = nm.array(output)
            output = (output + (256*output) + (256**2)*output) * 8
            im = Image.new("RGB", (int(w/2), int(h/2)))
            im.fromstring(output.tostring(), "raw", "RGBX", 0, -1)
            im.show()
        except ImportError as err:
            # Bail gracefully if we're using PyPy
            print("Couldn't import Image or numpy:", str(err))


if __name__ == "__main__":
    usage = "usage: %prog [options] image-width number-of-iterations"
    parser = OptionParser(usage=usage)
    parser.add_option("-n", "--no-display", dest="display",
                      action="store_false", default=True,
                      help="do not display result image")
    parser.add_option("-p", "--profile-calc", dest="profile_calc",
                      action="store_true", default=False,
                      help="run cProfile on the call to calc()")

    (options, args) = parser.parse_args()
    if len(args) == 2:
        # get width/height and max iterations from cmd line
        #     python mandelbrot.py 1000 50
        w = int(args[0])  # e.g. 1000
        h = w
        maxiter = int(args[1])  # e.g. 50
        # we can show_output for Python, not for PyPy
        is_not_pypy = sys.version.find('PyPy') < 0
        if not options.profile_calc:
            calc(maxiter, w, h, is_not_pypy and options.display)
        else:
            import cProfile
            cProfile.run('calc(is_not_pypy and options.display)')
    else:
        parser.print_help()
