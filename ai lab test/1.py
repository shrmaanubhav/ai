#Name - Anubhav Sharma
# Roll No - IIT2024234

# This section has definition of domains, constraints , labs and var..
var = ['A', 'B', 'C']
domain = {
    'A': [1, 2, 3],
    'B': [2, 3, 4],
    'C': [1, 3, 4]
}


labs = ['L1', 'L2']
lab_domain = {
    'A': ['L1'],
    'B': ['L1', 'L2'],
    'C': ['L2']
}

# All the GIven constraints have been defined in this section
cond = [
    lambda x: x['B'] != x['C'],  # B and C cannot be in same time slot
    lambda x: x['A'] != x['B'],  # A and B cannot be in same time slot
    lambda x: not (x['A'] == x['B'] and x['A'] == x['C']),  # A, B, and C cannot be in the same time slot
    lambda x: lab_domain['A'][0] != 'L2',  # A cannot use L2
    lambda x: lab_domain['C'][0] != 'L1',  # C cannot use L1
    lambda x: (x['B'] == 4) == (lab_domain['B'][0] == 'L2'),  # B is in L2 if and only if it's in time slot 4
    lambda x: abs(x['A'] - x['C']) != 1,  # A and C cannot be in consecutive time slots
]

# the backtracking function is defined in this section which will be used to find the solution of the given problem.
def backtracking(ass):
    if len(ass) == len(var):
        return ass
    
    not_asign = [var for var in var if var not in ass]
    mrv_var = min(not_asign, key=lambda v: len(domain[v]))
    
    for value in domain[mrv_var]:
        flag = True
        new_ass = ass.copy()
        new_ass[mrv_var] = value
        
        # Forward pass checking to satisfy the given condition.
        for other_var in not_asign:
            if other_var != mrv_var:
                domain_red = [d for d in domain[other_var] if (new_ass, {other_var: d}) not in cond]
                if len(domain_red) == 0:
                    flag = False
                    break
                else:
                    new_domain = domain.copy()
                    new_domain[other_var] = domain_red
        
        if flag:
            result = backtracking(new_ass)
            if result is not None:
                return result
    
    return None

# Initial call to the backtracking function , this is the section where backtracking function is called and the solution is printed if found or not found message is printed.
init_ass = {}
solution = backtracking(init_ass)

if solution:
    print("Solution found:")
    for section, time in solution.items():
        lab = 'L1' if section == 'A' else ('L2' if section != 'B' or solution['B'] != 4 else 'L2')
        print(f"Section {section}: Time Slot {time}, Lab Room {lab}")
else:
    print("No solution found.")