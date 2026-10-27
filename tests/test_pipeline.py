from pathlib import Path

import joblib
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["lead_region", "product_code", "product_type", "charge_basis", "freight_type",
            "origin_type", "dest_type", "origin_zone", "dest_zone", "min_weight_kg",
            "first_slab_end_kg", "n_slabs", "same_zone", "vol_divisor", "months_since_2025"]


@pytest.fixture(scope="module")
def clean():
    return pd.read_csv(ROOT / "data" / "processed" / "rate_lanes_clean.csv")


def test_clean_table_has_no_private_names(clean):
    assert not any(c in clean.columns for c in ("contract_name", "Contract Name"))
    assert clean["customer_id"].str.startswith("CUST-").all()


def test_clean_table_is_valid(clean):
    assert (clean["base_rate_inr"] > 0).all()
    assert (clean["min_weight_kg"] > 0).all()
    assert clean["vol_divisor"].isin([5000, 6000]).all()
    assert not clean.duplicated().any()


@pytest.mark.parametrize("name", [
    "test_lane_inputs.xlsx", "test_predictions_vs_actuals.xlsx", "test_volume_profile.xlsx",
    "test_rate_change_scenarios.xlsx", "test_invalid_rows.xlsx",
])
def test_every_test_sheet_has_50_rows(name):
    assert len(pd.read_excel(ROOT / "test_data" / name)) >= 50


def test_model_predicts_on_test_inputs():
    model = joblib.load(ROOT / "models" / "rate_model.joblib")
    sheet = pd.read_excel(ROOT / "test_data" / "test_lane_inputs.xlsx")
    pred = model.predict(sheet[FEATURES])
    assert len(pred) == len(sheet)
    assert (pd.Series(pred).pipe(lambda s: s.apply(lambda v: 2.718281828 ** v)) > 1).all()


def test_invalid_rows_sheet_flags_each_fault_type():
    sheet = pd.read_excel(ROOT / "test_data" / "test_invalid_rows.xlsx")
    kinds = set(sheet["expected_issue"])
    assert {"negative_rate", "zero_rate", "missing_zone", "bad_divisor", "zero_min_weight", "text_in_rate", "none"} <= kinds
