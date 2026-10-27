#Name - Anubhav Sharma
# Roll No - IIT2024234

import random
import math

# The coordinates of each city are stored in the `city_dist` dictionary
# the keys are city identifiers and the values are tuples containing the x and y coordinates of each city.
city_dist = {
    1 : {60,200},
    2 : {23,45},
    3 : {15,150},
    4 : {85,90},
    5 : {71,123},
    6 : {98,45},
    7 : {50,220},
    8 : {20,30},
    9 : {40,180},
    10 : {75,155},
    11 : {82,60},
    12 : {91,120},
    13 : {12,210},
    14 : {37,100},
    15 : {28,77},
    16 : {66,89},
    17 : {55,130},
    18 : {73 , 140},
    19 : {88,33},
    20 : {42,170}
}

# This function is used to calculate the euclidean distance between two cities based on their coordinates.
def dist(city1, city2):
    x1, y1 = city_dist[city1]
    x2, y2 = city_dist[city2]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This function sums up the entire distance of a given route by calculating the distance between each pair of consecutive cities  
def tot_dist(route):
    total = 0
    for i in range(len(route) - 1):
        total += dist(route[i], route[i + 1])
    total += dist(route[-1], route[0])  # Return to the hub
    return total

# This function represents the TSP as a chromosome
def make_ch(cities):
    chr = cities[:]
    random.shuffle(chr) #random path
    return chr

# This function populates the initial population by chromosomes
def init_pop(cities, ppl_size):
    ppl = []
    for _ in range(ppl_size):
        indi = make_ch(cities)
        ppl.append(indi)
    return ppl


def select(ppl, fit_sc):
    sl = random.choices(ppl, weights=fit_sc, k=2)
    return sl

#This function defines fitness function as an inverse of the total distance of given route.
def fitness(route):
    return 1 / tot_dist(route)

# This function is writing roulete wheel select function to select 2 parent for crossover
def rowlet_wheel(ppl):
    fit_sc = [fitness(individual) for individual in ppl]
    tot_fit = sum(fit_sc)
    pb = [score / tot_fit for score in fit_sc]
    selected_indices = random.choices(range(len(ppl)), weights=pb, k=2)
    return [ppl[i] for i in selected_indices]

#implementing mutation order 
def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end + 1] = parent1[start:end + 1]
    pointer = 0
    for i in range(size):
        if parent2[i] not in child:
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = parent2[i]
    return child

#elitism
def elitism(ppl, fit_sc):
    best_index = fit_sc.index(max(fit_sc))
    return ppl[best_index]

#This is the main function to run the genetic algorithm
def ga(cities, ppl_size, gnrs):
    ppl = init_pop(cities, ppl_size)
    best_route = None
    best_dist = float('inf')

    for gen in range(gnrs):
        fit_sc = [fitness(individual) for individual in ppl]
        new_ppl = []

        # Elitism: Keep the best individual
        best_indi = elitism(ppl, fit_sc)
        new_ppl.append(best_indi)

        while len(new_ppl) < ppl_size:
            parent1, parent2 = rowlet_wheel(ppl)
            child = order_crossover(parent1, parent2)

            # Mutation: Swap two cities with a small probability
            if random.random() < 0.1:
                i, j = random.sample(range(len(child)), 2)
                child[i], child[j] = child[j], child[i]

            new_ppl.append(child)

        ppl = new_ppl

        # Update the best route found so far
        curr = tot_dist(best_indi)
        if curr < best_dist:
            best_dist = curr
            best_route = best_indi

    return best_route, best_dist

# The section to run the code.
cities = list(city_dist.keys())
ppl_size = 100
gnrs = 200
best_route, best_dist = ga(cities, ppl_size, gnrs)
print("Best route found:", best_route)
print("Total distance:", best_dist)     