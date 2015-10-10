#include "calc_z_ser.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>

/*
 * calc_z_ser: calculates Mandelbrot series.
 * Parameters:
 *     q : array of complex_num struct
 *     output : array of complex_num struct for result
 *     len_q : length of q array
 *     maxiter : maximum number of loop iterations
 * Returns:
 *     1 if no errors, 0 otherwise
 */
 /*
  * TODO: Note that we don't need the macro that included __declspec().
  * (no code change required)
  */
int calc_z_ser(struct complex_num* q, int *output, int len_q, int maxiter) {
    struct complex_num z[len_q];
    int i, iteration;
    struct complex_num z_squared;
    double magnitude;
    for (i = 0; i < len_q; i++) {
        z[i].real = z[i].imag = 0.0;
        for (iteration = 0; iteration < maxiter; iteration++) {
            /* calculate z[i]**2 */
            z_squared.real = (z[i].real * z[i].real) - (z[i].imag * z[i].imag);
            z_squared.imag = 2 * (z[i].real * z[i].imag);

            /* calculate z[i]**2 + q[i] */
            z[i].real = z_squared.real + q[i].real;
            z[i].imag = z_squared.imag + q[i].imag;

            /* calculate abs(z[i]**2 + q[i]) */
            magnitude = sqrt(z[i].real*z[i].real + z[i].imag*z[i].imag);

            if (magnitude > 2.0) {
                output[i] = iteration;
                break;
            }
        }
    }
    return 1;
}
