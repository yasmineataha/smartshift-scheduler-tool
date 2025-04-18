import streamlit as st
import pandas as pd
import altair as alt
from scheduler import generate_schedule
from utils import check_compliance

PROCESSING_RATE = 50  # tasks/orders/calls handled per person per day

st.set_page_config(page_title="SmartShift Planner", layout="centered")
st.title("📦 SmartShift Planner")

# Sidebar: forecast input
st.sidebar.header("📈 Expected Volume per Day")
forecast_data = {
    "Monday": st.sidebar.number_input("Expected volume on Monday", value=600),
    "Tuesday": st.sidebar.number_input("Tuesday", value=620),
    "Wednesday": st.sidebar.number_input("Wednesday", value=640),
    "Thursday": st.sidebar.number_input("Thursday", value=660),
    "Friday": st.sidebar.number_input("Friday", value=680),
    "Saturday": st.sidebar.number_input("Saturday", value=700),
}

# File upload
uploaded_file = st.file_uploader("Upload employee file (CSV or Excel)", type=["csv", "xlsx"])

# Toggle: labor law
enforce_law = st.checkbox("Enforce German labor law (48h/week, 10h/day, 11h rest)")

# Main app logic
if uploaded_file:
    # Load employee data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("### 👥 Employee Data", df)

    if st.button("Generate Schedule"):
        # Generate shift plan
        schedule = generate_schedule(df)
        st.write("### 📅 Weekly Schedule")
        st.dataframe(schedule)

        # ⚖️ Compliance check
        if enforce_law:
            violations = check_compliance(schedule)
            if not violations.empty:
                st.warning("⚠️ Labor law violations found!")
                st.dataframe(violations)
            else:
                st.success("✅ Schedule is compliant with labor laws.")

        # 📊 Staffing by station per day
        st.write("### 🏭 Staffing by Station per Day")
        filtered = schedule[schedule["shift"] != "Training"]
        role_day_counts = (
            filtered.groupby(["day", "role"])["agent_id"]
            .nunique()
            .reset_index()
            .rename(columns={"agent_id": "Number of Workers"})
        )
        ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        role_day_counts["day"] = pd.Categorical(role_day_counts["day"], categories=ordered_days, ordered=True)
        role_day_counts = role_day_counts.sort_values("day")

        chart = alt.Chart(role_day_counts).mark_bar().encode(
            x=alt.X("day:N", title="Day of the Week"),
            y=alt.Y("Number of Workers:Q", stack="zero"),
            color=alt.Color("role:N", title="Station"),
            tooltip=["day", "role", "Number of Workers"]
        ).properties(
            title="Number of Employees Scheduled per Station (Role) by Day"
        )
        st.altair_chart(chart, use_container_width=True)

        # 🔮 Forecast vs. Scheduled
        st.write("### 🔍 Forecast vs. Actual Staffing")
        scheduled_counts = (
            schedule[schedule["shift"] != "Training"]
            .groupby("day")["agent_id"]
            .nunique()
            .reset_index()
            .rename(columns={"agent_id": "Scheduled Workers"})
        )

        forecast_df = pd.DataFrame([
            {"day": day, "Forecasted Volume": volume,
             "Required Workers": round(volume / PROCESSING_RATE)}
            for day, volume in forecast_data.items()
        ])

        staffing_df = pd.merge(forecast_df, scheduled_counts, on="day", how="left").fillna(0)
        staffing_df["Staffing Status"] = staffing_df["Scheduled Workers"] - staffing_df["Required Workers"]
        st.dataframe(staffing_df)

        forecast_chart = alt.Chart(staffing_df).transform_fold(
            ["Scheduled Workers", "Required Workers"]
        ).mark_bar().encode(
            x="day:N",
            y="value:Q",
            color="key:N",
            tooltip=["day", "Forecasted Volume", "Scheduled Workers", "Required Workers"]
        ).properties(
            title="Forecasted vs. Scheduled Staffing"
        )
        st.altair_chart(forecast_chart, use_container_width=True)

        # Download schedule
        csv = schedule.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Schedule", data=csv, file_name="schedule.csv", mime="text/csv")
