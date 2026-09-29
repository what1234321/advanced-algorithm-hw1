#include "sort.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int checks=0, failures=0;
static int compareKey(const void *x,const void *y) {
    int a=((const Record*)x)->key,b=((const Record*)y)->key;
    return (a>b)-(a<b);
}
static int stable(const Record a[],size_t n) {
    for (size_t i=1;i<n;++i) if(a[i-1].key==a[i].key&&a[i-1].tag>a[i].tag) return 0;
    return 1;
}
static void checkInput(const int keys[],size_t n) {
    Record a[501],expected[501];
    for (size_t k=0;k<3;++k) {
        for(size_t i=0;i<n;++i) a[i]=(Record){keys[i],(int)i};
        memcpy(expected,a,n*sizeof(*a));qsort(expected,n,sizeof(*a),compareKey);
        SORT_ALGORITHMS[k].sort(a,n);++checks;
        int seen[501]={0};
        for(size_t i=0;i<n;++i) {
            if(a[i].tag<0 || (size_t)a[i].tag>=n ||
               seen[a[i].tag] || keys[a[i].tag]!=a[i].key) {++failures;break;}
            seen[a[i].tag]=1;
        }
        for(size_t i=0;i<n;++i) if(a[i].key!=expected[i].key) {++failures;break;}
        if (SORT_ALGORITHMS[k].stable&&!stable(a,n)) ++failures;
    }
}
int main(void) {
    int keys[501]={0};
    for(size_t n=0;n<=200;++n) {
        for(size_t i=0;i<n;++i) keys[i]=(int)((i*37+n*11)%13)-6;
        checkInput(keys,n);
    }
    for(size_t i=0;i<500;++i) keys[i]=(int)((i*137+31)%503)-250;
    checkInput(keys,500);
    for(int type=0;type<3;++type) {
        for(size_t i=0;i<50;++i) keys[i]=type==0?(int)i:type==1?49-(int)i:7;
        checkInput(keys,50);
    }
    Record ties[4]={{1,0},{1,1},{1,2},{1,3}};
    heapSort(ties,4);++checks;
    if(stable(ties,4)) ++failures; /* concrete witness of heap instability */
    printf("%d checks, %d failures\n",checks,failures);
    return failures?EXIT_FAILURE:EXIT_SUCCESS;
}
