
# npc_astar.py
# 第4題：NPC搜尋玩家（A*）

import heapq

grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

start = (0, 0)
goal = (4, 4)

directions = [
    (0, 1), (1, 0),
    (0, -1), (-1, 0)
]


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar():
    open_list = []
    heapq.heappush(open_list, (0, start))

    came_from = {}
    g_score = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = [current]

            while current in came_from:
                current = came_from[current]
                path.append(current)

            return path[::-1]

        for dx, dy in directions:
            neighbor = (
                current[0] + dx,
                current[1] + dy
            )

            x, y = neighbor

            if not (0 <= x < len(grid)
                    and 0 <= y < len(grid[0])):
                continue

            if grid[x][y] == 1:
                continue

            new_g = g_score[current] + 1

            if new_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = new_g

                f = new_g + heuristic(neighbor, goal)

                heapq.heappush(open_list, (f, neighbor))

    return None


def print_grid(path):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            pos = (i, j)

            if pos == start:
                print("N", end=" ")
            elif pos == goal:
                print("P", end=" ")
            elif path and pos in path:
                print("*", end=" ")
            elif grid[i][j] == 1:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()


if __name__ == "__main__":
    path = astar()

    if path:
        print("NPC 找到玩家！")
        print("路徑：", path)
        print("移動步數：", len(path) - 1)
        print_grid(path)
    else:
        print("找不到玩家")
