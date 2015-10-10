#ifndef PRIMES_H
#define PRIMES_H

#ifdef __cplusplus
extern "C" { /* Required in order for compiler to handle name mangling correctly */
#endif

/*
 * To build the extension module, do not add __declspec(dllexport) or
 * __declspec(dllimport) to the function declarations.
 */
int primes_c(int how_many, int *p);
int is_prime(int n);

#ifdef __cplusplus
}
#endif


#endif
