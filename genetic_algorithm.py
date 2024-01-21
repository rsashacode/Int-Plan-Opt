import pygad
import numpy as np


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
