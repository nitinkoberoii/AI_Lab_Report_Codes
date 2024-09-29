import random

def generate_k_sat(k, m, n):
    variables = list(range(1, n + 1))
    clauses = []
    
    for _ in range(m):
        # Select k unique variables randomly
        selected_variables = random.sample(variables, k)
        clause = []
        
        for variable in selected_variables:
            # Randomly decide whether to negate the variable or not
            if random.choice([True, False]):
                clause.append(-variable)  # Negate variable
            else:
                clause.append(variable)   # Keep variable positive
        
        clauses.append(clause)
    
    return clauses

# Example usage:
k = 3  # Length of each clause
m = 5  # Number of clauses
n = 4  # Number of variables
clauses = generate_k_sat(k, m, n)
print(clauses)
