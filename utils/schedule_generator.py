import random


def initialize_schedule(data):
    """Creates a random initial schedule."""
    schedule = {}
    for course in data.get("Courses", []):
        course_id = course[0]
        schedule[course_id] = (
            random.randint(0, data["Days"] - 1),
            random.randint(0, data["Periods_per_day"] - 1),
            random.choice(data["Rooms"])[0],
        )
    return schedule


def get_neighbor(schedule, data):
    """Generates a neighboring solution by randomly changing a course's schedule."""
    new_schedule = schedule.copy()
    course = random.choice(list(new_schedule.keys()))
    new_schedule[course] = (
        random.randint(0, data["Days"] - 1),
        random.randint(0, data["Periods_per_day"] - 1),
        random.choice(data["Rooms"])[0],
    )
    return new_schedule
