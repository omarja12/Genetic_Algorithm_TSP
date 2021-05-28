from random import randint
from random import sample
from copy import deepcopy
import random


def template_mutation(individual):
    """[summary]
    Args:
        individual ([type]): [description]
    Returns:
        [type]: [description]
    """
    return individual


def swap_mutation(individual):
    """
    Parameters
    ----------
    individual : TYPE
        DESCRIPTION.
    Returns
    -------
    tmp : TYPE
        DESCRIPTION.
    """
    # Position of the start and end substring
    mut_points = sample(range(len(individual)),2)
    i = deepcopy(individual)
    i[mut_points[0]], i[mut_points[1]] = i[mut_points[1]], i[mut_points[0]]
    
    return i
    

def inversion_mutation(individual):
    """
    Parameters
    ----------
    individual : TYPE
        DESCRIPTION.
    Returns
    -------
    i : TYPE
        DESCRIPTION.
    """
    # Position of the start and end substring
    mut_points = sample(range(len(individual)), 2)
    i = deepcopy(individual)
    # This method assumes that the second point is after the first one.
    mut_points.sort()
    # Invert for the mutation
    i[mut_points[0]:mut_points[1]]= i[mut_points[0]:mut_points[1]][::-1]    
    
    return i


def shuffle_mutation(individual):
    """
    Parameters
    ----------
    individual : TYPE
        DESCRIPTION.
    Returns
    -------
    i : TYPE
        DESCRIPTION.
    """
    # Position of the start and end substring
    mut_points = sample(range(len(individual)),2)
    mut_points.sort()    
    i = deepcopy(individual)
    i[mut_points[0]:mut_points[1]] = sorted(i[mut_points[0]:mut_points[1]], key=lambda x: random.random())
            
    return i