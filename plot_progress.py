# -*- coding: utf-8 -*-
"""
Created on Sat May  1 18:11:33 2021

@author: user
"""
from charles.charles import *
from data.tsp_data import *
from charles.crossover import *
from charles.mutation import *
from charles.selection import *
from copy import deepcopy
import matplotlib.pyplot as plt


def geneticAlgorithmPlot(size, optim, elite_size, sol_size, replacement, valid_set, distance_matrix,
                         gens, select = ranking_selection, crossover = cycle_co, mutate = inversion_mutation, 
                         co_p=0.8, mu_p=0.2, elitism=False, fitness_sharing=False):
    """
    Parameters
    ----------
    size : TYPE
        DESCRIPTION.
    optim : TYPE
        DESCRIPTION.
    elite_size : TYPE
        DESCRIPTION.
    sol_size : TYPE
        DESCRIPTION.
    replacement : TYPE
        DESCRIPTION.
    valid_set : TYPE
        DESCRIPTION.
    distance_matrix : TYPE
        DESCRIPTION.
    gens : TYPE
        DESCRIPTION.
    select : TYPE, optional
        DESCRIPTION. The default is ranking_selection.
    crossover : TYPE, optional
        DESCRIPTION. The default is cycle_co.
    mutate : TYPE, optional
        DESCRIPTION. The default is inversion_mutation.
    co_p : TYPE, optional
        DESCRIPTION. The default is 0.8.
    mu_p : TYPE, optional
        DESCRIPTION. The default is 0.2.
    elitism : TYPE, optional
        DESCRIPTION. The default is False.
    fitness_sharing : TYPE, optional
        DESCRIPTION. The default is False.
    Returns
    
    -------
    None.
    """    
    pop1 = Population(size, optim, **{"elite_size":elite_size, "sol_size":sol_size, "replacement":replacement,
                                      "valid_set":valid_set, "distance_matrix": distance_matrix})
    pop2 = deepcopy(pop1)
    tmp1 = pop1.evolve(gens, select, crossover, mutate, co_p, mu_p, False, False)
    tmp2 = pop2.evolve(gens, select, crossover, mutate, co_p, mu_p, True, False)
    fig, ax = plt.subplots()
    ax.plot(tmp1[1], '-b', label='Without Elitism')
    ax.plot(tmp2[1], '--r', label='With Elitism')
    ax.legend()
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()
    

SIZE=50 #750 
OPTIM="min" 
SOL_SIZE=42 
ELITE_SIZE=6
#SIZE=20
REPLACEMENT=False
VALID_SET=[i for i in range(42)]
DISTANCE_MATRIX=swiss42
GENS=750#250
co_p=0.8 #0.8
mu_p=0.2 # 0.25
ELISTISM=False
FITNESS_SHARING=False
#Elitism_tournament_pmx_inversion
SELECT=tournament_selection #tournament_selection #ranking_selection ## tournament ##fps
CROSSOVER=cycle_co        #order_1_crossover #pmx_crossover ## cycle_co
MUTATE=inversion_mutation    #shuffle_mutation #swap_mutation #inversion_mutation    
    
geneticAlgorithmPlot(SIZE, OPTIM, ELITE_SIZE, SOL_SIZE, 
                         REPLACEMENT, VALID_SET, DISTANCE_MATRIX,
                         GENS, SELECT, CROSSOVER, MUTATE, 
                         co_p, mu_p, False, False)