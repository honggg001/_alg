# iter_framework.py 模組技術說明文件

本文件針對演算法課程倉庫中 iter_framework.py 之設計理念、架構層次與具體實作進行完整說明。

---

## 1. 核心理念與架構設計

### 1.1 離散動力系統的抽象表示

數值計算與機器學習中的諸多演算法本質上均可視為「離散狀態空間上的迭代推進」：

狀態推進式：s_(k+1) = T(s_k)

此腳本將控制流程與數值計算解耦：

* 引擎層 (Engine Layer)：由 generic_iterator 負責迭代推進、防護最大上限、狀態交替與收斂驗證。
* 策略層 (Strategy Layer)：使用者僅需注入狀態轉移函數 T 與收斂條件判斷式，無須重寫迴圈邏輯。
       |           generic_iterator 核心迴圈          |
       |                                             |
       |  for iteration in range(max_iter):          |
       |      next_state = transition_func(state)    |
       |      if is_converged(state, next_state):    |
       |          return next_state                  |
       +---------------------------------------------+
                        ^            ^
           注入轉移邏輯  |            | 注入終止條件
                        |            |
       +----------------+    +-------+---------------+
       | transition_func|    | is_converged          |
       | (不動點/梯度/   |    | (殘差範數/邊界條件/   |
       |  特徵值/EM步等)|    |  時間終點)            |
       +----------------+    +-----------------------+
2. 核心 API 規格說明

### generic_iterator 函式

函式原型：
generic_iterator(transition_func, is_converged, initial_state, max_iter=1000)

#### 參數規格

* transition_func: Callable[[T], T]
  推進函數 g(x)，輸入當前狀態並輸出新狀態。支援純量、NumPy 向量、矩陣或自定義元組。

* is_converged: Callable[[T, T, int], bool]
  終止判定回呼函數，簽章為 (old_state, new_state, iter_index) -> bool。

* initial_state: T
  迭代起點初值 s_0。

* max_iter: int
  安全最大迭代次數（預設 1000），避免發散時陷入無窮迴圈。

#### 回傳值

* final_state (T)：收斂達成時或步數耗盡時的狀態物件。
* iteration + 1 (int)：實際消耗的迭代次數。

---

3. 涵蓋領域與 9 大經典實作拆解

本腳本透過具體範例示範了該框架跨足 4 大數學與資工領域的通用性：

一、 數值分析與非線性求根

* 二維不動點迭代 (demo_fixed_point)：
  * 狀態：二維座標向量 [x1, x2]^T。
  * 轉移邏輯：X_(k+1) = A * X_k + B 線性轉換。
  * 終止條件：向量二範數差距 ||X_(k+1) - X_k|| < 1e-6。

* 牛頓-拉弗森法求根 (demo_newton)：
  * 狀態：純量 x。
  * 轉移邏輯：x_(k+1) = x_k - f(x_k) / f'(x_k)，此處求解 x^2 - 4 = 0。
  * 終止條件：絕對差值 |x_(k+1) - x_k| < 1e-6。

二、 數值線性代數

* 高斯-賽得爾求解器 (demo_gauss_seidel)：
  * 狀態：線性方程組 Ax = b 的解向量 x。
  * 轉移邏輯：逐分量以當期已更新之最新值向前推進（In-place 前向代入）。
  * 終止條件：無窮範數 max(|x_(k+1) - x_k|) < 1e-6。

* 冪次迭代法 (demo_power_iteration)：
  * 狀態：特徵向量 v。
  * 轉移邏輯：v_(k+1) = A * v_k / ||A * v_k||，提取主特徵向量與透過瑞利商導出主特徵值。
  * 終止條件：np.allclose(old, new, atol=1e-6)。

* QR 演算法 (demo_qr_algorithm)：
  * 狀態：矩陣 A_k。
  * 轉移邏輯：正交分解與反向乘積 A_k = Q_k * R_k -> A_(k+1) = R_k * Q_k。
  * 終止條件：非對角線元素的絕對值總和趨近於零（sum(|A_ij|) < 1e-6, i != j）。

三、 動態模擬與圖論演算法

* 經典四階龍格-庫塔法 (demo_rk4)：
  * 狀態：時間與變數複合元組 (t, y)。
  * 轉移邏輯：採納 k1, k2, k3, k4 加權斜率積分微分方程 dy/dt = y - t + 1。
  * 終止條件：模擬推進達到指定終點時間（t >= t_end - 1e-9），展示框架支援邊界條件導向的迭代控制。

* PageRank 演算法 (demo_pagerank)：
  * 狀態：網頁權重分佈機率向量 r。
  * 轉移邏輯：Google 矩陣乘法 r_(k+1) = (d * M + (1 - d) / n * E) * r_k。
  * 終止條件：機率向量的二範數差距 ||r_(k+1) - r_k|| < 1e-6。

四、 統計學習與分群演算法

* K-Means 分群 (demo_kmeans)：
  * 狀態：群中心座標矩陣 C。
  * 轉移邏輯：標準 Hard EM 流程（E 步計算全距指派標籤，M 步取樣本均值更新中心）。
  * 終止條件：群中心最大座標偏移 max(|C_(k+1) - C_k|) < 1e-6。

* Two-Coin 潛在變數 EM 估計 (demo_em_two_coin)：
  * 狀態：雙硬幣正面機率參數元組 (theta_A, theta_B)。
  * 轉移邏輯：E 步基於當前參數推導試驗硬幣後驗權重，M 步重新最大化似然函數計算新參數。
  * 終止條件：雙參數變動幅度同步小於 1e-6。

---

4. 框架特點與工程分析

1. 零依賴通用性：
   除矩陣計算依賴 numpy 外，迭代引擎本身未繫結任何領域特定結構，能兼容純量 float、陣列 np.ndarray、元組 tuple 乃至字典或自訂物件。

2. Lambda 與 Closure 封裝：
   策略實作大量運用閉包 (Closure) 與匿名函數 (Lambda)，將方程參數（如矩陣 A、步長 h、阻尼因子 d）鎖定於展示函式作用域內，使傳遞給引擎的介面維持單一輸入與輸出。

3. 終止機制多態：
   收斂判斷不限制於純量數值差，可彈性定義為範數收斂、非對角元素消除程度、時間軸區間終點或多參數同步收斂。