from random import sample
from operator import attrgetter
import random
import numpy as np



def fps_1(population):
    """Fitness proportionate selection implementation.
    Args:
        population (Population): The population we want to select from.
    Returns:
        Individual: selected individual.
    """ 
    # Sum total fitnesses
    total_fitness_max = sum([i.fitness for i in population])
    total_fitness_min = sum([1/i.fitness for i in population])
    #
    selection_probability_max = [i.fitness/total_fitness_max for i in population]
    selection_probability_min = [(1.0/i.fitness)/total_fitness_min for i in population]
    #    
    if population.optim == "max":
        return population[np.random.choice(population.size, p=selection_probability_max)]
    #
    if population.optim == "min":
        return population[np.random.choice(population.size, p=selection_probability_min)]  
    #
    else:
        raise Exception("No optimization specified")
        
def fps_2(population):
    """Fitness proportionate selection implementation.
    Args:
        population (Population): The population we want to select from.
    Returns:
        Individual: selected individual.
    """ 
    # Sum total fitnesses
    total_fitness_max = sum([i.fitness for i in population])
    total_fitness_min = sum([1.0/i.fitness for i in population])    
    # Get a 'position' on the wheel
    position = 0
    spin = random.random()
    # 
    if population.optim == "max":
        # Find individual in the position of the spin
        for individual in population:  
              position += individual.fitness
              if spin <= position/total_fitness_max:
                  return individual
    if population.optim == "min":
        # Find individual in the position of the spin
        for individual in population: 
            position += (1.0/individual.fitness)
            if spin <= position/total_fitness_min:
                return individual
    else:
        raise Exception("No optimization specified")        
            
def ranking_selection(population):
    """
    Parameters
    ----------
    population : TYPE
        DESCRIPTION.
    Returns
    -------
    individual : TYPE
        DESCRIPTION.
    """
    # Check if the problem is max or min 
    if population.optim == "max":        
        population.individuals.sort(key=attrgetter('fitness'))
    if population.optim == "min":        
        population.individuals.sort(key=attrgetter('fitness'), reverse = True)
    else:
        raise Exception("No optimization specified")
    #
    total = sum(range(population.size+1))
    position = 0
    spin = random.random()
    #    
    for count, individual in enumerate(population):
         position+=(count+1)/total
         if spin < position:
             return individual

def tournament_selection(population, size = 10):
    """
    Parameters
    ----------
    population : TYPE
        DESCRIPTION.
    size : TYPE, optional
        DESCRIPTION. The default is 10.
    Raises
    ------
    Exception
        DESCRIPTION.
    Returns
    -------
    TYPE
        DESCRIPTION.
    """
    # Select individuals based on tournament size
    tournament = sample(population.individuals, size)
    # Check if the problem is max or min
    if population.optim == "max":
        return max(tournament, key = attrgetter("fitness"))
    if population.optim == "min":
        return min(tournament, key = attrgetter("fitness"))
    else:
        raise Exception("No optimization specified")