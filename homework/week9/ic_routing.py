
# ic_routing.py
# 第5題：IC電路繞線（DFS、BFS、A*）

import time
import heapq
from collections import deque

grid = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (5, 5)

directions = [
    (0, 1), (1, 0),
    (0, -1), (-1, 0)
]


def neighbors(node):
    x, y = node

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] == 0:
                yield (nx, ny)


def reconstruct(parent, end):
    path = [end]

    while path[-1] in parent:
        path.append(parent[path[-1]])

    return path[::-1]


# DFS
def dfs():
    stack = [start]
    visited = {start}
    parent = {}

    while stack:
        node = stack.pop()

        if node == goal:
            return reconstruct(parent, node), len(visited)

        for next_node in neighbors(node):
            if next_node not in visited:
                visited.add(next_node)
                parent[next_node] = node
                stack.append(next_node)

    return None, len(visited)


# BFS
def bfs():
    queue = deque([start])
    visited = {start}
    parent = {}

    while queue:
        node = queue.popleft()

        if node == goal:
            return reconstruct(parent, node), len(visited)

        for next_node in neighbors(node):
            if next_node not in visited:
                visited.add(next_node)
                parent[next_node] = node
                queue.append(next_node)

    return None, len(visited)


# A*
def heuristic(node):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def astar():
    heap = [(heuristic(start), start)]
    g_score = {start: 0}
    parent = {}
    visited = set()

    while heap:
        _, node = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)

        if node == goal:
            return reconstruct(parent, node), len(visited)

        for next_node in neighbors(node):
            new_g = g_score[node] + 1

            if new_g < g_score.get(next_node, float("inf")):
                g_score[next_node] = new_g
                parent[next_node] = node

                f = new_g + heuristic(next_node)
                heapq.heappush(heap, (f, next_node))

    return None, len(visited)


def print_grid(path):
    path_set = set(path or [])

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            pos = (i, j)

            if pos == start:
                symbol = "S"
            elif pos == goal:
                symbol = "E"
            elif grid[i][j] == 1:
                symbol = "#"
            elif pos in path_set:
                symbol = "*"
            else:
                symbol = "."

            print(symbol, end=" ")
        print()


def test_algorithm(name, func):
    start_time = time.perf_counter()
    path, visited_count = func()
    elapsed = time.perf_counter() - start_time

    print(f"\n===== {name} =====")

    if path:
        print("路徑長度：", len(path) - 1)
        print("已發現/處理節點數：", visited_count)
        print(f"執行時間：{elapsed:.8f} 秒")
        print_grid(path)
    else:
        print("找不到路徑")


if __name__ == "__main__":
    test_algorithm("DFS", dfs)
    test_algorithm("BFS", bfs)
    test_algorithm("A*", astar)
