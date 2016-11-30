
'''
This is a genetic algorithm to generate names _close_ to the given name
But sufficiently different to be used as NPC names :)
'''

import name_matcher as nm
import numpy as np

class GeneticAlgorithm:

    def __init__(self, crossover_rate, mutation_rate, population_size, chromosome_size_range, fitness):
        self.fitness = fitness
        self.cr = crossover_rate
        self.mr = mutation_rate
        self.population = []
        self.fitnesses = []
        for i in range(population_size):
            size = chromosome_size_range[np.random.randint(len(chromosome_size_range))]
            chromo = []
            for j in range(size):
                g = np.random.randint(0,44)
                chromo.append(g)
            self.population.append(chromo)
            self.fitnesses.append(0)
        self.evaluate_fitness()
        print(self.population)

    # To move a generation ahead, the following steps need to be performed:
    # Generate new chromosomes based on roulette wheel selection
    # Mutate said chromosomes
    # Evaluate fitnesses
    # Terminate if fitness over threshold, else continue the cycle

    def main_loop(self, generations = 1000000, fitness_thresh = 99):
        '''
        Main loop with two possible termination conditions
        Returns the entire population. Converted to IPA.
        '''
        
        gencount = 0
        fitness_max = 0
        while gencount<generations and fitness_max<fitness_thresh:
            gencount += 1
            print(gencount)
            self.mate()
            self.mutate()
            self.evaluate_fitness()
            fitness_max = max(self.fitnesses)
            print(fitness_max)
        return self.population
        
    def __weighted_random_choice(self):
        '''
        Implement roulette wheel selection
        '''
        max = sum(self.fitnesses)
        pick = np.random.uniform(0, max)
        current = 0
        for i in range(len(self.population)):
            current += self.fitnesses[i]
            if current > pick:
                return self.population[i]

    def mutate(self):
        for chromo in self.population:
            for i in range(len(chromo)):
                if(np.random.uniform(0,1) < self.mr):
                    chromo[i] = np.random.randint(0,44)

    def mate(self):
        '''
        This returns a new set of chromosomes based on roulette wheel selection
        '''
        new_pop = []
        for i in range(len(self.population)):
            chromo = self.__weighted_random_choice()
            chromo2 = chromo
            if np.random.uniform(0,1) < self.cr:
                chromo2 = self.__weighted_random_choice()
            new_chromo = []
            crossover = np.random.randint(min(len(chromo), len(chromo2)))
            new_chromo_length = len(chromo[:crossover]) + len(chromo2[crossover:])
            for x in range(new_chromo_length):
                if x<crossover:
                    new_chromo.append(chromo[x])
                else:
                    new_chromo.append(chromo2[x])

            new_pop.append(new_chromo)
        self.population = new_pop
        
    
    def evaluate_fitness(self):
        for i in range(len(self.population)):
            self.fitnesses[i] = self.fitness(self.population[i])


            
n_m = nm.NameMatcher('comparison_matrix', 0.15)

def fn(string):
    converted_string = [nm.symlist[i] for i in string]
    return n_m.match(['d', '@', 'n', 'j', 'e', 'l'], converted_string)*2/(len(converted_string) + 5)
                
    

def gaTest():
    ga = GeneticAlgorithm(0.7, 0.1, 200, [6,7,8], fn)
    ga.main_loop(fitness_thresh = 0.95)
    for i in range(len(ga.population)):
        converted_string = [nm.symlist[j] for j in ga.population[i]]
        if ga.fitnesses[i] >= 0.8:
            print(ga.fitnesses[i], end = ' : ')
            print(' '.join(converted_string))

            

gaTest()
