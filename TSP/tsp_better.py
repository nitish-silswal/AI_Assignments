# TRAVELLING SALESMAN PROBLEM -> Optimised
import random
import time
import numpy
import functools
import matplotlib.pyplot as plt

random.seed(None)
INF = 1e4

grid = [
    [0, INF, INF, INF, INF, INF, 0.15, INF, INF, 0.2, INF, 0.12, INF, INF],  # A
    [INF, 0, INF, INF, INF, INF, INF, 0.19, 0.4, INF, INF, INF, INF, 0.13],  # B
    [INF, INF, 0, 0.6, 0.22, 0.4, INF, INF, 0.2, INF, INF, INF, INF, INF],  # C
    [INF, INF, 0.6, 0, INF, 0.21, INF, INF, INF, INF, 0.3, INF, INF, INF],  # D
    [INF, INF, 0.22, INF, 0, INF, INF, INF, 0.18, INF, INF, INF, INF, INF],  # E
    [INF, INF, 0.4, 0.21, INF, 0, INF, INF, INF, INF, 0.37, 0.6, 0.26, 0.9],  # F
    [0.15, INF, INF, INF, INF, INF, 0, INF, INF, INF, 0.55, 0.18, INF, INF],  # G
    [INF, 0.19, INF, INF, INF, INF, INF, 0, INF, 0.56, INF, INF, INF, 0.17],  # H
    [INF, 0.4, 0.2, INF, 0.18, INF, INF, INF, 0, INF, INF, INF, INF, 0.6],  # I
    [0.2, INF, INF, INF, INF, INF, INF, 0.56, INF, 0, INF, 0.16, INF, 0.5],  # J
    [INF, INF, INF, 0.3, INF, 0.37, 0.55, INF, INF, INF, 0, INF, 0.24, INF],  # K
    [0.12, INF, INF, INF, INF, 0.6, 0.18, INF, INF, 0.16, INF, 0, 0.4, INF],  # L
    [INF, INF, INF, INF, INF, 0.26, INF, INF, INF, INF, 0.24, 0.4, 0, INF],  # M
    [INF, 0.13, INF, INF, INF, 0.9, INF, 0.17, 0.6, 0.5, INF, INF, INF, 0],  # N
]

K = 20  # population size
TOURNAMENT_SIZE = 2
THRESHOLD = 0.20  # mutation probability = 10%
PERCENT = 0.8
record_best_fitness = 0
BREAKPOINT_GENERATION = 2 * 1e3


class TSP_better(object):
    """docstring for TSP"""

    def __init__(self):
        super(TSP_better, self).__init__()
        self.population = self.initialisation_TSP()

    def initialisation_TSP(self):
        return [list("ABCDEFGHIJKLMN")] * 20

    def get_distance_TSP(self, individual):
        distance = 0
        src = -1
        dest = -1
        for i in range(len(individual)):
            if i == len(individual) - 1:
                src = ord(individual[len(individual) - 1]) - ord("A")
                dest = ord(individual[0]) - ord("A")
            else:
                src = ord(individual[i]) - ord("A")
                dest = ord(individual[i + 1]) - ord("A")
            distance += grid[src][dest]
        return distance

    def get_fitness_TSP(self, individual):
        distance = 0
        src = -1
        dest = -1
        for i in range(len(individual)):
            if i == len(individual) - 1:
                src = ord(individual[len(individual) - 1]) - ord("A")
                dest = ord(individual[0]) - ord("A")
            else:
                src = ord(individual[i]) - ord("A")
                dest = ord(individual[i + 1]) - ord("A")
            distance += grid[src][dest]
        return 1 / distance

    def get_best_fitness_and_individual_TSP(self):
        best_fitness = -1
        best_individual = None
        for el in self.population:
            current_fitness = self.get_fitness_TSP(el)
            if current_fitness >= best_fitness:
                best_fitness = current_fitness
                best_individual = el
        return best_fitness, best_individual

    def count_distint(self):
        S = set()
        for ind in self.population:
            ss = ""
            for el in ind:
                ss += el
            S.add(ss)
        return len(S)

    def reproduce_TSP(self, x, y):
        start_index = random.randint(0, len(x) - 1)
        end_index = random.randint(0, len(x) - 1)
        if end_index < start_index:
            start_index, end_index = end_index, start_index

        child = [None] * len(x)
        vis = set()
        for i in range(start_index, end_index + 1):
            vis.add(x[i])
            child[i] = x[i]

        y_temp = list()
        for el in y:
            if el not in vis:
                vis.add(el)
                y_temp.append(el)

        y_temp_index = 0
        for i in range(0, start_index):
            child[i] = y_temp[y_temp_index]
            y_temp_index += 1

        for i in range(end_index + 1, len(child)):
            child[i] = y_temp[y_temp_index]
            y_temp_index += 1

        return child

    def random_selection_TSP(self):
        participants = random.sample(self.population, TOURNAMENT_SIZE)
        best_individual = None
        best_fitness = 0
        for el in participants:
            current_fitness = self.get_fitness_TSP(el)
            if current_fitness > best_fitness:
                best_fitness = current_fitness
                best_individual = el
        return best_individual

    def mutate_TSP(self, child):
        iterations = 0
        current_fitness = self.get_fitness_TSP(child)
        while current_fitness >= self.get_fitness_TSP(child) and iterations < 100:
            index1 = random.randint(0, len(child) - 1)
            index2 = random.randint(0, len(child) - 1)
            child[index1], child[index2] = child[index2], child[index1]
            iterations += 1
        return child

    def genetic_algorithm_TSP(self):
        global record_best_fitness
        record_best_fitness = 0
        current_generation = 0
        fitnesses = list()
        generations = list()
        while True:
            new_population = list()
            while len(new_population) < K:
                x = self.random_selection_TSP()
                y = self.random_selection_TSP()
                child = self.reproduce_TSP(x, y)

                if random.random() <= THRESHOLD:
                    child = self.mutate_TSP(child)

                new_population.append(child)

            self.population = new_population
            best_fitness, best_individual = self.get_best_fitness_and_individual_TSP()
            print(
                "current_generation = "
                + str(current_generation)
                + " ; best_fitness = "
                + str(best_fitness)
                + " ; best_individual = "
                + str(best_individual)
            )
            current_generation += 1
            record_best_fitness = max(record_best_fitness, best_fitness)
            print(
                "record_best_fitness = "
                + str(record_best_fitness)
                + " ; count_distint = "
                + str(self.count_distint())
            )

            fitnesses.append(best_fitness)
            generations.append(current_generation)

            if current_generation == BREAKPOINT_GENERATION:
                plt.plot(generations, fitnesses, color="blue")
                return best_individual, best_fitness


if __name__ == "__main__":
    plt.title("TSP ORIGINAL V/S IMPROVED COMPARISION")
    plt.xlabel("CURRENT GENERATION")
    plt.ylabel("BEST FITNESS PER GENERATION")
    for _ in range(5):
        p = TSP_better()
        p.genetic_algorithm_TSP()
    plt.show()
