
#A.1
# function GraphSearch(problem):
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
#

# #A.2
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


#A.4

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

#A.5
def generate_puzzle_instance(depth):
    state = (0, 1, 2, 3, 4, 5, 6, 7, 8)  # Start with the goal state
    for _ in range(depth):
        moves = get_possible_moves(state)
        move = random.choice(moves)
        state = apply_move(state, move)
    return state

#A.6
import time
import psutil
def measure_performance(depth, num_instances=10):
    total_time = 0
    total_memory = 0
    for _ in range(num_instances):
        initial_state = generate_puzzle_instance(depth)
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  
      
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  
        total_time += end_time - start_time
        total_memory += end_memory - start_memory 
    avg_time = total_time / num_instances
    avg_memory = total_memory / num_instances 
    return avg_time, avg_memory
print("Depth | Time (s) | Memory (MB)")
print("------|----------|------------")
for depth in range(5, 26, 5):  
    time, memory = measure_performance(depth)
    print(f"{depth:5d} | {time:8.3f} | {memory:11.2f}")
