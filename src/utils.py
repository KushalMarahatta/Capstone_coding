import numpy as np
import pandas as pd
from scipy.stats import binomtest

#failure flag parser
def make_fail_flag(series: pd.Series) -> pd.Series:
    #Convert Failure@5_primary to 0/1 int. Unknown -> 0.
    if pd.api.types.is_bool_dtype(series):
        return series.astype(int)
    if pd.api.types.is_numeric_dtype(series):
        return series.fillna(0).astype(float).round().astype(int).clip(0, 1)
    _T={'true', '1', 'yes', '1.0'}
    _F={'false', '0', 'no', '0.0', ''}
    def _p(v):
        if pd.isna(v): return 0
        if isinstance(v, bool): return int(v)
        if isinstance(v, (int, float)):
            return 0 if np.isnan(float(v)) else int(round(float(v)))
        if isinstance(v, str):
            vl=v.strip().lower()
            if vl in _T: return 1
            if vl in _F: return 0
        return 0
    return series.map(_p).astype(int)

#SELF-TEST
_test=pd.Series([True, False, 'True', 'false', '1', '0', 1.0, 0.0, pd.NA, None])
_expected=[1, 0, 1, 0, 1, 0, 1, 0, 0, 0]
assert list(make_fail_flag(_test))==_expected, 'make_fail_flag FAILED'
del _test, _expected
print('make_fail_flag')


def bh_fdr(pvals: list, alpha: float = 0.05) -> np.ndarray:
    #Benjamini-Hochberg FDR correction.
    pvals=np.asarray(pvals, dtype=float)
    n=len(pvals)
    if n==0:
        return np.array([])
    order=np.argsort(pvals)
    ranks=np.arange(1, n + 1)
    adj=np.minimum(pvals[order]*n / ranks, 1.0)
    adj=np.minimum.accumulate(adj[::-1])[::-1]
    q=np.empty(n)
    q[order]=adj
    return q

print('bh_fdr')


def safe_k(k: int, n_docs: int) -> int:
    #Return min(k, n_docs), guard k <= 0.
    if k <= 0:
        return 0
    return min(k, n_docs)

print('safe_k')


def check_sample_size(group_name: str, count: int, min_size: int = 10, warnings_issued: list = None):
    #Warning if count < min_size.
    if warnings_issued is None:
        warnings_issued=[]
    if count < min_size:
        msg=f'{group_name} has {count} samples (< {min_size}) → unstable'
        print(f'{msg}')
        warnings_issued.append(msg)

print('check_sample_size')


def compute_failure_at_k(pred_df: pd.DataFrame, k: int, relevance_threshold: int = 1) -> dict:
    #Computing failure@k per query. Returns {qid: {'failure': 0/1/nan, 'evaluable': bool}}.
    results={}
    for qid in pred_df['qid'].unique():
        q_docs=pred_df[pred_df['qid']==qid].copy()
        relevant=q_docs[q_docs['label'] >= relevance_threshold]
        if len(relevant)==0:
            results[qid]={'failure': np.nan, 'evaluable': False}
            continue
        q_docs=q_docs.sort_values('score', ascending=False)
        k_actual=safe_k(k, len(q_docs))
        if k_actual<=0:
            results[qid]={'failure': np.nan, 'evaluable': False}
            continue
        top_k=q_docs.iloc[:k_actual]
        has_relevant=(top_k['label'] >= relevance_threshold).any()
        results[qid]={'failure': 0 if has_relevant else 1, 'evaluable': True}
    return results

print('compute_failure_at_k')


def mcnemar_test(base_vals: np.ndarray, conf_vals: np.ndarray) -> dict:
    """
    McNemar test for paired binary data.
    Returns {'pval', 'n01', 'n10', 'note', 'method'}.
    """
    # Discordant counts
    n01=int(((base_vals==0) & (conf_vals==1)).sum())  # baseline success, config failure
    n10=int(((base_vals==1) & (conf_vals==0)).sum())  # baseline failure, config success
    
    if n01 + n10==0:
        return {'pval': 1.0, 'n01': n01, 'n10': n10, 'note': 'no discordant pairs', 'method': 'none'}
    
    #statsmodels
    try:
        from statsmodels.stats.contingency_tables import mcnemar as statsmodels_mcnemar
        n00=int(((base_vals==0) & (conf_vals==0)).sum())
        n11=int(((base_vals==1) & (conf_vals==1)).sum())
        table=np.array([[n00, n01], [n10, n11]])
        result=statsmodels_mcnemar(table, exact=True)
        return {'pval': float(result.pvalue), 'n01': n01, 'n10': n10, 'note': '', 'method': 'statsmodels_exact'}
    except ImportError:
        pass
    
    #Manual exact via Binomial
    n=n01 + n10
    k=min(n01, n10)
    pval=binomtest(k, n, p=0.5, alternative="two-sided").pvalue
    return {'pval': float(pval), 'n01': n01, 'n10': n10, 'note': '', 'method': 'manual_exact'}

print('mcnemar_test')
print('\nAll utilities defined')