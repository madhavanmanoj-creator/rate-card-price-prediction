from src.generate_synthetic_data import generate


def test_same_seed_gives_same_table():
    assert generate(1).equals(generate(1))


def test_table_has_expected_shape_and_valid_values():
    lanes = generate(1)
    assert len(lanes) > 1000
    assert lanes["customer_id"].nunique() == 8
    assert (lanes["base_rate_inr"] > 0).all()
    assert lanes["vol_divisor"].isin([5000, 6000]).all()


def test_international_product_costs_far_more():
    lanes = generate(1)
    med = lanes.groupby("product_code")["base_rate_inr"].median()
    assert med["I"] > 20 * med["D"]
