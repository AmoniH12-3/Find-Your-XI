# Find Your XI — SQL Notes

## Purpose

This document is a running set of SQL notes based on the work completed while building **Find Your XI**.

The goal is to understand not only what each SQL concept does, but how it is being used in a real sports analytics project.

---

## 1. SELECT

`SELECT` determines which columns we want to retrieve.

```sql
SELECT
  team,
  goals_for,
  goals_against
FROM `find-your-xi.find_your_xi.matches`;
```

### Find Your XI use

We use `SELECT` throughout the project to choose the fields needed for match analysis, team statistics, Team DNA, club preference profiles, and recommendations.

**Key idea:** `SELECT` answers: "What information do I want to see?"

---

## 2. FROM

`FROM` tells SQL where the data is coming from.

```sql
SELECT *
FROM `find-your-xi.find_your_xi.matches`;
```

Our main tables live inside the BigQuery dataset:

```text
find-your-xi.find_your_xi
```

**Key idea:** `FROM` answers: "Which table am I querying?"

---

## 3. GROUP BY

`GROUP BY` combines rows into groups so aggregate calculations can be performed for each group.

```sql
SELECT
  team,
  COUNT(*) AS matches_played
FROM `find-your-xi.find_your_xi.matches`
GROUP BY team;
```

We used `GROUP BY team` to turn match-level data into team-level statistics.

```text
Individual match rows
        ↓
Team-level statistics
```

**Key idea:** `GROUP BY` answers: "For what groups do I want to calculate these numbers?"

---

## 4. COUNT

`COUNT` counts rows or values.

```sql
COUNT(*) AS matches_played
```

We used it to calculate how many matches each team played.

For the 2025/26 Premier League season:

```text
20 teams × 38 matches = 760 team-match rows
```

Each real match appears twice in our team-oriented `matches` table: once from the home team's perspective and once from the away team's perspective.

---

## 5. COUNTIF

`COUNTIF` counts rows that satisfy a condition.

```sql
COUNTIF(goals_for > goals_against) AS wins
COUNTIF(goals_for = goals_against) AS draws
COUNTIF(goals_for < goals_against) AS losses
```

We used this to build a league-style team record directly from match data.

---

## 6. SUM

`SUM` adds values together.

```sql
SUM(goals_for) AS goals_for
```

We used it for total goals scored, total goals conceded, and goal difference:

```sql
SUM(goals_for) - SUM(goals_against) AS goal_difference
```

---

## 7. AVG

`AVG` calculates an average.

```sql
AVG(xg_for) AS avg_xg
```

We used averages to create team profiles from match-level statistics, including average xG, shots, shots on target, possession, tackles won, interceptions, blocks, and clearances.

This converts raw match statistics into a profile describing how a team generally played across the season.

---

## 8. JOIN

A `JOIN` combines information from different tables.

Our match data contained team codes, while the team reference table contained team names.

```sql
LEFT JOIN `find-your-xi.find_your_xi.teams_raw` AS home_team
  ON m.home_team = home_team.code
```

This allowed us to turn a team code such as:

```text
home_team = 39
```

into a team name.

### Important lesson

We initially joined against the wrong column. The correct relationship was:

```text
matches_raw.home_team
        ↓
teams_raw.code
```

Before joining tables, understand what the key actually represents.

---

## 9. LEFT JOIN

A `LEFT JOIN` keeps every row from the table on the left, even if a matching row cannot be found on the right.

```sql
FROM matches_raw AS m
LEFT JOIN teams_raw AS home_team
  ON m.home_team = home_team.code
```

We used `LEFT JOIN` when attaching team information to match records.

Our validation eventually showed:

```text
Missing team names: 0
Missing opponents: 0
```

---

## 10. UNION ALL

`UNION ALL` combines the results of multiple queries.

A Premier League match naturally has two perspectives.

Example:

```text
Arsenal 2–1 Chelsea
```

We wanted:

```text
Arsenal → Chelsea | Home
Chelsea → Arsenal | Away
```

So we created one query for home teams and one for away teams and combined them using `UNION ALL`.

This transformed:

```text
380 matches
```

into:

```text
760 team-match rows
```

**Key idea:** `UNION ALL` is useful when you want to stack datasets vertically.

---

## 11. Common Table Expressions (CTEs)

A CTE is a temporary named result set created with `WITH`.

```sql
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
```

We used CTEs to break complicated calculations into logical stages.

```text
Raw team statistics
        ↓
Ranked statistics
        ↓
Final Team DNA scores
```

CTEs let us build logic in steps instead of writing one enormous SQL statement.

---

## 12. Window Functions

Window functions calculate values across related rows without collapsing those rows into one row per group.

Example:

```sql
PERCENT_RANK() OVER (
  ORDER BY goals_per_match
)
```

We used window functions to compare clubs against one another while retaining the individual club rows.

---

## 13. PERCENT_RANK

`PERCENT_RANK()` calculates the relative rank of a value within a dataset.

```sql
PERCENT_RANK() OVER (
  ORDER BY avg_possession
)
```

We then multiplied the result by 100 to create comparable 0–100-style scores.

We used this approach for:

- Attack
- Chance creation
- Possession
- Defensive performance
- Defensive activity

### Important caveat

A percentile score is relative to the clubs in the dataset.

It does **not** mean that a club performs at that percentage level in an absolute sense.

---

## 14. CASE / Conditional Logic

Conditional logic allows SQL to return different results depending on a condition.

```sql
CASE
  WHEN goals_for > goals_against THEN 'Win'
  WHEN goals_for = goals_against THEN 'Draw'
  ELSE 'Loss'
END AS result
```

We currently use `COUNTIF` for win/draw/loss calculations, but `CASE` is another way to explicitly label match outcomes and will be useful as the project becomes more advanced.

---

## 15. CROSS JOIN

A `CROSS JOIN` combines every row from one table with every row from another table.

We used it to compare one quiz response against every club profile.

Conceptually:

```text
1 user preference profile
        ×
20 club profiles
        ↓
20 club comparisons
```

Example:

```sql
FROM club_preferences AS c
CROSS JOIN quiz_responses AS q
```

This allowed us to calculate the distance between the user's preferences and every Premier League club.

---

## 16. ABS

`ABS()` returns the absolute value of a number.

```sql
ABS(club_attacking - user_attacking)
```

If the club is 90 and the user is 75:

```text
ABS(90 - 75) = 15
```

If the numbers are reversed:

```text
ABS(75 - 90) = 15
```

We use this as the foundation of the club-matching algorithm because we care about the size of the difference, not whether the club is above or below the user's preference.

---

## 17. Weighted Scoring

The recommendation algorithm gives different importance to different preferences.

Current weights:

```text
Attacking football       35%
Possession                25%
Chance creation           25%
Defensive performance     10%
Defensive activity         5%
```

The algorithm calculates:

```text
difference × weight
```

for each category and adds the results together.

Not every preference needs to matter equally. The weights allow the matching model to reflect that.

---

## 18. Match Distance

The project calculates a `preference_distance`.

Conceptually:

```text
smaller distance = closer to the user's preferences
larger distance = farther from the user's preferences
```

Example:

```text
Man Utd      6.9
Arsenal      7.7
Liverpool   13.6
```

The app then converts the distance into the current prototype's match score:

```python
100 - distance
```

### Important caveat

The resulting number is a **prototype matching score**, not a probability.

A score of 93.1 does not mean there is a 93.1% chance the user will like that club. It represents how closely the club profile matches the current scoring model.

---

## 19. Data Validation

Data validation checks whether the data behaves as expected.

After creating the `matches` table, we checked:

```text
760 total rows
380 unique matches
20 teams
0 missing team names
0 missing opponents
```

This matters because SQL can successfully execute while still producing incorrect results.

**Key lesson:**

> A query running without an error does not mean the data is correct.

---

## 20. SQL → Python → Streamlit

The project now uses SQL and Python together.

Current architecture:

```text
Premier League data
        ↓
BigQuery
        ↓
SQL transformations
        ↓
Club preference profiles
        ↓
Python
        ↓
Streamlit
        ↓
Interactive Find Your XI quiz
```

Python connects to BigQuery using:

```python
from google.cloud import bigquery

client = bigquery.Client(project="find-your-xi")
```

The app retrieves club profiles with SQL and then applies the user's slider preferences.

---

## 21. What I Learned Building This

### SQL concepts practiced

- SELECT
- FROM
- GROUP BY
- COUNT
- COUNTIF
- SUM
- AVG
- JOIN
- LEFT JOIN
- UNION ALL
- CTEs
- Window functions
- PERCENT_RANK
- CROSS JOIN
- ABS
- Conditional logic
- Data validation

### Data engineering concepts practiced

- Loading raw data
- Working with a warehouse
- Understanding table relationships
- Identifying join keys
- Transforming raw data into analytical tables
- Validating transformed data
- Separating raw and transformed data
- Connecting an application to a data warehouse

### Important lesson

The goal of Find Your XI is not just to produce a recommendation.

The project is being used as a practical environment for learning how data moves from:

```text
Raw data
   ↓
Structured data
   ↓
Analytics
   ↓
Application
```

---

## 22. Next Concepts to Learn

As Find Your XI grows, the next concepts will include:

- Python data pipelines
- API ingestion
- Data cleaning
- Data modeling
- dbt
- ETL / ELT
- Automated pipelines
- Data quality tests
- More advanced player analytics
- Season-aware data models
- Application architecture
- Deployment

The project should introduce these technologies gradually rather than adding tools without a practical reason.
