# 數值微分與積分：6 題 Python 作業

## 使用環境

- Python 3.10 以上（Python 3.14 亦可）
- VS Code 或其他 Python 編輯器
- **不需要安裝第三方套件**：只使用 Python 內建的 `math`、`random`、`itertools`。

## 檔案與解題方法

| 題目 | 檔案 | 方法與測試內容 |
|---|---|---|
| 1 | `01_single_variable_numerical.py` | 中央差分法計算單變數導數；梯形法計算單變數積分；測試 $x^2$、$\sin x$。 |
| 2 | `02_single_variable_monte_carlo.py` | 在區間內均勻抽樣，取函數平均乘以區間長度；測試 $\int_0^1 x^2\,dx$。 |
| 3 | `03_multivariable_numerical.py` | 各變數的中央差分組成梯度；使用 n 維中點法計算超體積積分；測試 $x^2+y^2$。 |
| 4 | `04_multivariable_monte_carlo.py` | 在 n 維超長方體內均勻抽樣，函數平均乘上超體積；測試 $x^2+y^2+z^2$。 |
| 5 | `05_riemann_nd.py` | `integral(f, low, high)`；用 n 維黎曼和（中點法）測試 **1、2、5、10 維**。 |
| 6 | `06_monte_carlo_nd.py` | `integral(f, low, high)`；改用 n 維蒙地卡羅法測試 **1、2、5、10 維**。 |

## 如何在 VS Code 執行

1. 開啟 VS Code，選取本資料夾，確認電腦已安裝 Python。
2. 開啟 **Terminal → New Terminal（終端機）**。
3. 在資料夾內依序執行：

```bash
python 01_single_variable_numerical.py
python 02_single_variable_monte_carlo.py
python 03_multivariable_numerical.py
python 04_multivariable_monte_carlo.py
python 05_riemann_nd.py
python 06_monte_carlo_nd.py
```

> 如果系統使用 `python3` 指令，請將 `python` 改成 `python3`。

## 公式與原理

**中央差分微分：**

$$f'(x)\approx\frac{f(x+h)-f(x-h)}{2h}$$

**梯形積分：** 將 $[a,b]$ 分成 $m$ 小段，長度 $\Delta x=(b-a)/m$，每小段的面積以梯形近似，再加總。

**n 維中點黎曼和：** 把每一維分成 $k$ 段，在每個小格的中心點取函數值，乘以格子的 n 維體積 $\Delta V$ 後加總：

$$\int_D f(\mathbf{x})\,d\mathbf{x}\approx\sum_{\text{小格}} f(\text{中心點})\Delta V$$

**蒙地卡羅積分：** 在範圍 $D$ 內均勻隨機取樣 $N$ 個點：

$$\int_D f(\mathbf{x})\,d\mathbf{x}\approx V(D)\cdot\frac{1}{N}\sum_{i=1}^{N}f(\mathbf{x}_i)$$

其中 $V(D)=\prod_{j=1}^n(high_j-low_j)$ 為 n 維超長方體的超體積。

## 第 5、6 題的測試設定與正確答案

測試函數為：

$$f(x_1,\ldots,x_n)=x_1^2+x_2^2+\cdots+x_n^2$$

`low = [0.0] * n`、`high = [1.0] * n`，所以每個維度的積分區間都是 $[0,1]$。

因為每個 $x_i^2$ 在 $[0,1]$ 的積分是 $1/3$，因此 **n 維正確答案為 $n/3$**：

| 維度 n | 正確答案 n/3 | 第 5 題每維分段數 | 第 5 題取樣格點數 | 第 6 題隨機樣本數 |
|---|---:|---:|---:|---:|
| 1 | 0.33333333 | 1000 | 1,000 | 100,000 |
| 2 | 0.66666667 | 100 | 10,000 | 100,000 |
| 5 | 1.66666667 | 8 | 32,768 | 100,000 |
| 10 | 3.33333333 | 3 | 59,049 | 100,000 |

**注意：** 黎曼法格點數為 `steps ** n`，維度增加時計算量會快速成長，因此第 5 題對 10 維採取較少分段數。蒙地卡羅法的數值受抽樣影響，所以會和精確值有小幅差距；程式固定 `seed=42`，便於重現結果。`assert` 是用來自動檢查測試誤差是否在容許範圍內。

## AI 使用聲明

**有使用 AI。** 本作業的六份 Python 程式以及本 README.md 均由 **ChatGPT（OpenAI）協助撰寫**，包含演算法實作、程式註解、測試案例及文件說明。作業提交前應自行執行、理解並確認程式結果，並依課程規定揭露 AI 的使用情形。每份 `.py` 的開頭也各有 AI 使用說明。
