from src.simulate_data import generate_dataset
from src.analysis import find_resonant_stimulus

def test_generate_and_find_resonance():
    df = generate_dataset(n_subjects=5, n_sounds=6, seed=0)
    assert len(df) > 0
    best = find_resonant_stimulus(df)
    assert len(best) == 5
    assert (best["min_X_during"] >= 0).all()
