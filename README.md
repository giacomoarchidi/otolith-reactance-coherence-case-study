Otolith Reactance and Coherence — Case Study

This repository investigates how pulsed sonic stimuli influence reactance X and impedance Z measurements and whether, for each subject, there exists a single resonant stimulus that drives X towards zero. The repo is public safe and uses synthetic data that mimic real structure and noise characteristics. If or when permitted, real data should live in a private companion repository.

What is inside
- Synthetic data generator in src/simulate_data.py with realistic noise and one resonant sound per subject
- Analysis in src/analysis.py to detect the resonant stimulus, compute effect sizes, and run simple non parametric tests
- Plots in src/plots.py including subject by sound heatmap, per subject profiles, and distributions
- Notebook to be created as notebooks/01_eda.ipynb for exploratory analysis

Environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

Quick start
from src.simulate_data import generate_dataset
from src.analysis import find_resonant_stimulus
from src.plots import heatmap_minX, subject_profile

df = generate_dataset(n_subjects=20, n_sounds=14, seed=42)
best = find_resonant_stimulus(df)
print(best.head())

Repo structure
.
├─ data
├─ notebooks
├─ reports
│  └─ figures
├─ src
│  ├─ simulate_data.py
│  ├─ analysis.py
│  └─ plots.py
├─ tests
├─ requirements.txt
└─ README.md

Public vs private data
- Public repo uses synthetic data only
- Real data must stay in a private repo or remain local and be loaded by a local path

Roadmap
- Replace synthetic generator with a loader for real CSV or Parquet kept locally
- Add mixed effects modeling with subject as random effect
- Add a short data card and model card with limitations and ethics notes

License
MIT
