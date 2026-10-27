"""Generate the synthetic rate-card lane table used throughout the project.

The table mimics the structure of a courier BPM rate-card export (one row per
lane on a contract) without containing any real customer or price. Prices come
from a simple, documented recipe, so the patterns a model finds are known.

    python src/generate_synthetic_data.py --out data/processed/rate_lanes.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 2026

# lanes per customer, mix of products, home regions
CUSTOMERS = [
    # id, lanes, contracts, regions, products
    ("CUST-001", 560, 22, ["WEST1", "SOUTH1"], {"D": 0.62, "I": 0.30, "A": 0.08}),
    ("CUST-002", 170, 8, ["WEST1", "SOUTH2"], {"D": 0.60, "I": 0.30, "A": 0.10}),
    ("CUST-003", 150, 6, ["SOUTH2"], {"D": 0.65, "I": 0.35}),
    ("CUST-004", 130, 7, ["WEST1"], {"D": 0.60, "I": 0.40}),
    ("CUST-005", 110, 4, ["EAST"], {"D": 0.80, "I": 0.20}),
    ("CUST-006", 80, 4, ["SOUTH2", "WEST1"], {"D": 0.60, "I": 0.15, "A": 0.25}),
    ("CUST-007", 50, 1, ["NORTH"], {"D": 0.40, "I": 0.38, "V": 0.22}),
    ("CUST-008", 46, 2, ["NORTH"], {"D": 1.0}),
]
PRODUCT_BASE = {"D": 27.0, "A": 60.0, "I": 1700.0, "V": 4300.0}
REGION_EFFECT = {"WEST1": 0.0, "SOUTH1": -0.08, "SOUTH2": 0.25, "EAST": 0.30, "NORTH": 0.45}
DOMESTIC_ZONES = list("ABCDEFGHIJKL")
INTL_ZONES = [str(n) for n in range(1, 11)]


def _zone_effects(rng: np.random.Generator, zones: list[str], spread: float) -> dict[str, float]:
    return {z: rng.normal(0, spread) for z in zones}


def generate(seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dom_fx = _zone_effects(rng, DOMESTIC_ZONES, 0.18)
    intl_fx = _zone_effects(rng, INTL_ZONES, 0.35)
    rows = []
    contract_no = 0
    for cust_idx, (cust, n_lanes, n_contracts, regions, mix) in enumerate(CUSTOMERS, start=1):
        cust_effect = rng.normal(0, 0.12) + (0.25 if cust == "CUST-007" else 0)
        contracts = []
        for _ in range(n_contracts):
            contract_no += 1
            start = pd.Timestamp("2024-09-01") + pd.DateOffset(months=int(rng.integers(0, 21)))
            contracts.append((f"CTR-{contract_no:03d}", start, rng.normal(0, 0.05)))
        products = rng.choice(list(mix), size=n_lanes, p=list(mix.values()))
        for product in products:
            contract_id, effective, contract_effect = contracts[rng.integers(0, n_contracts)]
            region = regions[rng.integers(0, len(regions))]
            intl = product in ("I", "V")
            if intl:
                origin, dest = "IND", str(rng.choice(INTL_ZONES))
                freight, o_type, d_type = "Z2ZI", "ZONE", "ZONE"
                zone_fx, n_slabs = intl_fx[dest], int(rng.choice([12, 20, 27, 40, 57]))
            else:
                origin, dest = rng.choice(DOMESTIC_ZONES, size=2)
                freight = str(rng.choice(["Z2Z", "L2L", "R2R"], p=[0.8, 0.15, 0.05]))
                o_type = d_type = {"Z2Z": "ZONE", "L2L": "AREA", "R2R": "REGION"}[freight]
                zone_fx, n_slabs = dom_fx[origin] + dom_fx[dest], int(rng.choice([1, 2, 3, 4], p=[0.15, 0.45, 0.3, 0.1]))
            min_weight = float(rng.choice([0.25, 0.5, 1.0], p=[0.2, 0.7, 0.1]))
            first_end = float(rng.choice([0.25, 0.5, 1.0], p=[0.2, 0.75, 0.05]))
            log_rate = (np.log(PRODUCT_BASE[product]) + REGION_EFFECT[region] + zone_fx + cust_effect
                        + contract_effect + 0.35 * (min_weight - 0.5) + 0.2 * (first_end - 0.5)
                        + (0.1 if origin == dest else 0.0) + rng.normal(0, 0.08))
            rate = round(float(np.exp(log_rate)), 2)
            add_rate = round(rate * rng.uniform(0.7, 0.95), 2) if rng.random() > 0.15 else np.nan
            rows.append({
                "customer_id": cust, "contract_id": contract_id, "lead_region": region,
                "effective_date": effective.date().isoformat(), "product_code": product,
                "product_type": 1 if intl else 2,
                "charge_basis": "Per KG" if product == "A" else "Per Half KG",
                "freight_type": freight, "origin_type": o_type, "dest_type": d_type,
                "origin_zone": origin, "dest_zone": dest, "min_weight_kg": min_weight,
                "vol_divisor": int(rng.choice([5000, 6000], p=[0.9, 0.1])),
                "n_slabs": n_slabs, "first_slab_end_kg": first_end,
                "add_weight_kg": 0.5, "add_rate_inr": add_rate, "base_rate_inr": rate,
            })
    return pd.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=Path("data/processed/rate_lanes.csv"))
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()
    lanes = generate(args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    lanes.to_csv(args.out, index=False)
    print(f"wrote {len(lanes):,} synthetic lanes, {lanes['customer_id'].nunique()} customers, "
          f"{lanes['contract_id'].nunique()} contracts to {args.out}")


if __name__ == "__main__":
    main()
