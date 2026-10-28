
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

D = np.array([
    [distance(a, b) for b in names]
    for a in names
])

def decode(X):
    """將連續矩陣轉成合法的城市順序"""
    remaining = set(range(1, n))
    order = [0]

    for position in range(1, n):
        chosen = max(
            remaining,
            key=lambda i: X[i, position]
        )
        order.append(chosen)
        remaining.remove(chosen)

    return [names[i] for i in order]

def objective(X):
    # 每個城市只出現一次
    row_error = np.sum((X.sum(axis=1) - 1) ** 2)

    # 每個旅行位置只有一個城市
    col_error = np.sum((X.sum(axis=0) - 1) ** 2)

    # 相鄰旅行位置的距離
    next_X = np.roll(X, -1, axis=1)
    route_cost = np.sum(X * (D @ next_X))

    return 10 * row_error + 10 * col_error + route_cost

def gradient(X):
    row_error = X.sum(axis=1, keepdims=True) - 1
    col_error = X.sum(axis=0, keepdims=True) - 1

    prev_X = np.roll(X, 1, axis=1)
    next_X = np.roll(X, -1, axis=1)

    return (
        20 * row_error
        + 20 * col_error
        + D @ (prev_X + next_X)
    )

def steepest_descent():
    rng = np.random.default_rng(42)

    # 初始化連續矩陣
    X = rng.uniform(0.01, 0.2, (n, n))

    learning_rate = 0.005
    iterations = 5000

    best_route = None
    best_distance = float("inf")

    for step in range(iterations):
        grad = gradient(X)

        # 沿負梯度方向更新
        X = X - learning_rate * grad

        # 將數值限制在 0 到 1
        X = np.clip(X, 0, 1)

        if step % 50 == 0:
            route = decode(X)
            length = total_distance(route)

            if length < best_distance:
                best_distance = length
                best_route = route[:]

        if step % 1000 == 0:
            print(
                f"第 {step} 次迭代，"
                f"目標函數 = {objective(X):.4f}"
            )

    return best_route

def draw_route(route):
    path = route + [route[0]]
    x = [cities[c][0] for c in path]
    y = [cities[c][1] for c in path]

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, "o-", color="orange")

    for city, (cx, cy) in cities.items():
        plt.text(cx + 0.15, cy + 0.15, city, fontsize=12)

    plt.scatter(*cities["A"], color="red", s=120, zorder=5)
    plt.title("TSP - Steepest Descent")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")
    plt.show()

route = steepest_descent()

print("\n最速下降法結果")
print("最終路線：", " -> ".join(route + [route[0]]))
print(f"總距離：{total_distance(route):.4f}")

draw_route(route)
