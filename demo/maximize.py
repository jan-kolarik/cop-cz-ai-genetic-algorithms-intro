import argparse
import random

# Genetic Algorithm Parameters
population_size = 100
num_generations = 20
crossover_rate = 0.8
mutation_rate = 0.1

# Implementation Parameters
genome_size = 100

def fitness(individual):
    return sum(individual)

def random_gene():
    return random.randint(0, 1)

def mutate_gene(gene):
    return 1 - gene

def generate_random_population():
    return [[random_gene() for _ in range(genome_size)] 
            for _ in range(population_size)]

def evaluate_population(population):
    return [fitness(individual) for individual in population]

def select_parents(population, fitness_scores):
    selection = []
    for _ in range(len(population)):
        tournament = random.sample(list(zip(population, fitness_scores)), 3)
        winner = max(tournament, key=lambda x: x[1])[0]
        selection.append(winner)
    return selection

def crossover(parent1, parent2):
    cutpoint = random.randint(0, genome_size - 2)
    child1 = parent1[:cutpoint+1] + parent2[cutpoint+1:]
    child2 = parent2[:cutpoint+1] + parent1[cutpoint+1:]
    return child1, child2

def mutate(individual):
    position = random.randint(0, genome_size - 1)
    individual[position] = mutate_gene(individual[position])

# Parsing Parameters

parser = argparse.ArgumentParser()
parser.add_argument('--population', type=int)
parser.add_argument('--generations', type=int)
parser.add_argument('--genome', type=int)

args = parser.parse_args()

if args.population:
    population_size = args.population
if args.generations:
    num_generations = args.generations
if args.genome:
    genome_size = args.genome

# Genetic Algorithm

population = generate_random_population()
fitness_scores = evaluate_population(population)

best_fitness_values = []

for generation in range(num_generations):
    parents = select_parents(population, fitness_scores)

    offspring = []
    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        if random.random() < crossover_rate:
            child1, child2 = crossover(parent1, parent2)
        else:
            child1, child2 = parent1, parent2
        offspring.extend([child1, child2])

    for individual in offspring:
        if random.random() < mutation_rate:
            mutate(individual)

    fitness_scores = evaluate_population(offspring)
    population = offspring

    best_fitness_values.append(max(fitness_scores))
    print(f"Generation {generation + 1}: Best Fitness = {max(fitness_scores)}")