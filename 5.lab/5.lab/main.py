import random
import numpy as np
import config
import matplotlib.pyplot as plt

# Функция банана
def banana_function(x1, x2):
    return 100 * (x2 - x1 ** 2) ** 2 + (1 - x1) ** 2

def plot_population(population, generation, current_best_fitness, current_best_individual, previous_population=None):
    plt.clf()  

    x_values = [individual[0] for individual in population]
    y_values = [individual[1] for individual in population]

    fitness_values = [evaluate_fitness(individual) for individual in population]
    top_10_percent = int(0.1 * len(population))
    top_indices = np.argsort(fitness_values)[:top_10_percent]

    plt.scatter(x_values, y_values, label=f'Iteration {generation + 1}', s=1)  
    plt.scatter(np.array(x_values)[top_indices], np.array(y_values)[top_indices], color='red', label='Top 10%', s=5) 

    plt.legend(bbox_to_anchor=(0, 1.08), loc='center')
    plt.text(0.5, 1.1, f"Best Min = {current_best_fitness}",
             horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
    plt.text(0.5, -0.1, f"Best Particle = {current_best_individual}",
             horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)

    plt.title('Particle Swarm Optimization Progress')
    plt.xlabel('')
    plt.ylabel('y')
    
    plt.xlim(config.min_range*1.1, config.max_range*1.1)
    plt.ylim(config.min_range*1.1, config.max_range*1.1)

    #plt.savefig(f'{generation}.png')

    plt.pause(config.delay_between_iteration_sec)

class Particle:
    def __init__(self):
        self.position = [random.uniform(config.min_range, config.max_range), random.uniform(config.min_range, config.max_range)]
        self.velocity = [random.uniform(config.min_range, config.max_range), random.uniform(config.min_range,config.max_range)]
        self.best_position = self.position.copy()

def evaluate_fitness(position):
    return banana_function(position[0], position[1])

def update_particle(particle, global_best_position):
    for i in range(2):
        inertia_term = config.inertia_weight * particle.velocity[i]
        cognitive_term = config.cognitive_weight * random.random() * (particle.best_position[i] - particle.position[i])
        social_term = config.social_weight * random.random() * (global_best_position[i] - particle.position[i])

        particle.velocity[i] = inertia_term + cognitive_term + social_term

    for i in range(2):
        particle.position[i] += particle.velocity[i]

def particle_swarm_optimization(population_size, max_iterations):
    particles = [Particle() for _ in range(population_size)]

    global_best_position = particles[0].position.copy()
    global_best_fitness = evaluate_fitness(global_best_position)

    for generation in range(max_iterations):
        for particle in particles:
            fitness = evaluate_fitness(particle.position)

            if fitness < evaluate_fitness(particle.best_position):
                particle.best_position = particle.position.copy()

            if fitness < global_best_fitness:
                global_best_position = particle.position.copy()
                global_best_fitness = fitness

            update_particle(particle, global_best_position)

        plot_population([particle.position for particle in particles], generation, global_best_fitness, global_best_position)
        
        print(f"Iteration {generation + 1} : Best Min = {global_best_fitness}; Best Individual = {global_best_position}")

    print(f"Iteration: {max_iterations}: Best Min = {global_best_fitness}; Best Position = {global_best_position}")
    
    plt.show()

particle_swarm_optimization(config.population_size, config.max_iterations)