import pandas as pd
import streamlit as st


def display_schedule_table(best_schedule, data):
    """Displays the schedule in a table format using Streamlit."""
    days = data["Days"]
    periods_per_day = data["Periods_per_day"]
    rooms = [room[0] for room in data["Rooms"]]
    courses_data = {
        course[0]: course[1:] for course in data.get("Courses", [])
    }  # course_id: [name, ...]

    schedule_grid = [
        [["" for _ in rooms] for _ in range(periods_per_day)] for _ in range(days)
    ]

    for course_id, (day, period, room) in best_schedule.items():
        room_index = rooms.index(room)
        if schedule_grid[day][period][
            room_index
        ]:  # Handle potential clashes in display (though SA should minimize them)
            schedule_grid[day][period][room_index] += (
                f", {course_id} ({courses_data.get(course_id, ['Unknown'])[0]})"
            )
        else:
            schedule_grid[day][period][room_index] = (
                f"{course_id} ({courses_data.get(course_id, ['Unknown'])[0]})"
            )

    day_names = [f"Day {i + 1}" for i in range(days)]
    period_names = [f"Period {i + 1}" for i in range(periods_per_day)]

    index_columns = pd.MultiIndex.from_product(
        [day_names, period_names], names=["Day", "Period"]
    )
    df = pd.DataFrame(index=index_columns, columns=rooms)

    for day_idx in range(days):
        for period_idx in range(periods_per_day):
            for room_idx, room_name in enumerate(rooms):
                df.loc[(day_names[day_idx], period_names[period_idx]), room_name] = (
                    schedule_grid[day_idx][period_idx][room_idx]
                )

    st.dataframe(df)
