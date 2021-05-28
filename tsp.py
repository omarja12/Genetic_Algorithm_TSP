#from charles.charles import Population, Individual ## Not used till now
#from charles.search import hill_climb, sim_annealing ## Not used till now
#from data.tsp_data import distance_matrix_1, swiss42
from random import choices ## Not used till now
from copy import deepcopy
from charles.charles import *
from data.tsp_data import *
from charles.crossover import *
from charles.mutation import *
from charles.selection import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def evaluate(self):
    """A simple objective function to calculate distances
    for the TSP problem.

    Returns:
        int: the total distance of the path
    """
    fitness = 0
    for i in range(len(self.representation)):
        # Calculates full distance, including from last city
        # to first, to terminate the trip
        fitness += self.distance_matrix[self.representation[i - 1]][self.representation[i]]

    return fitness 


def get_neighbours(self):
    """A neighbourhood function for the TSP problem. Switches
    indexes around in pairs.

    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation) - 1)]

    for count, i in enumerate(n):
        i[count], i[count + 1] = i[count + 1], i[count]

    n = [Individual(i) for i in n]
    return n


# Monkey patching
#Individual.fitness = evaluate
Individual.get_neighbours = get_neighbours


REPRESENTATION=None
SIZE=42
REPLACEMENT=False
VALID_SET=[i for i in range(42)]
DISTANCE_MATRIX=swiss42


indiv = Individual(representation=REPRESENTATION, size=SIZE, replacement=REPLACEMENT, valid_set=VALID_SET, distance_matrix=DISTANCE_MATRIX)


## Pseudo code of the standard generational GA

#1 create an initial population P of N=42 individuals 

SIZE=100 
OPTIM="min"
SOL_SIZE=42 
ELITE_SIZE=4
#SIZE=20
REPLACEMENT=False
VALID_SET=[i for i in range(42)]
DISTANCE_MATRIX=swiss42


pop = Population(
     size=SIZE,
     optim=OPTIM,
     elite_size=ELITE_SIZE,
     sol_size=SOL_SIZE,
     replacement=REPLACEMENT,
     valid_set=VALID_SET,
     distance_matrix=DISTANCE_MATRIX)



gens= 100
select = ranking_selection
crossover = cycle_co
mutate = inversion_mutation
co_p=0.8
mu_p=0.2

x = pop.evolve(gens, select, crossover, mutate, co_p, mu_p, False, False)




# pop.evolve(
#     gens = 100,
#     select = fps,
#     crossover=cycle_co, ## khasni nzid had zbl tani
#     mutate=inversion_mutation,
#     co_p=0.6,
#     mu_p=0.4,
#     elitism=False)

    


















