"""Reusable data-cleaning functions for the Vanguard A/B test project."""

import pandas as pd

DATA_URL = (
    "https://raw.githubusercontent.com/data-bootcamp-v4/lessons/main/"
    "5_6_eda_inf_stats_tableau/project/files_for_project/"
)

EXPERIMENT_FILE = "df_final_experiment_clients.txt"
VALID_GROUPS = ["Control", "Test"]


def load_raw(file_name: str, base_url: str = DATA_URL) -> pd.DataFrame:
    """Read one of the project's raw .txt (comma-separated) files."""
    return pd.read_csv(base_url + file_name)


def clean_experiment_clients(df: pd.DataFrame, drop_unassigned: bool = True) -> pd.DataFrame:
    """Clean the experiment roster (df_final_experiment_clients).

    Steps
    -----
    1. Lowercase / strip column names  (Variation -> variation)
    2. Drop fully duplicated rows
    3. Drop rows with a missing or invalid client_id, cast client_id to int
    4. Standardise group labels (strip spaces, Title case)
    5. Keep only 'Control' / 'Test' (clients with NA were not part of the
       experiment) when ``drop_unassigned`` is True
    6. Drop clients that appear more than once (would be in both groups)
    7. Store ``variation`` as a categorical column
    """
    out = df.copy()

    # 1. column names
    out.columns = out.columns.str.strip().str.lower()

    # 2. exact duplicates
    out = out.drop_duplicates()

    # 3. client_id
    out["client_id"] = pd.to_numeric(out["client_id"], errors="coerce")
    out = out.dropna(subset=["client_id"])
    out = out[out["client_id"] > 0]
    out["client_id"] = out["client_id"].astype("int64")

    # 4. group labels
    out["variation"] = out["variation"].astype("string").str.strip().str.title()

    # 5. unassigned clients / unexpected labels
    if drop_unassigned:
        out = out[out["variation"].isin(VALID_GROUPS)]

    # 6. clients listed more than once (e.g. in both groups)
    out = out.drop_duplicates(subset="client_id", keep=False)

    # 7. dtype
    out["variation"] = pd.Categorical(out["variation"], categories=VALID_GROUPS)

    return out.sort_values("client_id").reset_index(drop=True)
