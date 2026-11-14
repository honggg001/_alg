
import time

from recursion import combination_recursive
from dynamic_programming import combination_dp


# 測試函式
def measure_time(func, n, k):
    start = time.perf_counter()
    result = func(n, k)
    end = time.perf_counter()

    return result, end - start


if __name__ == "__main__":

    test_cases = [
        (10, 5),
        (20, 10),
        (25, 12),
        (30, 15)
    ]

    print("===== 組合數演算法效率比較 =====")

    for n, k in test_cases:

        print(f"\n測試 C({n}, {k})")
        print("-" * 45)

        result1, time1 = measure_time(
            combination_recursive, n, k
        )

        result2, time2 = measure_time(
            combination_dp, n, k
        )

        print(f"一般遞迴結果：{result1}")
        print(f"一般遞迴時間：{time1:.8f} 秒")

        print(f"動態規劃結果：{result2}")
        print(f"動態規劃時間：{time2:.8f} 秒")

        if result1 == result2:
            print("結果驗證：正確")
        else:
            print("結果驗證：錯誤")

        if time2 > 0:
            print(f"速度比值：{time1 / time2:.2f} 倍")

        print("-" * 45)
