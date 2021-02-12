import random
import functools
class NQueens_Better(object):

    K = 20
    MAX_FITNESS = 29
    THRESHOLD = 0.15
    PERCENT = 0.80

    def __init__(self):
        super(NQueens_Better, self).__init__()
        self.population = list()
        self.initialisation()

    def initialisation(self):
        self.population = [x for x in [(str(random.randint(1 , 8)))*8]]*NQueens_Better.K

    def get_fitness_nqueens(self , individual):
        conflicting_pairs = 0
        for i in range(len(individual)):
            for j in range(i+1 ,len(individual)):
                if(individual[i] == individual[j]) or (abs(i-j) == abs(int(individual[i]) - int(individual[j]))):
                    conflicting_pairs += 1
        return (NQueens_Better.MAX_FITNESS - conflicting_pairs)


    def random_selection_nqueens(self):
        weights = list()
        fitnesses = list()
        sum = 0
        for el in self.population:
            temp_fitness = self.get_fitness_nqueens(el)
            fitnesses.append(temp_fitness)
            sum += temp_fitness

        for el in fitnesses:
            weights.append(el / sum)

        fittest_individual = random.choices(self.population , weights)[0]
        return fittest_individual

    def reproduce_nqueens(self,x , y):
        length = random.randint(0 , 8)
        if length == 0:
            return y
        elif length == 8:
            return x
        return x[0 : length] + "" + y[length : ]

    def mutate_nqueens(self , child):
        new_value = random.randint(1 , 8)
        change_index = random.randint(0 , 7)
        return child[0:change_index] + str(new_value) + child[change_index+1 : ]

    def mean_and_best_fitness_nqueens(self):
        sum = 0 ; best_fitness = 0
        for el in self.population:
            current_fitness = self.get_fitness_nqueens(el)
            best_fitness = max(best_fitness , current_fitness)
            sum += current_fitness
        return (sum / len(self.population)) , best_fitness

    def compare_nqueens(self , individual1 , individual2):
        return (self.get_fitness_nqueens(individual2) - self.get_fitness_nqueens(individual1))

    def modify_population_nqueens(self,new_population):
        new_population.sort(key = functools.cmp_to_key(self.compare_nqueens))
        return_population = new_population[0 : int(NQueens_Better.PERCENT * NQueens_Better.K)]

        while len(return_population) < NQueens_Better.K:
            rand_index = random.randint(0 , NQueens_Better.K - 1)
            return_population.append(self.population[rand_index])
            
        return return_population

    def genetic_algorithm_nqueens(self):
        current_generation = 0
        while True:   
            new_population = list()
            while(len(new_population) < NQueens_Better.K):
                x = self.random_selection_nqueens()
                y = self.random_selection_nqueens()             
                
                child = self.reproduce_nqueens(x , y)
                if(random.random() <= NQueens_Better.THRESHOLD):
                    child = self.mutate_nqueens(child)

                if(self.get_fitness_nqueens(child) == NQueens_Better.MAX_FITNESS):
                    return child , current_generation

                new_population.append(child)
            self.population = self.modify_population_nqueens(new_population)
            current_generation += 1
            mean_fitness , best_fitness = self.mean_and_best_fitness_nqueens()
            print("current_generation = " + str(current_generation) + " ; mean_fitness_this_gen = " + str(round(mean_fitness , 1)) + " ; best_fitness_this_gen = " + str(best_fitness))



if __name__ == "__main__":
    p = NQueens_Better()
    fittest_individual , generation_number = p.genetic_algorithm_nqueens()
    print()
    print("============+=================+==============+==============+===============+")
    print("Fittest individual : " + '"' + fittest_individual + '"')
    print("Generations produced : " + str(generation_number))
    print("============+=================+==============+==============+===============+") 



