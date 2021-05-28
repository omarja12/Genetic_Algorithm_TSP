from random import choice, uniform
from math import exp


def hill_climb(search_space, log=0):
    """Hill climbs a given search space.

    Args:
        search_space (Population): A Population of solutions
        log (int, optional): Prints info while running if set to 1. Defaults to 0.

    Raises:
        Exception: When unsure if facing maximization or minimization problem.

    Returns:
        Individual: Local optima Individual found in the search.
    """
    # Select a random solution
    start = choice(search_space)
    position = start
    # Counter to ensure we don't loop
    # infinitely if stuck in a plateu of optimas
    iter_plateu = 0

    if log == 1:
        print(f"Initial position: {start}")

    while True:
        # Return solution if we found same fitness
        # 5 times - to avoid infinite loop
        if iter_plateu >= 5:
            print(f"Best solution found: {position}")
            return position

        n = position.get_neighbours()
        n_fit = [i.fitness for i in n]

        if search_space.optim == "max":
            best_n = n[n_fit.index(max(n_fit))]
            if best_n.fitness > position.fitness:
                if log == 1:
                    print(f"Found better solution: {best_n}")
                iter_plateu = 0
                position = best_n
            elif best_n.fitness == position.fitness:
                if log == 1:
                    print(f"Found better solution: {best_n}")
                iter_plateu += 1
                position = best_n
            else:
                print(f"Best solution found: {position}")
                return position

        elif search_space.optim == "min":
            best_n = n[n_fit.index(min(n_fit))]
            if best_n.fitness < position.fitness:
                if log == 1:
                    print(f"Found better solution: {best_n}")
                iter_plateu = 0
                position = best_n
            elif best_n.fitness == position.fitness:
                if log == 1:
                    print(f"Found better solution: {best_n}")
                iter_plateu += 1
                position = best_n
            else:
                print(f"Best solution found: {position}")
                return position

        else:
            raise Exception("Problem doesn't specify if minimization or maximization.")


def sim_annealing(search_space, L=20, c=10, alpha=0.95):
    """Simulated annealing implementation.

    Args:
        search_space (Population): a Population object to search through.
        L (int, optional): Internal loop parameter. Defaults to 20.
        c (int, optional): Temperature parameter. Defaults to 10.
        alpha (float, optional): Alpha to decrease the temperature. Defaults to 0.95.

    Returns:
        Individual: an Individual object - the best found by SA.
    """
    # Select random solution from search space
    start = choice(search_space)
    # Let current solution be equal to random solution
    position = start
    # Initialize parameters L and c
    L, c = L, c
    # Repeat (loop)
    while c > 0.05:
    # Do L times
        for _ in range(L):
            # Generate solution from N(i)
            sol = choice(position.get_neighbours())
            # if new sol is better or equal - take it
            if sol.fitness >= position.fitness:
                position = sol
            # else, if solution is worse take it based on P
            else:
                p = uniform(0,1)
                pc = exp(-abs(sol.fitness - position.fitness)/c)
                if p < pc:
                    position = sol
        # Update c
        c = c*alpha
    # return solution with best fitness
    print(f"Best solution found: {position}")
    return position