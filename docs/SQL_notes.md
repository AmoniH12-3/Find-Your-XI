Find Your XI — SQL Notes

Purpose

This document is a running set of SQL notes based on the work completed while building Find Your XI.

The goal is to understand not only what each SQL concept does, but how it is being used in a real sports analytics project.

1. SELECT

SELECT determines which columns we want to retrieve.

SELECT
  team,
  goals_for,
  goals_against
FROM `find-your-xi.find_your_xi.matches`;

Find Your XI use

We use SELECT throughout the project to choose the fields needed for match analysis, team statistics, Team DNA, club preference profiles, and recommendations.

Key idea: SELECT answers: "What information do I want to see?"

2. FROM

FROM tells SQL where the data is coming from.

SELECT *
FROM `find-your-xi.find_your_xi.matches`;

Our main tables live inside the BigQuery dataset:

find-your-xi.find_your_xi

Key idea: FROM answers: "Which table am I querying?"

3. GROUP BY

GROUP BY combines rows into groups so aggregate calculations can be performed for each group.

SELECT
  team,
  COUNT(*) AS matches_played
FROM `find-your-xi.find_your_xi.matches`
GROUP BY team;

We used GROUP BY team to turn match-level data into team-level statistics.

Individual match rows
        ↓
Team-level statistics

Key idea: GROUP BY answers: "For what groups do I want to calculate these numbers?"

4. COUNT

COUNT counts rows or values.

COUNT(*) AS matches_played

We used it to calculate how many matches each team played.

For the 2025/26 Premier League season:

20 teams × 38 matches = 760 team-match rows

Each real match appears twice in our team-oriented matches table: once from the home team's perspective and once from the away team's perspective.

5. COUNTIF

COUNTIF counts rows that satisfy a condition.

COUNTIF(goals_for > goals_against) AS wins
COUNTIF(goals_for = goals_against) AS draws
COUNTIF(goals_for < goals_against) AS losses

We used this to build a league-style team record directly from match data.

6. SUM

SUM adds values together.

SUM(goals_for) AS goals_for

We used it for total goals scored, total goals conceded, and goal difference:

SUM(goals_for) - SUM(goals_against) AS goal_difference

7. AVG

AVG calculates an average.

AVG(xg_for) AS avg_xg

We used averages to create team profiles from match-level statistics, including average xG, shots, shots on target, possession, tackles won, interceptions, blocks, and clearances.

This converts raw match statistics into a profile describing how a team generally played across the season.

8. JOIN

A JOIN combines information from different tables.

Our match data contained team codes, while the team reference table contained team names.

LEFT JOIN `find-your-xi.find_your_xi.teams_raw` AS home_team
  ON m.home_team = home_team.code

This allowed us to turn a team code such as:

home_team = 39

into a team name.

Important lesson

We initially joined against the wrong column. The correct relationship was:

matches_raw.home_team
        ↓
teams_raw.code

Before joining tables, understand what the key actually represents.

9. LEFT JOIN

A LEFT JOIN keeps every row from the table on the left, even if a matching row cannot be found on the right.

FROM matches_raw AS m
LEFT JOIN teams_raw AS home_team
  ON m.home_team = home_team.code

We used LEFT JOIN when attaching team information to match records.

Our validation eventually showed:

Missing team names: 0
Missing opponents: 0

10. UNION ALL

UNION ALL combines the results of multiple queries.

A Premier League match naturally has two perspectives.

Example:

Arsenal 2–1 Chelsea

We wanted:

Arsenal → Chelsea | Home
Chelsea → Arsenal | Away

So we created one query for home teams and one for away teams and combined them using UNION ALL.

This transformed:

380 matches

into:

760 team-match rows

Key idea: UNION ALL is useful when you want to stack datasets vertically.

11. Common Table Expressions (CTEs)

A CTE is a temporary named result set created with WITH.

WITH team_stats AS (
  SELECT
    team,
    COUNT(*) AS matches_played,
    AVG(xg_for) AS avg_xg
  FROM `find-your-xi.find_your_xi.matches`
  GROUP BY team
)

SELECT *
FROM team_stats;

We used CTEs to break complicated calculations into logical stages.

Raw team statistics
        ↓
Ranked statistics
        ↓
Final Team DNA scores

CTEs let us build logic in steps instead of writing one enormous SQL statement.

12. Window Functions

Window functions calculate values across related rows without collapsing those rows into one row per group.

Example:

PERCENT_RANK() OVER (
  ORDER BY goals_per_match
)

We used window functions to compare clubs against one another while retaining the individual club rows.

13. PERCENT_RANK

PERCENT_RANK() calculates the relative rank of a value within a dataset.

PERCENT_RANK() OVER (
  ORDER BY avg_possession
)

We then multiplied the result by 100 to create comparable 0–100-style scores.

We used this approach for:

Attack

Chance creation

Possession

Defensive performance

Defensive activity

Important caveat

A percentile score is relative to the clubs in the dataset.

It does not mean that a club performs at that percentage level in an absolute sense.

14. CASE / Conditional Logic

Conditional logic allows SQL to return different results depending on a condition.

CASE
  WHEN goals_for > goals_against THEN 'Win'
  WHEN goals_for = goals_against THEN 'Draw'
  ELSE 'Loss'
END AS result

We currently use COUNTIF for win/draw/loss calculations, but CASE is another way to explicitly label match outcomes and will be useful as the project becomes more advanced.

15. CROSS JOIN

A CROSS JOIN combines every row from one table with every row from another table.

We used it to compare one quiz response against every club profile.

Conceptually:

