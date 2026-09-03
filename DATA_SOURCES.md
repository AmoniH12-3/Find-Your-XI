# Find Your XI — Data Sources

## Purpose

This document records the data sources used by Find Your XI,
their intended purpose, and relevant usage/licensing considerations.

---

## Initial Data Sources

### Football-Data.co.uk

Website:
https://www.football-data.co.uk/

Purpose:

- Premier League match results
- Match statistics
- Historical season data
- Team performance analysis

Initial use:

Football-Data.co.uk will be evaluated as an initial data source
for developing the SQL foundation of Find Your XI.

Important:

Raw source files will not automatically be committed to this
repository. The project will document the source and provide
instructions for obtaining the data where appropriate.

---

### StatsBomb Open Data

Repository:
https://github.com/statsbomb/open-data

Purpose:

- Match event data
- Player events
- Lineups
- Advanced football analysis
- Future player/team analytics

Initial use:

StatsBomb Open Data will be evaluated for future versions of
Find Your XI requiring deeper event-level analysis.

Attribution requirements will be followed when applicable.

---

## Data Principles

Find Your XI will prioritize:

1. Transparent data sourcing
2. Proper attribution
3. Respect for data licenses and terms
4. Reproducible data pipelines
5. Data quality and validation
6. Clear documentation of limitations

---

## Current Status

Phase 1 — SQL Foundation

Data source research complete.

Next step:

Select and load the initial Premier League dataset into a
SQL environment.
