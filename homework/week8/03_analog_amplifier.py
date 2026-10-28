
import math
import numpy as np
import matplotlib.pyplot as plt

cities = {
    "A": (2, 3),
    "B": (5, 8),
    "C": (9, 6),
    "D": (12, 2),
    "E": (8, 1),
    "F": (4, 1),
    "G": (1, 7),
    "H": (7, 4)
}

names = list(cities.keys())
n = len(names)

def distance(a, b):
    x1, y1 = cities[a]
    x2, y2 = cities[b]
    return math.hypot(x2 - x1, y2 - y1)

def total_distance(route):
    return sum(
        distance(route[i], route[(i + 1) % n])
        for i in range(n)
    )

# 建立城市距離矩陣
D = np.array([
    [distance(a, b) for b in names]
    for a in names
])

# 使用固定亂數種子
rng = np.random.default_rng(42)

def decode(V):
    """將神經元輸出轉成合法路線，固定 A 為起點"""
    remaining = set(range(1, n))
    order = [0]

    for position in range(1, n):
        chosen = max(
            remaining,
            key=lambda i: V[i, position]
        )
        order.append(chosen)
        remaining.remove(chosen)

    return [names[i] for i in order]

def hopfield():
    # Hopfield 神經網路參數
    A = 3.0
    B = 3.0
    C = 0.8
    dt = 0.01
    iterations = 5000

    # 神經元內部電位
    U = rng.normal(0, 0.1, (n, n))

    # sigmoid 活化函數
    def sigmoid(x):
        x = np.clip(x, -50, 50)
        return 1 / (1 + np.exp(-x))

    best_route = None
    best_distance = float("inf")

    for step in range(iterations):
        V = sigmoid(U)

        row_sum = V.sum(axis=1, keepdims=True)
        col_sum = V.sum(axis=0, keepdims=True)

        # 前一個與後一個旅行位置
        prev_V = np.roll(V, 1, axis=1)
        next_V = np.roll(V, -1, axis=1)

        # 類比神經網路能量梯度
        gradient = (
            A * (row_sum - 1)
            + B * (col_sum - 1)
            + C * (D @ (prev_V + next_V))
        )

        # 神經元連續動態更新
        U += dt * (-U - gradient)

        if step % 50 == 0:
            route = decode(sigmoid(U))
            length = total_distance(route)

            if length < best_distance:
                best_distance = length
                best_route = route[:]

    return best_route

def draw_route(route):
    path = route + [route[0]]
    x = [cities[c][0] for c in path]
    y = [cities[c][1] for c in path]

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, "o-", color="purple")

    for city, (cx, cy) in cities.items():
        plt.text(cx + 0.15, cy + 0.15, city, fontsize=12)

    plt.scatter(*cities["A"], color="red", s=120, zorder=5)
    plt.title("TSP - Analog Hopfield Network")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")
    plt.show()

route = hopfield()

print("Hopfield 神經網路結果")
print("最終路線：", " -> ".join(route + [route[0]]))
print(f"總距離：{total_distance(route):.4f}")

draw_route(route)
