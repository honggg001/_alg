
import math
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

def distance(a, b):
    x1, y1 = cities[a]
    x2, y2 = cities[b]
    return math.hypot(x2 - x1, y2 - y1)

def total_distance(route):
    return sum(
        distance(route[i], route[(i + 1) % len(route)])
        for i in range(len(route))
    )

def greedy():
    start = "A"
    route = [start]
    unvisited = set(cities.keys()) - {start}

    current = start

    while unvisited:
        # 選擇距離目前城市最近的城市
        nearest = min(
            unvisited,
            key=lambda city: (distance(current, city), city)
        )

        print(
            f"{current} -> {nearest}，"
            f"距離：{distance(current, nearest):.4f}"
        )

        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    print(
        f"{current} -> {start}，"
        f"距離：{distance(current, start):.4f}"
    )

    return route

def draw_route(route):
    path = route + [route[0]]
    x = [cities[c][0] for c in path]
    y = [cities[c][1] for c in path]

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, "o-", color="brown")

    for city, (cx, cy) in cities.items():
        plt.text(cx + 0.15, cy + 0.15, city, fontsize=12)

    plt.scatter(*cities["A"], color="red", s=120, zorder=5)
    plt.title("TSP - Greedy Algorithm")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")
    plt.show()

route = greedy()

print("\n貪婪演算法結果")
print("最終路線：", " -> ".join(route + [route[0]]))
print(f"總距離：{total_distance(route):.4f}")

draw_route(route)
