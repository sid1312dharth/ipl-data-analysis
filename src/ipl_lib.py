"""Loading, cleaning and feature helpers for the IPL analysis project."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Franchises that were renamed / re-spelled -> one canonical name
TEAM_MAP = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
    "Royal Challengers Bengaluru": "Royal Challengers Bangalore",
}

# First match ID of each season (IDs are assigned chronologically by the data source).
# 2020 playoffs were played with IDs ~1237177+, so 2021 starts later than they do.
SEASON_START_IDS = {
    2008: 335982, 2009: 392181, 2010: 419106, 2011: 501198, 2012: 548306,
    2013: 597998, 2014: 729279, 2015: 829705, 2016: 980901, 2017: 1082591,
    2018: 1136561, 2019: 1175356, 2020: 1216492, 2021: 1254000, 2022: 1304047,
}
EXPECTED_MATCHES = {2008: 58, 2009: 57, 2010: 60, 2011: 73, 2012: 74, 2013: 76, 2014: 60,
                    2015: 59, 2016: 60, 2017: 59, 2018: 60, 2019: 60, 2020: 60, 2021: 60, 2022: 74}


def canon(s: pd.Series) -> pd.Series:
    return s.replace(TEAM_MAP)


def load_balls() -> pd.DataFrame:
    """Ball-by-ball 2008-2022 with season, phase and tidy column names."""
    b = pd.read_csv(DATA / "ipl_ball_by_ball_2008_2022.csv", na_values=["NA"], keep_default_na=False)
    b = b.rename(columns={"ID": "match_id", "overs": "over", "batter": "batter",
                          "batsman_run": "batter_runs", "extras_run": "extra_runs",
                          "total_run": "total_runs", "isWicketDelivery": "is_wicket",
                          "kind": "dismissal_kind", "BattingTeam": "batting_team"})
    ids = sorted(SEASON_START_IDS.values())
    seasons = sorted(SEASON_START_IDS)
    b["season"] = pd.cut(b["match_id"], bins=ids + [10**9], labels=seasons, right=False).astype(int)
    b["batting_team"] = canon(b["batting_team"])
    b["over_no"] = b["over"] + 1                      # 1..20 (source is 0-indexed)
    b["phase"] = pd.cut(b["over"], [-1, 5, 14, 19], labels=["Powerplay (1-6)", "Middle (7-15)", "Death (16-20)"])
    b["faced"] = ~b["extra_type"].isin(["wides"])      # batter faces no-balls, not wides
    b["legal_delivery"] = ~b["extra_type"].isin(["wides", "noballs"])  # counts toward the over
    # runs charged to the bowler: not byes / leg-byes / penalty
    b["bowler_runs"] = b["total_runs"] - np.where(b["extra_type"].isin(["byes", "legbyes", "penalty"]), b["extra_runs"], 0)
    # dismissals credited to the bowler
    b["bowler_wicket"] = b["is_wicket"].eq(1) & b["dismissal_kind"].isin(
        ["caught", "bowled", "lbw", "stumped", "caught and bowled", "hit wicket"])
    return b


def check_seasons(b: pd.DataFrame) -> pd.Series:
    got = b.groupby("season")["match_id"].nunique()
    exp = pd.Series(EXPECTED_MATCHES)
    assert (got == exp).all(), f"season match counts differ:\n{pd.concat([got, exp], axis=1)}"
    return got


def load_matches() -> pd.DataFrame:
    m = pd.read_csv(DATA / "matches_2008_2017.csv", parse_dates=["date"])
    for c in ["team1", "team2", "toss_winner", "winner"]:
        m[c] = canon(m[c])
    m["venue"] = m["venue"].str.replace(r",.*$", "", regex=True)       # drop ", City" suffix
    m["venue"] = m["venue"].replace({"Punjab Cricket Association IS Bindra Stadium": "Punjab Cricket Association Stadium"})
    m["no_result"] = m["winner"].isna()
    m["toss_win_match_win"] = m["toss_winner"].eq(m["winner"])
    return m


def load_deliveries() -> pd.DataFrame:
    d = pd.read_csv(DATA / "deliveries_2008_2017.csv", encoding="utf-8-sig")
    d["batting_team"] = canon(d["batting_team"])
    d["bowling_team"] = canon(d["bowling_team"])
    return d


# ---------------------------------------------------------------- plotting helpers
import matplotlib.pyplot as plt

INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
C = {"blue": "#2a78d6", "orange": "#eb6834", "aqua": "#1baf7a", "yellow": "#eda100",
     "magenta": "#e87ba4", "violet": "#6250d6", "muted": "#b9b8b2"}
CHARTS = ROOT / "outputs" / "charts"
TABLES = ROOT / "outputs" / "tables"


def set_style():
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
        "text.color": INK, "axes.titlecolor": INK, "axes.titleweight": "bold", "axes.titlesize": 13,
        "axes.titlelocation": "left", "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
        "font.size": 10.5, "legend.frameon": False, "figure.dpi": 110, "lines.linewidth": 2,
    })


def save(fig, name):
    CHARTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHARTS / f"{name}.png", dpi=150, bbox_inches="tight")


def save_table(df, name):
    TABLES.mkdir(parents=True, exist_ok=True)
    df.to_csv(TABLES / f"{name}.csv")
