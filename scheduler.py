import pandas as pd
import random


SHIFT_TEMPLATES = {
    "Morning": {"start": "06:00", "end": "14:00"},
    "Evening": {"start": "14:00", "end": "22:00"},
    "Night": {"start": "22:00", "end": "06:00"}  # Optional for peak season
}

WORK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def generate_schedule(employee_df, num_shifts=2):
    schedule = []

    allowed_shifts = list(SHIFT_TEMPLATES.keys())[:num_shifts]

    for _, agent in employee_df.iterrows():
        total_hours = 0
        shift_hours = 8

        for day in WORK_DAYS:
            if total_hours + shift_hours > agent["max_hours_per_week"]:
                break

            preferred_shift = agent["preferred_shift"]
            shift_to_assign = preferred_shift if preferred_shift in allowed_shifts else allowed_shifts[0]
            shift = SHIFT_TEMPLATES[shift_to_assign]

            schedule.append({
                "agent_id": agent["agent_id"],
                "name": agent["name"],
                "role": agent["role"],
                "day": day,
                "shift": shift_to_assign,
                "start": shift["start"],
                "end": shift["end"]
            })

            total_hours += shift_hours

    # 🎯 Add training blocks
    for _, agent in employee_df.iterrows():
        if str(agent["training_required"]).strip().lower() == "yes":
            training_day = random.choice(WORK_DAYS)
            schedule.append({
                "agent_id": agent["agent_id"],
                "name": agent["name"],
                "role": agent["role"],
                "day": training_day,
                "shift": "Training",
                "start": "12:00",
                "end": "13:00"
            })

    return pd.DataFrame(schedule)
