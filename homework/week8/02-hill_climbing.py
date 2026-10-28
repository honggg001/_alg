
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

def hill_climbing():
    route = list(cities.keys())
    step = 0

    print("初始距離：", round(total_distance(route), 4))

    while True:
        best_route = route[:]
        best_distance = total_distance(route)

        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                neighbor = route[:i] + route[i:j+1][::-1] + route[j+1:]
                d = total_distance(neighbor)

                if d < best_distance - 1e-9:
                    best_route = neighbor
                    best_distance = d

        if best_route == route:
            break

        route = best_route
        step += 1
        print(f"第 {step} 次爬山：{best_distance:.4f}")

    return route

def draw_route(route):
    path = route + [route[0]]
    x = [cities[c][0] for c in path]
    y = [cities[c][1] for c in path]

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, "o-", color="green")

    for city, (cx, cy) in cities.items():
        plt.text(cx + 0.15, cy + 0.15, city, fontsize=12)

    plt.scatter(*cities["A"], color="red", s=120, zorder=5)
    plt.title("TSP - Hill Climbing")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")
    plt.show()

route = hill_climbing()
print("\n最終路線：", " -> ".join(route + [route[0]]))
print(f"總距離：{total_distance(route):.4f}")
draw_route(route)
