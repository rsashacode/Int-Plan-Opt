from solution import SolutionHandler


class FitnessFunctionWrapper:
    def __init__(self, solution_handler: SolutionHandler):
        self.solution_handler = solution_handler

    def custom_fitness_function(self, ga_instance, solution, solution_idx):
        self.solution_handler.assign_values_from_solution(solution)
        solution_state = self.solution_handler.solution_state

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
                if schedule[i-1]["time_end"] > schedule[i]["time_start"]:
                    print(0)
                    return 0
            if any([schedule[i]["time_start"] < schedule[i]['time_start_lower_boundary'],
                    schedule[i]["time_start"] > schedule[i]['time_start_upper_boundary'],
                    ]):
                print(0)
                return 0

        for i, meeting in enumerate(schedule):
            total_revenue += meeting["potential_revenue"]

        fitness_value = total_revenue
        # End of editable section
        print(fitness_value)
        return fitness_value
