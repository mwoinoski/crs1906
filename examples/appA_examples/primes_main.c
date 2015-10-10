#include <stdio.h>
#include "primes_c.h"

#define LIMIT 10000

/*
 * Driver for primes_c()
 */
int main(int argc, char **argv) {
    int primes[LIMIT];
    printf("Calling primes_c()...");
    primes_c(LIMIT, primes);
    printf("End of buffer: ...");
    int i;
    for (i = LIMIT-10; i < LIMIT-1; i++) {
        printf("%d ", primes[i]);
    }
    printf("\n");
    return 0;
}
