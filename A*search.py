import heapq

GOAL = ((1, 2, 3), (8, 0, 4), (7, 6, 5))


def manhattan(board):
  dist = 0
  pos = {val: (r, c) for r, row in enumerate(GOAL) for c, val in enumerate(row)}
  for r in range(3):
    for c in range(3):
      val = board[r][c]
      if val != 0:
        tr, tc = pos[val]
        dist += abs(r - tr) + abs(c - tc)
  return dist


def get_neighbors(board):
  neighbors = []
  r, c = next(
      (r, c) for r in range(3) for c in range(3) if board[r][c] == 0
  )
  for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
    nr, nc = r + dr, c + dc
    if 0 <= nr < 3 and 0 <= nc < 3:
      nb = [list(row) for row in board]
      nb[r][c], nb[nr][nc] = nb[nr][nc], nb[r][c]
      neighbors.append(tuple(tuple(row) for row in nb))
  return neighbors


def solve(start):
  start = tuple(tuple(row) for row in start)
  queue = [(manhattan(start), 0, start, [(start, manhattan(start))])]
  visited = {start: 0}

  while queue:
    _, g, curr, path = heapq.heappop(queue)

    if curr == GOAL:
      return path

    for nxt in get_neighbors(curr):
      if nxt not in visited or g + 1 < visited[nxt]:
        visited[nxt] = g + 1
        h = manhattan(nxt)
        heapq.heappush(queue, (g + 1 + h, g + 1, nxt, path + [(nxt, h)]))
  return None



start_board = ((2, 8, 3), (1, 6, 4), (7, 0, 5))
for step, h_val in solve(start_board):
  print(f'h-value: {h_val}')
  for row in step:
    print(row)
  print()
