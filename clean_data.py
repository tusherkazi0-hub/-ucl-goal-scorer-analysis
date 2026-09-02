import pandas as pd
import numpy as np

df = pd.read_csv("ucl_goal_scorers_raw.csv")

report_lines = []
report_lines.append(f"Raw rows loaded: {len(df)}")

# 1. Strip whitespace from string columns
str_cols = df.select_dtypes(include="object").columns
for c in str_cols:
    df[c] = df[c].astype(str).str.strip()
    df[c] = df[c].replace({"nan": np.nan, "None": np.nan, "": np.nan})

# 2. Standardize text case (Title Case for names/clubs/opponents, proper case for round/goal type/venue)
for c in ["Player", "Club", "Opponent", "Nationality"]:
    df[c] = df[c].str.title()

df["Round"] = df["Round"].str.title().replace({"R16": "Round Of 16"})
df["Goal_Type"] = df["Goal_Type"].str.title()
df["Venue"] = df["Venue"].str.title()

# 3. Clean Minute column: remove apostrophes, convert to numeric
df["Minute"] = df["Minute"].astype(str).str.replace("'", "", regex=False)
df["Minute"] = pd.to_numeric(df["Minute"], errors="coerce")

# 4. Drop rows where Opponent equals the player's own Club (bad scraped rows) or Opponent missing
before = len(df)
df = df[df["Opponent"] != df["Club"]]
report_lines.append(f"Rows removed (Opponent == Club, invalid record): {before - len(df)}")

# 5. Handle missing values
before = len(df)
missing_summary = df.isna().sum()
report_lines.append("Missing values per column before imputation:\n" + missing_summary.to_string())

# Drop rows missing Opponent (can't be recovered meaningfully)
df = df.dropna(subset=["Opponent"])

# Impute missing Minute with column median
median_minute = df["Minute"].median()
df["Minute"] = df["Minute"].fillna(median_minute)
df["Minute"] = df["Minute"].astype(int)

# Impute missing Nationality using the most common nationality for that player
nat_map = df.dropna(subset=["Nationality"]).groupby("Player")["Nationality"].agg(lambda x: x.mode()[0])
df["Nationality"] = df.apply(
    lambda r: nat_map.get(r["Player"], r["Nationality"]) if pd.isna(r["Nationality"]) else r["Nationality"],
    axis=1
)

report_lines.append(f"Rows removed (missing Opponent): {before - len(df)}")

# 6. Remove duplicate rows
before = len(df)
df = df.drop_duplicates()
report_lines.append(f"Duplicate rows removed: {before - len(df)}")

# 7. Validate Minute range (0-96)
before = len(df)
df = df[(df["Minute"] >= 1) & (df["Minute"] <= 96)]
report_lines.append(f"Rows removed (invalid Minute range): {before - len(df)}")

# 8. Validate Goals_In_Match
df["Goals_In_Match"] = pd.to_numeric(df["Goals_In_Match"], errors="coerce")
df = df.dropna(subset=["Goals_In_Match"])
df["Goals_In_Match"] = df["Goals_In_Match"].astype(int)

# 9. Reset index
df = df.reset_index(drop=True)

report_lines.append(f"Final clean row count: {len(df)}")
report_lines.append(f"Final columns: {list(df.columns)}")
report_lines.append(f"Remaining nulls total: {df.isna().sum().sum()}")

df.to_csv("ucl_goal_scorers_clean.csv", index=False)

with open("cleaning_log.txt", "w") as f:
    f.write("\n\n".join(report_lines))

print("\n\n".join(report_lines))
