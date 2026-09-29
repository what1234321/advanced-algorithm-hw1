#ifndef SORT_H
#define SORT_H
#include <stddef.h>
#include <stdint.h>
typedef struct { int key; int tag; } Record;
typedef uint64_t (*SortFunction)(Record a[], size_t n);
uint64_t insertionSort(Record a[], size_t n);
uint64_t mergeSort(Record a[], size_t n);
uint64_t heapSort(Record a[], size_t n);
typedef struct { const char *name; SortFunction sort; int stable; } SortAlgorithm;
extern const SortAlgorithm SORT_ALGORITHMS[3];
#endif
