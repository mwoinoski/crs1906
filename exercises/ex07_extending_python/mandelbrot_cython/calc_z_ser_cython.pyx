"""
Calculates Mandelbrot series.

Parameters:
    q: array of complex numbers
    maxiter: maximum number of iterations
Returns: array of doubles
"""

# TODO: paste the calculate_z_serial() function from mandelbrot.py here.



# TODO: now complete the remaining steps in mandelbrot_cython.py

# You can gain a little speed by adding type defintions to parameters and
# local variables, as in this example:
# import array
# def calculate_z_serial(list q, int maxiter):
#     cdef int i
#     cdef int iteration
#     z = [complex(0, 0)] * len(q)
#     output = array.array('i', [0] * len(q))
#     for i in range(len(q)):
#         for iteration in range(maxiter):
#             z[i] = z[i]*z[i] + q[i]
#             if abs(z[i]) > 2.0:
#                 output[i] = iteration
#                 break
#     return output
