# Capstone 20.1: Initial report and exploratory analysis

**Submit with this stage:** the two notebooks below (or the whole repository if the submission area asks for a link).

- `notebooks/01_data_cleaning.ipynb`
- `notebooks/02_exploratory_analysis.ipynb`

## Summary of the early evidence

**Data.** 1,296 synthetic lanes from 54 contracts and 8 fictional customers. One column (`add_rate_inr`) had missing values, meaning "no per-extra-weight step", so it was filled with 0 and flagged. All range checks passed, and there were no duplicate rows.

**Assumptions I made.**
- The price of the first slab (starting at 0 kg) is the quantity worth predicting.
- Outliers inside a product group are legitimate unusual prices, so they stay.
- `add_rate_inr` is left out of the model because it is part of the price itself.

**What exploration showed.**
- The entry price has two humps, around INR 30 and in the thousands, so a log scale is the right choice.
- Product `I` lanes cost about 56 times the other products at the median (Mann-Whitney p far below 0.001).
- A regional difference remains after setting product `I` aside (Kruskal-Wallis), and part of the raw regional gap also comes from product mix.
- The number of weight slabs correlates strongly with price (Spearman 0.65), largely because product `I` has far more slabs per lane.
- Contracts from one customer look alike, so later validation must keep customers together.

**Next:** modelling in notebook 03.
