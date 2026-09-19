import streamlit as st
import pandas as pd


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
# Club data
# -------------------------

clubs = pd.DataFrame({
    "team": [
        "Man Utd",
        "Arsenal",
        "Liverpool",
        "Bournemouth",
        "Chelsea",
        "Man City",
        "Aston Villa",
        "Brentford",
        "Newcastle",
        "Brighton"
    ],

    "attacking": [
        89.5, 94.7, 84.2, 73.7, 73.7,
        100.0, 68.4, 63.2, 57.9, 52.6
    ],

    "possession": [
        63.2, 84.2, 94.7, 47.4, 89.5,
        100.0, 73.7, 42.1, 68.4, 78.9
    ],

    "chance_creation": [
        89.5, 84.2, 73.7, 78.9, 94.7,
        100.0, 36.8, 68.4, 52.6, 57.9
    ],

    "defensive_performance": [
        64.5, 52.6, 26.3, 56.6, 46.1,
        56.6, 52.6, 56.6, 27.6, 63.2
    ],

    "defensive_activity": [
        63.2, 15.8, 10.5, 73.7, 47.4,
        14.0, 28.1, 56.1, 22.8, 49.1
    ]
})


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
