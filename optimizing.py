import copy
import os
import pygad
import datetime
import json

from solution import FitnessFunctionWrapper
from input_management import InputManager
from abc import ABC, abstractmethod


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


class Optimizer(ABC):
    @abstractmethod
    def optimize(self):
        raise NotImplemented("Please implement method")

    @abstractmethod
    def save_results(self):
        raise NotImplemented("Please implement method")


class GeneticOptimizer(Optimizer):
    def __init__(self,
                 solution_handler: SolutionHandler,
                 args_to_pygad: dict,
                 external_fitness_function: bool = False
                 ):

        self.solution_handler = solution_handler

        cpu_count = os.cpu_count()
        self.solution_handler.initialise_genes()
        f_wrapper = FitnessFunctionWrapper(self.solution_handler)
        initial_population = self.solution_handler.initial_state_list

        initial_pop = [initial_population for i in range(args_to_pygad['num_generations'])]
        gene_space = solution_handler.input_manager.gene_space
        gene_type = solution_handler.input_manager.gene_type
        if not external_fitness_function:
            fitness_function = f_wrapper.custom_fitness_function
        else:
            fitness_function = f_wrapper.call_api
        self.ga_instance = pygad.GA(
            fitness_func=fitness_function,
            num_genes=len(initial_population),
            num_generations=args_to_pygad['num_generations'],
            num_parents_mating=args_to_pygad['num_parents_mating'],
            sol_per_pop=cpu_count - 1,
            initial_population=initial_pop,
            parent_selection_type=args_to_pygad['parent_selection_type'],
            keep_parents=args_to_pygad['keep_parents'],
            crossover_type=args_to_pygad['crossover_type'],
            mutation_type=args_to_pygad['mutation_type'],
            mutation_percent_genes=args_to_pygad['mutation_percent_genes'],
            mutation_probability=args_to_pygad['mutation_probability'],
            parallel_processing=[args_to_pygad['parallel_method'], cpu_count],
            gene_space=gene_space,
            gene_type=gene_type,
            random_seed=42,
        )
        ...
        # ToDo check if unsuccessful init

        self.solution = None
        self.solution_fitness = None
        self.solution_idx = None

        self.result = None
        self.result_list = None

    def optimize(self):
        self.ga_instance.run()
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution()

        self.solution = solution
        self.solution_fitness = solution_fitness
        self.solution_idx = solution_idx

        self.solution_handler.assign_values_from_solution(solution)

        self.result = self.solution_handler.solution_state
        self.result_list = [self.result[key] for key in self.result.keys()]

        return solution, solution_fitness, solution_idx

    def save_results(self):
        now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        if not os.path.exists('./results'):
            os.mkdir('./results')
        result_to_file = {
            'best_fitness': self.solution_fitness,
            'best_result': self.result_list
        }
        with open(f'./results/{now}.json', 'w') as f:
            json.dump(result_to_file, f)
