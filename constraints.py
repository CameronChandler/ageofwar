''' This file can be used to '''

import math

def check_constraints(d1, d2, d3, h1, h2, h3):
    # Initialize a list to keep track of violated constraints
    violated_constraints = []

    # Constraints to check
    constraints = [
        h1 <= 3 * d1,            # 1      # 3d1 >= h1
        h1 <= 3 * d2,            # 2      # 3d2 >= h1
        h1 <= 2 * d3,            # 3      # 2d3 >= h1
        h2 <= 5 * d1,            # 4      # 5d1 >= h2
        h2 <= 3 * d2,            # 5      # 3d2 >= h2
        h2 <= 2 * d3,            # 6      # 2d3 >= h2
        h3 <= 7 * d1,            # 7      # 7d1 >= h3
        h3 <= 6 * d2,            # 8      # 6d2 >= h3
        h3 <= 4 * d3,            # 9      # 4d3 >= h3
        d3 > d2,                 #10      # d3 > d2
        d2 > d1,                 #11      # d2 > d1
        h3 > h2,                 #12      # h3 > h2
        h2 > h1,                 #13      # h2 > h1
        math.ceil(h1 / d1) == 3, #14      # ceil(h1 / d1) = 3
        math.ceil(h1 / d2) == 3, #15      # ceil(h1 / d2) = 3
        math.ceil(h1 / d3) == 2, #16      # ceil(h1 / d3) = 2
        math.ceil(h2 / d1) == 5, #17      # ceil(h2 / d1) = 5
        math.ceil(h2 / d2) == 3, #18      # ceil(h2 / d2) = 3
        math.ceil(h2 / d3) == 2, #19      # ceil(h2 / d3) = 2
        math.ceil(h3 / d1) == 7, #20      # ceil(h3 / d1) = 7
        math.ceil(h3 / d2) == 6, #21      # ceil(h3 / d2) = 6
        math.ceil(h3 / d3) == 4  #22      # ceil(h3 / d3) = 4
    ]

    # Evaluate constraints and check for violations
    for i, constraint in enumerate(constraints):
        if not constraint:
            violated_constraints.append(i + 1)

    return violated_constraints

def brute_force_search(max_value):
    for d1 in range(1, max_value + 1):
        for d2 in range(d1 + 1, max_value + 1):
            for d3 in range(d2 + 1, max_value + 1):            
                for h1 in range(max(2*d1, 2*d2, 1*d3), min(3*d1, 3*d2, 2*d3, max_value)+1):
                    for h2 in range(max(4*d1, 2*d2, 1*d3, h1 + 1), min(5*d1, 3*d2, 2*d3, max_value)+1):
                        for h3 in range(max(6*d1, 5*d2, 3*d3, h2 + 1), min(7*d1, 6*d2, 4*d3, max_value)+1):
                            violations = check_constraints(d1, d2, d3, h1, h2, h3)
                            if not violations:
                                return (d1, d2, d3, h1, h2, h3)
    return None

# Example usage
max_value = 100  # Adjust the range as needed # searched up to 1000
solution = brute_force_search(max_value)

if solution:
    print(f"Solution found: {solution}")
else:
    print("No solution found within the given range.")