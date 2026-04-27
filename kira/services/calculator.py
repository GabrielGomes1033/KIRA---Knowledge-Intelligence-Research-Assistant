import sympy as sp

SAFE_GLOBALS = {
    "__builtins__": {},
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "sqrt": sp.sqrt,
    "log": sp.log, "exp": sp.exp, "pi": sp.pi, "E": sp.E,
    "diff": sp.diff, "integrate": sp.integrate, "limit": sp.limit,
    "solve": sp.solve, "factor": sp.factor, "expand": sp.expand,
    "Matrix": sp.Matrix, "symbols": sp.symbols,
}

x, y, z, t = sp.symbols("x y z t")
SAFE_GLOBALS.update({"x": x, "y": y, "z": z, "t": t})


def calculate(expression: str) -> str:
    try:
        result = eval(expression, SAFE_GLOBALS, {})
        return str(result)
    except Exception as exc:
        return f"Erro no cálculo: {exc}"
