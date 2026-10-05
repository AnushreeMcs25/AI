def find_conflicts(board):
    n = len(board)
    pairs = []

    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                pairs.append((i + 1, j + 1, "same column"))
            elif abs(board[i] - board[j]) == abs(i - j):
                pairs.append((i + 1, j + 1, "same diagonal"))

    return pairs


n = int(input("Enter number of queens: "))
board = list(map(int, input("Enter positions: ").split()))

pairs = find_conflicts(board)

print("\nState:", board)
print("\nAttacking Queen Pairs:")

if len(pairs) == 0:
    print("No conflicts")
else:
    for q1, q2, reason in pairs:
        print("Queen", q1, "and Queen", q2, "->", reason)

print("\nHeuristic =", len(pairs))
