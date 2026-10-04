import math

_GRAD = [True]


class no_grad:
    def __enter__(self):
        self.prev = _GRAD[0]
        _GRAD[0] = False

    def __exit__(self, *a):
        _GRAD[0] = self.prev


class Value:
    def __init__(self, data, _children=(), _op=""):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children) if _GRAD[0] else set()
        self._op = _op

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"

    def __add__(self, o):
        o = o if isinstance(o, Value) else Value(o)
        out = Value(self.data + o.data, (self, o), "+")
        def _b():
            self.grad += out.grad
            o.grad += out.grad
        out._backward = _b
        return out

    def __mul__(self, o):
        o = o if isinstance(o, Value) else Value(o)
        out = Value(self.data * o.data, (self, o), "*")
        def _b():
            self.grad += o.data * out.grad
            o.grad += self.data * out.grad
        out._backward = _b
        return out

    def __pow__(self, k):
        out = Value(self.data ** k, (self,), f"**{k}")
        def _b():
            self.grad += k * self.data ** (k - 1) * out.grad
        out._backward = _b
        return out

    def __neg__(self): return self * -1
    def __sub__(self, o): return self + (-o if isinstance(o, Value) else -o)
    def __rsub__(self, o): return (-self) + o
    def __radd__(self, o): return self + o
    def __rmul__(self, o): return self * o
    def __truediv__(self, o): return self * (o if isinstance(o, Value) else Value(o)) ** -1
    def __rtruediv__(self, o): return Value(o) * self ** -1

    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,), "tanh")
        def _b(): self.grad += (1 - t * t) * out.grad
        out._backward = _b
        return out

    def relu(self):
        out = Value(max(0.0, self.data), (self,), "relu")
        def _b(): self.grad += (out.data > 0) * out.grad
        out._backward = _b
        return out

    def exp(self):
        e = math.exp(self.data)
        out = Value(e, (self,), "exp")
        def _b(): self.grad += e * out.grad
        out._backward = _b
        return out

    def log(self):
        out = Value(math.log(self.data), (self,), "log")
        def _b(): self.grad += (1.0 / self.data) * out.grad
        out._backward = _b
        return out

    def backward(self):
        topo, seen = [], set()
        def build(v):
            if v not in seen:
                seen.add(v)
                for c in v._prev:
                    build(c)
                topo.append(v)
        build(self)
        self.grad = 1.0
        for v in reversed(topo):
            v._backward()
