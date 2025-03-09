import numpy as np
import random

def cost_function(schedule, data):
    """Computes the cost of the current schedule based on constraints."""
    conflicts = 0
    occupied_slots = {}

    for course, (day, slot, room) in schedule.items():
        key = (day, slot, room)
        if key in occupied_slots:
            conflicts += (
                1  # More than one course scheduled in the same room at the same time
            )
        occupied_slots[key] = True

        # Check unavailability constraints
        for constraint in data.get("Constraints", []):
            if (
                constraint[0] == course
                and int(constraint[1]) == day
                and int(constraint[2]) == slot
            ):
                conflicts += 10  # High penalty for violating hard constraints

    return conflicts


def simulated_annealing(data, max_iterations, initial_temperature, cooling_rate):
    """Performs simulated annealing to optimize the timetable."""
    from .schedule_generator import initialize_schedule, get_neighbor # Relative import

    current_schedule = initialize_schedule(data)
    best_schedule = current_schedule
    current_cost = cost_function(current_schedule, data)
    best_cost = current_cost
    temperature = initial_temperature
    costs = []

    for i in range(max_iterations):
        new_schedule = get_neighbor(current_schedule, data)
        new_cost = cost_function(new_schedule, data)

        if (
            new_cost < current_cost
            or np.exp((current_cost - new_cost) / temperature) > random.random()
        ):
            current_schedule = new_schedule
            current_cost = new_cost
            if new_cost < best_cost:
                best_schedule = new_schedule
                best_cost = new_cost

        costs.append(best_cost)
        temperature *= cooling_rate  # Cooling schedule
        if temperature < 1e-3:
            break

    return best_schedule, costs