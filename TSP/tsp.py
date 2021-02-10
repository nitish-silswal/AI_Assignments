# TRAVELLING SALESMAN PROBLEM
# Complete reproduce(x , y) function

import random
import time
import numpy
import functools
random.seed(None)
INF = 1e4

grid = [[0,INF,INF,INF,INF,INF,0.15,INF,INF,0.2,INF,0.12,INF,INF], #A
		[INF,0,INF,INF,INF,INF,INF,0.19,0.4,INF,INF,INF,INF,0.13], #B
		[INF,INF,0,0.6,0.22,0.4,INF,INF,0.2,INF,INF,INF,INF,INF],  #C
		[INF,INF,0.6,0,INF,0.21,INF,INF,INF,INF,0.3,INF,INF,INF],  #D
		[INF,INF,0.22,INF,0,INF,INF,INF,0.18,INF,INF,INF,INF,INF], #E
		[INF,INF,0.4,0.21,INF,0,INF,INF,INF,INF,0.37,0.6,0.26,0.9],#F
		[0.15,INF,INF,INF,INF,INF,0,INF,INF,INF,0.55,0.18,INF,INF],#G
		[INF,0.19,INF,INF,INF,INF,INF,0,INF,0.56,INF,INF,INF,0.17],#H
		[INF,0.4,0.2,INF,0.18,INF,INF,INF,0,INF,INF,INF,INF,0.6], #I
		[0.2,INF,INF,INF,INF,INF,INF,0.56,INF,0,INF,0.16,INF,0.5], #J
		[INF,INF,INF,0.3,INF,0.37,0.55,INF,INF,INF,0,INF,0.24,INF], #K
		[0.12,INF,INF,INF,INF,0.6,0.18,INF,INF,0.16,INF,0,0.4,INF], #L
		[INF,INF,INF,INF,INF,0.26,INF,INF,INF,INF,0.24,0.4,0,INF], #M
		[INF,0.13,INF,INF,INF,0.9,INF,0.17,0.6,0.5,INF,INF,INF,0] #N
]

K = 20              # population size
THRESHOLD = 0.3   # mutation probability = 10%
PERCENT = 0.8
best_fitness = 0	
min_distance = INF

def print_grid(grid):
	for row in grid:
		for el in row:
			print(el , end = "  ")
		print()


def initialisation(population):
	string = "ABCDEFGHIJKLMN"
	individual = list()
	for el in string:
		individual.append(el)
	for i in range(K):
		population.append(individual)
	return population


def get_fitness(individual):
	distance = 0 ; src = -1 ; dest = -1;
	for i in range(len(individual)):
		if i == len(individual)-1:
			src = ord(individual[len(individual)-1]) - ord('A') ; dest = ord(individual[0]) - ord('A')
		else:	
			src = ord(individual[i]) - ord('A') ; dest = ord(individual[i+1]) - ord('A')

		if(grid[src][dest] == INF):
			return 0
		distance += grid[src][dest]		
	return 1/(distance+1)


def count_distinct_elements(individual):
	S = set()
	for el in individual:
		S.add(el)
	return len(S)

def all_same(individual):
	for i in range(len(individual)-1):
		if individual[i] != individual[i+1]:
			return False
	return True

def get_distance_from_fitness(fitness):
	if fitness == 0: return INF
	return 1/fitness - 1


def mean_fitness(population):
	sum = 0
	for el in population:
		sum += get_fitness(el)
	return sum/len(population)

def get_best_fitness(population):
	res = -1
	individual = None
	for el in population:
		if res  < get_fitness(el):
			res = get_fitness(el)
			individual = el
	return res , individual


def reproduce(x , y):
	pass


#Selection based on fitness as a criteria (Not completely random)
def random_selection(population):
    weights = list()
    fitnesses = list()
    sum = 0
    for el in population:
        temp_fitness = get_fitness(el)
        fitnesses.append(temp_fitness)
        sum += temp_fitness

    if sum == 0:
    	return population[random.randint(0, len(population)-1)]

    for el in fitnesses:
        weights.append(el / sum)

    fittest_individual = random.choices(population , weights)[0]
    return fittest_individual

def mutate(child):
	index1 = -1 ; index2 = -1;
	index1 = random.randint(0 , len(child)-1)
	index2 = random.randint(0 , len(child)-1)
	while index1 == index2:
		index2 = random.randint(0, len(child)-1)
	temp = child[index1]
	child[index1] = child[index2]
	child[index2] = temp
	return child



def genetic_algorithm(population):
	current_generation = 0
	while True:
		new_population = list()
		while len(new_population) < K:
			x = random_selection(population)
			y = random_selection(population)

			child = reproduce(x , y)
			if(random.random() <= 	THRESHOLD):
				child = mutate(child)

			new_population.append(child)

		current_generation += 1
		population = new_population
		best_fitness , best_individual = get_best_fitness(population)
		print("current_generation = " + str(current_generation) + " ; " + "best_fitness = " + str(best_fitness) + " ; best_individual" +  str(best_individual) + " ; count_distinct_elements = " + str(count_distinct_elements(best_individual)))

		if(all_same(best_individual)):
			return best_individual , best_fitness

		time.sleep(0.2)

if __name__ == "__main__":
	population = list()
	population = initialisation(population)
	print("Initial population :-" )
	print(population)
	best_individual , best_fitness = genetic_algorithm(population)
	print("best_fitness = "  + str(best_fitness) , end = " ; ")
	print("min_distance = "  + str(get_distance_from_fitness(best_fitness)))
