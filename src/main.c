#include "sort.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <time.h>
static int compareKey(const void *x,const void *y) {
    int a=((const Record*)x)->key,b=((const Record*)y)->key;
    return (a>b)-(a<b);
}
static int compareDouble(const void *x,const void *y) {
    double a=*(const double*)x,b=*(const double*)y;
    return (a>b)-(a<b);
}
int main(void) {
    const size_t sizes[]={100,1000,2000,4000};
    const char *cases[]={"sorted","reverse","random","duplicates"};
    FILE *csv=fopen("results/benchmark_c.csv","w");
    if(!csv) return EXIT_FAILURE;
    fputs("n,case,algorithm,comparisons,median_ms\n",csv);
    for(size_t s=0;s<4;++s)for(size_t shape=0;shape<4;++shape) {
        size_t n=sizes[s];char path[128];
        snprintf(path,sizeof(path),"results/inputs/%zu_%s.txt",n,cases[shape]);
        FILE *input=fopen(path,"r");
        if(!input) {fprintf(stderr,"Run make run-py first: %s\n",path);return EXIT_FAILURE;}
        Record *original=malloc(n*sizeof(*original)), *a=malloc(n*sizeof(*a)), *expected=malloc(n*sizeof(*expected));
        if(!original||!a||!expected) return EXIT_FAILURE;
        for(size_t i=0;i<n;++i) {
            if(fscanf(input,"%d",&original[i].key)!=1) return EXIT_FAILURE;
            original[i].tag=(int)i;
        }
        fclose(input);memcpy(expected,original,n*sizeof(*a));qsort(expected,n,sizeof(*a),compareKey);
        for(size_t k=0;k<3;++k) {
            double ms[5];uint64_t count=0;
            for(size_t rep=0;rep<5;++rep) {
                memcpy(a,original,n*sizeof(*a));clock_t start=clock();
                uint64_t current=SORT_ALGORITHMS[k].sort(a,n);
                ms[rep]=1000.0*(double)(clock()-start)/CLOCKS_PER_SEC;
                if(rep&&current!=count) return EXIT_FAILURE;
                count=current;
                for(size_t i=0;i<n;++i) if(a[i].key!=expected[i].key) return EXIT_FAILURE;
            }
            qsort(ms,5,sizeof(*ms),compareDouble);
            fprintf(csv,"%zu,%s,%s,%" PRIu64 ",%.4f\n",n,cases[shape],SORT_ALGORITHMS[k].name,count,ms[2]);
            printf("C %zu %-10s %-9s compares=%" PRIu64 " median_ms=%.4f\n",n,cases[shape],SORT_ALGORITHMS[k].name,count,ms[2]);
        }
        free(original);free(a);free(expected);
    }
    fclose(csv);return EXIT_SUCCESS;
}
