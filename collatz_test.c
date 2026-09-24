#include <stdio.h>
#include <stdint.h>

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
    uint32_t max_steps = 0;

    for (uint64_t i = 1; i <= N; i++) {
        uint32_t steps = collatz_steps(i);

        if (steps > max_steps)
            max_steps = steps;
    }

    printf("N = %llu\n", (unsigned long long)N);
    printf("Maximum stopping time = %u\n", max_steps);

    return 0;
}