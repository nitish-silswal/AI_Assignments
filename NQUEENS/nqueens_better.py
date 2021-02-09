# Code for NQUEENS as optimized implementation of Genetic Algorithm 

import random
import time
import numpy
import functools

random.seed(None)
K = 20              # population size
MAX_FITNESS = 29
THRESHOLD = 0.20    # mutation probability = 20%
PERCENT = 0.8

def initialisation(population):
    start_number = random.randint(1 , 8)
    s = ""
    for i in range(8):
        s += str(start_number)
    for i in range(K):    
        population.append(s)


def get_fitness(individual):
    conflicting_pairs = 0
    for i in range(len(individual)):
        for j in range(i+1 ,len(individual)):
            if(individual[i] == individual[j]) or (abs(i-j) == abs(int(individual[i]) - int(individual[j]))):
                conflicting_pairs += 1
    
    return (MAX_FITNESS - conflicting_pairs)


def random_selection(population):
    weights = list()
    fitnesses = list()
    sum = 0
    for el in population:
        temp_fitness = get_fitness(el)
        fitnesses.append(temp_fitness)
        sum += temp_fitness

    for el in fitnesses:
        weights.append(el / sum)

    fittest_individual = random.choices(population , weights)[0]
    return fittest_individual




def reproduce(x , y):
    length = random.randint(0 , 8)
    if length == 0:
        return y
    elif length == 8:
        return x
    return x[0 : length] + "" + y[length : ]


def mutate(child):
    new_value = random.randint(1 , 8)
    change_index = random.randint(0 , 7)
    return child[0:change_index] + str(new_value) + child[change_index+1 : ]


def get_mean_fitness(population):
    sum = 0
    for el in population:
        sum += get_fitness(el)    
    return sum/len(population)
    

def get_distinct_elements(population):
    S = set()
    for el in population:
        S.add(el)
    return len(S)

def compare(chrom1,chrom2):
    return (get_fitness(chrom2)-get_fitness(chrom1))

def modify_population(population , new_population):
    new_population.sort(key = functools.cmp_to_key(compare ))
    return_population = new_population[0 : int(PERCENT * K)]

    while len(return_population) < K:
        rand_index = random.randint(0 , K - 1)
        return_population.append(population[rand_index])
        
    return return_population


def genetic_algorithm(population):
    current_generation = 0
    while True:   
        new_population = list()
        while(len(new_population) < K):
            x = random_selection(population)
            y = random_selection(population)
            
            
            child = reproduce(x , y)
            if(random.random() <= THRESHOLD):
                child = mutate(child)

            if(get_fitness(child) == MAX_FITNESS):
                return child , current_generation

            new_population.append(child)

        population = modify_population(population ,new_population)
        current_generation += 1
        print("current_generation = " + str(current_generation) + " ; " + "mean_fitness = " + str(get_mean_fitness(population)))
        
        

    print("current_generation = " + str(current_generation))


def get_average(arr):
    sum = 0
    for el in arr:
        sum += el
    return sum /len(arr)


# 5 iterations of this algo -> Then compute the average number of generations produced to reach the final solution
if __name__== "__main__": 
    iterations = 1
    generations_per_iteration = list()    
    for _ in range(iterations):
        population = list()
        initialisation(population)
        print("initial population :-")
        print(population)
        best_individual , gen = genetic_algorithm(population)
        # print(best_individual)
        generations_per_iteration.append(gen)

    print()
    print("Generations produced per iteration = " , end = " ")
    print(generations_per_iteration)
    print("Average number of generations produced per iteration = " + str(get_average(generations_per_iteration)))


#[255, 326, 3227, 267, 184]  ; Average generations required = 851.8
