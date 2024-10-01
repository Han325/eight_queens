import sys
from random import randint
from matplotlib import pyplot as plt
from copy import copy
chessboard = [3 ,  8 ,  4 ,  7 ,  None ,  6 ,  2 ,  5 ]

mutated = 4
size = 8

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
    for idx in [0, 1, 2, 3, 5, 6, 7]:
        check = chessboard[idx] + abs(idx-mutated)
        if row5 == check: fitness -= 1
        check = chessboard[idx] - abs(idx-mutated)
        if row5 == check: fitness -= 1

    return(fitness)

def get_neighbours(solution):
    current = solution[mutated]
    neighbour_1 = copy(chessboard)
    neighbour_2 = copy(chessboard)
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

def show_fitnesses(values):
    plt.plot(list(range(1,len(values)+1)),values)
    plt.xlabel('Iteration Number')
    plt.ylabel('Fitness Value')
    plt.show()

if __name__=='__main__':
    search = sys.argv[1]
    if search == 'random':
      solution,fitness,values = random_search(int(sys.argv[2]))
      print('Solution: '+str(solution),'Fitness: '+str(fitness))
      show_fitnesses(values)
    if search == 'hill_climbing':
      solution,fitness,values = hill_climbing()
      print('Solution: '+str(solution),'Fitness: '+str(fitness))
      show_fitnesses(values)