from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.stats import ttest_rel

def find_resonant_stimulus(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each subject, find the sound_id with the smallest during reactance_X.
    Returns a dataframe with subject_id, resonant_sound_id, min_X_during.
    """
    during = df[(df["kind"] == "sound") & (df["timepoint"] == "during")]
    idx = during.groupby("subject_id")["reactance_X"].idxmin()
    best = during.loc[idx, ["subject_id", "sound_id", "reactance_X"]].rename(
        columns={"sound_id": "resonant_sound_id", "reactance_X": "min_X_during"}
    )
    return best.sort_values("subject_id").reset_index(drop=True)

def effect_size_cohens_d(baseline: np.ndarray, during: np.ndarray) -> float:
    """
    Paired Cohen d between baseline and during.
    """
    diff = baseline - during
    return diff.mean() / (diff.std(ddof=1) + 1e-12)

def paired_t_test(baseline: np.ndarray, during: np.ndarray) -> dict:
    """
    Paired t test with scipy, alternative baseline greater than during.
    """
    t, p = ttest_rel(baseline, during, alternative="greater")
    return {"t": float(t), "p": float(p)}

def permutation_test_resonance(baseline: np.ndarray, during: np.ndarray, n_perm: int = 5000, seed: int = 42) -> dict:
    """
    Non parametric permutation test for median of baseline minus during greater than zero.
    """
    rng = np.random.default_rng(seed)
    obs = np.median(baseline - during)
    count = 0
    concat = np.vstack([baseline, during])
    for _ in range(n_perm):
        mask = rng.integers(0, 2, size=baseline.shape[0]).astype(bool)
        a = np.where(mask, concat[0], concat[1])
        b = np.where(mask, concat[1], concat[0])
        stat = np.median(a - b)
        if stat >= obs:
            count += 1
    pval = (count + 1) / (n_perm + 1)
    return {"stat": float(obs), "p": float(pval)}
