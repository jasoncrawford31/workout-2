
import streamlit as st
import pandas as pd
from datetime import date

# Full 5-day workout plan
workout_plan = {
    "Day 1 – Chest & Triceps": [
        "Incline Dumbbell Press", "Flat Bench Press", "Dumbbell/Cable Chest Flyes",
        "Dips", "Overhead Triceps Extension", "Rope Triceps Pushdown"
    ],
    "Day 2 – Back & Biceps": [
        "Pull-Ups/Lat Pulldown", "Bent Over Barbell Rows", "Seated Cable Row",
        "Face Pulls", "Barbell/EZ-Bar Curl", "Hammer Curls"
    ],
    "Day 3 – Legs (No Lunges)": [
        "Barbell/Hack Squats", "Leg Press", "Romanian Deadlifts",
        "Seated Leg Curl", "Standing/Seated Calf Raises"
    ],
    "Day 4 – Shoulders & Abs": [
        "Seated DB Shoulder Press", "Lateral Raises", "Rear Delt Flyes",
        "Front Raises", "Plank", "Hanging Leg Raises/Cable Crunch"
    ],
    "Day 5 – Full Upper + HIIT": [
        "Push-Ups", "Pull-Ups", "Dumbbell Bench Press",
        "Dumbbell Rows", "Arnold Press", "Barbell Curl + Triceps Rope Superset"
    ]
}

st.title("Workout + Measurement Tracker")
selected_day = st.selectbox("Select Workout Day", list(workout_plan.keys()))
today = date.today()

st.subheader(f"{selected_day} – {today}")
exercise_data = []

# Per-set entry for each exercise
for exercise in workout_plan[selected_day]:
    st.markdown(f"### {exercise}")
    num_sets = st.number_input(f"How many sets for {exercise}?", min_value=1, max_value=10, value=4, key=f"{exercise}_sets")

    for set_num in range(1, num_sets + 1):
        col1, col2 = st.columns(2)
        with col1:
            reps = st.number_input(f"Set {set_num} Reps", min_value=0, max_value=50, value=10, key=f"{exercise}_reps_{set_num}")
        with col2:
            weight = st.number_input(f"Set {set_num} Weight (lbs)", min_value=0, max_value=1000, value=0, key=f"{exercise}_weight_{set_num}")

        exercise_data.append({
            "Date": today,
            "Day": selected_day,
            "Exercise": exercise,
            "Set": set_num,
            "Reps": reps,
            "Weight (lbs)": weight
        })

# Cardio tracking
st.subheader("Incline Walking – Cardio")
cardio_minutes = st.slider("Duration (minutes)", 0, 60, 30)
calories_burned = round(cardio_minutes * 6.8)
st.write(f"Estimated Calories Burned: **{calories_burned} kcal**")

# Body measurements
st.subheader("Body Measurements (inches)")
biceps = st.number_input("Biceps", min_value=0.0, max_value=30.0, step=0.1)
forearms = st.number_input("Forearms", min_value=0.0, max_value=25.0, step=0.1)
waist = st.number_input("Waist", min_value=0.0, max_value=60.0, step=0.1)
thigh = st.number_input("Thigh", min_value=0.0, max_value=40.0, step=0.1)

# Notes
notes = st.text_area("Workout Notes")

# Save workout
if st.button("Save Workout"):
    df = pd.DataFrame(exercise_data)
    df["Cardio (min)"] = cardio_minutes
    df["Cardio Calories"] = calories_burned
    df["Biceps"] = biceps
    df["Forearms"] = forearms
    df["Waist"] = waist
    df["Thigh"] = thigh
    df["Notes"] = notes

    try:
        existing = pd.read_csv("workout_log.csv")
        df = pd.concat([existing, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv("workout_log.csv", index=False)
    st.success("Workout saved!")

# View history
if st.checkbox("Show Workout History"):
    try:
        log_df = pd.read_csv("workout_log.csv")
        st.dataframe(log_df)
    except FileNotFoundError:
        st.info("No workout data found yet.")
