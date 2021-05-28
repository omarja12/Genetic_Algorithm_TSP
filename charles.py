from random import shuffle, choice, sample, random, uniform
from operator import  attrgetter
import pandas as pd
import numpy as np
from data.tsp_data import *
from copy import deepcopy
import csv
import time
#from data.tsp_data import distance_matrix_1, swiss42


class Individual:
    def __init__(self, representation=None, size=None, replacement=True, valid_set=[i for i in range(100)], distance_matrix=swiss42):
        if representation == None:
            if replacement == True:
                self.representation = [choice(valid_set) for i in range(size)]
            elif replacement == False:
                self.representation = sample(valid_set, size)
        else:
            self.representation = representation
        self.fitness = self.evaluate(distance_matrix) 
     
    def evaluate(self, distance_matrix): 
        """A simple objective function to calculate distances
               for the TSP problem.
               Returns:
               int: the total distance of the path
        """
        fitness = 0
        for i in range(len(self.representation)):
            # Calculates full distance, including from last city
            # to first, to terminate the trip
            fitness += distance_matrix[self.representation[i - 1]][self.representation[i]] 
            
        return fitness

    def get_neighbours(self, func, **kwargs):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def __len__(self):
        return len(self.representation)

    def calculate_fitness(self):
        self.fitness = self.evaluate()

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value
        self.fitness = self.evaluate()

    def __repr__(self):
        return f"Individual(representation={self.representation}); Fitness: {self.fitness}"


class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.ordered_individuals = []
        self.size = size
        self.optim = optim
        self.gen = 1
        self.timestamp = int(time.time())
        self.elite_size = kwargs['elite_size']
        self.df = pd.DataFrame(columns=['Generation', 'Best Individual', 'Best Fitness'])
        for _ in range(size):
            self.individuals.append(
                Individual(size=kwargs["sol_size"], replacement=kwargs["replacement"], valid_set=kwargs["valid_set"], 
                           distance_matrix=kwargs["distance_matrix"]))
          
    def selection_elitism(self):
        """
        Returns
        -------
        result_selection : TYPE
            DESCRIPTION.
        """
        if self.optim == "max":
            ordered_individuals = sorted(self, key=lambda x: x.fitness, reverse = True)
        if self.optim == "min":
            ordered_individuals = sorted(self, key=lambda x: x.fitness, reverse = False)
        result_selection = [] 
        for i in range(self.elite_size):
            result_selection.append(ordered_individuals[i]) #self.        
        return result_selection 
      

    def fitness_sharing(self):
        individualFitness = []
        tmp = []
        sum_distances = 0
        for indiv1 in self.individuals:
            individualFitness.append(indiv1.fitness)
            sum_distances += indiv1.fitness 
            
        for i in range(self.size):
            nicheCount = 0
            for indiv2 in self.individuals:
                distance = abs(individualFitness[i] - indiv2.fitness)/sum_distances
                nicheCount += (1-(distance))
            #nicheCount  = nicheCount - 1
            tmp.append(individualFitness[i]*nicheCount)
        for i in range(self.size):
            self.individuals[i].fitness = tmp[i]
            return tmp[i]
            
    def evolve(self, gens, select, crossover, mutate, co_p, mu_p, elitism, fitness_sharing):
        """
        Parameters
        ----------
        gens : TYPE
            DESCRIPTION.
        select : TYPE
            DESCRIPTION.
        crossover : TYPE
            DESCRIPTION.
        mutate : TYPE
            DESCRIPTION.
        co_p : TYPE
            DESCRIPTION.
        mu_p : TYPE
            DESCRIPTION.
        elitism : TYPE
            DESCRIPTION.
        fitness_sharing : TYPE
            DESCRIPTION.
        Returns
        -------
        None.
        """
        
        iterations_fitness=[]
        for gen in range(gens):
            new_pop = []
            
            if fitness_sharing == True:
                self.fitness_sharing()
            
            # Check if elitism is set to true
            if elitism == True:
                new_pop = self.selection_elitism()
            
            while len(new_pop) < self.size:
                # Selecting two individuals
                parent1, parent2 = select(self), select(self)
                # Crossover
                if random() < co_p:
                    offspring1, offspring2 = crossover(parent1.representation, parent2.representation)
                else:
                    offspring1, offspring2 = parent1.representation, parent2.representation                
                # Mutation
                if random() < mu_p:
                    offspring1 = mutate(offspring1)
                if random() < mu_p:
                    offspring2 = mutate(offspring2)
                    
                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))
            
            self.log(elitism)
            self.individuals = new_pop
            self.gen +=1
            
            shortest_path = min(self, key=lambda x: x.fitness)
            iterations_fitness.append(shortest_path.fitness)
            
            print(f'Best Individual: {min(self, key=attrgetter("fitness"))}')
        return(shortest_path, iterations_fitness)
    
    def log(self, elitism):
        if self.optim == "min":
            if elitism == False:
                
                shortest_path = min(self, key=lambda x: x.fitness)
                data = [self.gen, shortest_path, shortest_path.fitness]
                self.df.loc[self.gen-1] = data
                self.df.to_csv(f'tournament_cycle_inversion_swiss42{self.timestamp}.csv', mode='w', index=False, header=True) 
                
            if elitism == True:
                
                shortest_path = min(self, key=lambda x: x.fitness)
                data = [self.gen, shortest_path, shortest_path.fitness]
                self.df.loc[self.gen-1] = data
                self.df.to_csv(f'Elitism_tournament_cycle_inversion_swiss42{self.timestamp}.csv', mode='w', index=False, header=True) 
          

    def __len__(self):
        return len(self.individuals)
    
    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, individual_size={len(self.individuals[0])})"
