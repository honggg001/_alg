
# maze_dfs.py
# 第1題：老鼠走迷宮（DFS）

maze = [
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0]
]

ROWS = len(maze)
COLS = len(maze[0])

start = (0, 0)
end = (4, 4)

visited = set()
path = []

# 上、右、下、左
directions = [
    (-1, 0), (0, 1),
    (1, 0), (0, -1)
]


def dfs(x, y):
    if (x, y) == end:
        path.append((x, y))
        return True

    visited.add((x, y))
    path.append((x, y))

    for dx, dy in directions:
        nx = x + dx
        ny = y + dy

        if 0 <= nx < ROWS and 0 <= ny < COLS:
            if maze[nx][ny] == 0 and (nx, ny) not in visited:
                if dfs(nx, ny):
                    return True

    path.pop()
    return False


def print_maze():
    for i in range(ROWS):
        for j in range(COLS):
            if (i, j) == start:
                print("S", end=" ")
            elif (i, j) == end:
                print("E", end=" ")
            elif (i, j) in path:
                print("*", end=" ")
            elif maze[i][j] == 1:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()


if __name__ == "__main__":
    if dfs(*start):
        print("找到路徑！")
        print("路徑：", path)
        print_maze()
    else:
        print("找不到路徑")
