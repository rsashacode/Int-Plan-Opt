import numpy as np


def fitness_function(solution_state: dict) -> float:

    # Editable section. All updated objects are stored in solution_state dictionary. All keys are as specified in
    # schema and input.

    total_revenue = 0

    meetings_list = [
        solution_state[meeting] for meeting in solution_state.keys() if solution_state[meeting]["included"] >= 0
    ]

    schedule = sorted(meetings_list, key=lambda x: x['time_start'], reverse=False)
    for i, meeting in enumerate(schedule):
        schedule[i]["time_end"] = meeting["time_start"] + meeting["duration"]
        if i >= 1:
            if schedule[i - 1]["time_end"] > schedule[i]["time_start"]:
                return -1 * np.inf
        if any([schedule[i]["time_start"] < schedule[i]['time_start_lower_boundary'],
                schedule[i]["time_start"] > schedule[i]['time_start_upper_boundary'],
                ]):
            return -1 * np.inf

    for i, meeting in enumerate(schedule):
        total_revenue += meeting["potential_revenue"]

    fitness_value = total_revenue

    # end of editable section

    return fitness_value
