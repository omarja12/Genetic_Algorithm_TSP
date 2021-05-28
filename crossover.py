from random import randint
from random import uniform
from random import sample


def template_co(p1, p2):
    """[summary]
    Args:
        p1 ([type]): [description]
        p2 ([type]): [description]
    Returns:
        [type]: [description]
    """
    return offspring1, offspring2


def cycle_co(p1,p2):
    """
    Parameters
    ----------
    p1 : TYPE
        DESCRIPTION.
    p2 : TYPE
        DESCRIPTION.
    Returns
    -------
    offspring1 : TYPE
        DESCRIPTION.
    offspring2 : TYPE
        DESCRIPTION.
    """
    offspring1=[None]*len(p1)
    offspring2=[None]*len(p2)
    
    while None in offspring1:
        index = offspring1.index(None)
        # alternate parents between cycles beginning on second cycle
        if index!=0:
            p1,p2=p2,p1
        
        val1=p1[index]
        val2=p2[index]
       
        while val1!=val2:
            offspring1[index]=p1[index]
            offspring2[index]=p2[index]
            val2=p2[index]
            index=list(p1).index(val2)

        offspring1[index]=p1[index]
        offspring2[index]=p2[index]
        
    return offspring1, offspring2  


def pmx_crossover(p1,p2):
    """
    Parameters
    ----------
    p1 : TYPE
        DESCRIPTION.
    p2 : TYPE
        DESCRIPTION.
    Returns
    -------
    TYPE
        DESCRIPTION.
    """
    # Sample two crossover points
    co_points = sample(range(len(p1)), 2)
    co_points.sort()    
    
    def PMX(x, y):
        # Create holders for offspring
        o = [None]*len(p1)
        # Copy co segement to offspring
        o[co_points[0]:co_points[1]] = x[co_points[0]:co_points[1]]    
        # Find set of values not in offspring from co segment in P2
        z = set(y[co_points[0]:co_points[1]]) -set(x[co_points[0]:co_points[1]])
        # Map values in set to corresponding position in offspring 
        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])
            while o[index] != None:
                temp = index
                index = y.index(x[temp])
            o[index] = i
        while None in o:
            index = o.index(None)
            o[index]=y[index]    
        return o
            
    o1, o2 = (PMX(p1, p2), PMX(p2, p1))
    return o1, o2

                
def order_1_crossover(p1, p2):
    """
    Parameters
    ----------
    p1 : TYPE
        DESCRIPTION.
    p2 : TYPE
        DESCRIPTION.
    Returns
    -------
    offspring1 : TYPE
        DESCRIPTION.
    offspring2 : TYPE
        DESCRIPTION.
    """
    # Choose random start/end position for crossover
    offspring1 = [None]*len(p1)
    offspring2 = [None]*len(p1)
    
    co_points = sample(range(len(p1)), 2)
    co_points.sort()    
    
    # Replicate mum's sequence for alice, dad's sequence for bob    
    offspring1[co_points[0]:(co_points[1]+1)] = p1[co_points[0]:(co_points[1]+1)]
    offspring2[co_points[0]:(co_points[1]+1)] = p2[co_points[0]:(co_points[1]+1)]

    #Fill the remaining position with the other parents' entries
    current_p2_position, current_p1_position = 0, 0

    fixed_pos = list(range(co_points[0], co_points[1] + 1))       
    i = 0
    while i < len(p1):
        if i in fixed_pos:
            i += 1
            continue
        if offspring1[i]==None: 
            p2_trait = p2[current_p2_position]
            while p2_trait in offspring1: 
                current_p2_position += 1
                p2_trait = p2[current_p2_position]
            offspring1[i] = p2_trait
            
        if offspring2[i]==None: #to be filled
            p1_trait = p1[current_p1_position]
            while p1_trait in offspring2: 
                current_p1_position += 1
                p1_trait = p1[current_p1_position]
            offspring2[i] = p1_trait
            
        i +=1

    return offspring1, offspring2
         

                