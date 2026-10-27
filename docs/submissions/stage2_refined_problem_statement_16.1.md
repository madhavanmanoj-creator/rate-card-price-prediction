# Capstone 16.1: Refined problem statement

## What changed since the draft
Early exploration showed that the data holds 54 contracts but only 8 customers, and one customer supplies close to half the lanes. That makes a random train/test split misleading, so the plan now validates by customer. It also showed that prices fall into two very different groups, so the target will be modelled on a log scale.

## Scope
Predict the price of the first weight slab (`base_rate_inr`) for each freight lane on a contract. Heavier slabs, surcharges and value-added services are out of scope.

## Target outcome
A regression model whose typical error, measured as the mean absolute error of the log price, is clearly lower than a median-guess baseline on customers held out of training.

## Data
`data/processed/rate_lanes.csv`: 1,296 synthetic lanes, 54 contracts, 8 fictional customers, effective dates from September 2024 to May 2026, produced by `src/generate_synthetic_data.py`.

## Constraints
- Only eight customers, so results can swing depending on which are held out.
- Product codes `A` and `V` have few lanes.
- The data is simulated, so results show the method works rather than how accurate it is on real contracts.
- Product letters are treated as labels; I make no claim about what each means.

## How success will be judged
1. Leave-one-customer-out cross-validation error lower than the median baseline.
2. One held-out test on two untouched customers, reported with an interval.
3. Results explained in plain language, including where the model is unreliable.
4. Concrete recommendations that a pricing analyst could act on.

## Models planned
Median baseline, ridge regression, random forest and gradient boosting, with grid search on all three real models.
