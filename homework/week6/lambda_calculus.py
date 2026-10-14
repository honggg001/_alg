
from dataclasses import dataclass
import re


# ==========================================
# 1. Lambda Calculus 的資料結構
# ==========================================

class Expr:
    """所有 Lambda 表達式的父類別"""
    pass


@dataclass(frozen=True)
class Var(Expr):
    name: str


@dataclass(frozen=True)
class Abs(Expr):
    param: str
    body: Expr


@dataclass(frozen=True)
class App(Expr):
    func: Expr
    arg: Expr


# ==========================================
# 2. 將表達式轉換成字串
# ==========================================

def to_string(expr):
    if isinstance(expr, Var):
        return expr.name

    if isinstance(expr, Abs):
        return f"(λ{expr.param}.{to_string(expr.body)})"

    if isinstance(expr, App):
        return f"({to_string(expr.func)} {to_string(expr.arg)})"

    raise TypeError("未知的表達式類型")


# ==========================================
# 3. 詞法分析 Tokenizer
# ==========================================

TOKEN_PATTERN = re.compile(
    r"\s*(lambda\b|[λ\\().]|[A-Za-z_][A-Za-z0-9_']*)"
)


def tokenize(text):
    tokens = []
    pos = 0

    while pos < len(text):
        if text[pos:].strip() == "":
            break

        match = TOKEN_PATTERN.match(text, pos)

        if not match:
            raise SyntaxError(
                f"位置 {pos} 附近有無法辨識的字元：{text[pos:]}"
            )

        tokens.append(match.group(1))
        pos = match.end()

    return tokens


# ==========================================
# 4. 語法分析 Parser
# ==========================================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected=None):
        token = self.peek()

        if token is None:
            raise SyntaxError("表達式不完整")

        if expected is not None and token != expected:
            raise SyntaxError(
                f"預期 '{expected}'，但得到 '{token}'"
            )

        self.pos += 1
        return token

    def parse(self):
        expr = self.parse_expr()

        if self.peek() is not None:
            raise SyntaxError(
                f"多餘的符號：{self.peek()}"
            )

        return expr

    def parse_expr(self):
        # Lambda 抽象
        if self.peek() in ("λ", "\\", "lambda"):
            return self.parse_lambda()

        # 函數應用
        return self.parse_application()

    def parse_lambda(self):
        self.consume()

        params = []

        while self.peek() not in (".", None):
            token = self.consume()

            if not re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_']*", token
            ) or token == "lambda":
                raise SyntaxError("Lambda 參數名稱不合法")

            params.append(token)

        if not params:
            raise SyntaxError("Lambda 缺少參數")

        self.consume(".")

        body = self.parse_expr()

        # λx y.x 等同 λx.λy.x
        for param in reversed(params):
            body = Abs(param, body)

        return body

    def parse_application(self):
        expr = self.parse_atom()

        while self.peek() not in (None, ")", "."):
            arg = self.parse_atom()
            expr = App(expr, arg)

        return expr

    def parse_atom(self):
        token = self.peek()

        if token == "(":
            self.consume("(")
            expr = self.parse_expr()
            self.consume(")")
            return expr

        if token in ("λ", "\\", "lambda"):
            return self.parse_lambda()

        if token is None:
            raise SyntaxError("缺少表達式")

        if re.fullmatch(
            r"[A-Za-z_][A-Za-z0-9_']*", token
        ) and token != "lambda":
            self.consume()
            return Var(token)

        raise SyntaxError(f"不合法的符號：{token}")


def parse(text):
    tokens = tokenize(text)

    if not tokens:
        raise SyntaxError("不能輸入空白表達式")

    return Parser(tokens).parse()


# ==========================================
# 5. 找出自由變數 Free Variables
# ==========================================

def free_vars(expr):
    if isinstance(expr, Var):
        return {expr.name}

    if isinstance(expr, Abs):
        return free_vars(expr.body) - {expr.param}

    if isinstance(expr, App):
        return free_vars(expr.func) | free_vars(expr.arg)

    raise TypeError("未知的表達式類型")


def all_vars(expr):
    if isinstance(expr, Var):
        return {expr.name}

    if isinstance(expr, Abs):
        return {expr.param} | all_vars(expr.body)

    if isinstance(expr, App):
        return all_vars(expr.func) | all_vars(expr.arg)

    raise TypeError("未知的表達式類型")


# ==========================================
# 6. 產生不會衝突的新變數名稱
# ==========================================

def fresh_name(base, used):
    index = 1
    name = f"{base}_{index}"

    while name in used:
        index += 1
        name = f"{base}_{index}"

    return name


# ==========================================
# 7. Alpha Conversion 與變數替換
# ==========================================

def rename_bound(expr, old, new):
    """
    將目前作用域內，由外層 Lambda 綁定的 old
    改成 new；遇到同名內層 Lambda 則停止深入。
    """
    if isinstance(expr, Var):
        if expr.name == old:
            return Var(new)
        return expr

    if isinstance(expr, App):
        return App(
            rename_bound(expr.func, old, new),
            rename_bound(expr.arg, old, new)
        )

    if isinstance(expr, Abs):
        if expr.param == old:
            return expr

        return Abs(
            expr.param,
            rename_bound(expr.body, old, new)
        )

    raise TypeError("未知的表達式類型")


def substitute(expr, var, replacement):
    """
    將 expr 中自由出現的 var 替換成 replacement。
    使用 Alpha Conversion 避免變數捕獲。
    """
    if isinstance(expr, Var):
        if expr.name == var:
            return expr_replace(replacement)
        return expr

    if isinstance(expr, App):
        return App(
            substitute(expr.func, var, replacement),
            substitute(expr.arg, var, replacement)
        )

    if isinstance(expr, Abs):
        # 同名參數會遮蔽外層變數
        if expr.param == var:
            return expr

        # 不需要替換時直接返回
        if var not in free_vars(expr.body):
            return expr

        # 可能發生變數捕獲，先改名
        if expr.param in free_vars(replacement):
            used = (
                all_vars(expr)
                | all_vars(replacement)
                | {var}
            )

            new_param = fresh_name(expr.param, used)

            new_body = rename_bound(
                expr.body, expr.param, new_param
            )

            return Abs(
                new_param,
                substitute(new_body, var, replacement)
            )

        return Abs(
            expr.param,
            substitute(expr.body, var, replacement)
        )

    raise TypeError("未知的表達式類型")


def expr_replace(expr):
    # 表達式是不可變資料結構，可以直接重用
    return expr


# ==========================================
# 8. 執行一次 Beta Reduction
# ==========================================

def beta_step(expr):
    """
    Normal Order：
    優先歸約最左側、最外層的 Redex。

    回傳：
    (新表達式, 是否成功歸約, 步驟說明)
    """

    if isinstance(expr, App):

        # (λx.body) arg -> body[x := arg]
        if isinstance(expr.func, Abs):
            param = expr.func.param
            body = expr.func.body

            result = substitute(body, param, expr.arg)

            description = (
                f"β-歸約：將 {param} 替換為 "
                f"{to_string(expr.arg)}"
            )

            return result, True, description

        # 先嘗試歸約函數部分
        new_func, changed, description = beta_step(expr.func)

        if changed:
            return (
                App(new_func, expr.arg),
                True,
                description
            )

        # 再嘗試歸約參數部分
        new_arg, changed, description = beta_step(expr.arg)

        if changed:
            return (
                App(expr.func, new_arg),
                True,
                description
            )

    if isinstance(expr, Abs):
        new_body, changed, description = beta_step(expr.body)

        if changed:
            return (
                Abs(expr.param, new_body),
                True,
                description
            )

    return expr, False, ""


# ==========================================
# 9. 顯示完整計算過程
# ==========================================

def evaluate(expr, max_steps=100):
    print("\n" + "=" * 60)
    print("Lambda Calculus 計算過程")
    print("=" * 60)

    print(f"初始表達式：{to_string(expr)}")
    print(f"自由變數：{sorted(free_vars(expr))}")
    print("-" * 60)

    current = expr

    for step in range(1, max_steps + 1):
        new_expr, changed, description = beta_step(current)

        if not changed:
            print("\n已達到 Normal Form（正規形式）")
            print(f"最終結果：{to_string(current)}")
            print(f"總計算步數：{step - 1}")
            return current

        print(f"\nStep {step}")
        print(f"規則：{description}")
        print(f"原式：{to_string(current)}")
        print(f"結果：{to_string(new_expr)}")

        current = new_expr

    # 檢查是否恰好在最後一步完成
    _, changed, _ = beta_step(current)

    if not changed:
        print("\n已達到 Normal Form（正規形式）")
        print(f"最終結果：{to_string(current)}")
        print(f"總計算步數：{max_steps}")
    else:
        print("\n已達到最大計算步數")
        print("表達式可能無限歸約，或需要更多步數。")
        print(f"目前結果：{to_string(current)}")

    return current


# ==========================================
# 10. 內建測試範例
# ==========================================

EXAMPLES = [
    ("Identity Function", r"(\x.x) y"),
    ("Constant Function", r"(\x.\y.x) a b"),
    ("Function Application", r"(\f.\x.f x) (\y.y) z"),
    ("Nested Reduction", r"(\x.x x) (\y.y)"),
    ("Alpha Conversion", r"(\x.\y.x) y"),
    ("Church Boolean TRUE", r"(\t.\f.t) a b"),
    ("Church Boolean FALSE", r"(\t.\f.f) a b"),
    ("Infinite Reduction", r"(\x.x x) (\x.x x)")
]


# ==========================================
# 11. 主程式與操作選單
# ==========================================

def main():
    print("=" * 60)
    print("Lambda Calculus Interpreter")
    print("有名稱 Lambda 演算解譯器")
    print("=" * 60)

    print("支援語法：")
    print("  變數：x, y, abc")
    print(r"  Lambda：\x.x")
    print("  Lambda：λx.x")
    print("  Lambda：lambda x.x")
    print(r"  函數應用：(\x.x) y")

    while True:
        print("\n" + "=" * 60)
        print("1. 自行輸入 Lambda 表達式")
        print("2. 執行內建範例")
        print("3. 顯示所有內建範例")
        print("0. 離開程式")

        choice = input("\n請選擇功能：").strip()

        if choice == "0":
            print("程式結束！")
            break

        elif choice == "3":
            print("\n內建範例：")

            for i, (name, expression) in enumerate(
                EXAMPLES, 1
            ):
                print(f"{i}. {name}")
                print(f"   {expression}")

        elif choice in ("1", "2"):
            if choice == "1":
                expression = input(
                    "\n請輸入 Lambda 表達式："
                ).strip()

            else:
                print("\n請選擇範例：")

                for i, (name, expression) in enumerate(
                    EXAMPLES, 1
                ):
                    print(f"{i}. {name}: {expression}")

                try:
                    index = int(input("\n範例編號："))

                    if not 1 <= index <= len(EXAMPLES):
                        print("範例編號超出範圍")
                        continue

                    expression = EXAMPLES[index - 1][1]

                except ValueError:
                    print("請輸入正確的數字")
                    continue

            try:
                limit_text = input(
                    "最大計算步數（Enter 預設 100）："
                ).strip()

                max_steps = (
                    int(limit_text) if limit_text else 100
                )

                if max_steps <= 0:
                    print("最大步數必須大於 0")
                    continue

                expr = parse(expression)

                evaluate(expr, max_steps)

            except (SyntaxError, ValueError) as error:
                print(f"\n輸入錯誤：{error}")

            except RecursionError:
                print("\n表達式過於複雜，超過遞迴深度")

        else:
            print("無效選項，請重新輸入")


if __name__ == "__main__":
    main()
