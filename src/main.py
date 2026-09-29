"""Common benchmark and identical input files for Python/C."""
import csv, random, statistics, sys, time
from pathlib import Path
from sort import SORTS
ROOT=Path(__file__).resolve().parents[1]
SIZES=(100,1000,2000,4000)
CASES=('sorted','reverse','random','duplicates')
REPEATS=5
SEED=20260930

def make_data(n,case):
    if case=='sorted':return list(range(n))
    if case=='reverse':return list(range(n,0,-1))
    rng=random.Random(SEED+n)
    if case=='duplicates':return [rng.randrange(10) for _ in range(n)]
    data=list(range(n));rng.shuffle(data);return data

def run():
    (ROOT/'results'/'inputs').mkdir(parents=True,exist_ok=True)
    rows=[]
    for n in SIZES:
        for case in CASES:
            original=make_data(n,case);expected=sorted(original)
            (ROOT/'results'/'inputs'/f'{n}_{case}.txt').write_text(' '.join(map(str,original))+'\n')
            for name,sorter in SORTS.items():
                times=[];counts=[]
                for _ in range(REPEATS):
                    data=original.copy()
                    start=time.perf_counter_ns();comparisons=sorter(data)
                    elapsed=time.perf_counter_ns()-start
                    assert data==expected,(name,n,case)
                    times.append(elapsed/1e6);counts.append(comparisons)
                assert len(set(counts))==1
                row=dict(n=n,case=case,algorithm=name,comparisons=counts[0],median_ms=round(statistics.median(times),4))
                rows.append(row);print(row)
    with (ROOT/'results'/'benchmark.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    print('Python:',sys.version.split()[0])
if __name__=='__main__':run()
