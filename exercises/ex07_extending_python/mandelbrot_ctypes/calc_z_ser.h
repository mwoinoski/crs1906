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

struct complex_num {
    double j;
    double i;
}

struct complex_num* CALC_Z_SER_DLL
                    calc_z_ser(struct complex_num* q, int len_q, int maxiter);

#ifdef __cplusplus
}
#endif


#endif
