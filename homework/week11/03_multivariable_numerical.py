"""第 3 題：用數值方法計算 n 變數梯度與超體積積分。
AI 使用說明：本程式由 ChatGPT 協助撰寫，使用前請自行理解與測試。
"""

from itertools import product


def gradient(f, x, h=1e-5):
    """分別對每個變數做中央差分，回傳梯度向量。"""
    if h <= 0:
        raise ValueError("h 必須大於 0")
    if len(x) == 0:
        raise ValueError("x 不可以是空陣列")
    result = []
    for i in range(len(x)):
        x_plus = list(x)
        x_minus = list(x)
        x_plus[i] += h
        x_minus[i] -= h
        result.append((f(x_plus) - f(x_minus)) / (2 * h))
    return result


def integral_nd(f, low, high, steps=50):
    """n 維中點法：每個維度分成 steps 份，累加格子中心的函數值。"""
    if len(low) == 0 or len(low) != len(high):
        raise ValueError("low 和 high 長度必須相等且不能為空")
    if not isinstance(steps, int) or steps <= 0:
        raise ValueError("steps 必須是正整數")

    widths = [(b - a) / steps for a, b in zip(low, high)]
    cell_volume = 1.0
    for width in widths:
        cell_volume *= width

    total = 0.0
    for indices in product(range(steps), repeat=len(low)):
        point = [a + (i + 0.5) * width for a, i, width in zip(low, indices, widths)]
        total += f(point)
    return total * cell_volume


if __name__ == "__main__":
    # 測試：f(x,y)=x^2+y^2，梯度=(2x,2y)，在 (1,2) 時是 (2,4)。
    f = lambda x: x[0] ** 2 + x[1] ** 2
    grad = gradient(f, [1.0, 2.0])
    print("測試 f(x,y) = x^2 + y^2")
    print(f"梯度在 (1,2)：{[round(v, 6) for v in grad]}，正確值=[2, 4]")
    assert all(abs(g - e) < 1e-4 for g, e in zip(grad, [2, 4]))

    # 在單位正方形上積分，正確值為 2/3。
    result = integral_nd(f, [0, 0], [1, 1], steps=100)
    print(f"二維積分：{result:.8f}，正確值={2/3:.8f}")
    assert abs(result - 2/3) < 1e-3
    print("第 3 題測試通過！")
