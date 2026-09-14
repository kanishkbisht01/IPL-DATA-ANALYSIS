<<<<<<< HEAD
# IPL-DATA-ANALYSIS
IPL matches data analysis using python, sql and power bi
=======
<img width="1536" height="1024" alt="ChatGPT Image Aug 28, 2026, 10_24_15 AM" src="https://github.com/user-attachments/assets/d7aa4674-e57f-45b5-ad83-dc85675fd4e4" />

# 🏏 IPL Analysis Dashboard | 2008–2025

An interactive **Power BI dashboard** built to analyze Indian Premier League (IPL) data from **2008 to 2025**, providing insights into team performance, player statistics, tournament records, and season-wise trends.

---

## 📊 Project Overview

The **IPL Analysis Dashboard** is an interactive sports analytics project developed using **Microsoft Power BI**. The dashboard transforms IPL match-level and ball-by-ball data into meaningful visual insights, allowing users to explore tournament performance across different seasons.

Users can select an IPL season and dynamically analyze:
* Team performance
* Match results
* Player batting and bowling performance
* Orange Cap & Purple Cap winners
* Boundary statistics
* Points tables
* Tournament-level KPIs

The primary objective of this project is to demonstrate practical skills in **data cleaning, data modeling, DAX, data visualization, and analytical storytelling** using Power BI.

---

## ⚠️ Data Quality & Validation

> **Data validation is currently in progress.**

The initial dataset used for this project contains a few inconsistencies that are being identified and corrected through data cleaning and validation.

The **dashboard architecture, data model, visualization framework, and DAX-based calculations have been developed to support dynamic analysis**. The dataset will continue to be refined to improve the accuracy and reliability of the final results.

This section is intentionally included to maintain **transparency regarding the current project status**.

---

# 🎯 Key Features & DAX Logic (With Results Explained)

Each feature is documented separately below, including its DAX code and the result it produces.

---

## 🔹 Feature 1: Season Slicer

**What it does:** When the user selects a season from the dropdown, the entire dashboard updates dynamically.

**DAX Code:**
```dax
Year = SELECTEDVALUE(ipl_matches_data[season])
```

**Result / Explanation:**
If the user selects "2024", this measure returns `2024`. All other measures use this `Year` value to filter their calculations.

---

## 🔹 Feature 2: Total 6's

**What it does:** Counts the total number of sixes hit in the selected season.

**DAX Code:**
```dax
Total 6's = 
CALCULATE(
    COUNTROWS(ball_by_ball_data),
    ball_by_ball_data[batter_runs] = 6,
    KEEPFILTERS(VALUES(ipl_matches_data[season]))
)
```

**Result / Explanation:**
* `COUNTROWS(ball_by_ball_data)` counts every delivery.
* `batter_runs = 6` filters only deliveries where 6 runs were scored.
* `KEEPFILTERS` ensures the selected season filter is preserved.

**Result:** For 2025, it returned **1296 Sixes**.

---

## 🔹 Feature 3: Total 4's

**What it does:** Counts the total number of fours hit in the selected season.

**DAX Code:**
```dax
Total 4's = 
CALCULATE(
    COUNTROWS(ball_by_ball_data),
    ball_by_ball_data[batter_runs] = 4,
    KEEPFILTERS(VALUES(ipl_matches_data[season]))
)
```

**Result / Explanation:**
* Same logic as sixes, but filters for `batter_runs = 4`.

**Result:** For 2025, it returned **2251 Fours**.

---

## 🔹 Feature 4: Total Matches

**What it does:** Counts the total number of unique matches played in the selected season.

**DAX Code:**
```dax
Total Matches = 
CALCULATE(
    DISTINCTCOUNT(ipl_matches_data[match_id])
)
```

**Result / Explanation:**
* `DISTINCTCOUNT` is used so duplicate match IDs are not counted.
* Each match has a unique ID.

**Result:** For 2025, it returned **74 Matches**.

---

## 🔹 Feature 5: Total Teams

**What it does:** Counts the total number of teams that participated in the selected season.

**DAX Code:**
```dax
Total Teams = 
CALCULATE(
    DISTINCTCOUNT(ipl_matches_data[team1])
)
```

**Result / Explanation:**
* Counts unique teams from the `team1` column.
* `DISTINCTCOUNT` removes duplicates.

**Result:** For 2025, it returned **10 Teams**.

---

## 🔹 Feature 6: Total Venues

**What it does:** Counts the total number of unique venues used in the selected season.

**DAX Code:**
```dax
Total Venues = 
CALCULATE(
    DISTINCTCOUNT(ipl_matches_data[venue])
)
```

**Result / Explanation:**
* Counts unique venues from the `venue` column.

**Result:** For 2025, it returned **14 Venues**.

---

## 🔹 Feature 7: Centuries

**What it does:** Counts how many centuries (100+ runs) were scored in the selected season.

**DAX Code:**
```dax
Centuries = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonData = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason)
VAR BatterRuns = SUMMARIZE(SeasonData, ball_by_ball_data[match_id], ball_by_ball_data[batter], "TotalRuns", SUM(ball_by_ball_data[batter_runs]))
VAR CenturyCount = FILTER(BatterRuns, [TotalRuns] >= 100)
RETURN COUNTROWS(CenturyCount)
```

**Result / Explanation:**
* `SUMMARIZE` calculates total runs per batter per match.
* `FILTER(TotalRuns >= 100)` keeps only innings with 100+ runs.
* `COUNTROWS` counts those innings.

**Result:** For 2025, it returned **9 Centuries**.

---

## 🔹 Feature 8: Half Centuries

**What it does:** Counts how many half-centuries (50–99 runs) were scored in the selected season.

**DAX Code:**
```dax
Half Centuries = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonData = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason)
VAR BatterRuns = SUMMARIZE(SeasonData, ball_by_ball_data[match_id], ball_by_ball_data[batter], "TotalRuns", SUM(ball_by_ball_data[batter_runs]))
VAR FiftyCount = FILTER(BatterRuns, [TotalRuns] >= 50 && [TotalRuns] < 100)
RETURN COUNTROWS(FiftyCount)
```

**Result / Explanation:**
* Same logic as centuries, but with the condition `50 <= TotalRuns < 100`.

**Result:** For 2025, it returned **143 Half-Centuries**.

---

## 🔹 Feature 9: Champion Team

**What it does:** Identifies the winner (champion) of the selected season.

**DAX Code:**
```dax
Champion Team = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR FinalMatchDate = CALCULATE(MAX(ipl_matches_data[match_date]), ipl_matches_data[season] = SelectedSeason)
VAR FinalMatchWinner = CALCULATE(MAX(ipl_matches_data[match_winner]), 
                                 ipl_matches_data[season] = SelectedSeason, 
                                 ipl_matches_data[match_date] = FinalMatchDate)
RETURN FinalMatchWinner
```

**Result / Explanation:**
* `MAX(match_date)` finds the final match date of the season.
* `match_winner` is extracted for that final match date.
* That team becomes the champion.

**Result:** For 2025, **Royal Challengers Bangalore** became the Champion.

---

## 🔹 Feature 10: Runner Up Team

**What it does:** Identifies the runner-up (2nd place) team of the selected season.

**DAX Code:**
```dax
Runner Up = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR FinalMatchDate = CALCULATE(MAX(ipl_matches_data[match_date]), ipl_matches_data[season] = SelectedSeason)
VAR FinalMatchWinner = CALCULATE(MAX(ipl_matches_data[match_winner]), 
                                 ipl_matches_data[season] = SelectedSeason, 
                                 ipl_matches_data[match_date] = FinalMatchDate)
VAR Team1 = CALCULATE(MAX(ipl_matches_data[team1]), 
                       ipl_matches_data[season] = SelectedSeason, 
                       ipl_matches_data[match_date] = FinalMatchDate)
VAR Team2 = CALCULATE(MAX(ipl_matches_data[team2]), 
                       ipl_matches_data[season] = SelectedSeason, 
                       ipl_matches_data[match_date] = FinalMatchDate)
RETURN IF(FinalMatchWinner = Team1, Team2, Team1)
```

**Result / Explanation:**
* Both teams from the final match are extracted (Team1 and Team2).
* The team that is not the winner is the Runner-Up.
* `IF` condition decides this.

**Result:** For 2025, **Punjab Kings** became the Runner-Up.

---
<img width="200" height="200" alt="Orange Cap" src="https://github.com/user-attachments/assets/3bff501f-644d-4610-b576-380e11fa7077" />

## 🔹 Feature 11: Orange Cap Holder

**What it does:** Identifies the top run-scorer (Orange Cap winner) of the selected season.

**DAX Code:**
```dax
Orange Cap Holder = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonDataOnly = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason)
VAR RunSummary = SUMMARIZE(SeasonDataOnly, ball_by_ball_data[batter], "Total Runs", SUM(ball_by_ball_data[batter_runs]))
VAR MaxRuns = MAXX(RunSummary, [Total Runs])
VAR TopScorer = CALCULATETABLE(VALUES(ball_by_ball_data[batter]), FILTER(RunSummary, [Total Runs] = MaxRuns))
RETURN MAXX(TopScorer, ball_by_ball_data[batter])
```

**Result / Explanation:**
* `SUMMARIZE` calculates total runs per batter.
* `MAXX` finds the highest run tally.
* `CALCULATETABLE` + `FILTER` extracts the name of that batter.

**Result:** For 2025, **B Sai Sudharsan** won the Orange Cap with **759 Runs**.

---

## 🔹 Feature 12: Orange Cap Runs

**What it does:** Displays the total runs of the Orange Cap winner.

**DAX Code:**
```dax
Orange Cap Runs = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonDataOnly = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason)
VAR RunSummary = SUMMARIZE(SeasonDataOnly, ball_by_ball_data[batter], "Total Runs", SUM(ball_by_ball_data[batter_runs]))
VAR MaxRuns = MAXX(RunSummary, [Total Runs])
RETURN MaxRuns
```

**Result / Explanation:**
* Same logic as above, but only returns `MaxRuns` (not the name).

**Result:** For 2025, it returned **759 Runs**.

---

## 🔹 Feature 13: Orange Cap Image

**What it does:** Displays the photo of the Orange Cap winner.

**DAX Code:**
```dax
Orange Cap Image = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonDataOnly = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason)
VAR RunSummary = SUMMARIZE(SeasonDataOnly, ball_by_ball_data[batter], "Total Runs", SUM(ball_by_ball_data[batter_runs]))
VAR MaxRuns = MAXX(RunSummary, [Total Runs])
VAR TopScorer = CALCULATETABLE(VALUES(ball_by_ball_data[batter]), FILTER(RunSummary, [Total Runs] = MaxRuns))
RETURN LOOKUPVALUE('players-data-updated'[player_image], 'players-data-updated'[player_name], MAXX(TopScorer, ball_by_ball_data[batter]))
```

**Result / Explanation:**
* `LOOKUPVALUE` fetches the player's image URL using their name.
* That image is displayed on the dashboard.

**Result:** For 2025, **B Sai Sudharsan's photo** is displayed.

---

## 🔹 Feature 14: Orange Cap Team Name

**What it does:** Displays the team name of the Orange Cap winner.

**DAX Code:**
```dax
Orange Cap Team Name = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonDataOnly = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason)
VAR RunSummary = SUMMARIZE(SeasonDataOnly, ball_by_ball_data[batter], "Total Runs", SUM(ball_by_ball_data[batter_runs]))
VAR MaxRuns = MAXX(RunSummary, [Total Runs])
VAR TopScorer = CALCULATETABLE(VALUES(ball_by_ball_data[batter]), FILTER(RunSummary, [Total Runs] = MaxRuns))
VAR FullTeamName = CALCULATE(MAX(ball_by_ball_data[team_batting]), 
                              FILTER(SeasonDataOnly, ball_by_ball_data[batter] = MAXX(TopScorer, ball_by_ball_data[batter])))
RETURN FullTeamName
```

**Result / Explanation:**
* Fetches the top scorer's `team_batting` value.

**Result:** For 2025, **Gujarat Titans**.

---
<img width="200" height="200" alt="Purple Cap" src="https://github.com/user-attachments/assets/568ceffc-c326-4c93-8ca5-b3bfc1dbeb7c" />

## 🔹 Feature 15: Purple Cap Holder

**What it does:** Identifies the top wicket-taker (Purple Cap winner) of the selected season. It excludes dismissals like run-outs and retired hurt to ensure only bowler wickets are counted.

**DAX Code:**
```dax
PurpleCapHolder = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonWickets = 
    FILTER(
        ball_by_ball_data,
        RELATED(ipl_matches_data[season]) = SelectedSeason &&
        ball_by_ball_data[is_wicket] = TRUE() &&
        NOT ball_by_ball_data[wicket_kind] IN {"run out","retired hurt","obstructing the field","retired out"}
    )
VAR WicketSummary = 
    SUMMARIZE(
        SeasonWickets,
        ball_by_ball_data[bowler],
        "wicket count", COUNTROWS(FILTER(SeasonWickets, ball_by_ball_data[bowler] = EARLIER(ball_by_ball_data[bowler])))
    )
VAR MaxWickets = MAXX(WicketSummary, [wicket count])
VAR TopBowler = CALCULATETABLE(VALUES(ball_by_ball_data[bowler]), FILTER(WicketSummary, [wicket count] = MaxWickets))
RETURN MAXX(TopBowler, ball_by_ball_data[bowler])
```

**Result / Explanation:**
* `FILTER` keeps only deliveries where `is_wicket = TRUE` and the wicket kind is valid (excludes run-out, retired hurt).
* `SUMMARIZE` counts total valid wickets per bowler.
* `MAXX` finds the highest wicket count.

**Result:** For 2025, **M Prasidh Krishna** won the Purple Cap with **25 Wickets**.

---

## 🔹 Feature 16: Purple Cap Wicket Count

**What it does:** Displays the total valid wickets of the Purple Cap winner.

**DAX Code:**
```dax
PurpleCapWicketCount = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonWickets = 
    FILTER(
        ball_by_ball_data,
        RELATED(ipl_matches_data[season]) = SelectedSeason &&
        ball_by_ball_data[is_wicket] = TRUE() &&
        NOT ball_by_ball_data[wicket_kind] IN {"run out","retired hurt","retired out","obstructing the field"}
    )
VAR WicketSummary = SUMMARIZE(SeasonWickets, ball_by_ball_data[bowler], "wicket count", COUNTROWS(FILTER(SeasonWickets, ball_by_ball_data[bowler] = EARLIER(ball_by_ball_data[bowler]))))
VAR MaxWickets = MAXX(WicketSummary, [wicket count])
RETURN MaxWickets
```

**Result / Explanation:**
* Same logic, but only returns `MaxWickets`.

**Result:** For 2025, it returned **25 Wickets**.

---

## 🔹 Feature 17: Purple Cap Image

**What it does:** Displays the photo of the Purple Cap winner.

**DAX Code:**
```dax
PurpleCapImage = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonWickets = 
    FILTER(
        ball_by_ball_data,
        RELATED(ipl_matches_data[season]) = SelectedSeason &&
        ball_by_ball_data[is_wicket] = TRUE() &&
        NOT ball_by_ball_data[wicket_kind] IN {"run out","retired hurt","obstructing the field","retired out"}
    )
VAR WicketSummary = SUMMARIZE(SeasonWickets, ball_by_ball_data[bowler], "wicket count", COUNTROWS(FILTER(SeasonWickets, ball_by_ball_data[bowler] = EARLIER(ball_by_ball_data[bowler]))))
VAR MaxWickets = MAXX(WicketSummary, [wicket count])
VAR TopBowler = CALCULATETABLE(VALUES(ball_by_ball_data[bowler]), FILTER(WicketSummary, [wicket count] = MaxWickets))
RETURN LOOKUPVALUE('players-data-updated'[player_image], 'players-data-updated'[player_name], MAXX(TopBowler, ball_by_ball_data[bowler]))
```

**Result / Explanation:**
* `LOOKUPVALUE` fetches the bowler's image URL using their name.

**Result:** For 2025, **M Prasidh Krishna's photo**.

---

## 🔹 Feature 18: Purple Cap Team Name

**What it does:** Displays the team name of the Purple Cap winner.

**DAX Code:**
```dax
PurpleCapTeam = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonWickets = 
    FILTER(
        ball_by_ball_data,
        RELATED(ipl_matches_data[season]) = SelectedSeason &&
        ball_by_ball_data[is_wicket] = TRUE() &&
        NOT ball_by_ball_data[wicket_kind] IN {"run out","retired hurt","obstructing the field","retired out"}
    )
VAR WicketSummary = 
    ADDCOLUMNS(
        SUMMARIZE(SeasonWickets, ball_by_ball_data[bowler], ball_by_ball_data[team_bowling]),
        "wicket count", COUNTROWS(FILTER(SeasonWickets, ball_by_ball_data[bowler] = EARLIER(ball_by_ball_data[bowler])))
    )
VAR MaxWickets = MAXX(WicketSummary, [wicket count])
RETURN MAXX(WicketSummary, IF([wicket count] = MaxWickets, ball_by_ball_data[team_bowling]))
```

**Result / Explanation:**
* `ADDCOLUMNS` keeps the bowler's `team_bowling` alongside the wicket count.
* Returns the team of the bowler with maximum wickets.

**Result:** For 2025, **Gujarat Titans**.

---

## 🔹 Feature 19: Top Fours Count

**What it does:** Displays the count of the player who hit the most fours in the selected season.

**DAX Code:**
```dax
Top Fours Count = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonFours = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason && ball_by_ball_data[batter_runs] = 4)
VAR FourSummary = SUMMARIZE(SeasonFours, ball_by_ball_data[batter], "FoursCount", COUNTROWS(FILTER(SeasonFours, ball_by_ball_data[batter] = EARLIER(ball_by_ball_data[batter]))))
VAR MaxFours = MAXX(FourSummary, [FoursCount])
RETURN MaxFours
```

**Result / Explanation:**
* Filters only 4-run deliveries.
* Counts them per batter.
* Returns the highest count.

**Result:** For 2025, it returned **88 Fours**.

---

## 🔹 Feature 20: Top Fours Player Name

**What it does:** Displays the name of the player who hit the most fours.

**DAX Code:**
```dax
Top Fours Player Name = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonFours = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason && ball_by_ball_data[batter_runs] = 4)
VAR FourSummary = SUMMARIZE(SeasonFours, ball_by_ball_data[batter], "FoursCount", COUNTROWS(FILTER(SeasonFours, ball_by_ball_data[batter] = EARLIER(ball_by_ball_data[batter]))))
VAR MaxFours = MAXX(FourSummary, [FoursCount])
VAR TopFoursPlayer = CALCULATETABLE(VALUES(ball_by_ball_data[batter]), FILTER(FourSummary, [FoursCount] = MaxFours))
RETURN MAXX(TopFoursPlayer, ball_by_ball_data[batter])
```

**Result / Explanation:**
* Returns the name of the batter with the maximum fours.

**Result:** For 2025, **B Sai Sudharsan**.

---

## 🔹 Feature 21: Top Fours Player Image

**What it does:** Displays the photo of the player who hit the most fours.

**DAX Code:**
```dax
Top Fours Player Image = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonFours = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason && ball_by_ball_data[batter_runs] = 4)
VAR FourSummary = SUMMARIZE(SeasonFours, ball_by_ball_data[batter], "FoursCount", COUNTROWS(FILTER(SeasonFours, ball_by_ball_data[batter] = EARLIER(ball_by_ball_data[batter]))))
VAR MaxFours = MAXX(FourSummary, [FoursCount])
VAR TopFoursPlayer = CALCULATETABLE(VALUES(ball_by_ball_data[batter]), FILTER(FourSummary, [FoursCount] = MaxFours))
RETURN LOOKUPVALUE('players-data-updated'[player_image], 'players-data-updated'[player_name], MAXX(TopFoursPlayer, ball_by_ball_data[batter]))
```

**Result / Explanation:**
* Uses `LOOKUPVALUE` to fetch the player's image.

**Result:** For 2025, **B Sai Sudharsan's photo**.

---

## 🔹 Feature 22: Top Fours Player Team Name

**What it does:** Displays the team of the player who hit the most fours.

**DAX Code:**
```dax
Top Fours Player Team Name = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonFours = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason && ball_by_ball_data[batter_runs] = 4)
VAR FourSummary = SUMMARIZE(SeasonFours, ball_by_ball_data[batter], "FoursCount", COUNTROWS(FILTER(SeasonFours, ball_by_ball_data[batter] = EARLIER(ball_by_ball_data[batter]))))
VAR MaxFours = MAXX(FourSummary, [FoursCount])
VAR TopFoursPlayer = CALCULATETABLE(VALUES(ball_by_ball_data[batter]), FILTER(FourSummary, [FoursCount] = MaxFours))
VAR BatterTeamName = CALCULATE(MAX(ball_by_ball_data[team_batting]), FILTER(SeasonFours, ball_by_ball_data[batter] = MAXX(TopFoursPlayer, ball_by_ball_data[batter])))
RETURN BatterTeamName
```

**Result / Explanation:**
* Fetches the `team_batting` value of the top fours player.

**Result:** For 2025, **Gujarat Titans**.

---

## 🔹 Feature 23: Six Count (Top Sixes Count)

**What it does:** Displays the count of the player who hit the most sixes in the selected season.

**DAX Code:**
```dax
Six Count = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonSix = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason && ball_by_ball_data[batter_runs] = 6)
VAR SixSummary = SUMMARIZE(SeasonSix, ball_by_ball_data[batter], "SixCount", COUNTROWS(FILTER(SeasonSix, ball_by_ball_data[batter] = EARLIER(ball_by_ball_data[batter]))))
VAR MaxSix = MAXX(SixSummary, [SixCount])
RETURN MaxSix
```

**Result / Explanation:**
* Filters only 6-run deliveries.
* Counts them per batter.
* Returns the highest count.

**Result:** For 2025, it returned **40 Sixes**.

---

## 🔹 Feature 24: Top Six Player Name

**What it does:** Displays the name of the player who hit the most sixes.

**DAX Code:**
```dax
Top Six Player Name = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonSix = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason && ball_by_ball_data[batter_runs] = 6)
VAR SixSummary = SUMMARIZE(SeasonSix, ball_by_ball_data[batter], "SixCount", COUNTROWS(FILTER(SeasonSix, ball_by_ball_data[batter] = EARLIER(ball_by_ball_data[batter]))))
VAR MaxSix = MAXX(SixSummary, [SixCount])
VAR TopSixPlayer = CALCULATETABLE(VALUES(ball_by_ball_data[batter]), FILTER(SixSummary, [SixCount] = MaxSix))
RETURN MAXX(TopSixPlayer, ball_by_ball_data[batter])
```

**Result / Explanation:**
* Returns the name of the batter with the maximum sixes.

**Result:** For 2025, **N Pooran**.

---

## 🔹 Feature 25: Top Six Player Image

**What it does:** Displays the photo of the player who hit the most sixes.

**DAX Code:**
```dax
Top Six Player Image = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonSix = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason && ball_by_ball_data[batter_runs] = 6)
VAR SixSummary = SUMMARIZE(SeasonSix, ball_by_ball_data[batter], "SixCount", COUNTROWS(FILTER(SeasonSix, ball_by_ball_data[batter] = EARLIER(ball_by_ball_data[batter]))))
VAR MaxSix = MAXX(SixSummary, [SixCount])
VAR TopSixPlayer = CALCULATETABLE(VALUES(ball_by_ball_data[batter]), FILTER(SixSummary, [SixCount] = MaxSix))
RETURN LOOKUPVALUE('players-data-updated'[player_image], 'players-data-updated'[player_name], MAXX(TopSixPlayer, ball_by_ball_data[batter]))
```

**Result / Explanation:**
* Uses `LOOKUPVALUE` to fetch the player's image.

**Result:** For 2025, **N Pooran's photo**.

---

## 🔹 Feature 26: Top Six Player Team Name

**What it does:** Displays the team of the player who hit the most sixes.

**DAX Code:**
```dax
Top Six Player Team Name = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR SeasonSix = FILTER(ball_by_ball_data, RELATED(ipl_matches_data[season]) = SelectedSeason && ball_by_ball_data[batter_runs] = 6)
VAR SixSummary = SUMMARIZE(SeasonSix, ball_by_ball_data[batter], "SixCount", COUNTROWS(FILTER(SeasonSix, ball_by_ball_data[batter] = EARLIER(ball_by_ball_data[batter]))))
VAR MaxSix = MAXX(SixSummary, [SixCount])
VAR TopSixPlayer = CALCULATETABLE(VALUES(ball_by_ball_data[batter]), FILTER(SixSummary, [SixCount] = MaxSix))
VAR BatterTeamName = CALCULATE(MAX(ball_by_ball_data[team_batting]), FILTER(SeasonSix, ball_by_ball_data[batter] = MAXX(TopSixPlayer, ball_by_ball_data[batter])))
RETURN BatterTeamName
```

**Result / Explanation:**
* Fetches the `team_batting` value of the top sixes player.

**Result:** For 2025, **Lucknow Super Giants**.

---

## 🔹 Feature 27: Matches Played (Points Table)

**What it does:** Counts how many matches each team played in the selected season.

**DAX Code:**
```dax
Matches Played = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR Team1matchesCount = CALCULATE(COUNTROWS(ipl_matches_data), 
                                   USERELATIONSHIP(ipl_matches_data[team1], teams_data[team_name]), 
                                   ipl_matches_data[season] = SelectedSeason, 
                                   ipl_matches_data[match_type] = "T20")
VAR Team2matchesCount = CALCULATE(COUNTROWS(ipl_matches_data), 
                                   USERELATIONSHIP(ipl_matches_data[team2], teams_data[team_name]), 
                                   ipl_matches_data[season] = SelectedSeason, 
                                   ipl_matches_data[match_type] = "T20")
RETURN Team1matchesCount + Team2matchesCount
```

**Result / Explanation:**
* `USERELATIONSHIP` activates both team1 and team2 relationships.
* Counts matches for Team1 and Team2, then adds them.

**Result:** For 2025, each team played **14 Matches**.

---

## 🔹 Feature 28: Matches Won (Points Table)

**What it does:** Counts how many matches each team won in the selected season.

**DAX Code:**
```dax
Matches Won = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR CurrentTeam = SELECTEDVALUE(teams_data[team_name])
RETURN CALCULATE(COUNTROWS(ipl_matches_data), 
                 ipl_matches_data[season] = SelectedSeason, 
                 ipl_matches_data[match_winner] = CurrentTeam, 
                 ipl_matches_data[match_type] = "T20", 
                 ipl_matches_data[stage] = "")
```

**Result / Explanation:**
* Filters `match_winner` for the current team.
* Counts only league-stage matches.

**Result:** For 2025, Punjab Kings won **9 Matches**.

---

## 🔹 Feature 29: Lost Matches (Points Table)

**What it does:** Counts how many matches each team lost in the selected season.

**DAX Code:**
```dax
Lost Matches = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR Team1Lost = CALCULATE(COUNTROWS(ipl_matches_data), 
                          USERELATIONSHIP(ipl_matches_data[team1], teams_data[team_name]), 
                          ipl_matches_data[season] = SelectedSeason, 
                          ipl_matches_data[match_type] = "T20", 
                          NOT ISBLANK(ipl_matches_data[match_winner]), 
                          ipl_matches_data[match_winner] <> ipl_matches_data[team1], 
                          ipl_matches_data[stage] = "")
VAR Team2Lost = CALCULATE(COUNTROWS(ipl_matches_data), 
                          USERELATIONSHIP(ipl_matches_data[team2], teams_data[team_name]), 
                          ipl_matches_data[season] = SelectedSeason, 
                          ipl_matches_data[match_type] = "T20", 
                          NOT ISBLANK(ipl_matches_data[match_winner]), 
                          ipl_matches_data[match_winner] <> ipl_matches_data[team1], 
                          ipl_matches_data[stage] = "")
RETURN Team1Lost + Team2Lost
```

**Result / Explanation:**
* Counts matches where the team played but was not the winner.
* Excludes No Result matches.

**Result:** For 2025, Punjab Kings lost **8 Matches** (1 match was No Result).

---

## 🔹 Feature 30: No Result Played (Points Table)

**What it does:** Counts how many matches ended in "No Result" for each team.

**DAX Code:**
```dax
No Result Played = 
VAR SelectedSeason = SELECTEDVALUE(ipl_matches_data[season])
VAR Team1matchesCount = CALCULATE(COUNTROWS(ipl_matches_data), 
                                   USERELATIONSHIP(ipl_matches_data[team1], teams_data[team_name]), 
                                   ipl_matches_data[season] = SelectedSeason, 
                                   ipl_matches_data[match_type] = "T20", 
                                   ipl_matches_data[result] = "no result")
VAR Team2matchesCount = CALCULATE(COUNTROWS(ipl_matches_data), 
                                   USERELATIONSHIP(ipl_matches_data[team2], teams_data[team_name]), 
                                   ipl_matches_data[season] = SelectedSeason, 
                                   ipl_matches_data[match_type] = "T20", 
                                   ipl_matches_data[result] = "no result")
RETURN Team1matchesCount + Team2matchesCount
```

**Result / Explanation:**
* Filters only matches where `result = "no result"`.
* Counts them for both team1 and team2.

**Result:** For 2025, Punjab Kings had **1 No Result** match.

---

## 🔹 Feature 31: Total Points (Points Table)

**What it does:** Calculates the total points for each team.

**DAX Code:**
```dax
Total Points = 
VAR Win = [Matches Won]
VAR NR = [No Result Played]
RETURN (Win * 2) + NR
```

**Result / Explanation:**
* Points = (Wins × 2) + No Results.
* This follows standard IPL points system.

**Result:** For 2025, Punjab Kings got **19 Points** (9×2 + 1 = 19).

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Microsoft Power BI** | Dashboard & Data Visualization |
| **DAX** | Measures & Analytical Calculations |
| **Power Query** | Data Cleaning & Transformation |
| **Excel / CSV** | Data Sources |
| **Data Modeling** | Relationships & Analytical Structure |

---

## 📂 Data Sources

The project is based on IPL:
* Match-level data
* Ball-by-ball data
* Player statistics
* Team information
* Venue information
* Season information

The dataset is currently undergoing additional **data validation and cleaning**.

---

## 🔄 Data Preparation Workflow

```text
Raw IPL Data
     ↓
Data Cleaning
     ↓
Data Transformation
     ↓
Data Validation
     ↓
Data Modeling
     ↓
DAX Measures
     ↓
Interactive Power BI Dashboard
     ↓
Insights & Analysis
```

---

## 📈 Analytical Skills Demonstrated

This project demonstrates practical knowledge of:
* Data Cleaning
* Data Transformation
* Data Modeling
* DAX
* KPI Development
* Dynamic Filtering
* Conditional Calculations
* Aggregations
>>>>>>> d27a41fb5cd8d4dcec31fb8e4f21940a432775de
