import pygad
import numpy

# Function to process and simulate the Rock-Paper-Scissors tournament rounds
def process_tournament(tournament, m):
    while len(tournament) > 1:
        new_round = ""
        for i in range(0, len(tournament), 2):
            winner = rock_paper_scissors(tournament[i], tournament[i + 1])
            new_round += winner
        tournament = new_round
    return tournament


# Fitness function based on win condition
def fitness_win(pairing, m, rcount, pcount, scount, lcount, ycount):
    if letter_count(pairing, m) != (rcount, pcount, scount, lcount, ycount):
        return 0
    processed_pairing, score = fitness_helper(pairing, m)
    if processed_pairing == "S":
        return 100
    else:
        return score

# Function to help fitness function determine score
def fitness_helper(tournament, m):
    score = 0
    while len(tournament) > 1:
        new_round = ""
        for i in range(0, len(tournament), 2):
            winner = rock_paper_scissors(tournament[i], tournament[i + 1])
            new_round += winner
        tournament = new_round
        if "S" in tournament:
            score += (100 / int(math.log2(m))) + random.randint(1, 5)
    return (tournament, score)

function_inputs = [4, -2, 3.5, 5, -11, -4.7] # Function inputs.
desired_output = 44 # Function output.

def fitness_func(ga_instance, solution, solution_idx):
    output = numpy.sum(solution*function_inputs)
    fitness = 1.0 / numpy.abs(output - desired_output)
    return fitness

def on_gen(ga_instance):
    print("Generation : ", ga_instance.generations_completed)
    print("Fitness of the best solution :", ga_instance.best_solution()[1])

num_generations = 50
num_parents_mating = 4

fitness_function = fitness_func

sol_per_pop = 8
num_genes = len(function_inputs)

init_range_low = -2
init_range_high = 5

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 10

ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes)

ga_instance.run()
""" Inside this method, the genetic algorithm evolves over some generations by doing the following tasks:

    Calculating the fitness values of the solutions within the current population.
    Select the best solutions as parents in the mating pool.
    Apply the crossover & mutation operation
    Repeat the process for the specified number of generations. """
    
ga_instance.plot_fitness()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print(f"Parameters of the best solution : {solution}")
print(f"Fitness value of the best solution = {solution_fitness}")
print(f"Index of the best solution : {solution_idx}")

if ga_instance.best_solution_generation != -1:
    print(f"Best fitness value reached after {ga_instance.best_solution_generation} generations.")

filename = 'genetic'
ga_instance.save(filename=filename)

#loaded_ga_instance = pygad.load(filename=filename)
#print(loaded_ga_instance.best_solution())
