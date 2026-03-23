import tkinter as tk
from tkinter import messagebox
import math

# ── Colour palette ──────────────────────────────────────────────────────────
BG          = "#1a1a2e"   # deep navy background
PANEL       = "#16213e"   # slightly lighter panel
BTN_NUM     = "#0f3460"   # number buttons
BTN_OP      = "#e94560"   # operator buttons (red-pink)
BTN_MATH    = "#533483"   # math-module buttons (purple)
BTN_EQ      = "#e94560"   # equals
BTN_CLR     = "#22304a"   # clear / util buttons
FG          = "#eaeaea"   # primary text
FG_DIM      = "#8892a4"   # secondary / smaller text
ACCENT      = "#e94560"   # accent highlight
FONT_DISP   = ("Courier New", 28, "bold")
FONT_SMALL  = ("Courier New", 12)
FONT_BTN    = ("Courier New", 14, "bold")
FONT_BTN_SM = ("Courier New", 11, "bold")


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CALC //")
        self.resizable(False, False)
        self.configure(bg=BG)

        # ── state ──
        self.expression   = ""   # full expression string
        self.result_shown = False

        self._build_display()
        self._build_buttons()

    # ── Display ─────────────────────────────────────────────────────────────
    def _build_display(self):
        frame = tk.Frame(self, bg=PANEL, padx=16, pady=12)
        frame.grid(row=0, column=0, columnspan=5, sticky="ew", padx=12, pady=(12, 0))

        # history label (small, dim)
        self.lbl_history = tk.Label(frame, text="", font=FONT_SMALL,
                                    bg=PANEL, fg=FG_DIM, anchor="e")
        self.lbl_history.pack(fill="x")

        # main display
        self.lbl_display = tk.Label(frame, text="0", font=FONT_DISP,
                                    bg=PANEL, fg=FG, anchor="e")
        self.lbl_display.pack(fill="x")

    # ── Buttons ──────────────────────────────────────────────────────────────
    def _build_buttons(self):
        pad = dict(padx=5, pady=5, ipadx=6, ipady=10, sticky="nsew")

        def btn(parent, text, color, cmd, row, col, colspan=1, font=FONT_BTN):
            b = tk.Button(parent, text=text, font=font,
                          bg=color, fg=FG, activebackground=ACCENT,
                          activeforeground=FG, bd=0, relief="flat",
                          cursor="hand2", command=cmd)
            b.grid(row=row, column=col, columnspan=colspan, **pad)
            # hover effect
            b.bind("<Enter>", lambda e, w=b, c=color: w.config(bg=_lighten(c)))
            b.bind("<Leave>", lambda e, w=b, c=color: w.config(bg=c))
            return b

        outer = tk.Frame(self, bg=BG)
        outer.grid(row=1, column=0, padx=12, pady=12)

        # configure columns to be equal width
        for c in range(5):
            outer.columnconfigure(c, weight=1, minsize=68)

        # ── Row 0: utility ──
        btn(outer, "AC",    BTN_CLR, self.clear_all,    0, 0)
        btn(outer, "⌫",    BTN_CLR, self.backspace,     0, 1)
        btn(outer, "%",     BTN_OP,  lambda: self._append("%"),  0, 2)
        btn(outer, "(",     BTN_CLR, lambda: self._append("("), 0, 3)
        btn(outer, ")",     BTN_CLR, lambda: self._append(")"), 0, 4)

        # ── Row 1: math module ──
        btn(outer, "√",     BTN_MATH, lambda: self._math_fn("sqrt"),     1, 0, font=FONT_BTN_SM)
        btn(outer, "x²",    BTN_MATH, lambda: self._math_fn("sq"),       1, 1, font=FONT_BTN_SM)
        btn(outer, "xʸ",    BTN_MATH, lambda: self._append("**"),        1, 2, font=FONT_BTN_SM)
        btn(outer, "log",   BTN_MATH, lambda: self._math_fn("log10"),    1, 3, font=FONT_BTN_SM)
        btn(outer, "ln",    BTN_MATH, lambda: self._math_fn("ln"),       1, 4, font=FONT_BTN_SM)

        # ── Row 2: math module cont. ──
        btn(outer, "sin",   BTN_MATH, lambda: self._math_fn("sin"),      2, 0, font=FONT_BTN_SM)
        btn(outer, "cos",   BTN_MATH, lambda: self._math_fn("cos"),      2, 1, font=FONT_BTN_SM)
        btn(outer, "tan",   BTN_MATH, lambda: self._math_fn("tan"),      2, 2, font=FONT_BTN_SM)
        btn(outer, "n!",    BTN_MATH, lambda: self._math_fn("fact"),     2, 3, font=FONT_BTN_SM)
        btn(outer, "π",     BTN_MATH, lambda: self._append(str(math.pi)[:10]), 2, 4, font=FONT_BTN_SM)

        # ── Rows 3-6: digits + operators ──
        layout = [
            ("7", "8", "9", "÷"),
            ("4", "5", "6", "×"),
            ("1", "2", "3", "−"),
            ("0", ".", "  ", "+"),
        ]
        op_map = {"÷": "/", "×": "*", "−": "-", "+": "+"}

        for r, row_items in enumerate(layout, start=3):
            for c, label in enumerate(row_items):
                if label.strip() == "":
                    continue
                color = BTN_OP if label in op_map else BTN_NUM
                val   = op_map.get(label, label)
                btn(outer, label, color, lambda v=val: self._append(v), r, c)

        # ── Equals spans two rows on the right ──
        eq = tk.Button(outer, text="=", font=FONT_BTN,
                       bg=BTN_EQ, fg=FG, activebackground="#c73652",
                       activeforeground=FG, bd=0, relief="flat",
                       cursor="hand2", command=self.calculate)
        eq.grid(row=5, column=4, rowspan=2, padx=5, pady=5,
                ipadx=6, ipady=10, sticky="nsew")
        eq.bind("<Enter>", lambda e: eq.config(bg="#c73652"))
        eq.bind("<Leave>", lambda e: eq.config(bg=BTN_EQ))

        # 0 spans two columns
        btn(outer, "0", BTN_NUM, lambda: self._append("0"), 6, 0, colspan=2)
        btn(outer, ".", BTN_NUM, lambda: self._append("."), 6, 2)
        btn(outer, "+/−", BTN_CLR, self.negate,              6, 3, font=FONT_BTN_SM)

        # bind keyboard
        self.bind("<Key>", self._keypress)
        self.bind("<Return>",    lambda e: self.calculate())
        self.bind("<BackSpace>", lambda e: self.backspace())
        self.bind("<Escape>",    lambda e: self.clear_all())

    # ── Core logic ───────────────────────────────────────────────────────────
    def _append(self, char):
        if self.result_shown and char not in "+-*/.**%()":
            self.expression = ""
        self.result_shown = False
        self.expression += char
        self._refresh()

    def _refresh(self):
        disp = self.expression if self.expression else "0"
        # keep display readable
        disp = disp.replace("*", "×").replace("/", "÷").replace("-", "−")
        self.lbl_display.config(text=disp[-22:])  # truncate if very long

    def _math_fn(self, fn):
        """Apply a math function to the current expression."""
        expr = self.expression.strip()
        if not expr:
            return
        try:
            val = float(eval(expr))  # evaluate what's currently typed
        except Exception:
            self.lbl_display.config(text="Error")
            return

        try:
            if fn == "sqrt":
                result = math.sqrt(val)
            elif fn == "sq":
                result = math.pow(val, 2)
            elif fn == "log10":
                result = math.log10(val)
            elif fn == "ln":
                result = math.log(val)
            elif fn == "sin":
                result = math.sin(math.radians(val))
            elif fn == "cos":
                result = math.cos(math.radians(val))
            elif fn == "tan":
                result = math.tan(math.radians(val))
            elif fn == "fact":
                result = math.factorial(int(val))
            else:
                return
        except Exception as err:
            self.lbl_display.config(text="Error")
            self.lbl_history.config(text=str(err))
            self.expression = ""
            return

        self.lbl_history.config(text=f"{fn}({_fmt(val)})")
        self.expression   = str(result)
        self.result_shown = True
        self.lbl_display.config(text=_fmt(result))

    def calculate(self):
        if not self.expression:
            return
        try:
            raw    = self.expression.replace("%", "/100")
            result = eval(raw)
            self.lbl_history.config(text=self.expression.replace("*","×").replace("/","÷").replace("-","−"))
            self.expression   = str(result)
            self.result_shown = True
            self.lbl_display.config(text=_fmt(result))
        except ZeroDivisionError:
            self.lbl_display.config(text="÷ 0  Error")
            self.expression = ""
        except Exception:
            self.lbl_display.config(text="Syntax Error")
            self.expression = ""

    def clear_all(self):
        self.expression   = ""
        self.result_shown = False
        self.lbl_history.config(text="")
        self.lbl_display.config(text="0")

    def backspace(self):
        if self.result_shown:
            self.clear_all()
            return
        self.expression = self.expression[:-1]
        self._refresh()

    def negate(self):
        if self.expression:
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self._refresh()

    def _keypress(self, event):
        char = event.char
        allowed = "0123456789.+-*/()"
        if char in allowed:
            self._append(char)


# ── Helpers ──────────────────────────────────────────────────────────────────
def _fmt(val):
    """Format number: remove .0 from integers, limit decimals."""
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return f"{val:.10g}"

def _lighten(hex_color):
    """Return a slightly lighter shade for hover effects."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = min(r+30, 255), min(g+30, 255), min(b+30, 255)
    return f"#{r:02x}{g:02x}{b:02x}"


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
