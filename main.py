import json

from optimizer import GeneticOptimizer
from input_management import ConfigurationManager, InputManager
from solution import SolutionHandler, FitnessFunctionWrapper
from pathlib import Path

CONFIG_PATH = Path('./config.json')


def main():
    config_manager = ConfigurationManager(CONFIG_PATH)
    config_manager.load_configuration()

    with open('./test/input.json', 'r') as j:
        input_ = json.loads(j.read())

    schema = config_manager.configuration_settings["schema"]

    input_manger = InputManager(schema, input_)
    input_manger.register_input()

    sh = SolutionHandler(input_manger)
    sh.initialise_genes()

    f_wrapper = FitnessFunctionWrapper(sh)

    # initialise pygad
    initial_population = sh.initial_state_list
    go = GeneticOptimizer(
        fitness_function=f_wrapper.custom_fitness_function,
        num_genes=len(initial_population),
        num_generations=500,
        num_parents_mating=4,
        sol_per_pop=16,
        initial_population=initial_population,
        parent_selection_type='sss',
        keep_parents=1,
        crossover_type='single_point',
        mutation_type='random',
        mutation_percent_genes=40,
        # parallel_processing=['process', 10]
    )
    t = go.optimize()
    sh.assign_values_from_solution(t[0])
    res = sh.solution_state
    res_list = [res[key] for key in res.keys()]
    res_sorted = sorted(res_list, key=lambda x: x['time_start'], reverse=False)
    res_sorted_incl = [meeting for meeting in res_sorted if meeting['included'] > 0]
    print()


if __name__ == "__main__":
    main()

# ToDo ServiceManagement
