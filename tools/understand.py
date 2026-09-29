"""Small causal checks, separate from the runtime benchmark; standard library only."""
import csv,inspect,io,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'tests'))
from sort import SORTS
from test_sort import Tagged,stable,SortTests

def inversions(a):
    return sum(x>y for i,x in enumerate(a) for y in a[i+1:])
def prefix_minima(a):
    if not a:return 0
    smallest=a[0];count=0
    for x in a[1:]:
        if x<smallest:smallest=x;count+=1
    return count

def run():
    n=1000
    cases={'sorted':list(range(n)),'swap_first':list(range(n)),
           'swap_middle':list(range(n)),'swap_ends':list(range(n)),
           'all_equal':[7]*n,'reverse':list(range(n-1,-1,-1))}
    cases['swap_first'][0],cases['swap_first'][1]=cases['swap_first'][1],cases['swap_first'][0]
    cases['swap_middle'][499],cases['swap_middle'][500]=cases['swap_middle'][500],cases['swap_middle'][499]
    cases['swap_ends'][0],cases['swap_ends'][-1]=cases['swap_ends'][-1],cases['swap_ends'][0]
    rows=[]
    for name,original in cases.items():
        inv=inversions(original);mins=prefix_minima(original)
        counts={}
        for algorithm,sorter in SORTS.items():
            a=original.copy();counts[algorithm]=sorter(a);assert a==sorted(original)
        predicted=inv+(n-1)-mins
        assert counts['insertion']==predicted
        rows.append(dict(case=name,n=n,inversions=inv,prefix_minima=mins,
                         predicted_insertion=predicted,**counts))
    with (ROOT/'results/understanding.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator="\n");w.writeheader();w.writerows(rows)
    mutations=[]
    for name in ('insertion','merge'):
        original_sort=SORTS[name]
        source=inspect.getsource(original_sort)
        # Change only the tie condition; key order stays correct, stability fails.
        if name=='insertion':source=source.replace('a[j] <= key','a[j] < key')
        else:source=source.replace('a[i] <= a[j]','a[i] < a[j]')
        namespace={};exec(source,namespace)
        mutated=namespace[original_sort.__name__]
        a=[Tagged(key,i) for i,key in enumerate([2,1,2,1])]
        mutated(a)
        keys_correct=[x.key for x in a]==[1,1,2,2]
        tag_order_stable=stable(a)
        SORTS[name]=mutated
        stream=io.StringIO()
        result=unittest.TextTestRunner(stream=stream).run(unittest.TestSuite([SortTests('test_stability')]))
        SORTS[name]=original_sort
        assert keys_correct and not tag_order_stable and not result.wasSuccessful()
        mutations.append(dict(algorithm=name,change='<= to <',keys_correct=keys_correct,
                              stable=tag_order_stable,stability_test_detected=not result.wasSuccessful(),
                              key_tag_output=[[x.key,x.tag] for x in a]))
    (ROOT/'results/mutation.json').write_text(json.dumps(mutations,indent=2)+'\n')
    print('Verified inversion formula for 6 inputs and detected both tie-condition mutations')
if __name__=='__main__':run()
