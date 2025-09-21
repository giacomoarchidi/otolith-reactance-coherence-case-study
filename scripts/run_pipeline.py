from src.simulate_data import generate_dataset
from src.analysis import find_resonant_stimulus, effect_size_cohens_d, paired_t_test, permutation_test_resonance
from src.plots import heatmap_minX, subject_profile
from pathlib import Path
import numpy as np

Path("reports/figures").mkdir(parents=True, exist_ok=True)

df = generate_dataset(n_subjects=20, n_sounds=14, seed=42)
best = find_resonant_stimulus(df)

heatmap_minX(df, out="reports/figures/heatmap_minX.png")
subject_profile(df, subject_id=int(best.subject_id.iloc[0]), out="reports/figures/subject_profile.png")

baseline = df[df.kind=="baseline"].groupby("subject_id")["reactance_X"].mean().reindex(best.subject_id.values).values
during_best = []
for sid, sid_best in zip(best.subject_id.values, best.resonant_sound_id.values):
    v = df[(df.subject_id==sid) & (df.sound_id==sid_best) & (df.timepoint=="during")]["reactance_X"].values
    during_best.append(v[0] if len(v) else np.nan)
during_best = np.array(during_best)

mask = ~np.isnan(during_best)
baseline = baseline[mask]
during_best = during_best[mask]

d = effect_size_cohens_d(baseline, during_best)
tt = paired_t_test(baseline, during_best)
pt = permutation_test_resonance(baseline, during_best, n_perm=2000, seed=1)

with open("reports/results.md","w") as f:
    f.write("Results summary\n\n")
    f.write(f"Cohens d {d:.3f}\n")
    f.write(f"t test {tt['t']:.3f} p {tt['p']:.4g}\n")
    f.write(f"permutation median diff {pt['stat']:.3f} p {pt['p']:.4g}\n")

print("pipeline complete, see reports/")
