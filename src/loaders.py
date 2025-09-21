import pandas as pd

def load_real_csv(path: str) -> pd.DataFrame:
    """
    Load real measurement data from a local CSV.
    The CSV must match the schema used in the synthetic generator:
    subject_id, sound_id, kind, frequency_hz, amplitude_db, duration_s,
    phase, impedance_Z, reactance_X, timepoint
    """
    df = pd.read_csv(path)
    return df
