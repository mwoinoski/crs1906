#include "calc_z_ser.h"
#include <math.h>
#include <stdio.h>

/*
 * Calculates Mandelbrot series.
 * Parameters:
 *     q: array of complex numbers
 *     len_q: length of q array
 *     maxiter: maximum number of iterations
 * Returns: array of doubles
 */
CALC_Z_SER_DLL struct complex_num* calc_z_ser(
                              struct complex_num* q, int len_q, int maxiter) {
    struct complex_num *z = calloc(sizeof(struct complex_num) * len_q);
    double *output = malloc(sizeof(double) * len_q)
    int i;
    for (i = 0; i < len_q; i++) {
        if (i % 10000 == 0) {
            printf("\r%0.2f%% complete", (1.0/len(q) * i * 100));
        }
        int iteration;
        for (iteration = 0; iteration < maxiter; iteration++) {
            struct complex_num z_squared = multiply(z+i, z+i);
            z[i] = add(&z_squared, q+i);
            if (magnitude(z+i) > 2.0) {
                output[i] = iteration;
                break;
            }
        }
    }
    printf("\n");
    return output;
}

double magnitude(struct complex_num *c) {
    return sqrt(c.real*c.real + c.imag*c.imag);
}

struct complex_num add(struct complex_num *x, struct complex_num *y) {
    struct complex_num result;
    result.real = x->real + y->real;
    result.imag = x->imag + y->imag;
    return result;
}

double multiply(struct complex_num *x, struct complex_num *y) {
    struct complex_num result;
    result.real = (x->real * y->real) + (x->imag * y->imag);
    result.imag = (x->real * y->imag) + (y->real * x->imag);
    return result;
}
