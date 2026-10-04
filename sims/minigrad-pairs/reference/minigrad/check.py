from minigrad.engine import Value


def grad_check(f, inputs, eps=1e-6, tol=1e-4):
    vals = [Value(x) for x in inputs]
    f(*vals).backward()
    for i, v in enumerate(vals):
        hi = [x + (eps if j == i else 0.0) for j, x in enumerate(inputs)]
        lo = [x - (eps if j == i else 0.0) for j, x in enumerate(inputs)]
        num = (f(*[Value(x) for x in hi]).data - f(*[Value(x) for x in lo]).data) / (2 * eps)
        if abs(num - v.grad) > tol:
            return False
    return True
