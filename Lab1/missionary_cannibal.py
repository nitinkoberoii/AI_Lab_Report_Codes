from collections import deque


class State:
    def __init__(self, m, c, b, parent=None, action=None):
        self.m = m
        self.c = c
        self.b = b
        self.parent = parent
        self.action = action

    def __eq__(self, other):
        return self.m == other.m and self.c == other.c and self.b == other.b

    def __hash__(self):
        return hash((self.m, self.c, self.b))


def is_valid(state):
    if state.m < 0 or state.c < 0 or state.m > 3 or state.c > 3:
        return False
    if state.m < state.c and state.m > 0:
        return False
    if 3 - state.m < 3 - state.c and 3 - state.m > 0:
        return False
    return True


def generate_successors(state):
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    successors = []
    for dm, dc in moves:
        if state.b == 1:
            new_state = State(state.m - dm, state.c - dc, 0, state, (dm, dc))
        else:
            new_state = State(state.m + dm, state.c + dc, 1, state, (dm, dc))
        if is_valid(new_state):
            successors.append(new_state)
    return successors


def bfs():
    initial_state = State(3, 3, 1)
    goal_state = State(0, 0, 0)

    queue = deque([initial_state])
    visited = set([initial_state])

    while queue:
        current_state = queue.popleft()
        if current_state == goal_state:
            return reconstruct_path(current_state)

        for successor in generate_successors(current_state):
            if successor not in visited:
                queue.append(successor)
                visited.add(successor)

    return None


def reconstruct_path(state):
    path = []
    while state.parent:
        path.append(state.action)
        state = state.parent
    return list(reversed(path))


# Run the BFS algorithm
solution = bfs()
print("BFS Solution:")
for step, (m, c) in enumerate(solution):
    print(f"Step {step + 1}: Move {m} missionary(ies) and {c} cannibal(s)")
print(f"Total steps: {len(solution)}")