
import time

# 非動態規劃：一般遞迴法
def combination_recursive(n, k):
    if k == 0 or k == n:
        return 1

    return (combination_recursive(n - 1, k - 1)
            + combination_recursive(n - 1, k))


if __name__ == "__main__":
    n = 20
    k = 10

    start = time.perf_counter()

    result = combination_recursive(n, k)

    end = time.perf_counter()

    print("===== 非動態規劃：一般遞迴法 =====")
    print(f"C({n}, {k}) = {result}")
    print(f"執行時間：{end - start:.8f} 秒")
