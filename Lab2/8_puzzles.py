
#A.1  Pseudo-Code for the graph search agent.
# def GraphSearch(problem):
#     initialize frontier as a queue with the initial state
#     initialize explored as an empty set
#     while frontier is not empty:
#         state = frontier.pop()
#         if state is goal:
#             return solution
#         add state to explored
#         for each action in problem.actions(state):
#             child = problem.result(state, action)
#             if child is not in explored and not in frontier:
#                 if child is goal:
#                     return solution
#                 frontier.add(child)
#     return failure


#A.2 functions  for Puzzle-8. 
import random

def create_initial_state():

    return tuple(random.sample(range(9),9))

def is_goal_state(state):

    return state ==(0,1,2, 3, 4, 5, 6, 7, 8)

def get_blank_position(state):
    
    return state.index(0)

def get_possible_moves(state):
    blank = get_blank_position(state)
    moves = []
    if blank not in [0, 1, 2]:  # move up
        moves.append('UP')
    if blank not in [6, 7, 8]:  # move down
        moves.append('DOWN')
    if blank not in [0, 3, 6]:  # move left
        moves.append('LEFT')
    if blank not in [2, 5, 8]:  # move right
        moves.append('RIGHT')
    return moves

def apply_move(state, move):
    state = list(state)
    blank = get_blank_position(state)
    if move == 'UP':
        state[blank], state[blank - 3] = state[blank - 3], state[blank]
    elif move == 'DOWN':
        state[blank], state[blank + 3] = state[blank + 3], state[blank]
    elif move == 'LEFT':
        state[blank], state[blank - 1] = state[blank - 1], state[blank]
    elif move == 'RIGHT':
        state[blank], state[blank + 1] = state[blank + 1], state[blank]
    return tuple(state)

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()


#A.4 function for backtracing

def backtrack(came_from, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path
def print_solution(path):
    """Print the solution path with moves."""
    for i in range(len(path) - 1):
        current_state = path[i]
        next_state = path[i + 1]
        move = get_move(current_state, next_state)
        print(f"Move {i + 1}: {move}")
        print_state(next_state)

def get_move(state1, state2):
    blank1 = get_blank_position(state1)
    blank2 = get_blank_position(state2)
    if blank2 == blank1 - 3:
        return "UP"
    elif blank2 == blank1 + 3:
        return "DOWN"
    elif blank2 == blank1 - 1:
        return "LEFT"
    elif blank2 == blank1 + 1:
        return "RIGHT"

#A.5 Puzzle-8 instances with the goal state at depth “d”. 
def generate_puzzle_instance(depth):
    state = (0, 1, 2, 3, 4, 5, 6, 7, 8)  # Start with the goal state
    previous_move = None
    for _ in range(depth):
        moves = get_possible_moves(state)
        if previous_move:
            
            if previous_move == 'UP' and 'DOWN' in moves:
                moves.remove('DOWN')
            elif previous_move == 'DOWN' and 'UP' in moves:
                moves.remove('UP')
            elif previous_move == 'LEFT' and 'RIGHT' in moves:
                moves.remove('RIGHT')
            elif previous_move == 'RIGHT' and 'LEFT' in moves:
                moves.remove('LEFT')
        
        move = random.choice(moves)  
        state = apply_move(state, move)
        previous_move = move  
    return state

#A.6 code to prepare table indicating the memory and time requirements to solve Puzzle-8 instances 
import random
import time
import tracemalloc
from collections import deque
import statistics

def create_state():
    return tuple(random.sample(range(9), 9))

def is_goal(s):
    return s == (0, 1, 2, 3, 4, 5, 6, 7, 8)

def get_blank_pos(s):
    return s.index(0)

def get_moves(s):
    blank = get_blank_pos(s)
    moves = []
    if blank not in [0, 1, 2]: moves.append('UP')
    if blank not in [6, 7, 8]: moves.append('DOWN')
    if blank not in [0, 3, 6]: moves.append('LEFT')
    if blank not in [2, 5, 8]: moves.append('RIGHT')
    return moves

def apply_move(s, move):
    s = list(s)
    blank = get_blank_pos(s)
    if move == 'UP': s[blank], s[blank - 3] = s[blank - 3], s[blank]
    elif move == 'DOWN': s[blank], s[blank + 3] = s[blank + 3], s[blank]
    elif move == 'LEFT': s[blank], s[blank - 1] = s[blank - 1], s[blank]
    elif move == 'RIGHT': s[blank], s[blank + 1] = s[blank + 1], s[blank]
    return tuple(s)

def generate_instance(depth):
    s = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    moves_applied = 0
    while moves_applied < depth:
        move = random.choice(get_moves(s))
        new_s = apply_move(s, move)
        if new_s != s:  
            s = new_s
            moves_applied += 1
    return s

def search(initial_state, max_depth=100):
    if is_goal(initial_state):
        return []
    frontier = deque([(initial_state, [])])
    explored = set()
    while frontier:
        s, path = frontier.popleft()
        if len(path) > max_depth:
            continue  
        if s not in explored:
            explored.add(s)
            if is_goal(s):
                return path
            for move in get_moves(s):
                child = apply_move(s, move)
                if child not in explored:
                    frontier.append((child, path + [move]))
    return None

def measure_performance(depth, trials=10):
    results = []
    for _ in range(trials):
        initial_state = generate_instance(depth)
        
        tracemalloc.start()
        start_time = time.perf_counter()
        
        solution = search(initial_state)
        
        end_time = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        results.append({
            "time": end_time - start_time,
            "memory_kb": peak / 1024,
            "solution_length": len(solution) if solution else -1
        })
    
    avg_time = statistics.mean(r["time"] for r in results)
    avg_memory = statistics.mean(r["memory_kb"] for r in results)
    avg_solution_length = statistics.mean(r["solution_length"] for r in results)
    
    return {
        "depth": depth,
        "avg_time": avg_time,
        "avg_memory": avg_memory,
        "avg_solution_length": avg_solution_length
    }

def main():
    depths = [1, 2, 3, 5, 10, 15, 20]
    results = []
    
    for depth in depths:
        result = measure_performance(depth)
        results.append(result)
    
    print(f"{'Depth (d)':<10}{'Avg Time (s)':<20}{'Avg Memory (KB)':<20}{'Avg Solution Length':<20}")
    for result in results:
        print(f"{result['depth']:<10}{result['avg_time']:<20.6f}{result['avg_memory']:<20.2f}{result['avg_solution_length']:<20.2f}")

if __name__ == "__main__":
    main()
