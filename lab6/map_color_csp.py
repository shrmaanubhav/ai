def backtracking(variables, domains, neighbors, assignment={}):
    # If all variables are assigned
    if len(assignment) == len(variables):
        return assignment

    # Select the next unassigned variable
    var = next(v for v in variables if v not in assignment)

    # Try every value in its domain
    for color in domains[var]:
        # Check whether the color is valid
        valid = True

        for neighbor in neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == color:
                valid = False
                break

        if valid:
            assignment[var] = color

            result = backtracking(
                variables, domains, neighbors, assignment
            )

            if result:
                return result

            # Backtrack
            del assignment[var]

    return None


def mrv(variables, domains, neighbors, assignment):
    unassigned = [v for v in variables if v not in assignment]

    # Choose variable with the smallest number of legal values
    best_var = None
    best_count = float('inf')

    for var in unassigned:
        legal_values = []

        for value in domains[var]:
            valid = True

            for neighbor in neighbors[var]:
                if neighbor in assignment and assignment[neighbor] == value:
                    valid = False
                    break

            if valid:
                legal_values.append(value)

        if len(legal_values) < best_count:
            best_count = len(legal_values)
            best_var = var

    return best_var


def backtracking_mrv(variables, domains, neighbors, assignment={}):
    if len(assignment) == len(variables):
        return assignment

    var = mrv(variables, domains, neighbors, assignment)

    for color in domains[var]:
        valid = True

        for neighbor in neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == color:
                valid = False
                break

        if valid:
            assignment[var] = color

            result = backtracking_mrv(
                variables, domains, neighbors, assignment
            )

            if result:
                return result

            del assignment[var]

    return None


# -------------------------------
# Map Coloring Problem
# -------------------------------

variables = ['A', 'B', 'C', 'D', 'E']

colors = ['Red', 'Green', 'Blue']

domains = {
    'A': colors,
    'B': colors,
    'C': colors,
    'D': colors,
    'E': colors
}

neighbors = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D', 'E'],
    'C': ['A', 'B', 'E'],
    'D': ['B', 'E'],
    'E': ['B', 'C', 'D']
}

print("Ordinary Backtracking:")
solution = backtracking(variables, domains, neighbors, {})
print(solution)

print("\nBacktracking with MRV:")
solution = backtracking_mrv(variables, domains, neighbors, {})
print(solution)
