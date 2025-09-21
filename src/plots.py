from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def heatmap_minX(df: pd.DataFrame, out: str | None = None):
    """
    Heatmap of minimum during reactance per subject by sound.
    """
    during = df[(df["kind"] == "sound") & (df["timepoint"] == "during")]
    pivot = during.pivot_table(index="subject_id", columns="sound_id", values="reactance_X", aggfunc="min")
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=False, cbar=True)
    plt.title("Minimum during reactance X per subject by sound")
    plt.xlabel("sound_id")
    plt.ylabel("subject_id")
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out, bbox_inches="tight", dpi=150)
    plt.show()

def subject_profile(df: pd.DataFrame, subject_id: int, out: str | None = None):
    """
    Line plot of reactance across sounds for a given subject during phase.
    """
    d = df[(df["subject_id"] == subject_id) & (df["kind"] == "sound") & (df["timepoint"] == "during")]
    d = d.sort_values("sound_id")
    plt.figure(figsize=(9, 4))
    plt.plot(d["sound_id"], d["reactance_X"], marker="o")
    plt.title(f"Subject {subject_id} — during reactance across sounds")
    plt.xlabel("sound_id")
    plt.ylabel("reactance_X")
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out, bbox_inches="tight", dpi=150)
    plt.show()
