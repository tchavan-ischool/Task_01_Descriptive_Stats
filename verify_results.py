"""Compare independent JSON outputs, allowing floating point rounding differences."""
import argparse,json,math
from pathlib import Path

def compare(a,b,path='root'):
    errors=[]
    if isinstance(a,dict) and isinstance(b,dict):
        if a.keys()!=b.keys():errors.append(f'{path}: keys differ')
        for k in a.keys() & b.keys():errors+=compare(a[k],b[k],f'{path}.{k}')
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b):errors.append(f'{path}: lengths differ')
        for i,(x,y) in enumerate(zip(a,b)):errors+=compare(x,y,f'{path}[{i}]')
    elif isinstance(a,(int,float)) and isinstance(b,(int,float)) and not isinstance(a,bool) and not isinstance(b,bool):
        if not math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-8):errors.append(f'{path}: {a} != {b}')
    elif a!=b:errors.append(f'{path}: {a!r} != {b!r}')
    return errors

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('pure_json');p.add_argument('pandas_json');a=p.parse_args()
    x=json.loads(Path(a.pure_json).read_text());y=json.loads(Path(a.pandas_json).read_text())
    errors=compare(x,y)
    if errors:
        print('\n'.join(errors[:50]));raise SystemExit(f'FAILED: {len(errors)} differences')
    print('PASS: all columns and statistics agree (within floating point tolerance)')
