"""第 5 題：用黎曼和（中點法）計算 n 維積分，測試 1、2、5、10 維。
AI 使用說明：本程式由 ChatGPT 協助撰寫，使用前請自行理解與測試。
"""

from itertools import product


def integral(f, low, high, steps=3):
    """n 維黎曼和：n 由 low/high 長度決定，每軸切分 steps 小段。

    函數可直接以 integral(f, low, high) 呼叫，steps 是可選的精度參數。
    總取樣點數 = steps ** n，n 很大時須避免 steps 設定過高。
    """
    if len(low) == 0 or len(low) != len(high):
        raise ValueError("low、high 必須是非空且長度相同的陣列")
    if not isinstance(steps, int) or steps <= 0:
        raise ValueError("steps 必須是正整數")

    n = len(low)
    widths = [(high[i] - low[i]) / steps for i in range(n)]
    cell_volume = 1.0
    for width in widths:
        cell_volume *= width

    total = 0.0
    for indices in product(range(steps), repeat=n):
        point = [low[i] + (indices[i] + 0.5) * widths[i] for i in range(n)]
        total += f(point)
    return total * cell_volume


if __name__ == "__main__":
    # 題目範例：f(x)=x1^2+...+xn^2，在 [0,1]^n 上正確積分為 n/3。
    f = lambda x: sum(value ** 2 for value in x)

    # 高維每增加一個維度，格點數會大幅增加，因此分別設定每軸切分數。
    steps_by_dimension = {1: 1000, 2: 100, 5: 8, 10: 3}
    print("n 維黎曼積分（中點法）：f(x)=x1^2+...+xn^2，low=0，high=1")
    for n, steps in steps_by_dimension.items():
        low = [0.0] * n
        high = [1.0] * n
        result = integral(f, low, high, steps=steps)
        exact = n / 3
        print(f"{n:2d} 維：格點數={steps**n:>7d}，數值={result:.8f}，正確值={exact:.8f}，誤差={abs(result-exact):.8f}")
        # 中點法對平方函數有確定的誤差：n/(12*steps^2)。
        assert abs(result - exact) < n / (12 * steps**2) + 1e-8
    print("第 5 題測試通過！")
