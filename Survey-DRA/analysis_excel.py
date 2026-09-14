import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import statsmodels
import math

# 1) LOAD EXCEL
file_path = "Failure_Analysis_Questionnaire_B.xlsx"  # Change as needed
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name='Form responses 1')

# 2) IDENTIFY POSSIBLE ANSWERS & RATING COLUMNS
POSSIBLE_ANSWERS = ["A", "B", "C"]
rating_columns = [col for col in df.columns if "Rate answer" in col]

# Convert rating columns to numeric (handles NaNs gracefully)
df_ratings = df[rating_columns].apply(pd.to_numeric, errors='coerce')

# 3) READ QUESTIONS ORDER FROM JSON
with open('random_tuples.json') as f:
    questions_order = json.load(f)
questions_order = questions_order[32:]  # Adjust as needed
# 4) FILL EMPTY "CHOOSE THE BEST ANSWER" CELLS BASED ON HIGHEST RATING
question_count = 0
for i in range(len(df.columns)):
    if "Choose the best answer" in df.columns[i]:
        new_order = questions_order[question_count]  # e.g. [1, 2, 0]
        
        question_col = df.columns[i]
        rate_a_col = df.columns[i + 1]
        rate_b_col = df.columns[i + 2]
        rate_c_col = df.columns[i + 3]

        # Fill empty "Choose the best answer" with whichever rating is highest
        df[question_col] = df[question_col].fillna(
            df[[rate_a_col, rate_b_col, rate_c_col]]
            .idxmax(axis=1)
            .str.extract(r'Rate answer: (A|B|C)')[0]
        )
        
        # Keep only the first letter (in case of partial strings)
        df[question_col] = df[question_col].astype(str).str[0]

        # Re-map the answers according to new_order
        df[question_col] = df[question_col].replace(
            {
                "A": POSSIBLE_ANSWERS[new_order[0]], 
                "B": POSSIBLE_ANSWERS[new_order[1]], 
                "C": POSSIBLE_ANSWERS[new_order[2]]
            }
        )

        # Rearrange the rating columns so they match the new question order
        cols = list(df.columns)
        cols[i + 1], cols[i + 2], cols[i + 3] = (
            cols[i + new_order[0] + 1],
            cols[i + new_order[1] + 1],
            cols[i + new_order[2] + 1]
        )
        df.columns = cols

        question_count += 1

# 5) BUILD THE QUESTIONS_DICT STRUCTURE
questions_dict = {"Model A": {}, "Model B": {}, "Model C": {}}
# Adjust number of questions as needed (here: 35)
NUM_QUESTIONS = 30

for k in questions_dict.keys():
    for i in range(NUM_QUESTIONS):
        questions_dict[k][f"Question_{i}"] = {"Favorite": [], "Rating": []}

question_nb = 0
qustion_A_encountered = False
qustion_B_encountered = False
qustion_C_encountered = False

for col in df.columns:
    # Whenever we see "Choose the best answer", that indicates a new question
    if col.startswith("Choose the best answer"):
        # Populate "Favorite"
        for i in range(len(df[col])):
            if df[col].iloc[i] == "A":
                questions_dict["Model A"][f"Question_{question_nb}"]["Favorite"].append(1)
                questions_dict["Model B"][f"Question_{question_nb}"]["Favorite"].append(0)
                questions_dict["Model C"][f"Question_{question_nb}"]["Favorite"].append(0)
            elif df[col].iloc[i] == "B":
                questions_dict["Model A"][f"Question_{question_nb}"]["Favorite"].append(0)
                questions_dict["Model B"][f"Question_{question_nb}"]["Favorite"].append(1)
                questions_dict["Model C"][f"Question_{question_nb}"]["Favorite"].append(0)
            elif df[col].iloc[i] == "C":
                questions_dict["Model A"][f"Question_{question_nb}"]["Favorite"].append(0)
                questions_dict["Model B"][f"Question_{question_nb}"]["Favorite"].append(0)
                questions_dict["Model C"][f"Question_{question_nb}"]["Favorite"].append(1)

    # Ratings for Model A
    if col.startswith("Rate answer: A"):
        for i in range(len(df[col])):
            questions_dict["Model A"][f"Question_{question_nb}"]["Rating"].append(df[col].iloc[i])
        qustion_A_encountered = True

    # Ratings for Model B
    if col.startswith("Rate answer: B"):
        for i in range(len(df[col])):
            questions_dict["Model B"][f"Question_{question_nb}"]["Rating"].append(df[col].iloc[i])
        qustion_B_encountered = True

    # Ratings for Model C
    if col.startswith("Rate answer: C"):
        for i in range(len(df[col])):
            questions_dict["Model C"][f"Question_{question_nb}"]["Rating"].append(df[col].iloc[i])
        qustion_C_encountered = True

    # Once we've encountered A, B, C columns, move to next question
    if qustion_A_encountered and qustion_B_encountered and qustion_C_encountered:
        question_nb += 1
        qustion_A_encountered = qustion_B_encountered = qustion_C_encountered = False

# 1) LOAD EXCEL
file_path = "Failure_Analysis_Questionnaire_A.xlsx"  # Change as needed
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name='Form responses 1')

# 2) IDENTIFY POSSIBLE ANSWERS & RATING COLUMNS
POSSIBLE_ANSWERS = ["A", "B", "C"]
rating_columns = [col for col in df.columns if "Rate answer" in col]

# Convert rating columns to numeric (handles NaNs gracefully)
df_ratings = df[rating_columns].apply(pd.to_numeric, errors='coerce')

# 3) READ QUESTIONS ORDER FROM JSON
with open('random_tuples.json') as f:
    questions_order = json.load(f)
questions_order = questions_order[:32]  # Adjust as needed
# 4) FILL EMPTY "CHOOSE THE BEST ANSWER" CELLS BASED ON HIGHEST RATING
question_count = 0
for i in range(len(df.columns)):
    if "Choose the best answer" in df.columns[i]:
        new_order = questions_order[question_count]  # e.g. [1, 2, 0]
        
        question_col = df.columns[i]
        rate_a_col = df.columns[i + 1]
        rate_b_col = df.columns[i + 2]
        rate_c_col = df.columns[i + 3]

        # Fill empty "Choose the best answer" with whichever rating is highest
        df[question_col] = df[question_col].fillna(
            df[[rate_a_col, rate_b_col, rate_c_col]]
            .idxmax(axis=1)
            .str.extract(r'Rate answer: (A|B|C)')[0]
        )
        
        # Keep only the first letter (in case of partial strings)
        df[question_col] = df[question_col].astype(str).str[0]

        # Re-map the answers according to new_order
        df[question_col] = df[question_col].replace(
            {
                "A": POSSIBLE_ANSWERS[new_order[0]], 
                "B": POSSIBLE_ANSWERS[new_order[1]], 
                "C": POSSIBLE_ANSWERS[new_order[2]]
            }
        )

        # Rearrange the rating columns so they match the new question order
        cols = list(df.columns)
        cols[i + 1], cols[i + 2], cols[i + 3] = (
            cols[i + new_order[0] + 1],
            cols[i + new_order[1] + 1],
            cols[i + new_order[2] + 1]
        )
        df.columns = cols

        question_count += 1

# 5) BUILD THE QUESTIONS_DICT STRUCTURE
NUM_QUESTIONS_B = 32

for k in questions_dict.keys():
    for i in range(NUM_QUESTIONS):
        # print(f"Adding Question_{NUM_QUESTIONS + i} to {k}")
        questions_dict[k][f"Question_{NUM_QUESTIONS + i}"] = {"Favorite": [], "Rating": []}

qustion_A_encountered = False
qustion_B_encountered = False
qustion_C_encountered = False

for col in df.columns:
    # Whenever we see "Choose the best answer", that indicates a new question
    if question_nb >= 60:
        break
    if col.startswith("Choose the best answer"):
        # Populate "Favorite"
        for i in range(len(df[col])):
            if df[col].iloc[i] == "A":
                questions_dict["Model A"][f"Question_{question_nb}"]["Favorite"].append(1)
                questions_dict["Model B"][f"Question_{question_nb}"]["Favorite"].append(0)
                questions_dict["Model C"][f"Question_{question_nb}"]["Favorite"].append(0)
            elif df[col].iloc[i] == "B":
                questions_dict["Model A"][f"Question_{question_nb}"]["Favorite"].append(0)
                questions_dict["Model B"][f"Question_{question_nb}"]["Favorite"].append(1)
                questions_dict["Model C"][f"Question_{question_nb}"]["Favorite"].append(0)
            elif df[col].iloc[i] == "C":
                questions_dict["Model A"][f"Question_{question_nb}"]["Favorite"].append(0)
                questions_dict["Model B"][f"Question_{question_nb}"]["Favorite"].append(0)
                questions_dict["Model C"][f"Question_{question_nb}"]["Favorite"].append(1)

    # Ratings for Model A
    if col.startswith("Rate answer: A"):
        for i in range(len(df[col])):
            questions_dict["Model A"][f"Question_{question_nb}"]["Rating"].append(df[col].iloc[i])
        qustion_A_encountered = True

    # Ratings for Model B
    if col.startswith("Rate answer: B"):
        for i in range(len(df[col])):
            questions_dict["Model B"][f"Question_{question_nb}"]["Rating"].append(df[col].iloc[i])
        qustion_B_encountered = True

    # Ratings for Model C
    if col.startswith("Rate answer: C"):
        for i in range(len(df[col])):
            questions_dict["Model C"][f"Question_{question_nb}"]["Rating"].append(df[col].iloc[i])
        qustion_C_encountered = True

    # Once we've encountered A, B, C columns, move to next question
    if qustion_A_encountered and qustion_B_encountered and qustion_C_encountered:
        question_nb += 1
        qustion_A_encountered = qustion_B_encountered = qustion_C_encountered = False

# 6) FLATTEN questions_dict INTO A PANDAS DATAFRAME
records = []
for model, question_data in questions_dict.items():
    for question_id, info in question_data.items():
        fav_list = info["Favorite"]
        rate_list = info["Rating"]
        for fav, rating in zip(fav_list, rate_list):
            records.append({
                "Model": model,
                "Question": question_id,
                "Favorite": fav,
                "Rating": rating
            })

stats_df = pd.DataFrame(records)


# Number of participants (rows in original DF)
num_participants = len(df)

# 7) COMPUTE STATISTICS FOR EACH MODEL
# (A) Total times chosen as favorite
favorite_counts = (stats_df
                   .groupby("Model")["Favorite"]
                   .sum()
                   .reset_index(name="FavoriteCount"))

# (B) Mean rating
avg_rating = (stats_df
              .groupby("Model")["Rating"]
              .mean()
              .reset_index(name="MeanRating"))

# (C) Variance of the rating  <<< NEW
#     • ddof=0 → population variance; use ddof=1 for sample variance if you prefer
rating_var = (stats_df
              .groupby("Model")["Rating"]
              .var(ddof=0)
              .reset_index(name="VarRating"))

# (D) Percentage chosen as favorite
actual_num_questions = question_nb          # you already derived this above
all_favorite_counts = favorite_counts["FavoriteCount"].sum()
favorite_counts["PercPreferred"] = (
    favorite_counts["FavoriteCount"] /
    (all_favorite_counts) * 100
)

# Standard deviation of ratings
rating_sd = (stats_df
             .groupby("Model")["Rating"]
             .std(ddof=0)        # ddof=0 for population SD
             .reset_index(name="StdRating"))

def pop_sd(series):
    """Population SD implemented from scratch."""
    series = series.dropna()
    μ = series.mean()
    return math.sqrt(math.fsum((x - μ)**2 for x in series) / len(series))

sd_manual = (stats_df
             .groupby("Model")["Rating"]
             .apply(pop_sd)
             .rename("SD_manual"))


# save all MODEL A Ratings in a file
stats_df.to_csv("model_a_ratings.csv", index=False)


# 95% CI for percentage preferred (Wilson)
import statsmodels.stats.proportion as smp
ci_rows = []
total_trials = stats_df.groupby("Model")["Favorite"].count().values[0]
for _, row in favorite_counts.iterrows():
    ci_low, ci_upp = smp.proportion_confint(
        count=row.FavoriteCount,
        nobs=total_trials ,
        alpha=0.05,
        method='wilson')
    ci_rows.append((row.Model, ci_low*100, ci_upp*100))
ci_df = pd.DataFrame(ci_rows, columns=["Model", "CI_Low", "CI_High"])

# Merge into your summary table
stats_summary = (favorite_counts
                 .merge(avg_rating, on="Model")
                 .merge(rating_sd,  on="Model")
                 .merge(ci_df,      on="Model"))

print("\n=== Statistics Summary (per Model) ===")
print(stats_summary)

# 9) SAVE RESULTS (unchanged, but now VarRating is included)
output_file = "my_statistics.xlsx"
with pd.ExcelWriter(output_file) as writer:
    stats_summary.to_excel(writer, sheet_name="ModelSummary", index=False)
    stats_df.to_excel(writer,       sheet_name="AllData",     index=False)

print(f"Results saved to: {output_file}")

# === SIGNIFICANCE TESTS FOR YOUR 3 MODELS ===
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.api as sm

# --- 0) Small helpers ---
def cohens_d(x, y):
    x = pd.Series(x).dropna().to_numpy()
    y = pd.Series(y).dropna().to_numpy()
    nx, ny = len(x), len(y)
    if nx < 2 or ny < 2:
        return np.nan
    sx, sy = x.std(ddof=1), y.std(ddof=1)
    # pooled SD
    s_p = np.sqrt(((nx-1)*sx**2 + (ny-1)*sy**2) / (nx + ny - 2))
    return (x.mean() - y.mean()) / s_p if s_p > 0 else np.nan

def eta_squared_anova(F, k, N):
    # k groups, N total observations
    return (F * (k - 1)) / (F * (k - 1) + (N - k)) if N > k and F is not None else np.nan

# --- 1) FAVORITES: Chi-square goodness-of-fit vs equal split ---
# Observed favorites per model
fav_df = favorite_counts.copy()
fav_df = fav_df.sort_values("Model")
obs = fav_df["FavoriteCount"].to_numpy()
labels = fav_df["Model"].tolist()

# Expected = equal share
exp = np.full_like(obs, fill_value=obs.sum() / len(obs), dtype=float)

chi2_stat, chi2_p = stats.chisquare(f_obs=obs, f_exp=exp)

# Cohen's w (effect size for GOF chi-square)
N = obs.sum()
cohens_w = np.sqrt(chi2_stat / N) if N > 0 else np.nan

print("\n=== FAVORITES: Chi-square Goodness-of-Fit (vs equal A/B/C) ===")
print(f"Observed counts: {dict(zip(labels, obs))}")
print(f"Chi² = {chi2_stat:.3f},  df = {len(obs)-1},  p-value = {chi2_p:.4g}")
print(f"Effect size (Cohen's w) = {cohens_w:.3f}  "
      "(~0.1 small, ~0.3 medium, ~0.5 large)\n")

# --- 1b) FAVORITES: Pairwise z-tests of proportions (Bonferroni corrected) ---
# Each model has the same denominator = total number of trials where a favorite could be chosen
# following your CI computation:
n_trials_each = num_participants * actual_num_questions

pairs = [("Model A", "Model B"), ("Model A", "Model C"), ("Model B", "Model C")]
pair_rows = []
for a, b in pairs:
    ca = int(fav_df.loc[fav_df.Model == a, "FavoriteCount"])
    cb = int(fav_df.loc[fav_df.Model == b, "FavoriteCount"])
    stat, pval = proportions_ztest([ca, cb], [n_trials_each, n_trials_each])
    pair_rows.append((a, b, stat, pval))

pair_df = pd.DataFrame(pair_rows, columns=["Group1", "Group2", "Z", "p_raw"])
# Bonferroni correction for 3 tests
pair_df["p_Bonferroni"] = np.minimum(pair_df["p_raw"] * len(pair_df), 1.0)

print("=== FAVORITES: Pairwise Proportion z-tests (Bonferroni corrected) ===")
print(pair_df.to_string(index=False), "\n")

# --- 2) RATINGS: ANOVA across the 3 models ---
ratings_A = stats_df.loc[stats_df.Model == "Model A", "Rating"].dropna()
ratings_B = stats_df.loc[stats_df.Model == "Model B", "Rating"].dropna()
ratings_C = stats_df.loc[stats_df.Model == "Model C", "Rating"].dropna()

f_stat, p_val = stats.f_oneway(ratings_A, ratings_B, ratings_C)
N_total = len(ratings_A) + len(ratings_B) + len(ratings_C)
eta2 = eta_squared_anova(f_stat, k=3, N=N_total)

print("=== RATINGS: One-way ANOVA ===")
print(f"F = {f_stat:.3f},  p-value = {p_val:.4g},  η² = {eta2:.3f} "
      "(~0.01 small, ~0.06 medium, ~0.14 large)\n")

# --- 2b) RATINGS: Tukey HSD post-hoc (which pairs differ) ---
tukey = pairwise_tukeyhsd(endog=stats_df["Rating"].dropna(),
                          groups=stats_df["Model"][stats_df["Rating"].notna()],
                          alpha=0.05)
print("=== RATINGS: Tukey HSD Post-hoc ===")
print(tukey.summary(), "\n")

# --- 2c) RATINGS: Pairwise Cohen's d (effect size) ---
d_rows = []
pairs_mod = [("Model A", ratings_A), ("Model B", ratings_B), ("Model C", ratings_C)]
for i in range(len(pairs_mod)):
    for j in range(i+1, len(pairs_mod)):
        g1, x = pairs_mod[i]
        g2, y = pairs_mod[j]
        d = cohens_d(x, y)
        d_rows.append((g1, g2, d))
d_df = pd.DataFrame(d_rows, columns=["Group1", "Group2", "Cohen_d"])

print("=== RATINGS: Pairwise Effect Sizes (Cohen's d) ===")
print(d_df.to_string(index=False))
print("\nNotes:")
print("- For favorites: significant chi-square => distribution not equal; see pairwise z-tests for which pairs differ (use Bonferroni p).")
print("- For ratings: significant ANOVA => at least one mean differs; see Tukey for pairwise differences.")
print("- Report effect sizes (w, d, η²) alongside p-values.")
