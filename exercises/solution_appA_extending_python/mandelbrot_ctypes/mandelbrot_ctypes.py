import sys
import datetime
from optparse import OptionParser

from ctypes import cdll, c_int, cast, POINTER, Structure, c_double
from os.path import abspath, join, split

# .dll file is located in the current directory.
# To build the DLL, run:  make

library = 'calc_z_ser.dll'

library = join(*(split(abspath(__file__))[:1] + (library,)))
print("Loading DLL from " + library)

# TODO: note how we load the DLL and save a reference to it in library_mod
# (no code change required)
library_mod = cdll.LoadLibrary(library)

# The type of ctypes.cdll is ctypes.LibraryLoader. If you reference an
# attribute with the same name as a DLL, the LibraryLoader loads the DLL.
# So the following line of code can replace the call to LoadLibrary:
# library_mod = ctypes.cdll.calc_z_ser

# TODO: note the definition of the Python COMPLEX class. This will map to
# the C complex_num struct declared in calc_z_ser.h
# (no code change required)
class COMPLEX(Structure):
    _fields_ = [
        ("real", c_double),  # defines a field named `real` of type double
        ("imag", c_double)   # defines a field named `imag` of type double
    ]

# area of space to investigate
x1, x2, y1, y2 = -2.13, 0.77, -1.3, 1.3

# TODO: note the definition of the calculate_z_serial() function
# (no code change required)
def calculate_z_serial(q, maxiter):
    """Calculate values to plot a Mandelbrot function."""
    # TODO: note the descriptions of the parameters to calculate_z_serial:
    """
    :param q: list of built-in complex objects. The Python complex class
        defines two data attributes, `real` and `imag`
    :param maxiter: maximum number of loops
    """

    # TODO: note that we save the number of elements on the input list
    # in the variable len_q. You'll need this later.
    # (no code change required)
    len_q = len(q)

    # double* calc_z_ser(COMPLEX*, int, int)

    # TODO: note how we set calc_z_ser to reference the C function from the
    # library.
    # (no code change required)
    calc_z_ser = library_mod.calc_z_ser

    # TODO: set calc_z_ser.argtypes to a tuple with the types of the arguments
    # to the calc_z_ser() function:
    # 1. POINTER to COMPLEX
    # 2. POINTER to c_int
    # 3. c_int
    # 4. c_int
    calc_z_ser.argtypes = (POINTER(COMPLEX), POINTER(c_int), c_int, c_int)

    # TODO: set the C function's result type to be c_int
    calc_z_ser.restype = c_int

    # Convert Python array of complex to ctypes array of COMPLEX structs

    # TODO: create a new array class for the first argument to the C function.
    # This array will have the same length as the input list.
    complex_array_class = COMPLEX * len_q

    # TODO: create an array of COMPLEX by calling the constructor for the
    # array class that you just created.
    # Assign the array to a variable named `complex_array`
    complex_array = complex_array_class()

    # TODO: create a new array class for the second argument to the C function.
    # This array will have the same length as the input list.
    int_array_class = c_int * len_q

    # TODO: create an array of c_int by calling the constructor for the
    # array class that you just created.
    # Assign the array to a variable named `output_array`
    output_array = int_array_class()

    for index in range(len_q):
        # TODO: note how we copy the attributes from each complex object on
        # the input list to an element complex_array.
        # (no code change required)
        q_value = q[index]
        complex_array[index].real = q_value.real
        complex_array[index].imag = q_value.imag

    # TODO: call the C function calc_z_ser(), passing the following arguments:
    # 1. complex_array
    # 2. output_array
    # 3. the length of the arrays
    # 4. maxiter
    # import pdb; pdb.set_trace();
    calc_z_ser(complex_array, output_array, len_q, maxiter)

    # TODO: create a Python list from the output_array. Store the Python list
    # in a variable named output_list.
    output_list = list(output_array)

    # TODO: return the Python list
    return output_list


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

    start_time = datetime.datetime.now()

    # TODO: note the call to calculate_z_serial().
    # (no code change required)
    output = calculate_z_serial(q, maxiter)

    end_time = datetime.datetime.now()
    secs = end_time - start_time
    print("Main took", secs)

    validation_sum = sum(output)
    print("Total sum of elements (for validation):", validation_sum)

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
