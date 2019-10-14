import sys
import datetime
from optparse import OptionParser
from ctypes import Structure, c_int, c_double

# TODO: import calc_z_ser from the calc_z_ser_ext_mod extension module
# Note: ignore the error message from PyCharm. It doesn't recognize
# C extension modules.
....

# TODO: import array from the array module
# HINT: see slide A-21
....

# area of space to investigate
x1, x2, y1, y2 = -2.13, 0.77, -1.3, 1.3


class COMPLEX(Structure):
    _fields_ = [
        ("real", c_double),  # defines a field named "real" of type double
        ("imag", c_double)   # defines a field named "imag" of type double
    ]


def calc(maxiter, w, h, show_output):
    """Make a list of x and y values which will represent q"""
    start_time = datetime.datetime.now()
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

    len_q = len(q)

    print("Total elements:", len_q)

    # TODO: create an array of COMPLEX with length len_q exactly as you did in
    # mandelbrot_ctypes/mandelbrot_ctypes.py. Assign the array to a variable
    # named complex_array.
    complex_array = ....

    for index in range(len_q):
        # TODO: note how we copy the attributes from each complex object on
        # the input list to an element complex_array.
        # (no code change required)
        complex_array[index].real = q[index].real
        complex_array[index].imag = q[index].imag

    # TODO: note how assign an array of int to output_array, with each
    # element initialized to 0.
    # (no code change required)
    output_array = array('i', [0] * len_q)

    # TODO: call the calc_z_ser() function from the extension module.
    # Arguments: complex_array, output_array, len(q), maxiter
    ....

    end_time = datetime.datetime.now()
    secs = end_time - start_time
    print(f"Calculations completed in {end_time - start_time} seconds")

    # TODO: note how we sum the output_array elements, exactly as before
    # (no code change required)
    validation_sum = sum(output_array)
    print("Total sum of elements (for validation):", validation_sum)

    if show_output:
        try:
            from PIL import Image
            import numpy as nm
            output = nm.array(output_array)
            output = (output + (256*output) + (256**2)*output) * 8
            im = Image.new("RGB", (int(w/2), int(h/2)))
            im.frombytes(output.tostring(), "raw", "RGBX", 0, -1)
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
