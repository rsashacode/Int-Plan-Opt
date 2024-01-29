import copy

from configuration.fitness_function import fitness_function
from input_management import InputManager


class SolutionHandler:
    def __init__(self, input_manager: InputManager):
        self.input_manager = input_manager

        self.index_to_parameter = self.input_manager.index_to_parameter
        self.parameter_to_index = self.input_manager.parameter_to_index
        self.user_input = self.input_manager.user_input

        self.initial_state_list = []
        self.solution_state_list = []

        self.initial_state = {}
        self.solution_state: dict = {}

    def initialise_genes(self):
        if self.input_manager.indexes_assigned:
            for ind in self.index_to_parameter:
                address = self.index_to_parameter[ind]
                self.initial_state_list.insert(ind, self.user_input[address["name"]][address["parameter"]])
                self.solution_state_list = copy.deepcopy(self.initial_state_list)
            self.initial_state = copy.deepcopy(self.user_input)
            self.solution_state = copy.deepcopy(self.initial_state)
        else:
            raise RuntimeError("No indexes found to create initial guess genes")

    def assign_values_from_solution(self, solution: list):
        self.solution_state_list = copy.deepcopy(solution)
        for ind in range(len(solution)):
            value = solution[ind]
            address = self.index_to_parameter[ind]
            self.solution_state[address["name"]][address["parameter"]] = value


class FitnessFunctionWrapper:
    def __init__(self, solution_handler: SolutionHandler):
        self.solution_handler = solution_handler

    def custom_fitness_function(self, ga_instance, solution, solution_idx):
        self.solution_handler.assign_values_from_solution(solution)
        solution_state = self.solution_handler.solution_state

        fitness_value = fitness_function(solution_state)

        print(fitness_value)
        return fitness_value
