"""Check comparison-count agreement between the two implementations."""
import csv
from pathlib import Path
root=Path(__file__).resolve().parents[1]
key=lambda r:(r['n'],r['case'],r['algorithm'])
with (root/'results/benchmark.csv').open() as f:py={key(r):int(r['comparisons']) for r in csv.DictReader(f)}
with (root/'results/benchmark_c.csv').open() as f:c={key(r):int(r['comparisons']) for r in csv.DictReader(f)}
if len(py)!=48 or py!=c:raise SystemExit('FAIL: C/Python comparison counts differ')
print('PASS: C/Python comparison counts match for all 48 conditions')
