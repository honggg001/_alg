
import math

# 第 1 題：T(n) = T(n-1) + 8
def T1(n):
    if n == 1:
        return 1
    return T1(n - 1) + 8


# 第 2 題：T(n) = 2T(n-1) + 9
def T2(n):
    if n == 1:
        return 1
    return 2 * T2(n - 1) + 9


# 第 3 題：T(n) = 2T(n/2) + 1
def T3(n):
    if n == 1:
        return 1
    return 2 * T3(n // 2) + 1


# 第 4 題：T(n) = T(n/2) + 1
def T4(n):
    if n == 1:
        return 1
    return T4(n // 2) + 1


# 主程式
if __name__ == "__main__":

    print("===== 遞迴方程式與時間複雜度 =====")

    # 使用 2 的次方方便計算
    test_values = [2, 4, 8, 16, 32, 64]

    for n in test_values:
        print(f"\nn = {n}")
        print("-" * 45)

        print(f"第 1 題：T(n) = {T1(n)}")
        print(f"公式：8n - 7 = {8*n - 7}")
        print("時間複雜度：O(n)")

        print(f"\n第 2 題：T(n) = {T2(n)}")
        print(f"公式：10*2^(n-1)-9 = {10*2**(n-1)-9}")
        print("時間複雜度：O(2^n)")

        print(f"\n第 3 題：T(n) = {T3(n)}")
        print(f"公式：2n - 1 = {2*n - 1}")
        print("時間複雜度：O(n)")

        print(f"\n第 4 題：T(n) = {T4(n)}")
        print(f"公式：log2(n)+1 = {int(math.log2(n))+1}")
        print("時間複雜度：O(log n)")
