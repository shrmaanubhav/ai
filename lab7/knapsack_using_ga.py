import random

POP_SIZE = 10
BITS = 4
GENERATIONS = 20
MUTATION_RATE = 0.05

items = [
    ('A', 7, 500),
    ('B', 2, 400),
    ('C', 1, 700),
    ('D', 9, 200)
]

KNAPSACK_CAPACITY = 15

def random_chromosome():
    return ''.join(random.choice('01') for _ in range(BITS))

def calculate(chromosome):
    total_weight = 0
    total_value = 0

    for i in range(BITS):
        if chromosome[i] == '1':
            total_weight += items[i][1]
            total_value += items[i][2]

    if total_weight > KNAPSACK_CAPACITY:
        return total_weight, total_value, 0

    return total_weight, total_value, total_value

def roulette_selection(population, fitness_values):
    total_fitness = sum(fitness_values)

    if total_fitness == 0:
        return random.choice(population)

    r = random.uniform(0, total_fitness)
    cumulative = 0

    for chromosome, fit in zip(population, fitness_values):
        cumulative += fit

        if cumulative >= r:
            return chromosome

    return population[-1]

def crossover(parent1, parent2):
    point = random.randint(1, BITS - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2

def mutate(chromosome):
    chromosome = list(chromosome)

    for i in range(BITS):
        if random.random() < MUTATION_RATE:
            chromosome[i] = '1' if chromosome[i] == '0' else '0'

    return ''.join(chromosome)

population = [random_chromosome() for _ in range(POP_SIZE)]

best_chromosome = None
best_fitness = -1

for generation in range(GENERATIONS):

    fitness_values = []

    for chromosome in population:
        weight, value, fitness = calculate(chromosome)

        fitness_values.append(fitness)

        if fitness > best_fitness:
            best_fitness = fitness
            best_chromosome = chromosome

    print(f"\nGeneration {generation + 1}")

    for chromosome, fitness in zip(population, fitness_values):
        weight, value, fitness = calculate(chromosome)

        print(
            f"{chromosome} -> "
            f"Weight = {weight:2d} kg, "
            f"Value = Rs.{value:4d}, "
            f"Fitness = {fitness:4d}"
        )

    new_population = []

    while len(new_population) < POP_SIZE:

        parent1 = roulette_selection(population, fitness_values)
        parent2 = roulette_selection(population, fitness_values)

        child1, child2 = crossover(parent1, parent2)

        child1 = mutate(child1)
        child2 = mutate(child2)

        new_population.append(child1)

        if len(new_population) < POP_SIZE:
            new_population.append(child2)

    population = new_population

weight, value, fitness = calculate(best_chromosome)

print("\n========== FINAL RESULT ==========")
print("Best chromosome :", best_chromosome)
print("Total weight    :", weight, "kg")
print("Total value     : Rs.", value)
print("Fitness         :", fitness)

print("\nItems selected:")

for i in range(BITS):
    if best_chromosome[i] == '1':
        print(
            items[i][0],
            "-> Weight:", items[i][1], "kg,",
            "Value: Rs.", items[i][2]
        )

