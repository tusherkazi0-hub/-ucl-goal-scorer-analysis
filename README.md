# UEFA Champions League Goal Scorer — Data Project

## Files
- `ucl_goal_scorers_raw.csv` — raw (uncleaned) scraped-style dataset (2,040 rows)
- `ucl_goal_scorers_clean.csv` — cleaned dataset used for analysis (1,731 rows)
- `UCL_Lab_Report.docx` — 2-page Lab Report (submit as hard copy)
- `cleaning_log.txt` — step-by-step cleaning log with before/after counts
- `insights_summary.txt` — full text output of all data insights
- `generate_raw.py`, `clean_data.py`, `insights.py` — scripts used (put these in GitHub too, for transparency)

## Note on data source
This dataset was generated programmatically (not scraped live) because this
working environment does not have network access to sports data sites.
Player names, clubs, seasons, and goal patterns reflect real, well-known UEFA
Champions League scorers and are statistically realistic, but individual
records are simulated, not scraped. The cleaning and insight pipeline
(`clean_data.py`, `insights.py`) will work unchanged on a real scraped CSV
with the same column structure — swap in the real file and rerun.

## How to upload to GitHub
1. Create a new repository, e.g. `ucl-goal-scorer-analysis`.
2. Add these files: raw CSV, clean CSV, the three Python scripts, and the
   Lab Report (docx or a PDF export of it).
3. Add this README.md as the repo's front page.
4. Commit and push:
   ```
   git init
   git add .
   git commit -m "UCL goal scorer data cleaning and insight project"
   git branch -M main
   git remote add origin https://github.com/<your-username>/ucl-goal-scorer-analysis.git
   git push -u origin main
   ```
