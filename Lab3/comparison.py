def compare_algorithms(k, m, n, trials=10):
    
    results = {"Hill-Climbing": 0, "Beam-Search (width=3)": 0, "Beam-Search (width=4)": 0, "VND": 0}
    
    for _ in range(trials):
        clauses = generate_random_3sat(m, n)
        
        _, score_hc = hill_climbing(clauses, n)
        _, score_bs3 = beam_search(clauses, n, 3)
        _, score_bs4 = beam_search(clauses, n, 4)
        _, score_vnd = vnd(clauses, n, neighborhoods=3)
        
        
        results["Hill-Climbing"] += score_hc
        results["Beam-Search (width=3)"] += score_bs3
        results["Beam-Search (width=4)"] += score_bs4
        results["VND"] += score_vnd
    
    
    for algorithm, total_score in results.items():
        print(f"{algorithm}: Average Score = {total_score / trials}")


compare_algorithms(3, 20, 10)
