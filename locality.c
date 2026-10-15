#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#define N 2048
#define RUNS 3

static uint32_t array[N][N];

double get_time_ms(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1000.0 + t.tv_nsec / 1000000.0;
}

int main(void) {
    uint64_t checksum = 0;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            array[i][j] = (uint32_t)((i + j) % 100);
        }
    }

    printf("Array size: %d x %d (%.2f MiB)\n",
           N, N, sizeof(array) / (1024.0 * 1024.0));

    for (int run = 1; run <= RUNS; run++) {
        double start = get_time_ms();

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                checksum += array[i][j];
            }
        }

        double end = get_time_ms();
        printf("Row-major run %d: %.3f ms\n", run, end - start);
    }

    for (int run = 1; run <= RUNS; run++) {
        double start = get_time_ms();

        for (int j = 0; j < N; j++) {
            for (int i = 0; i < N; i++) {
                checksum += array[i][j];
            }
        }

        double end = get_time_ms();
        printf("Column-major run %d: %.3f ms\n", run, end - start);
    }

    printf("Checksum: %llu\n", (unsigned long long)checksum);
    return 0;
}
