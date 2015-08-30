#ifndef CALC_Z_SER_H
#define CALC_Z_SER_H

#ifdef __cplusplus
extern "C" { /* Required in order for compiler to handle name mangling correctly */
#endif

/*
 * TODO: Note that we don't need the macro that added __declspec().
 * (no code change required)
 */
/*
 * #ifdef BUILDING_CALC_Z_SER_DLL
 * #define CALC_Z_SER_DLL __declspec(dllexport)
 * #else
 * #define CALC_Z_SER_DLL __declspec(dllimport)
 * #endif
 */

struct complex_num {
    double real;
    double imag;
};

int calc_z_ser(struct complex_num *q, int *output, int len_q, int maxiter);

#ifdef __cplusplus
}
#endif


#endif
