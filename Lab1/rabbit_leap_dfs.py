class State:
    def __init__(self, configuration, parent=None, action=None):
        self.configuration = configuration
        self.parent = parent
        self.action = action

    def __eq__(self, other):
        return self.configuration == other.configuration

    def __hash__(self):
        return hash(self.configuration)


def generate_successors(state):
    successors = []
    empty_index = state.configuration.index('_')

    # Move east-bound rabbits
    for i in [-2, -1]:
        if 0 <= empty_index + i < 7 and state.configuration[empty_index + i] == 'E':
            new_config = list(state.configuration)
            new_config[empty_index], new_config[empty_index + i] = new_config[empty_index + i], new_config[empty_index]
            successors.append(State(''.join(new_config), state, f"Move E from {empty_index + i} to {empty_index}"))

    # Move west-bound rabbits
    for i in [1, 2]:
        if 0 <= empty_index + i < 7 and state.configuration[empty_index + i] == 'W':
            new_config = list(state.configuration)
            new_config[empty_index], new_config[empty_index + i] = new_config[empty_index + i], new_config[empty_index]
            successors.append(State(''.join(new_config), state, f"Move W from {empty_index + i} to {empty_index}"))

    return successors


def dfs():
    initial_state = State("EEEW_WWW")
    goal_state = State("WWWE_EEE")

    stack = [initial_state]
    visited = set()

    while stack:
        current_state = stack.pop()
        if current_state == goal_state:
            return reconstruct_path(current_state)

        if current_state not in visited:
            visited.add(current_state)
            for successor in generate_successors(current_state):
                if successor not in visited:
                    stack.append(successor)

    return None


def reconstruct_path(state):
    path = []
    while state.parent:
        path.append(state.action)
        state = state.parent
    return list(reversed(path))


# Run the DFS algorithm
solution = dfs()
print("DFS Solution:")
for step, action in enumerate(solution):
    print(f"Step {step + 1}: {action}")
print(f"Total steps: {len(solution)}")