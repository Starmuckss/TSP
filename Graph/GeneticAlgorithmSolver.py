from RouteManager import RouteManager
from Route import Route

import numpy as np


class GeneticAlgorithmSolver:
    def __init__(self, cities, population_size=50, mutation_rate=0.2, tournament_size=10, elitism=False):
        self.cities = cities
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism = elitism

    def solve(self, rm):
        rm = self.evolve(rm)
        for i in range(100):
            rm = self.evolve(rm)
        return rm

    def evolve(self, routes):
        # YOUR CODE HERE
        return None

    def crossover(self, route_1, route_2):
        # YOUR CODE HERE
        return None

    def mutate(self, route):
        # YOUR CODE HERE
        return

    def tournament(self, routes):
        # YOUR CODE HERE
        return None
