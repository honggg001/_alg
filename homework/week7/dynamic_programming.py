
import time

# 動態規劃：表格法
def combination_dp(n, k):
    dp = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        for j in range(min(i, k) + 1):

            if j == 0 or j == i:
                dp[i][j] = 1
            else:
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]

    return dp[n][k]


if __name__ == "__main__":
    n = 20
    k = 10

    start = time.perf_counter()

    result = combination_dp(n, k)

    end = time.perf_counter()

    print("===== 動態規劃：表格法 =====")
    print(f"C({n}, {k}) = {result}")
    print(f"執行時間：{end - start:.8f} 秒")

