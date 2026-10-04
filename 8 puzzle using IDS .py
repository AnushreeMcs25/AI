from collections import deque
import copy


MOVES = {
    'Up': (-1, 0),
    'Down': (1, 0),
    'Left': (0, -1),
    'Right': (0, 1)
}

class PuzzleState:
    def __init__(self, board, depth=0, path=None):
        self.board = board
        self.depth = depth
        self.path = path or []  # Moves taken to reach this state

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def find_blank(self):
        """Find the position of the blank (0) tile."""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def generate_moves(self):
        """Generate all possible moves from the current state."""
        moves = []
        x, y = self.find_blank()
        for move, (dx, dy) in MOVES.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_board = copy.deepcopy(self.board)
                # Swap blank with the target tile
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                moves.append(PuzzleState(new_board, self.depth + 1, self.path + [move]))
        return moves


def depth_limited_search(state, goal, limit, visited):
    """Recursive depth-limited search."""
    if state.board == goal:
        return state.path

    if limit <= 0:
        return None

    visited.add(state)

    for neighbor in state.generate_moves():
        if neighbor not in visited:
            result = depth_limited_search(neighbor, goal, limit - 1, visited)
            if result is not None:
                return result

    return None


def iterative_deepening_search(start, goal, max_depth=50):
    """Perform IDS from depth 0 to max_depth."""
    for depth in range(max_depth + 1):
        visited = set()
        result = depth_limited_search(start, goal, depth, visited)
        if result is not None:
            return result
    return None


if __name__ == "__main__":
   
    start_board = [
        [2, 8, 3],
        [1, 6, 4],
        [7, 0, 5]
    ]

    goal_board = [
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ]

    start_state = PuzzleState(start_board)
    print("Starting IDS search...")

    solution = iterative_deepening_search(start_state, goal_board, max_depth=30)

    if solution:
        print(f"Solution found in {len(solution)} moves: {solution}")
    else:
        print("No solution found within depth limit.")
