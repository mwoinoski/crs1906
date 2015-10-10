#ifndef CALC_Z_SER_H
#define CALC_Z_SER_H

#ifdef __cplusplus
extern "C" { /* Required in order for compiler to handle name mangling correctly */
#endif

/*
 * BUILDING_CALC_Z_SER_DLL is set with a compiler option when building the DLL.
 * If we're building the DLL, we need to export function declarations.
 * If we're building client code, we need to import the function declarations.
 */
#ifdef BUILDING_CALC_Z_SER_DLL
#define CALC_Z_SER_DLL __declspec(dllexport)
#else
#define CALC_Z_SER_DLL __declspec(dllimport)
#endif

/*
 * TODO: note the declaration of the complex_num struct.
 * (no code change required)
 */
struct complex_num {
    double real;
    double imag;
};

/*
 * TODO: note the declaration of the calc_z_ser() function.
 * Parameters:
 *     q : array of complex_num struct
 *     output : array of complex_num struct for result
 *     len_q : length of q array
 *     maxiter : maximum number of loop iterations
 * Returns:
 *     1 if no errors, 0 otherwise
 * (no code change required).
*/
int CALC_Z_SER_DLL calc_z_ser(struct complex_num *q, int *output,
                               int len_q, int maxiter);

#ifdef __cplusplus
}
#endif


#endif
