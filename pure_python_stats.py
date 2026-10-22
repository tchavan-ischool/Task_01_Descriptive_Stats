"""Task 1: descriptive statistics using only the Python standard library."""
import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

MISSING = {'', 'na', 'n/a', 'null', 'none', 'nan'}

def clean(value):
    if value is None: return None
    s = str(value).strip()
    return None if s.lower() in MISSING else s

def numeric_value(s):
    try:
        v = float(s.replace(',', ''))
        return v if math.isfinite(v) else None
    except (ValueError, AttributeError):
        return None

def describe(values):
    valid = [v for v in values if v is not None]
    if not valid:
        return {'type': 'empty', 'count': 0, 'missing': len(values)}
    nums = [numeric_value(v) for v in valid]
    if all(v is not None for v in nums):
        n = len(nums)
        mean = math.fsum(nums) / n
        ordered = sorted(nums)
        median = ordered[n//2] if n % 2 else (ordered[n//2-1] + ordered[n//2]) / 2
        std = math.sqrt(math.fsum((x-mean)**2 for x in nums)/(n-1)) if n>1 else None
        return {'type':'numeric','count':n,'missing':len(values)-n,'mean':mean,'min':ordered[0],
                'max':ordered[-1],'std_sample':std,'median':median}
    freq = Counter(valid)
    top = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:5]
    return {'type':'categorical','count':len(valid),'missing':len(values)-len(valid),
            'unique':len(freq),'mode':top[0][0],'mode_frequency':top[0][1],
            'top_5':[{'value':v,'frequency':n} for v,n in top]}

def analyze(path):
    with open(path, newline='', encoding='utf-8-sig', errors='replace') as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames: raise ValueError('CSV has no header')
        fields=reader.fieldnames
        cols={k:[] for k in fields}
        n=0
        for row in reader:
            n+=1
            for k in fields: cols[k].append(clean(row.get(k)))
    return {'dataset':Path(path).name,'rows':n,'columns':len(fields),
            'column_stats':{k:describe(cols[k]) for k in fields}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv_file');p.add_argument('--output',default=None)
    a=p.parse_args();result=analyze(a.csv_file)
    report=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)
    if a.output: Path(a.output).write_text(report,encoding='utf-8');print('Saved',a.output)
    else: print(report)
