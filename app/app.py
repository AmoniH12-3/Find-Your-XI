import streamlit as st
import pandas as pd
from google.cloud import bigquery


# -------------------------
# Page setup
# -------------------------

st.set_page_config(
    page_title="Find Your XI",
    page_icon="⚽",
    layout="centered"
)


# -------------------------
# Title
# -------------------------

st.title("⚽ Find Your XI")

st.subheader(
    "Which Premier League club fits how you like to watch football?"
)

st.write(
    "Answer a few questions and we'll match your preferences "
    "with Premier League club profiles."
)


# -------------------------
# Quiz
# -------------------------

st.header("Build Your Football Profile")

attacking = st.slider(
    "How important is attacking football?",
    min_value=0,
    max_value=100,
    value=50
)

possession = st.slider(
    "How important is possession?",
    min_value=0,
    max_value=100,
    value=50
)

chance_creation = st.slider(
    "How important is chance creation?",
    min_value=0,
    max_value=100,
    value=50
)

defensive_performance = st.slider(
    "How important is defensive performance?",
    min_value=0,
    max_value=100,
    value=50
)

defensive_activity = st.slider(
    "How important is defensive intensity?",
    min_value=0,
    max_value=100,
    value=50
)


# -------------------------
# BigQuery connection
# -------------------------

client = bigquery.Client(project="find-your-xi")

query = """
SELECT
    team,
    match_score,
    attacking,
    possession,
    chance_creation,
    defensive_performance,
    defensive_activity
FROM `find-your-xi.find_your_xi.club_match_reasons_clean`
ORDER BY match_score DESC
"""

clubs = client.query(query).to_dataframe()
# -------------------------
# Recommendation
# -------------------------

if st.button("Find My XI"):

    clubs["distance"] = (
        abs(clubs["attacking"] - attacking) * 0.35
        + abs(clubs["possession"] - possession) * 0.25
        + abs(clubs["chance_creation"] - chance_creation) * 0.25
        + abs(
            clubs["defensive_performance"]
            - defensive_performance
        ) * 0.10
        + abs(
            clubs["defensive_activity"]
            - defensive_activity
        ) * 0.05
    )

    clubs["match_score"] = (
        100 - clubs["distance"]
    ).round(1)

    clubs = clubs.sort_values(
        "match_score",
        ascending=False
    )

    best_match = clubs.iloc[0]

    # -------------------------
    # Result
    # -------------------------

    st.divider()

    st.header("Your Match")

    st.subheader(best_match["team"])

    st.metric(
        "Match Score",
        f'{best_match["match_score"]}%'
    )

    st.write("### Why this club?")

    st.write(
        f"Attacking profile: "
        f'{best_match["attacking"]:.1f}'
    )

    st.write(
        f"Possession profile: "
        f'{best_match["possession"]:.1f}'
    )

    st.write(
        f"Chance creation: "
        f'{best_match["chance_creation"]:.1f}'
    )

    st.write(
        f"Defensive performance: "
        f'{best_match["defensive_performance"]:.1f}'
    )

    st.write(
        f"Defensive activity: "
        f'{best_match["defensive_activity"]:.1f}'
    )

    st.divider()

    st.subheader("Other clubs that match you")

    st.dataframe(
        clubs[
            [
                "team",
                "match_score"
            ]
        ].head(5),
        hide_index=True
    )
