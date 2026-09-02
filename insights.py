import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["figure.dpi"] = 150
df = pd.read_csv("ucl_goal_scorers_clean.csv")

insights = []

# 1. Top 10 goal scorers
top_scorers = df["Player"].value_counts().head(10)
insights.append(("Top 10 Goal Scorers", top_scorers))

# 2. Goals per club
goals_per_club = df["Club"].value_counts().head(10)
insights.append(("Top 10 Clubs by Goals", goals_per_club))

# 3. Goals per season
goals_per_season = df.groupby("Season").size().sort_index()
insights.append(("Goals per Season", goals_per_season))

# 4. Goal type distribution
goal_type_dist = df["Goal_Type"].value_counts()
insights.append(("Goal Type Distribution", goal_type_dist))

# 5. Home vs Away goals
venue_dist = df["Venue"].value_counts()
insights.append(("Home vs Away Goals", venue_dist))

# 6. Goals by match round
round_dist = df["Round"].value_counts()
insights.append(("Goals by Round", round_dist))

# 7. Average goal minute
avg_minute = df["Minute"].mean()

# 8. Goals by 15-min interval
bins = [0, 15, 30, 45, 60, 75, 96]
labels = ["1-15", "16-30", "31-45", "46-60", "61-75", "76-96"]
df["Minute_Bucket"] = pd.cut(df["Minute"], bins=bins, labels=labels)
minute_bucket_dist = df["Minute_Bucket"].value_counts().reindex(labels)

# Print all insights
with open("insights_summary.txt", "w") as f:
    for title, data in insights:
        f.write(f"=== {title} ===\n{data.to_string()}\n\n")
    f.write(f"Average goal-scoring minute: {avg_minute:.1f}\n\n")
    f.write(f"=== Goals by 15-min Interval ===\n{minute_bucket_dist.to_string()}\n")

for title, data in insights:
    print(f"=== {title} ===")
    print(data)
    print()
print(f"Average goal-scoring minute: {avg_minute:.1f}")
print(minute_bucket_dist)

# ---- Charts ----
# Chart 1: Top 10 scorers
plt.figure(figsize=(8,5))
top_scorers.sort_values().plot(kind="barh", color="#1f4e8c")
plt.title("Top 10 Goal Scorers - UEFA Champions League")
plt.xlabel("Goals")
plt.tight_layout()
plt.savefig("chart_top_scorers.png")
plt.close()

# Chart 2: Goals per season
plt.figure(figsize=(9,5))
goals_per_season.plot(kind="line", marker="o", color="#c0392b")
plt.title("Goals per Season")
plt.xlabel("Season")
plt.ylabel("Number of Goals")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart_goals_per_season.png")
plt.close()

# Chart 3: Goal type distribution (pie)
plt.figure(figsize=(6,6))
goal_type_dist.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Goal Type Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("chart_goal_types.png")
plt.close()

# Chart 4: Minute buckets
plt.figure(figsize=(8,5))
minute_bucket_dist.plot(kind="bar", color="#27ae60")
plt.title("Goals by Match Minute Interval")
plt.xlabel("Minute Range")
plt.ylabel("Goals")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart_minute_buckets.png")
plt.close()

print("\nCharts saved.")
