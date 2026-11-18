"""第 1 題：用數值方法計算單變數微分與積分。
AI 使用說明：本程式由 ChatGPT 協助撰寫，使用前請自行理解與測試。
"""

import math


def derivative(f, x, h=1e-5):
    """中央差分法：f'(x) ≈ [f(x+h) - f(x-h)] / (2h)。"""
    if h <= 0:
        raise ValueError("h 必須大於 0")
    return (f(x + h) - f(x - h)) / (2 * h)


def integral(f, low, high, n=10000):
    """梯形法：把區間切成 n 個小梯形後加總面積。"""
    if n <= 0 or not isinstance(n, int):
        raise ValueError("n 必須是正整數")
    dx = (high - low) / n
    total = (f(low) + f(high)) / 2
    for i in range(1, n):
        total += f(low + i * dx)
    return total * dx


if __name__ == "__main__":
    # 測試 1：f(x)=x^2，在 x=2 時導數應為 4；在 [0,1] 積分應為 1/3。
    f = lambda x: x ** 2
    d = derivative(f, 2)
    area = integral(f, 0, 1)
    print("測試 f(x) = x^2")
    print(f"f'(2)：數值={d:.8f}，正確值=4")
    print(f"積分 [0,1]：數值={area:.8f}，正確值={1/3:.8f}")
    assert abs(d - 4) < 1e-4
    assert abs(area - 1/3) < 1e-4

    # 測試 2：f(x)=sin(x)，在 x=0 時導數應為 1；在 [0,pi] 積分應為 2。
    d2 = derivative(math.sin, 0)
    area2 = integral(math.sin, 0, math.pi)
    print("\n測試 f(x) = sin(x)")
    print(f"f'(0)：數值={d2:.8f}，正確值=1")
    print(f"積分 [0,pi]：數值={area2:.8f}，正確值=2")
    assert abs(d2 - 1) < 1e-4
    assert abs(area2 - 2) < 1e-4
    print("第 1 題測試通過！")
