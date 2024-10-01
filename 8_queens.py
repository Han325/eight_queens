import math
import sys
import random
from random import randint
from matplotlib import pyplot as plt
from copy import copy

# modified to make chessboard becoming n-size
# chessboard = [3 ,  8 ,  4 ,  7 ,  None ,  6 ,  2 ,  5 ]

# mutated = 4
# size = 8

def initialize_chessboard(n):
    global size, mutated, chessboard
    size = n
    mutated = random.randint(0, size - 1)  # Randomly pick one queen to mutate
    chessboard = [random.randint(1, size) for _ in range(size)]  # Randomly place queens on the board

def get_random_solution():
    chessboard[mutated] = randint(1,size)
    return chessboard

def evaluate_fitness(solution):
    fitness = 0
    row5 = solution[mutated]
    # check on the same row
    fitness = fitness - sum([x==row5 for x in solution]) + 1
    # check on the same column - not needed as we only vary one queen position
    # check on the same diagonal, note: 'mutated' is the queen position we vary
    for idx in range(size):
        if idx != mutated:
            if solution[idx] + abs(idx - mutated) == row5 or solution[idx] - abs(idx - mutated) == row5:
                fitness -= 1
    
    return fitness

def get_neighbours(solution):
    current = solution[mutated]
    neighbour_1 = copy(solution)
    neighbour_2 = copy(solution)
    result = []
    if (current - 1):
        neighbour_1[mutated] = current - 1
        result.append(neighbour_1)
    if (current + 1) < size + 1:
        neighbour_2[mutated] = current + 1
        result.append(neighbour_2)
    return(result)

def random_search(guesses):
    values = []
    solution = get_random_solution()
    fitness = evaluate_fitness(solution)
    values.append(fitness)
    guesses -= 1
    while (fitness < 0) and guesses:
        solution = get_random_solution()
        fitness = evaluate_fitness(solution)
        values.append(fitness)
        guesses -= 1
    return solution,fitness,values

def hill_climbing():
    solution = get_random_solution()
    fitness = evaluate_fitness(solution)
    values = [fitness]
    while (fitness < 0):
      neighbours = get_neighbours(solution)
      fitnesses = [evaluate_fitness(x) for x in neighbours]
      maxfit = max(fitnesses)
      if maxfit > fitness:
          solution = neighbours[fitnesses.index(maxfit)]
          fitness = maxfit
          values.append(fitness)
      else: 
          break 
    return solution,fitness,values

def hill_climbing_v2(iteration_limit):
    solution = get_random_solution()
    fitness = evaluate_fitness(solution)
    values = [fitness]
    iterations = 0
    
    while (fitness < 0 and iterations < iteration_limit):
        neighbours = get_neighbours(solution)
        fitnesses = [evaluate_fitness(x) for x in neighbours]
        maxfit = max(fitnesses)
        
        if maxfit > fitness:
            solution = neighbours[fitnesses.index(maxfit)]
            fitness = maxfit
            values.append(fitness)
        else:
            break
        
        iterations += 1
        
    return solution, fitness, values

def hill_climbing_with_restarts(max_restarts, iteration_limit):
    best_solution = None
    best_fitness = float('-inf')
    all_values = []

    for restart in range(max_restarts):
        solution, fitness, values = hill_climbing_v2(iteration_limit)
        all_values.extend(values)

        if fitness > best_fitness:
            best_solution = solution
            best_fitness = fitness

    return best_solution, best_fitness, all_values

def simulated_annealing(initial_temp, cooling_rate, iteration_limit):
    # Step 1: Start with a random solution
    current_solution = get_random_solution()
    current_fitness = evaluate_fitness(current_solution)
    best_solution = current_solution
    best_fitness = current_fitness
    
    # Step 2: Initialize temperature
    temp = initial_temp
    values = [current_fitness]
    
    iterations = 0
    
    while temp > 0.01 and iterations < iteration_limit:
        # Step 3: Get a random neighbor
        neighbours = get_neighbours(current_solution)
        new_solution = random.choice(neighbours)
        new_fitness = evaluate_fitness(new_solution)
        
        # Step 4: Calculate fitness difference
        fitness_diff = new_fitness - current_fitness
        
        # Step 5: Acceptance criteria
        if fitness_diff > 0 or random.random() < math.exp(fitness_diff / temp):
            current_solution = new_solution
            current_fitness = new_fitness
        
        # Track the best solution
        if current_fitness > best_fitness:
            best_solution = current_solution
            best_fitness = current_fitness
        
        # Track fitness values over iterations
        values.append(current_fitness)
        
        # Step 6: Decrease temperature according to cooling schedule
        temp *= cooling_rate
        iterations += 1
    
    return best_solution, best_fitness, values

def show_fitnesses(values):
    plt.plot(list(range(1,len(values)+1)),values)
    plt.xlabel('Iteration Number')
    plt.ylabel('Fitness Value')
    plt.show()

if __name__=='__main__':
    search = sys.argv[1]

    n = int(sys.argv[2])
    
    initialize_chessboard(n)

    if search == 'random':
      solution,fitness,values = random_search(int(sys.argv[3]))
      print('Solution: '+str(solution),'Fitness: '+str(fitness))
      show_fitnesses(values)
    if search == 'hill_climbing':
      solution,fitness,values = hill_climbing()
      print('Solution: '+str(solution),'Fitness: '+str(fitness))
      show_fitnesses(values)
    if search == 'hill_climbing_with_restarts':
        solution, fitness, values = hill_climbing_with_restarts(int(sys.argv[3]), int(sys.argv[4]))
        print('Solution: ' + str(solution), 'Fitness: ' + str(fitness))
        show_fitnesses(values)
    if search == 'simulated_annealing':
        solution, fitness, values = simulated_annealing(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
        print('Solution: ' + str(solution), 'Fitness: ' + str(fitness))
        show_fitnesses(values)

