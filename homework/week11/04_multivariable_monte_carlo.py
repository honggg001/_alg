"""第 4 題：用蒙地卡羅法計算 n 變數積分（超體積）。
AI 使用說明：本程式由 ChatGPT 協助撰寫，使用前請自行理解與測試。
"""

import random


def integral_mc_nd(f, low, high, samples=100000, seed=None):
    """n 維蒙地卡羅積分：區域超體積 × 隨機取樣函數平均值。"""
    if len(low) == 0 or len(low) != len(high):
        raise ValueError("low 和 high 長度必須相等且不能為空")
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
    # 測試 f(x,y,z)=x^2+y^2+z^2，在 [0,1]^3 積分正確值=3/3=1。
    f = lambda x: sum(value ** 2 for value in x)
    result = integral_mc_nd(f, [0, 0, 0], [1, 1, 1], samples=100000, seed=42)
    exact = 1.0
    print("測試 f(x,y,z) = x^2 + y^2 + z^2，範圍 [0,1]^3")
    print(f"蒙地卡羅積分：{result:.8f}")
    print(f"正確值：{exact:.8f}")
    print(f"絕對誤差：{abs(result - exact):.8f}")
    assert abs(result - exact) < 0.02
    print("第 4 題測試通過！")
