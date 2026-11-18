"""第 6 題：改用蒙地卡羅法計算第 5 題的 n 維積分，測試 1、2、5、10 維。
AI 使用說明：本程式由 ChatGPT 協助撰寫，使用前請自行理解與測試。
"""

import random


def integral(f, low, high, samples=100000, seed=None):
    """n 維蒙地卡羅積分，可直接以 integral(f, low, high) 呼叫。"""
    if len(low) == 0 or len(low) != len(high):
        raise ValueError("low、high 必須是非空且長度相同的陣列")
    if not isinstance(samples, int) or samples <= 0:
        raise ValueError("samples 必須是正整數")

    volume = 1.0
    for a, b in zip(low, high):
        volume *= b - a

    rng = random.Random(seed)
    total = 0.0
    for _ in range(samples):
        point = [rng.uniform(a, b) for a, b in zip(low, high)]
        total += f(point)
    return volume * total / samples


if __name__ == "__main__":
    # 題目範例：f(x)=x1^2+...+xn^2，在 [0,1]^n 上正確積分為 n/3。
    f = lambda x: sum(value ** 2 for value in x)
    print("n 維蒙地卡羅積分：f(x)=x1^2+...+xn^2，low=0，high=1")
    for n in [1, 2, 5, 10]:
        low = [0.0] * n
        high = [1.0] * n
        result = integral(f, low, high, samples=100000, seed=42)
        exact = n / 3
        print(f"{n:2d} 維：數值={result:.8f}，正確值={exact:.8f}，誤差={abs(result-exact):.8f}")
        assert abs(result - exact) < 0.05
    print("第 6 題測試通過！")
