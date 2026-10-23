# IPL Data Analysis (2008–2022)

End-to-end data analyst project on 15 seasons of the Indian Premier League: data cleaning and validation, exploratory analysis, 10 charts, 9 summary tables and written findings.

## Questions answered
1. How has IPL scoring changed (run rate, sixes, fours)?
2. Who are the most productive *and* most efficient batters and bowlers?
3. Which innings phase (powerplay / middle / death) drove the scoring boom?
4. Does the toss matter — is chasing better?
5. Which venues, teams and players stand out?

## Project structure
```
ipl-analysis/
├── data/
│   ├── ipl_ball_by_ball_2008_2022.csv   # 225,954 balls, 950 matches
│   ├── matches_2008_2017.csv            # 636 matches: toss, winner, venue, player of match
│   └── deliveries_2008_2017.csv         # ball-by-ball for the same 636 matches
├── src/ipl_lib.py                       # loading, cleaning, validation, chart helpers
├── notebooks/IPL_Analysis.ipynb         # the analysis (already executed, outputs included)
├── outputs/charts/                      # 10 PNG charts
└── outputs/tables/                      # 9 CSV summary tables (Excel / Power BI ready)
```

## Run it
```bash
pip install -r requirements.txt
cd notebooks && jupyter nbconvert --to notebook --execute --inplace IPL_Analysis.ipynb
```

## Data cleaning highlights
- Franchise renames unified (Delhi Daredevils → Capitals, Kings XI → Punjab Kings, Supergiant/Supergiants).
- Season for the 2008–22 file is derived from match-ID blocks and **asserted against official match counts** for all 15 seasons.
- `NA` strings → nulls; 0-indexed overs → 1–20; wides excluded from balls faced; byes/leg-byes excluded from bowler runs; run-outs excluded from bowler wickets.

## Headline findings
- Run rate: **7.49 (2009) → 8.65 (2018)**; sixes/match **~8.8 (2011) → ~14.5 (2018)**.
- Death overs gained the most (+0.61 runs/over vs 2008–12) and score ~2 runs/over more than any other phase.
- Kohli leads runs (6,634); de Villiers (SR 151.9) and Gayle (149.3) lead efficiency; Bravo leads wickets (183); Narine's economy (6.64) is the best among top wicket-takers.
- Toss winner wins only 51.3%, but **chasing wins 55.1%** (2008–17); teams moved from ~35–40% choosing to field (2009–10) to >80% (2016–17).
- Chinnaswamy averages ~167 first-innings runs vs ~154 at Eden Gardens.

## Source material
Built from the `IPL` datasets in the Pandas and Matplotlib course folders. Unrelated files (iris, fortune500, font cache, small pre-aggregated CSVs such as `batter.csv`) were deliberately left out — everything they contained is recomputed from the raw data here.

**Tools:** Python, pandas, NumPy, Matplotlib, Jupyter.
