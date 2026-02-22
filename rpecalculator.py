"""RPE Calculator with Streamlit frontend for tracking powerlifting sets."""

import streamlit as st


class Lift:
    """Represents a single powerlifting set with RPE-based e1RM calculation."""

    RPE_CHART = {
        10: 1.0, 9.5: 0.978, 9: 0.955, 8.5: 0.939,
        8: 0.917, 7.5: 0.901, 7: 0.885, 6.5: 0.869, 6: 0.853
    }

    def __init__(self, exercise, weight, reps, rpe):
        """Initialize a lift with exercise, weight, reps and RPE."""
        self.exercise = exercise
        self.weight = weight
        self.reps = reps
        self.rpe = rpe
        self.e1rm = self._calculate_e1rm()

    def _calculate_e1rm(self):
        """Calculate estimated 1 rep max based on RPE and reps."""
        rpe_factor = self.RPE_CHART.get(self.rpe, 0.885)
        reps_factor = 1 + (0.0333 * self.reps)
        return round((self.weight / rpe_factor) * reps_factor, 1)


class LiftTracker:
    """Tracks and analyzes powerlifting sets."""

    def __init__(self):
        """Initialize an empty lift tracker."""
        self.lifts = []

    def log_lift(self, exercise, weight, reps, rpe):
        """Log a new lift and return the created Lift object."""
        lift = Lift(exercise, weight, reps, rpe)
        self.lifts.append(lift)
        return lift

    def delete_lift(self, index):
        """Delete a lift by index."""
        if 0 <= index < len(self.lifts):
            self.lifts.pop(index)

    def get_best_set(self, exercise):
        """Return the best set for a given exercise based on e1RM."""
        exercise_lifts = [lift for lift in self.lifts if lift.exercise == exercise]
        if not exercise_lifts:
            return None
        return max(exercise_lifts, key=lambda x: x.e1rm)

    def get_all_lifts(self):
        """Return all logged lifts."""
        return self.lifts

    def get_target_weight(self, exercise, target_reps, target_rpe):
        """Calculate target weight for a given exercise, reps and RPE."""
        best = self.get_best_set(exercise)
        if not best:
            return None
        rpe_factor = Lift.RPE_CHART.get(target_rpe, 0.885)
        reps_factor = 1 + (0.0333 * target_reps)
        return round((best.e1rm / reps_factor) * rpe_factor, 1)


def main():
    """Main function to run the Streamlit RPE calculator app."""
    st.title("RPE Lift Tracker")

    if "tracker" not in st.session_state:
        st.session_state.tracker = LiftTracker()

    tracker = st.session_state.tracker

    st.header("Log Lift")
    col1, col2 = st.columns(2)

    with col1:
        exercise = st.selectbox("Exercise", ["Squat", "Bench", "Deadlift"])
        weight = st.number_input("Weight (kg)", min_value=0.0, step=2.5)
        reps = st.number_input("Reps", min_value=1, max_value=20, step=1)

    with col2:
        rpe = st.selectbox("RPE", [6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10])

    if st.button("Log Lift"):
        lift = tracker.log_lift(exercise, weight, reps, rpe)
        st.success(f"Logged: {exercise} {weight}kg x{reps} @{rpe} | e1RM: {lift.e1rm}kg")

    st.header("All Logged Lifts")
    lifts = tracker.get_all_lifts()
    if lifts:
        for i, lift in enumerate(lifts):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.write(f"{i+1}. {lift.exercise}: {lift.weight}kg "
                         f"x{lift.reps} @{lift.rpe} | e1RM: {lift.e1rm}kg")
            with col_b:
                if st.button("Delete", key=f"delete_{i}"):
                    tracker.delete_lift(i)
                    st.rerun()
    else:
        st.info("No lifts logged yet.")

    st.header("Personal Bests")
    for ex in ["Squat", "Bench", "Deadlift"]:
        best = tracker.get_best_set(ex)
        if best:
            st.metric(label=ex, value=f"{best.e1rm}kg e1RM",
                      delta=f"{best.weight}kg x{best.reps} @{best.rpe}")

    st.header("Target Weight Calculator")
    col3, col4 = st.columns(2)

    with col3:
        target_exercise = st.selectbox("Exercise ", ["Squat", "Bench", "Deadlift"])
        target_reps = st.number_input("Target Reps", min_value=1, max_value=20, step=1)

    with col4:
        target_rpe = st.selectbox("Target RPE", [6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10])

    if st.button("Calculate Target"):
        target = tracker.get_target_weight(target_exercise, target_reps, target_rpe)
        if target:
            st.success(f"Target weight: {target}kg")
        else:
            st.warning(f"No data logged for {target_exercise} yet.")


main()