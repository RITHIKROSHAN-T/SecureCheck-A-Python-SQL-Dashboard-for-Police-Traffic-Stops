import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# phase 1

# --- PAGE CONFIG ---
st.set_page_config(page_title="SecureCheck Dashboard", layout="wide")

# --- TITLE ---
st.title("🚓 SecureCheck: Police Post Monitoring Dashboard")

# --- CONNECT TO POSTGRES ---
db_url = "postgresql://rithik23:fyDw5Z9Byz5k9vuhptiECMGLWARPTFlA@dpg-d1e4cp6mcj7s73b215v0-a.singapore-postgres.render.com/rithik_rnrt"
engine = create_engine(db_url)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    query = "SELECT * FROM traffic_stop"
    df = pd.read_sql(query, engine)
    return df

traffic_df = load_data()

# --- SHOW FULL DATA ---
st.subheader("🧾 Full Traffic Stop Dataset")
st.dataframe(traffic_df, use_container_width=True)

# phase 2

# --- KEY METRICS SECTION ---
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Police Stops", len(traffic_df))

with col2:
    total_arrests = traffic_df[traffic_df['stop_outcome'] == 'Arrest'].shape[0]
    st.metric("Total Arrests", total_arrests)

with col3:
    total_warnings = traffic_df[traffic_df['stop_outcome'] == 'Warning'].shape[0]
    st.metric("Total Warnings", total_warnings)

with col4:
    total_drugs = traffic_df[traffic_df['drugs_related_stop'] == True].shape[0]
    st.metric("Drug-Related Stops", total_drugs)

# phase 3

import altair as alt

# --- VISUAL INSIGHTS SECTION ---
st.subheader("📊 Visual Insights")

tab1, tab2 = st.tabs(["Stops by Violation", "Driver Gender Distribution"])

# --- TAB 1: Stops by Violation ---
with tab1:
    st.markdown("### 🚦 Stops by Violation Type (Cleaned)")

    filtered_df = traffic_df[traffic_df['violation'].notna()]
    filtered_df['violation'] = filtered_df['violation'].astype(str).str.strip().str.title()

    violation_counts = filtered_df['violation'].value_counts().reset_index()
    violation_counts.columns = ['Violation', 'Count']

    chart = alt.Chart(violation_counts).mark_bar().encode(
        x=alt.X('Violation', sort='-y'),
        y='Count',
        color='Violation'
    ).properties(width=700, height=400)

    st.altair_chart(chart, use_container_width=True)

# --- TAB 2: Driver Gender Distribution ---
with tab2:
    st.markdown("### 🧍 Driver Gender Distribution (Cleaned)")

    gender_df = traffic_df[traffic_df['driver_gender'].notna()]
    gender_df['driver_gender'] = gender_df['driver_gender'].astype(str).str.strip().str.title()

    gender_counts = gender_df['driver_gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    chart2 = alt.Chart(gender_counts).mark_bar().encode(
        x='Gender',
        y='Count',
        color='Gender'
    ).properties(width=700, height=400)

    st.altair_chart(chart2, use_container_width=True)

# PHASE 4: ADVANCED SQL INSIGHTS
st.subheader("🧠 Advanced SQL Insights")

# -- Create TABS for Medium and Complex queries
tab_medium, tab_complex = st.tabs(["🟡 Medium-Level", "🔴 Complex-Level"])

# --- Updated Query dictionary ---
query_map = {
    "Medium": {
        "Top 10 vehicle numbers in drug-related stops":
            "SELECT vehicle_number, COUNT(*) AS total_stops FROM traffic_stop WHERE drugs_related_stop = TRUE GROUP BY vehicle_number ORDER BY total_stops DESC LIMIT 10",

        "Most frequently searched vehicles":
            "SELECT vehicle_number, COUNT(*) AS searches FROM traffic_stop WHERE search_conducted = TRUE GROUP BY vehicle_number ORDER BY searches DESC LIMIT 10",

        "Driver age group with highest arrest rate":
            """
            SELECT driver_age, COUNT(*) FILTER (WHERE stop_outcome = 'Arrest')::float / COUNT(*) AS arrest_rate
            FROM traffic_stop
            WHERE driver_age IS NOT NULL
            GROUP BY driver_age
            ORDER BY arrest_rate DESC LIMIT 10
            """,

        "Gender distribution of drivers stopped in each country":
            """
            SELECT country_name, driver_gender, COUNT(*) AS count
            FROM traffic_stop
            GROUP BY country_name, driver_gender
            ORDER BY country_name, count DESC
            """,

        "Race and gender combination with highest search rate":
            """
            SELECT driver_race, driver_gender,
                   COUNT(*) FILTER (WHERE search_conducted = TRUE)::float / COUNT(*) AS search_rate
            FROM traffic_stop
            GROUP BY driver_race, driver_gender
            ORDER BY search_rate DESC LIMIT 10
            """,

        "Time of day with most traffic stops":
            """
            SELECT EXTRACT(HOUR FROM timestamp) AS hour, COUNT(*) AS total_stops
            FROM traffic_stop
            GROUP BY hour ORDER BY total_stops DESC
            """,

        "Average stop duration by violation":
            """
            SELECT violation, AVG(
                CASE 
                    WHEN stop_duration = '0-15 Min' THEN 15
                    WHEN stop_duration = '16-30 Min' THEN 30
                    WHEN stop_duration = '30+ Min' THEN 45
                END
            ) AS avg_duration
            FROM traffic_stop
            GROUP BY violation
            ORDER BY avg_duration DESC
            """,

        "Night stops more likely to lead to arrests?":
            """
            SELECT CASE 
                       WHEN EXTRACT(HOUR FROM timestamp) BETWEEN 20 AND 23 OR EXTRACT(HOUR FROM timestamp) BETWEEN 0 AND 5 THEN 'Night'
                       ELSE 'Day'
                   END AS time_period,
                   COUNT(*) FILTER (WHERE stop_outcome = 'Arrest')::float / COUNT(*) AS arrest_rate
            FROM traffic_stop
            GROUP BY time_period
            """,

        "Violations most associated with searches or arrests":
            """
            SELECT violation,
                   COUNT(*) FILTER (WHERE search_conducted = TRUE)::float / COUNT(*) AS search_rate,
                   COUNT(*) FILTER (WHERE stop_outcome = 'Arrest')::float / COUNT(*) AS arrest_rate
            FROM traffic_stop
            GROUP BY violation
            ORDER BY search_rate DESC
            """,

        "Most common violations among younger drivers (<25)":
            """
            SELECT violation, COUNT(*) AS count
            FROM traffic_stop
            WHERE driver_age < 25
            GROUP BY violation
            ORDER BY count DESC
            """,

        "Violations that rarely result in search or arrest":
            """
            SELECT violation,
                   COUNT(*) FILTER (WHERE search_conducted = TRUE)::float / COUNT(*) AS search_rate,
                   COUNT(*) FILTER (WHERE stop_outcome = 'Arrest')::float / COUNT(*) AS arrest_rate
            FROM traffic_stop
            GROUP BY violation
            HAVING COUNT(*) > 100
            ORDER BY search_rate ASC, arrest_rate ASC
            """,

        "Countries with highest drug-related stop rate":
            """
            SELECT country_name,
                   COUNT(*) FILTER (WHERE drugs_related_stop = TRUE)::float / COUNT(*) AS drug_stop_rate
            FROM traffic_stop
            GROUP BY country_name
            ORDER BY drug_stop_rate DESC
            """,

        "Arrest rate by country and violation":
            """
            SELECT country_name, violation,
                   COUNT(*) FILTER (WHERE stop_outcome = 'Arrest')::float / COUNT(*) AS arrest_rate
            FROM traffic_stop
            GROUP BY country_name, violation
            ORDER BY arrest_rate DESC
            """,

        "Countries with most searches conducted":
            """
            SELECT country_name, COUNT(*) FILTER (WHERE search_conducted = TRUE) AS searches
            FROM traffic_stop
            GROUP BY country_name
            ORDER BY searches DESC
            """
    },

    "Complex": {
        "Yearly breakdown of stops and arrests by country":
            """
            SELECT country_name, DATE_PART('year', timestamp) AS year,
                   COUNT(*) AS total_stops,
                   COUNT(*) FILTER (WHERE stop_outcome = 'Arrest') AS total_arrests
            FROM traffic_stop
            GROUP BY country_name, year
            ORDER BY country_name, year
            """,

        "Driver violation trends based on age and race":
            """
            SELECT driver_race, driver_age, violation, COUNT(*) AS count
            FROM traffic_stop
            GROUP BY driver_race, driver_age, violation
            ORDER BY count DESC LIMIT 20
            """,

        "Stops by Year, Month, Hour":
            """
            SELECT DATE_PART('year', timestamp) AS year,
                   DATE_PART('month', timestamp) AS month,
                   DATE_PART('hour', timestamp) AS hour,
                   COUNT(*) AS total_stops
            FROM traffic_stop
            GROUP BY year, month, hour
            ORDER BY year, month, hour
            """,

        "Violations with high search and arrest rates":
            """
            SELECT violation,
                   COUNT(*) FILTER (WHERE search_conducted = TRUE)::float / COUNT(*) AS search_rate,
                   COUNT(*) FILTER (WHERE stop_outcome = 'Arrest')::float / COUNT(*) AS arrest_rate
            FROM traffic_stop
            GROUP BY violation
            ORDER BY search_rate DESC, arrest_rate DESC
            """,

        "Driver demographics by country":
            """
            SELECT country_name, AVG(driver_age) AS avg_age,
                   COUNT(*) FILTER (WHERE driver_gender = 'M') AS male_count,
                   COUNT(*) FILTER (WHERE driver_gender = 'F') AS female_count
            FROM traffic_stop
            GROUP BY country_name
            """,

        "Top 5 violations with highest arrest rates":
            """
            SELECT violation,
                   COUNT(*) FILTER (WHERE stop_outcome = 'Arrest')::float / COUNT(*) AS arrest_rate
            FROM traffic_stop
            GROUP BY violation
            ORDER BY arrest_rate DESC LIMIT 5
            """
    }
}

# --- MEDIUM LEVEL TAB ---
with tab_medium:
    question = st.selectbox("Select a Medium-Level Question", ["-- Select --"] + list(query_map["Medium"].keys()), key="medium_q")
    if question != "-- Select --":
        sql = query_map["Medium"][question]
        result_df = pd.read_sql(sql, engine)
        st.dataframe(result_df, use_container_width=True)

# --- COMPLEX LEVEL TAB ---
with tab_complex:
    question = st.selectbox("Select a Complex-Level Question", ["-- Select --"] + list(query_map["Complex"].keys()), key="complex_q")
    if question != "-- Select --":
        sql = query_map["Complex"][question]
        result_df = pd.read_sql(sql, engine)
        st.dataframe(result_df, use_container_width=True)


# --- PHASE 5: Predictive Summary Form ---
st.subheader("📝 Predictive Form: Driver Stop Summary")

with st.form("predictive_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        driver_age = st.number_input("Driver Age", min_value=15, max_value=100, value=30)
        driver_gender = st.selectbox("Driver Gender", ["Male", "Female"])
        stop_time = st.time_input("Stop Time")
        violation = st.selectbox("Violation", ["Speeding", "DUI", "Seatbelt", "Signal", "Other"])
    
    with col2:
        search_conducted = st.selectbox("Was Search Conducted?", ["Yes", "No"])
        stop_outcome = st.selectbox("Stop Outcome", ["Warning", "Ticket", "Arrest"])
        stop_duration = st.selectbox("Stop Duration", ["0-15 Min", "16-30 Min", "30+ Min"])
        drugs_related_stop = st.selectbox("Was it Drug Related?", ["Yes", "No"])
    
    submit_btn = st.form_submit_button("🚦 Generate Driver Summary")

if submit_btn:
    # Cleaned-up logic
    gender_text = "male" if driver_gender == "Male" else "female"
    pronoun = "he" if driver_gender == "Male" else "she"
    
    search_text = "a search was conducted" if search_conducted == "Yes" else "no search was conducted"
    citation_text = f"{pronoun} received a {stop_outcome.lower()}"
    drugs_text = "was drug-related" if drugs_related_stop == "Yes" else "was not drug-related"
    
    # Format time
    try:
        formatted_time = stop_time.strftime('%I:%M %p').lstrip('0')  # e.g., 2:30 PM
    except:
        formatted_time = str(stop_time)

    # --- Predict Violation & Outcome from similar pattern (optional logic stub) ---
    # You can improve this later using real ML models
    predicted_violation = violation  # placeholder logic
    predicted_outcome = stop_outcome  # placeholder logic

    # --- Display Section ---
    st.markdown("---")
    st.subheader("🔎 Prediction Result")
    st.markdown(f"**Predicted Violation:** `{predicted_violation}`")
    st.markdown(f"**Predicted Stop Outcome:** `{predicted_outcome}`")

    st.markdown("---")
    st.subheader("📋 Predictive Summary")

    st.markdown(
        f"""
🚗 A {driver_age}-year-old {gender_text} driver was stopped for **{violation}** at **{formatted_time}**.  
🔍 {search_text.capitalize()}, and {citation_text}.  
🕒 The stop lasted **{stop_duration}** and {drugs_text}.
        """
    )
