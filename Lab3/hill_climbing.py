def evaluate_solution(clauses, solution):
    """Evaluate the number of satisfied clauses for a given solution."""
    satisfied_clauses = 0
    for clause in clauses:
        if any((literal > 0 and solution[abs(literal) - 1]) or 
               (literal < 0 and not solution[abs(literal) - 1]) for literal in clause):
            satisfied_clauses += 1
    return satisfied_clauses

def hill_climbing(clauses, n, max_iter=1000):
    """Hill-Climbing algorithm to solve 3-SAT problems."""
    solution = [random.choice([True, False]) for _ in range(n)]
    best_score = evaluate_solution(clauses, solution)
    
    for _ in range(max_iter):
        improved = False
        for i in range(n):
            solution[i] = not solution[i] 
            new_score = evaluate_solution(clauses, solution)
            
            if new_score > best_score:
                best_score = new_score
                improved = True
            else:
                solution[i] = not solution[i]  
        
        if not improved:
            break
    
    return solution, best_score
