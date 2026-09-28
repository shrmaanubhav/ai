def is_consistent(course, slot, assignment, conflicts):
    for other in conflicts[course]:
        if other in assignment and assignment[other] == slot:
            return False

    return True


def forward_check(course, slot, domains, assignment, conflicts):
    new_domains = {
        c: list(values) for c, values in domains.items()
    }

    # The assigned course no longer needs a domain
    new_domains[course] = [slot]

    # Remove the selected slot from conflicting courses
    for other in conflicts[course]:
        if other not in assignment:
            if slot in new_domains[other]:
                new_domains[other].remove(slot)

                # Empty domain means failure
                if len(new_domains[other]) == 0:
                    return None

    return new_domains


def select_mrv(variables, domains, assignment):
    unassigned = [v for v in variables if v not in assignment]

    # Variable having the smallest remaining domain
    return min(
        unassigned,
        key=lambda v: len(domains[v])
    )


def backtracking_mrv_fc(
    variables,
    domains,
    conflicts,
    assignment={}
):
    # All courses assigned
    if len(assignment) == len(variables):
        return assignment

    # MRV
    course = select_mrv(
        variables,
        domains,
        assignment
    )

    # Try each possible slot
    for slot in domains[course]:

        # Check constraints
        if is_consistent(
            course,
            slot,
            assignment,
            conflicts
        ):

            # Forward Checking
            new_domains = forward_check(
                course,
                slot,
                domains,
                assignment,
                conflicts
            )

            if new_domains is not None:

                assignment[course] = slot

                result = backtracking_mrv_fc(
                    variables,
                    new_domains,
                    conflicts,
                    assignment
                )

                if result:
                    return result

                # Backtrack
                del assignment[course]

    return None


# -----------------------------------
# University Course Scheduling
# -----------------------------------

courses = ['AI', 'DBMS', 'OS', 'CN']

domains = {
    'AI': [1, 2, 3],
    'DBMS': [1, 2, 4],
    'OS': [2, 3, 4],
    'CN': [1, 3, 4]
}

# Courses that cannot have the same slot
conflicts = {
    'AI': ['DBMS', 'OS'],
    'DBMS': ['AI', 'CN'],
    'OS': ['AI', 'CN'],
    'CN': ['DBMS', 'OS']
}

solution = backtracking_mrv_fc(
    courses,
    domains,
    conflicts,
    {}
)

print("Final Timetable:")
print(solution)
