import random
import numpy as np
import math
import config
import matplotlib.pyplot as plt

# Функция банана
def banana_function(x1, x2):
    return 100 * (x2 - x1 ** 2) ** 2 + (1 - x1) ** 2

def plot_binary_population(population, generation, current_best_fitness, current_best_individual):
    plt.clf()
    x_values = [binary_to_decimal(individual[0]) for individual in population]
    y_values = [binary_to_decimal(individual[1]) for individual in population]

    fitness_values = [banana_function(binary_to_decimal(individual[0]), binary_to_decimal(individual[1])) for individual in population]
    top_10_percent = int(0.1 * len(population))
    top_indices = np.argsort(fitness_values)[:top_10_percent]

    plt.scatter(x_values, y_values, label=f'Generation {generation + 1}', s=1)
    plt.scatter(np.array(x_values)[top_indices], np.array(y_values)[top_indices], color='red', label='Top 10%', s=5)

    plt.legend(bbox_to_anchor=(0, 1.08), loc='center')
    decoded_current_best_individual = (binary_to_decimal(current_best_individual[0]), binary_to_decimal(current_best_individual[1]))
    plt.text(0.5, 1.1, f"Best Min = {current_best_fitness}",
             horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
    plt.text(0.5, -0.1, f"Best Individual = {decoded_current_best_individual}",
             horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)

    plt.title('Genetic Algorithm Progress')
    plt.xlabel('')
    plt.ylabel('y')
    
    plt.xlim(config.min_range*1.1, config.max_range*1.1)
    plt.ylim(config.min_range*1.1, config.max_range*1.1)

    #plt.savefig(f'{generation}.png')

    plt.pause(config.delay_between_iteration_sec)

def initialize_binary_population(population_size):
    binary_length = int(math.ceil(math.log2((config.max_range - config.min_range) * (10 ** 10))))
    return [(decimal_to_binary(random.uniform(config.min_range, config.max_range)),
             decimal_to_binary(random.uniform(config.min_range, config.max_range))) for _ in range(population_size)]

def binary_crossover(parent1, parent2, mutation_chance):
    binary_length = len(parent1[0])
    crossover_point = random.randint(0, binary_length - 1)

    child_x1 = parent1[0][:crossover_point] + parent2[0][crossover_point:]
    child_x2 = parent1[1][:crossover_point] + parent2[1][crossover_point:]

    if random.random() < mutation_chance:
        mutation_point = random.randint(0, binary_length - 1)
        child_x1 = child_x1[:mutation_point] + ('0' if child_x1[mutation_point] == '1' else '1') + child_x1[mutation_point + 1:]
        child_x2 = child_x2[:mutation_point] + ('0' if child_x2[mutation_point] == '1' else '1') + child_x2[mutation_point + 1:]

    return (child_x1, child_x2)

def decimal_to_binary(decimal):
    binary_length = int(math.ceil(math.log2((config.max_range - config.min_range) * (10 ** 10))))
    binary = format(int((decimal - config.min_range) / (config.max_range - config.min_range) * (2 ** binary_length - 1)), '0' + str(binary_length) + 'b')
    return binary

def binary_to_decimal(binary):
    binary_length = len(binary)
    decimal = int(binary, 2)
    return config.min_range + decimal * (config.max_range - config.min_range) / (2 ** (binary_length) - 1)

def evaluate_binary_fitness(individual):
    return banana_function(binary_to_decimal(individual[0]), binary_to_decimal(individual[1]))

def evaluate_binary_population(population):
    fitness_values = [evaluate_binary_fitness(x) for x in population]
    best_fitness = min(fitness_values)
    best_individual = population[fitness_values.index(best_fitness)]
    return best_fitness, best_individual

def choose_binary_parents(population, tournament_size=3):
    tournament = random.sample(population, tournament_size)
    tournament_fitness = [evaluate_binary_fitness(individual) for individual in tournament]
    winner_index = tournament_fitness.index(min(tournament_fitness))
    return tournament[winner_index]

def binary_genetic_algorithm(population_size, mutation_chance, max_iterations):
    population = initialize_binary_population(population_size)

    for generation in range(max_iterations):
        new_population = []
        for _ in range(population_size):
            parent1 = choose_binary_parents(population)
            parent2 = choose_binary_parents(population)

            child = binary_crossover(parent1, parent2, mutation_chance)

            new_population.append(child)

        combined_population = population + new_population
        combined_fitness = [evaluate_binary_fitness(x) for x in combined_population]

        sorted_combined = [x for _, x in sorted(zip(combined_fitness, combined_population))]
        selected_population = sorted_combined[:population_size // 2]

        population = selected_population + initialize_binary_population(population_size // 2)

        current_best_fitness, current_best_individual = evaluate_binary_population(population)
        
        plot_binary_population(population, generation, current_best_fitness, current_best_individual)
        
        print(f"Generation {generation + 1}: Best Min = {current_best_fitness}; Best Individual = {current_best_individual}")
        
    best_fitness, best_individual = evaluate_binary_population(population)
    decoded_best_individual = (binary_to_decimal(best_individual[0]), binary_to_decimal(best_individual[1]))
    print(f"\nMinimum achieved at x = {round(decoded_best_individual[0], 4)}; y = {round(decoded_best_individual[1], 4)} with f(x, y) = {banana_function(decoded_best_individual[0], decoded_best_individual[1])}")

    plt.show()

binary_genetic_algorithm(config.population_size, config.mutation_chance, config.max_iterations)
