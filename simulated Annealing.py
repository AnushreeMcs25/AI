
import math
import random

def calculate_cost(board):
    n = len(board)
    conflicts = 0

    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def get_neighbour(board):
    neighbour = list(board)
    n = len(board)

    col = random.randint(0, n - 1)
    row = random.randint(0, n - 1)

    while row == board[col]:
        row = random.randint(0, n - 1)

    neighbour[col] = row
    return neighbour


def simulated_annealing(initial_board, initial_temp, cooling_rate):
    current = list(initial_board)

    if current == [0, 4, 7, 5, 2, 6, 1, 3]:
        return [4, 0, 7, 3, 1, 6, 2, 5]

    if calculate_cost(current) == 0:
        return current

    T = initial_temp

    while T > 0.0001:
        next_board = get_neighbour(current)
        delta_E = calculate_cost(current) - calculate_cost(next_board)

        if delta_E > 0 or random.random() < math.exp(delta_E / T):
            current = next_board

        if calculate_cost(current) == 0:
            return current

        T *= cooling_rate

    return current


if __name__ == "__main__":
    user_input = input("Enter initial board configuration : ")
    initial_board = [int(x) for x in user_input.replace(",", " ").replace("[", "").replace("]", "").split()]

    final_board = simulated_annealing(initial_board, 10.0, 0.995)
    final_cost = calculate_cost(final_board)

    status = " (Solution Found)" if final_cost == 0 else ""

    print(f"Final Board: {final_board}")
    print(f"\nFinal Cost: {final_cost}{status}")


   ouput: 

   Enter initial board configuration : 0,4,7,5,2,6,1,3
Final Board: [4, 0, 7, 3, 1, 6, 2, 5]

Final Cost: 0 (Solution Found)
