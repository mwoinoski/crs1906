#ifndef PRIMES_H
#define PRIMES_H

#ifdef __cplusplus
extern "C" { /* Required in order for compiler to handle name mangling correctly */
#endif

/*
 * If we're building the DLL, we need to export function declarations.
 * If we're building client code, we need to import the function declarations.
 */
#ifdef BUILDING_PRIMES_DLL
#define PRIMES_DLL __declspec(dllexport)
#else
#define PRIMES_DLL __declspec(dllimport)
#endif

int PRIMES_DLL primes_c(int how_many, int *p);
int PRIMES_DLL is_prime(int n);

#ifdef __cplusplus
}
#endif


#endif
