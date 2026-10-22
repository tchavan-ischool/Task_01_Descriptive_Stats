"""Task 1: equivalent descriptive statistics using pandas."""
import argparse
import json
from pathlib import Path
import pandas as pd

MISSING = {'', 'na', 'n/a', 'null', 'none', 'nan'}

def analyze(path):
    df=pd.read_csv(path,dtype='string',keep_default_na=False,encoding='utf-8-sig',encoding_errors='replace')
    result={'dataset':Path(path).name,'rows':len(df),'columns':len(df.columns),'column_stats':{}}
    for col in df.columns:
        series=df[col].str.strip()
        series=series.mask(series.str.lower().isin(MISSING))
        valid=series.dropna()
        missing=int(series.isna().sum())
        if valid.empty:
            stats={'type':'empty','count':0,'missing':missing}
        else:
            parsed=pd.to_numeric(valid.str.replace(',','',regex=False),errors='coerce')
            if parsed.notna().all():
                nums=parsed.astype('float64')
                stats={'type':'numeric','count':len(nums),'missing':missing,
                       'mean':float(nums.mean()),'min':float(nums.min()),'max':float(nums.max()),
                       'std_sample':float(nums.std(ddof=1)) if len(nums)>1 else None,
                       'median':float(nums.median())}
            else:
                counts=valid.value_counts(dropna=True)
                ordered=sorted(((str(k),int(v)) for k,v in counts.items()),key=lambda kv:(-kv[1],kv[0]))
                top=ordered[:5]
                stats={'type':'categorical','count':len(valid),'missing':missing,'unique':int(valid.nunique()),
                       'mode':top[0][0],'mode_frequency':top[0][1],
                       'top_5':[{'value':v,'frequency':n} for v,n in top]}
        result['column_stats'][col]=stats
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv_file');p.add_argument('--output',default=None)
    a=p.parse_args();result=analyze(a.csv_file)
    report=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)
    if a.output:Path(a.output).write_text(report,encoding='utf-8');print('Saved',a.output)
    else:print(report)
