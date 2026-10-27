"""Create the Excel test sheets in test_data/.

Every sheet has at least 50 rows. Three are synthetic, one is a slice of the
anonymised held-out predictions, and one is deliberately broken so the
cleaning checks have something to catch.

    python src/make_test_data.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "test_data"
SEED = 7
FEATURES = ["lead_region", "product_code", "product_type", "charge_basis", "freight_type",
            "origin_type", "dest_type", "origin_zone", "dest_zone", "min_weight_kg",
            "first_slab_end_kg", "n_slabs", "same_zone", "vol_divisor", "months_since_2025"]


def lane_inputs(clean: pd.DataFrame, rng: np.random.Generator, n: int = 60) -> pd.DataFrame:
    """Plausible lanes for a customer the model has never seen."""
    picked = clean[FEATURES].sample(n, random_state=SEED).reset_index(drop=True)
    picked["first_slab_end_kg"] = picked["first_slab_end_kg"].fillna(10).clip(upper=10)
    picked.insert(0, "lane_id", [f"TEST-{i:03d}" for i in range(1, n + 1)])
    picked["months_since_2025"] = rng.integers(14, 19, size=n)
    return picked


def predictions_with_actuals(n: int = 60) -> pd.DataFrame:
    preds = pd.read_csv(ROOT / "reports" / "test_predictions.csv")
    return preds.sample(min(n, len(preds)), random_state=SEED).reset_index(drop=True)


def volume_profile(clean: pd.DataFrame, rng: np.random.Generator, n: int = 52) -> pd.DataFrame:
    lanes = clean[["origin_zone", "dest_zone", "product_code"]].drop_duplicates().sample(n, random_state=SEED)
    lanes = lanes.reset_index(drop=True)
    lanes["monthly_shipments"] = rng.integers(20, 5000, size=n)
    lanes["avg_weight_kg"] = rng.choice([0.5, 1, 2, 5, 10, 25], size=n).astype(float)
    return lanes


def rate_change_scenarios(rng: np.random.Generator, n: int = 50) -> pd.DataFrame:
    return pd.DataFrame({
        "scenario": [f"S{i:02d}" for i in range(1, n + 1)],
        "price_change_pct": np.round(rng.uniform(-10, 15, n), 1),
        "customer_sensitivity": np.round(rng.uniform(0.3, 2.0, n), 2),
        "fuel_surcharge_pct": np.round(rng.choice([0, 5, 10, 15, 20, 25], n), 1),
        "discount_pct": np.round(rng.choice([0, 2, 5, 8, 10], n), 1),
    })


def broken_rows(clean: pd.DataFrame, rng: np.random.Generator, n: int = 55) -> pd.DataFrame:
    """Rows with known faults; `expected_issue` says what a validator should flag."""
    base = clean[["customer_id", "contract_id", "lead_region", "product_code", "origin_zone",
                  "dest_zone", "min_weight_kg", "vol_divisor", "base_rate_inr"]].sample(n, random_state=SEED)
    base = base.reset_index(drop=True).astype(object)
    base["expected_issue"] = "none"
    faults = {
        "negative_rate": ("base_rate_inr", lambda v: -abs(v)),
        "zero_rate": ("base_rate_inr", lambda v: 0),
        "missing_zone": ("origin_zone", lambda v: None),
        "bad_divisor": ("vol_divisor", lambda v: 1234),
        "zero_min_weight": ("min_weight_kg", lambda v: 0),
        "text_in_rate": ("base_rate_inr", lambda v: "N/A"),
    }
    names = list(faults)
    for i in range(36):  # the first 36 rows get a fault, the rest stay clean
        kind = names[i % len(names)]
        column, change = faults[kind]
        base.at[i, column] = change(base.at[i, column])
        base.at[i, "expected_issue"] = kind
    return base


def main() -> None:
    clean_path = ROOT / "data" / "processed" / "rate_lanes_clean.csv"
    if not clean_path.exists():
        raise FileNotFoundError("Run notebook 01 first so rate_lanes_clean.csv exists")
    clean = pd.read_csv(clean_path)
    rng = np.random.default_rng(SEED)
    OUT.mkdir(exist_ok=True)
    sheets = {
        "test_lane_inputs.xlsx": lane_inputs(clean, rng),
        "test_predictions_vs_actuals.xlsx": predictions_with_actuals(),
        "test_volume_profile.xlsx": volume_profile(clean, rng),
        "test_rate_change_scenarios.xlsx": rate_change_scenarios(rng),
        "test_invalid_rows.xlsx": broken_rows(clean, rng),
    }
    for name, frame in sheets.items():
        assert len(frame) >= 50, f"{name} has only {len(frame)} rows"
        frame.to_excel(OUT / name, index=False, sheet_name="data")
        print(f"{name}: {len(frame)} rows")


if __name__ == "__main__":
    main()
