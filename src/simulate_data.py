from __future__ import annotations
import numpy as np
import pandas as pd

def generate_dataset(
    n_subjects: int = 20,
    n_sounds: int = 14,
    include_controls: bool = True,
    seed: int = 42
) -> pd.DataFrame:
    """
    Synthetic dataset mimicking per-subject sonic stimuli exposures with
    a single resonant sound that tends to minimize reactance X.
    Columns:
      subject_id, sound_id, kind, frequency_hz, amplitude_db, duration_s,
      phase, impedance_Z, reactance_X, timepoint (baseline/during/post)
    """
    rng = np.random.default_rng(seed)
    subjects = np.arange(1, n_subjects + 1)

    base_freqs = np.linspace(100, 4000, n_sounds).astype(int)
    base_amp_db = 70
    duration_s = 3.0

    rows = []

    for s in subjects:
        resonant = rng.integers(1, n_sounds + 1)
        baseline_X = rng.normal(loc=6.0, scale=1.0)
        baseline_Z = rng.normal(loc=50.0, scale=3.0)

        rows.append(dict(
            subject_id=s, sound_id=0, kind="baseline", frequency_hz=0,
            amplitude_db=0, duration_s=0.0, phase="baseline",
            impedance_Z=baseline_Z, reactance_X=baseline_X, timepoint="baseline"
        ))

        for sound_id in range(1, n_sounds + 1):
            f = int(base_freqs[sound_id - 1])
            resonance_drop = rng.normal(4.5, 0.6) if sound_id == resonant else rng.normal(0.6, 0.3)
            noise = rng.normal(0.0, 0.4)
            X_during = max(0.0, baseline_X - resonance_drop + noise)
            Z_during = baseline_Z + rng.normal(0.0, 1.0)

            rows.append(dict(
                subject_id=s, sound_id=sound_id, kind="sound",
                frequency_hz=f, amplitude_db=base_amp_db,
                duration_s=duration_s, phase="during",
                impedance_Z=Z_during, reactance_X=X_during, timepoint="during"
            ))

            recovery = rng.normal(0.5, 0.3)
            X_post = max(0.0, X_during + recovery)
            Z_post = baseline_Z + rng.normal(0.0, 1.0)

            rows.append(dict(
                subject_id=s, sound_id=sound_id, kind="sound",
                frequency_hz=f, amplitude_db=base_amp_db,
                duration_s=duration_s, phase="post",
                impedance_Z=Z_post, reactance_X=X_post, timepoint="post"
            ))

        if include_controls:
            for kind in ("noise", "music"):
                for phase in ("during", "post"):
                    rows.append(dict(
                        subject_id=s, sound_id=-1, kind=kind,
                        frequency_hz=0, amplitude_db=base_amp_db,
                        duration_s=duration_s, phase=phase,
                        impedance_Z=baseline_Z + rng.normal(0, 1.0),
                        reactance_X=max(0.0, baseline_X + rng.normal(0, 0.4)),
                        timepoint=phase
                    ))

    df = pd.DataFrame(rows)
    return df
