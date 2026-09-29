"""Generate a reproducible SVG chart using only the Python standard library."""
import csv,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((ROOT/'results/benchmark.csv').open()))
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="640" height="320" viewBox="0 0 640 320">',
'<rect width="640" height="320" fill="white"/>',
'<text x="65" y="25" font-family="sans-serif" font-size="15">Random input: key comparisons (log10 scale)</text>']
for power in range(2,8):
 y=270-(power-2)/5*220
 parts.extend([f'<line x1="65" y1="{y}" x2="605" y2="{y}" stroke="#dfe5ed"/>',f'<text x="15" y="{y+4}" font-size="12" font-family="sans-serif">10^{power}</text>'])
for n in (100,1000,2000,4000):
 x=65+math.log10(n/100)/math.log10(40)*540
 parts.append(f'<text x="{x-12}" y="292" font-size="12" font-family="sans-serif">{n}</text>')
for name,color in [('insertion','#c76545'),('merge','#356c9b'),('heap','#39836a')]:
 series=[r for r in rows if r['case']=='random' and r['algorithm']==name]
 coords=[(65+math.log10(int(r['n'])/100)/math.log10(40)*540,270-(math.log10(int(r['comparisons']))-2)/5*220) for r in series]
 parts.append(f'<polyline points="'+ ' '.join(f'{x},{y}' for x,y in coords)+f'" fill="none" stroke="{color}" stroke-width="2"/>')
 for x,y in coords:parts.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{color}"/>')
 idx=['insertion','merge','heap'].index(name)
 parts.append(f'<text x="{180+idx*130}" y="315" font-size="12" font-family="sans-serif" fill="{color}">{name}</text>')
parts.append('</svg>');(ROOT/'report/growth.svg').write_text('\n'.join(parts))
