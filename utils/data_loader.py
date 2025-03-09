def load_timetable_from_string(file_content):
    """Loads timetable data from a string content."""
    lines = file_content.splitlines()

    data = {}
    section = None

    for line in lines:
        line = line.strip()
        if not line or line == "END.":
            continue

        if line.startswith("Name:"):
            data["Name"] = line.split(": ")[1]
        elif line.startswith("Courses:"):
            data["Courses_count"] = int(line.split(": ")[1])
        elif line.startswith("Rooms:"):
            data["Rooms_count"] = int(line.split(": ")[1])
        elif line.startswith("Days:"):
            data["Days"] = int(line.split(": ")[1])
        elif line.startswith("Periods_per_day:"):
            data["Periods_per_day"] = int(line.split(": ")[1])
        elif line.startswith("Curricula:"):
            data["Curricula_count"] = int(line.split(": ")[1])
        elif line.startswith("Constraints:"):
            data["Constraints_count"] = int(line.split(": ")[1])
        elif line.startswith("COURSES:"):
            section = "Courses"
            data[section] = []
        elif line.startswith("ROOMS:"):
            section = "Rooms"
            data[section] = []
        elif line.startswith("CURRICULA:"):
            section = "Curricula"
            data[section] = []
        elif line.startswith("UNAVAILABILITY_CONSTRAINTS:"):
            section = "Constraints"
            data[section] = []
        elif section:
            data[section].append(line.split())

    return data