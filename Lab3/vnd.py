def vnd(clauses, n, neighborhoods, max_iter=1000):
    """Variable-Neighborhood-Descent algorithm with 3 neighborhoods."""
    solution = [random.choice([True, False]) for _ in range(n)]
    best_score = evaluate_solution(clauses, solution)
    
    def neighborhood_1(sol):
        return [not sol[i] for i in range(n)] s
    
    def neighborhood_2(sol):
        return [not sol[i] if i % 2 == 0 else sol[i] for i in range(n)] 
    
    def neighborhood_3(sol):
        return sol[::-1] 
    
    neighborhoods = [neighborhood_1, neighborhood_2, neighborhood_3]
    
    for _ in range(max_iter):
        improved = False
        for neighborhood in neighborhoods:
            new_solution = neighborhood(solution)
            new_score = evaluate_solution(clauses, new_solution)
            if new_score > best_score:
                best_score = new_score
                solution = new_solution
                improved = True
                break
        
        if not improved:
            break
    
    return solution, best_score
