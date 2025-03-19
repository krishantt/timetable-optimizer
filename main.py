import matplotlib.pyplot as plt
import streamlit as st
import time

from utils.algorithm import simulated_annealing  # Relative import
from utils.data_loader import load_timetable_from_string  # Relative import
from utils.schedule_display import display_schedule_table  # Relative import


def main():
    st.set_page_config(page_title="Course Timetable Optimizer", page_icon="✨")
    st.title("Course Timetable Optimizer")
    st.write("### A Simulated Annealing Example")

    # Sidebar parameters
    st.sidebar.header("Algorithm Parameters")
    max_iterations = st.sidebar.slider("Max Iterations", 100, 10000, 2000)
    initial_temperature = st.sidebar.slider("Initial Temperature", 100, 2000, 500)
    cooling_rate = st.sidebar.slider("Cooling Rate", 0.9, 0.9999, 0.995)

    uploaded_file = st.file_uploader(
        "Upload your timetable dataset file (.ctt)", type=["ctt"]
    )

    if uploaded_file is not None:
        file_content = uploaded_file.getvalue().decode("utf-8")
        data = load_timetable_from_string(file_content)

        if (
            "Courses" in data
            and "Rooms" in data
            and "Days" in data
            and "Periods_per_day" in data
        ):
            st.success("Dataset loaded successfully!")

            if st.button("Optimize Schedule"):
                with st.spinner("Optimizing schedule..."):
                    start_time = time.time()
                    best_schedule, costs,initial_cost,iterations_to_converge = simulated_annealing(
                        data, max_iterations, initial_temperature, cooling_rate
                    )
                    end_time = time.time()

                st.header("Optimized Schedule")
                min_cost = (
                    min(costs) if costs else 0
                )  # Handle cases where costs might be empty
                st.write(f"Minimum Conflicts Found: {min_cost}")
                st.write(f"Initial Conflicts: {initial_cost}")
                st.write(f"Iterations to Converge: {iterations_to_converge}")
                st.write(f"Time Taken: {end_time - start_time:.2f} seconds")
                if initial_cost>0:
                    reduction_percentage = ((initial_cost-min_cost)/initial_cost)*100
                    st.write(f"Reduction in Conflicts: {reduction_percentage:.2f}%")

                st.subheader("Schedule Table")
                display_schedule_table(best_schedule, data)

                schedule_text = ""
                for course, (day, slot, room) in best_schedule.items():
                    schedule_text += f"Course {course}: Day {day + 1}, Period {slot + 1}, Room {room}\n"

                st.download_button(
                    label="Download Schedule as Text",
                    data=schedule_text,
                    file_name="optimized_schedule.txt",
                    mime="text/plain",
                )

                st.subheader("Cost Optimization Progress")
                fig, ax = plt.subplots()
                ax.plot(costs)
                ax.set_xlabel("Iterations")
                ax.set_ylabel("Cost (Conflicts)")
                st.pyplot(fig)

        else:
            st.error(
                "Invalid dataset format. Please ensure your file has 'Courses', 'Rooms', 'Days', and 'Periods_per_day' information."
            )


if __name__ == "__main__":
    main()
