# Max 48 hours per week
# Min 11 hours rest between shifts
# Not more than 10 hours per day
import pandas as pd
from datetime import datetime

def parse_time(t):
    return datetime.strptime(t, "%H:%M")

def check_compliance(schedule_df):
    violations = []

    schedule_df = schedule_df.sort_values(by=["agent_id", "day"])

    grouped = schedule_df.groupby("agent_id")

    for agent_id, group in grouped:
        total_hours = 0
        last_end_time = None

        for _, row in group.iterrows():
            shift_start = parse_time(row["start"])
            shift_end = parse_time(row["end"])
            shift_hours = (shift_end - shift_start).seconds / 3600
            total_hours += shift_hours

            # Check 11h rest rule
            if last_end_time:
                rest_hours = (shift_start - last_end_time).seconds / 3600
                if rest_hours < 11:
                    violations.append({
                        "agent_id": row["agent_id"],
                        "name": row["name"],
                        "day": row["day"],
                        "issue": f"Only {rest_hours:.1f}h rest between shifts"
                    })

            # Check 10h max per day
            if shift_hours > 10:
                violations.append({
                    "agent_id": row["agent_id"],
                    "name": row["name"],
                    "day": row["day"],
                    "issue": f"{shift_hours:.1f}h worked in one day (limit is 10h)"
                })

            last_end_time = shift_end

        # Check 48h per week
        if total_hours > 48:
            violations.append({
                "agent_id": group.iloc[0]['agent_id'],
                "name": group.iloc[0]['name'],
                "day": "Week Total",
                "issue": f"Worked {total_hours:.1f}h (over 48h limit)" })

    return pd.DataFrame(violations)