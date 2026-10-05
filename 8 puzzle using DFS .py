MOVES = {
    'UP': -3,
    'DOWN': 3,
    'LEFT': -1,
    'RIGHT': 1
}

INVALID = {
    0: ['UP', 'LEFT'],
    1: ['UP'],
    2: ['UP', 'RIGHT'],
    3: ['LEFT'],
    5: ['RIGHT'],
    6: ['DOWN', 'LEFT'],
    7: ['DOWN'],
    8: ['DOWN', 'RIGHT']
}

def move(state, direction):
    pos = state.index(0)

    if direction in INVALID.get(pos, []):
        return None

    new_pos = pos + MOVES[direction]
    s = list(state)

    s[pos], s[new_pos] = s[new_pos], s[pos]

    return tuple(s)

def dfs(start, goal):
    stack = [(start, [])]
    visited = set()

    while stack:
        state, path = stack.pop()

        if state == goal:
            return path + [state]

        if state in visited:
            continue

        visited.add(state)

        for direction in MOVES:
            new_state = move(state, direction)

            if new_state is not None and new_state not in visited:
                stack.append((new_state, path + [state]))

    return None

def display(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

start = tuple(map(int, input("Enter initial state: ").split()))
goal = tuple(map(int, input("Enter goal state: ").split()))

print("\nInitial State:")
display(start)

print("Goal State:")
display(goal)

solution = dfs(start, goal)

if solution:
    print("Solution found in", len(solution) - 1, "moves:\n")

    for state in solution:
        display(state)
else:
    print("No solution found.")
