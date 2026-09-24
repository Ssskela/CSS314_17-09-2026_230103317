#include <stdio.h>
#include <stdint.h>
#include <omp.h>

static inline uint32_t collatz_steps(uint64_t n) {
    uint32_t steps = 0;

    while (n > 1) {
        if ((n & 1) == 0)
            n >>= 1;
        else
            n = 3 * n + 1;

        steps++;
    }

    return steps;
}

int main(void) {
    const uint64_t N = 13317000;
    const uint64_t MOD = 1000000007ULL;

    uint32_t max_steps = 0;
    uint64_t checksum = 0;

    double start = omp_get_wtime();

    for (uint64_t i = 1; i <= N; i++) {
        uint32_t steps = collatz_steps(i);

        if (steps > max_steps)
            max_steps = steps;

        checksum = (checksum + steps) % MOD;
    }

    double end = omp_get_wtime();

    printf("N = %llu\n", (unsigned long long)N);
    printf("Maximum stopping time = %u\n", max_steps);
    printf("Checksum = %llu\n", (unsigned long long)checksum);
    printf("Time = %.6f seconds\n", end - start);

    return 0;
}