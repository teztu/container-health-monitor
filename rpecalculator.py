import streamlit as st


class Lift:
    RPE_CHART = {
        10: 1.0, 9.5: 0.978, 9: 0.955, 8.5: 0.939,
        8: 0.917, 7.5: 0.901, 7: 0.885, 6.5: 0.878
    }

    def __init__(self, exercise, weight, reps, rpe):
        self.exercise = exercise
        self.weight = weight
        self.reps = reps
        self.rpe = rpe
        self.e1rm = self._calculate_e1rm()

    def _calculate_e1rm(self):
        rpe_factor = self.RPE_CHART.get(self.rpe, 0.885)
        reps_factor = 1 + (0.0333 * self.reps)
        return round((self.weight / rpe_factor) * reps_factor, 1)


class LiftTracker:
    def __init__(self):
        self.lifts = []

    def log_lift(self, exercise, weight, reps, rpe):
        lift = Lift(exercise, weight, reps, rpe)
        self.lifts.append(lift)
        return lift

    def get_best_set(self, exercise):
        exercise_lifts = [l for l in self.lifts if l.exercise == exercise]
        if not exercise_lifts:
            return None
        return max(exercise_lifts, key=lambda x: x.e1rm)

    def get_all_lifts(self):
        return self.lifts

    def get_target_weight(self, exercise, target_reps, target_rpe):
        best = self.get_best_set(exercise)
        if not best:
            return None
        rpe_factor = Lift.RPE_CHART.get(target_rpe, 0.885)
        reps_factor = 1 + (0.0333 * target_reps)
        return round((best.e1rm / reps_factor) * rpe_factor, 1)


# Streamlit app
st.title("RPE Lift Tracker")

if "tracker" not in st.session_state:
    st.session_state.tracker = LiftTracker()

tracker = st.session_state.tracker

# Log a lift
st.header("Log Lift")
col1, col2 = st.columns(2)

with col1:
    exercise = st.selectbox("Exercise", ["Squat", "Bench", "Deadlift"])
    weight = st.number_input("Weight (kg)", min_value=0.0, step=2.5)
    reps = st.number_input("Reps", min_value=1, max_value=20, step=1)

with col2:
    rpe = st.selectbox("RPE", [6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10])

if st.button("Log Lift"):
    lift = tracker.log_lift(exercise, weight, reps, rpe)
    st.success(f"Logged: {exercise} {weight}kg x{reps} @{rpe} | e1RM: {lift.e1rm}kg")

# All lifts
st.header("All Logged Lifts")
lifts = tracker.get_all_lifts()
if lifts:
    data = [{
        "Exercise": l.exercise,
        "Weight (kg)": l.weight,
        "Reps": l.reps,
        "RPE": l.rpe,
        "e1RM (kg)": l.e1rm
    } for l in lifts]
    st.table(data)
else:
    st.info("No lifts logged yet.")

# Personal bests
st.header("Personal Bests")
for ex in ["Squat", "Bench", "Deadlift"]:
    best = tracker.get_best_set(ex)
    if best:
        st.metric(label=ex, value=f"{best.e1rm}kg e1RM",
                  delta=f"{best.weight}kg x{best.reps} @{best.rpe}")

# Target weight calculator
st.header("Target Weight Calculator")
col3, col4 = st.columns(2)

with col3:
    target_exercise = st.selectbox("Exercise ", ["Squat", "Bench", "Deadlift"])
    target_reps = st.number_input("Target Reps", min_value=1, max_value=20, step=1)

with col4:
    target_rpe = st.selectbox("Target RPE", [7, 7.5, 8, 8.5, 9, 9.5, 10])

if st.button("Calculate Target"):
    target = tracker.get_target_weight(target_exercise, target_reps, target_rpe)
    if target:
        st.success(f"Target weight: {target}kg")
    else:
        st.warning(f"No data logged for {target_exercise} yet.")