import random

def generate_random_3sat(m, n):
    """Generates a random 3-SAT problem with m clauses and n variables."""
    clauses = []
    for _ in range(m):
        clause = random.sample(range(1, n+1), 3)  
        clause = [(var if random.choice([True, False]) else -var) for var in clause] 
        clauses.append(clause)
    return clauses
