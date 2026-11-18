"""第 2 題：用蒙地卡羅法計算單變數積分。
AI 使用說明：本程式由 ChatGPT 協助撰寫，使用前請自行理解與測試。
"""

import random


def integral_mc(f, low, high, samples=100000, seed=None):
    """隨機均勻取樣：積分 ≈ 區間長度 × 函數值平均。"""
    if not isinstance(samples, int) or samples <= 0:
        raise ValueError("samples 必須是正整數")
    rng = random.Random(seed)
    total = 0.0
    for _ in range(samples):
        x = rng.uniform(low, high)
        total += f(x)
    return (high - low) * total / samples


if __name__ == "__main__":
    # 測試：∫(0 到 1) x^2 dx = 1/3。
    f = lambda x: x ** 2
    result = integral_mc(f, 0, 1, samples=100000, seed=42)
    exact = 1 / 3
    print("測試 f(x) = x^2，範圍 [0, 1]")
    print(f"蒙地卡羅積分：{result:.8f}")
    print(f"正確值：{exact:.8f}")
    print(f"絕對誤差：{abs(result - exact):.8f}")
    assert abs(result - exact) < 0.01
    print("第 2 題測試通過！")
