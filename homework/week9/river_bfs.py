
# river_bfs.py
# 第2題：狼羊甘藍菜過河（BFS）

from collections import deque

# 狀態：(農夫, 狼, 羊, 甘藍菜)
# 0 = 左岸，1 = 右岸

start = (0, 0, 0, 0)
goal = (1, 1, 1, 1)

names = ["農夫", "狼", "羊", "甘藍菜"]


def is_valid(state):
    farmer, wolf, goat, cabbage = state

    if wolf == goat and farmer != wolf:
        return False

    if goat == cabbage and farmer != goat:
        return False

    return True


def get_next_states(state):
    next_states = []

    # 農夫單獨過河，或帶一樣物品
    for item in [None, 1, 2, 3]:
        new_state = list(state)

        if item is not None:
            if state[item] != state[0]:
                continue
            new_state[item] = 1 - new_state[item]

        new_state[0] = 1 - new_state[0]
        new_state = tuple(new_state)

        if is_valid(new_state):
            next_states.append(new_state)

    return next_states


def bfs():
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        state, path = queue.popleft()

        if state == goal:
            return path

        for next_state in get_next_states(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append(
                    (next_state, path + [next_state])
                )

    return None


if __name__ == "__main__":
    solution = bfs()

    if solution:
        print("找到最短過河方案！")

        for i, state in enumerate(solution):
            left = [
                names[j] for j in range(4)
                if state[j] == 0
            ]

            right = [
                names[j] for j in range(4)
                if state[j] == 1
            ]

            print(f"\n步驟 {i}")
            print("左岸：", left)
            print("右岸：", right)

        print("\n總渡河次數：", len(solution) - 1)
    else:
        print("找不到解答")
