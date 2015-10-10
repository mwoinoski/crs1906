#include "primes.h"
#include <math.h>

/*
 * Calculates the first how_many prime numbers.
 * Parameters:
 *     how_many: the number of primes to calculate
 *     p: pointer to a buffer large enough to hold how_many ints
 * Returns: how_many
 */
int primes_c(int how_many, int *p) {
    int n, k, i;
    k = 0;
    n = 2;
    while (k < how_many) {
        i = 0;
        while (i < k && n % p[i] != 0) {
            i = i + 1;
        }
        if (i == k) {
            p[k] = n;
            k = k + 1;
        }
        n = n + 1;
    }
    return how_many;
}

/*
 * Returns 1 is parameter is a prime number, 0 otherwise.
 */
int is_prime(int n) {
    int i;
    int has_factor = 0;
    int limit = (int) sqrt(n);
    for (i = 2; i <= limit && !has_factor; i++) {
        if (n % i == 0) {
            has_factor = 1;
        }
    }
    return !has_factor;
}
