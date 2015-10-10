import sys
import datetime
from optparse import OptionParser


# TODO: cut the entire calculate_z_serial() function from here and paste it
# in the calc_z_ser_cython.pyx file.
# def calculate_z_serial(q, maxiter):
#     """Pure python with complex datatype, iterating over list of q and z"""
#     z = [complex(0, 0)] * len(q)
#     output = [0] * len(q)
#     for i in range(len(q)):
#         for iteration in range(maxiter):
#             z[i] = z[i]*z[i] + q[i]
#             if abs(z[i]) > 2.0:
#                 output[i] = iteration
#                 break
#     return output

# TODO: import the calc_z_ser function from the calc_z_ser_cython module.
# Note: ignore PyCharm errors from the import.
from calc_z_ser_cython import calculate_z_serial


# area of space to investigate
x1, x2, y1, y2 = -2.13, 0.77, -1.3, 1.3


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

    len_q = len(q)
    print("Total elements:", len_q)
    start_time = datetime.datetime.now()

    # TODO: note that the call to calculate_z_serial is unchanged.
    output = calculate_z_serial(q, maxiter)

    end_time = datetime.datetime.now()
    secs = end_time - start_time
    print("Main took", secs)

    validation_sum = sum(output)
    print("Total sum of elements (for validation):", validation_sum)

    # replace this when mingw64 works
    # if show_output:
    #     try:
    #         from PIL import Image
    #         import numpy as nm
    #         output = nm.array(output)
    #         output = (output + (256*output) + (256**2)*output) * 8
    #         im = Image.new("RGB", (int(w/2), int(h/2)))
    #         im.fromstring(output.tostring(), "raw", "RGBX", 0, -1)
    #         im.show()
    #     except ImportError as err:
    #         # Bail gracefully if we're using PyPy
    #         print("Couldn't import Image or numpy:", str(err))


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
