import copy

import numpy as np
import pygad

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

    # ToDo Check restrictions


class Optimizer:
    pass


class GeneticOptimizer(Optimizer):
    def __init__(self,
                 fitness_function: callable,
                 num_genes: int,
                 num_generations: int,
                 **args_to_pygad
                 ):
        self.fitness_function = fitness_function
        self.num_genes = num_genes
        self.num_generations = num_generations

        if np.array(args_to_pygad["initial_population"]).ndim != 2:
            initial_pop = [args_to_pygad["initial_population"] for i in range(self.num_generations)]
            args_to_pygad["initial_population"] = initial_pop
        self.ga_instance = pygad.GA(
            fitness_func=self.fitness_function,
            num_genes=self.num_genes,
            num_generations=self.num_generations,
            **args_to_pygad
        )

    def optimize(self):
        self.ga_instance.run()
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution()
        return solution, solution_fitness, solution_idx
