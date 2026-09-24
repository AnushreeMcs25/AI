board = ["1", "2", "3",
         "4", "5", "6",
         "7", "8", "9"]

players = {
    "X": "human",
    "O": "computer"
}

winning_combinations = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
)

occupied = set()

def display_board():
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])
    print()

def check_winner(symbol):
    for combination in winning_combinations:
        if all(board[position] == symbol for position in combination):
            return True
    return False

def make_move(symbol):
    while True:
        choice = input(
            f"{players[symbol]} ({symbol}), choose a position (1-9): "
        )

        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        position = int(choice) - 1

        if position < 0 or position > 8:
            print("Please choose a position between 1 and 9.")
            continue

        if position in occupied:
            print("This position is already occupied.")
            continue

        board[position] = symbol
        occupied.add(position)
        break

print("Welcome to Tic-Tac-Toe!")

current_player = "X"

while True:
    display_board()

    make_move(current_player)

    if check_winner(current_player):
        display_board()
        print(players[current_player], "wins!")
        break

    if len(occupied) == 9:
        display_board()
        print("It's a draw!")
        break

    current_player = "O" if current_player == "X" else "X"

print("\nThanks for playing!")
