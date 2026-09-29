#include "sort.h"
#include <stdio.h>
#include <stdlib.h>

uint64_t insertionSort(Record a[], size_t n) {
    uint64_t comparisons = 0;
    for (size_t i = 1; i < n; ++i) {
        Record key = a[i];
        size_t j = i;
        while (j > 0) {
            ++comparisons;
            if (a[j-1].key <= key.key) break;
            a[j] = a[j-1];
            --j;
        }
        a[j] = key;
    }
    return comparisons;
}

static uint64_t mergeRange(Record a[], Record temp[], size_t lo, size_t hi) {
    if (hi-lo <= 1) return 0;
    size_t mid = lo + (hi-lo)/2;
    uint64_t comparisons = mergeRange(a,temp,lo,mid) + mergeRange(a,temp,mid,hi);
    size_t i=lo, j=mid;
    for (size_t k=lo;k<hi;++k) {
        if (i==mid) temp[k]=a[j++];
        else if (j==hi) temp[k]=a[i++];
        else {
            ++comparisons;
            if (a[i].key <= a[j].key) temp[k]=a[i++];
            else temp[k]=a[j++];
        }
    }
    for (size_t k=lo;k<hi;++k) a[k]=temp[k];
    return comparisons;
}

uint64_t mergeSort(Record a[], size_t n) {
    if (n<2) return 0;
    Record *temp=malloc(n*sizeof(*temp));
    if (!temp) { fputs("mergeSort: allocation failed\n",stderr); exit(EXIT_FAILURE); }
    uint64_t comparisons=mergeRange(a,temp,0,n);
    free(temp);
    return comparisons;
}

static uint64_t siftDown(Record a[], size_t root, size_t size) {
    uint64_t comparisons=0;
    while (root<size/2) {
        size_t child=2*root+1;
        if (child+1<size) {
            ++comparisons;
            if (a[child].key<a[child+1].key) ++child;
        }
        ++comparisons;
        if (a[root].key>=a[child].key) break;
        Record temp=a[root];a[root]=a[child];a[child]=temp;
        root=child;
    }
    return comparisons;
}

uint64_t heapSort(Record a[], size_t n) {
    uint64_t comparisons=0;
    for (size_t root=n/2;root>0;--root) comparisons+=siftDown(a,root-1,n);
    for (size_t size=n;size>1;--size) {
        Record temp=a[0];a[0]=a[size-1];a[size-1]=temp;
        comparisons+=siftDown(a,0,size-1);
    }
    return comparisons;
}
const SortAlgorithm SORT_ALGORITHMS[3]={
    {"insertion",insertionSort,1},{"merge",mergeSort,1},{"heap",heapSort,0}
};
