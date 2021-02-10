 # TRAVELLING SALESMAN PROBLEM


import random
import time
import numpy
import functools
import matplotlib.pyplot as plt 
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

K = 20           # population size
THRESHOLD = 0.1  # mutation probability = 10%
PERCENT = 0.8
record_best_fitness = 0	
BREAKPOINT_GENERATION = 2*1e3


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

		distance += grid[src][dest]	

	return 1/distance


def count_distinct_elements(population):
	S = set()
	for individual in population:
		s = ""
		for el in individual:
			s += el
		S.add(s)
	return len(S)


def get_best_fitness(population):
	res = -1
	individual = None
	for el in population:
		temp_fitness = get_fitness(el)
		if res  < temp_fitness:
			res = temp_fitness
			individual = el
	return res , individual


def reproduce(x , y):
	start_index = random.randint(0 , len(x)-1)
	end_index = random.randint(0 , len(x)-1)
	if(end_index < start_index) :
		start_index , end_index = end_index , start_index

	child = [None] * len(x)
	vis = set()
	for i in range(start_index ,end_index+1):
		vis.add(x[i])
		child[i] = x[i]

	y_temp = list()
	for el in y:
		if el not in vis:
			vis.add(el)
			y_temp.append(el)

	y_temp_index = 0
	for i in range(0 , start_index):
		child[i] = y_temp[y_temp_index]
		y_temp_index += 1

	for i in range(end_index+1 , len(child)):
		child[i] = y_temp[y_temp_index]
		y_temp_index += 1

	return child




#Selection based on fitness as a criteria (Not completely random)
def random_selection(population):
    weights = list()
    fitnesses = list()
    sum = 0
    for el in population:
        temp_fitness = get_fitness(el)
        fitnesses.append(temp_fitness)
        sum += temp_fitness
  
    for el in fitnesses:
        weights.append(el/sum)

    fittest_individual = random.choices(population , weights)[0]
    return fittest_individual



def mutate(child):
	index1 = -1 ; index2 = -1;
	index1 = random.randint(0 , len(child)-1)
	index2 = random.randint(0 , len(child)-1)
	while index1 == index2:
		index2 = random.randint(0, len(child)-1)
	child[index1] , child[index2] = child[index2] , child[index1]
	return child



def genetic_algorithm(population):
	global record_best_fitness
	record_best_fitness = 0
	current_generation = 0
	fitnesses = list()
	generations = list()
	while True:
		new_population = list()
		while len(new_population) < K:
			x = random_selection(population)
			y = random_selection(population)
			child = reproduce(x , y)

			if(random.random() <= 	THRESHOLD):
				child = mutate(child)

			new_population.append(child)

		population = new_population
		best_fitness , best_individual = get_best_fitness(population)
		print("current_generation = " +str(current_generation)+" ; best_fitness = " + str(best_fitness) + " ; best_individual = " + str(best_individual))
		current_generation += 1
		record_best_fitness = max(record_best_fitness , best_fitness)
		print("record_best_fitness = " + str(record_best_fitness))

		fitnesses.append(best_fitness)
		generations.append(current_generation)

		if current_generation ==  BREAKPOINT_GENERATION:
			plt.plot(generations , fitnesses)
			return best_individual , best_fitness


		
		#print("count_distinct_elements = " + str(count_distinct_elements(population)))


if __name__ == "__main__":
	
	fitnesses = list()
	for iter in range(0 , 3):
		population = list()
		population = initialisation(population)
		best_individual , best_fitness = genetic_algorithm(population)
	plt.show()
	
