def beam_search(clauses, n, beam_width, max_iter=1000):
    """Beam Search algorithm to solve 3-SAT problems with a given beam width."""
    def random_solutions(width):
        return [[random.choice([True, False]) for _ in range(n)] for _ in range(width)]
    
   
    beam = random_solutions(beam_width)
    best_solution = None
    best_score = 0
    
    for _ in range(max_iter):
        candidates = []
        for solution in beam:
            for i in range(n):
                new_solution = solution[:]
                new_solution[i] = not new_solution[i]
                candidates.append((new_solution, evaluate_solution(clauses, new_solution)))
        
       
        candidates.sort(key=lambda x: x[1], reverse=True)
        beam = [candidate[0] for candidate in candidates[:beam_width]]
        
        if candidates[0][1] > best_score:
            best_solution, best_score = candidates[0]
    
    return best_solution, best_score
