import copy

import requests

from logs.log import logger
from configuration.fitness_function import fitness_function
from input_management import InputManager


class SolutionHandler:
    """
    Solution handler. Transforms genes to a readable format and initialises them.

    """
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
        """
        Initialise the genes based on the input.

        :return:
        """
        if self.input_manager.indexes_assigned:
            for ind in self.index_to_parameter:
                address = self.index_to_parameter[ind]
                self.initial_state_list.insert(ind, self.user_input[address["name"]][address["parameter"]])
                self.solution_state_list = copy.deepcopy(self.initial_state_list)
            self.initial_state = copy.deepcopy(self.user_input)
            self.solution_state = copy.deepcopy(self.initial_state)
        else:
            logger.error("No indexes found to create initial guess genes")
            raise RuntimeError("No indexes found to create initial guess genes")

    def assign_values_from_solution(self, solution: list):
        """
        Update the genes from the solution provided by the optimizer.

        :param solution:
        :return:
        """
        self.solution_state_list = copy.deepcopy(solution)
        for ind in range(len(solution)):
            value = solution[ind]
            address = self.index_to_parameter[ind]
            self.solution_state[address["name"]][address["parameter"]] = value


class FitnessFunctionWrapper:
    """
    Wrapper to handle calls of fitness_functions

    """
    def __init__(self, solution_handler: SolutionHandler, external_api: str = None):
        self.solution_handler = solution_handler
        self.external_api = external_api

    def custom_fitness_function(self, ga_instance, solution, solution_idx):
        """
        Custom fitness function provided as configuration.

        :param ga_instance:
        :param solution:
        :param solution_idx:
        :return:
        """
        self.solution_handler.assign_values_from_solution(solution)
        solution_state = self.solution_handler.solution_state

        fitness_value = fitness_function(solution_state)

        print(fitness_value)
        return fitness_value

    def call_api(self, ga_instance, solution, solution_idx):
        """
        Fitness function provided as external endpoint.

        :param ga_instance:
        :param solution:
        :param solution_idx:
        :return:
        """
        if self.external_api is None:
            logger.error("Unable to call api without external api address")
            raise ValueError('Unable to call api without external api address')

        self.solution_handler.assign_values_from_solution(solution)
        solution_state = self.solution_handler.solution_state

        fitness_value = requests.post(self.external_api, data=solution_state)
        logger.debug(fitness_value)
        return fitness_value
