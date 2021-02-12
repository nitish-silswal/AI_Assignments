import random
class NQueens(object):

    K = 20
    MAX_FITNESS = 29
    THRESHOLD = 0.10

    def __init__(self):
        super(NQueens, self).__init__()
        self.population = list()
        self.initialisation()

    def initialisation(self):
        self.population = [x for x in [(str(random.randint(1 , 8)))*8]]*NQueens.K

    def get_fitness_nqueens(self , individual):
        conflicting_pairs = 0
        for i in range(len(individual)):
            for j in range(i+1 ,len(individual)):
                if(individual[i] == individual[j]) or (abs(i-j) == abs(int(individual[i]) - int(individual[j]))):
                    conflicting_pairs += 1
        return (NQueens.MAX_FITNESS - conflicting_pairs)


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

    def get_mean_fitness_nqueens(self):
        sum = 0
        for el in self.population:
            sum += self.get_fitness_nqueens(el)    
        return sum/len(self.population)

    def genetic_algorithm_nqueens(self):
        current_generation = 0
        while True:   
            new_population = list()
            while(len(new_population) < NQueens.K):
                x = self.random_selection_nqueens()
                y = self.random_selection_nqueens()             
                
                child = self.reproduce_nqueens(x , y)
                if(random.random() <= NQueens.THRESHOLD):
                    child = self.mutate_nqueens(child)

                if(self.get_fitness_nqueens(child) == NQueens.MAX_FITNESS):
                    return child , current_generation

                new_population.append(child)
            self.population = new_population
            current_generation += 1
            print("current_generation = " + str(current_generation) + " ; " + "mean_fitness = " + str(self.get_mean_fitness_nqueens()) )



if __name__ == "__main__":
    p = NQueens()
    fittest_individual , generation_number = p.genetic_algorithm_nqueens()
    print()
    print("============+=================+==============+==============+===============+")
    print("Fittest individual : " + '"' + fittest_individual + '"')
    print("Genrations produced : " + str(generation_number))
    print("============+=================+==============+==============+===============+") 
