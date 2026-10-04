"""Hidden test suite for the minigrad game. Run: python hidden_tests.py REPO_DIR [N_TASKS]. Prints JSON. Never mounted into agent containers."""
import importlib, json, math, random, signal, sys

repo, ntasks = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8
sys.path.insert(0, repo)
TESTS = []


def test(task):
    def deco(fn):
        TESTS.append((task, fn.__name__, fn))
        return fn
    return deco


def V(x):
    return importlib.import_module("minigrad.engine").Value(x)


@test(1)
def value_basic():
    a, b = V(2), V(3)
    assert (a + b).data == 5 and (a * b).data == 6 and (b - a).data == 1 and a.grad == 0.0 and (a + 1.5).data == 3.5

@test(1)
def value_repr_format():
    assert repr(V(1.5)) == "Value(data=1.5, grad=0.0)"

@test(2)
def div_pow_neg():
    assert (V(6) / V(3)).data == 2 and (V(2) ** 3).data == 8 and (-V(4)).data == -4 and (V(6) / 3).data == 2

@test(2)
def reflected_ops():
    assert (2 * V(3)).data == 6 and (1 + V(1)).data == 2 and (10 - V(4)).data == 6 and (8 / V(2)).data == 4

@test(3)
def backward_chain():
    a, b = V(2), V(3)
    c = a * b + a
    c.backward()
    assert a.grad == 4 and b.grad == 2

@test(3)
def grad_accumulates_for_reused_nodes():
    a = V(3)
    b = a * a + a
    b.backward()
    assert a.grad == 7
    x = V(2); y = x * 3; z = y + y * x; z.backward()
    assert x.grad == 3 + 3 * 2 + 3 * 2 or x.grad == 15 or abs(x.grad - 15) < 1e-9, x.grad

@test(4)
def activations_forward_and_grad():
    for name, x, d in [("tanh", 0.3, 1 - math.tanh(0.3) ** 2), ("relu", 0.7, 1.0), ("relu", -0.7, 0.0), ("exp", 0.4, math.exp(0.4)), ("log", 1.7, 1 / 1.7)]:
        v = V(x)
        out = getattr(v, name)()
        out.backward()
        assert abs(v.grad - d) < 1e-9, (name, v.grad, d)
    assert abs(V(0.3).tanh().data - math.tanh(0.3)) < 1e-12 and V(-2).relu().data == 0

@test(5)
def mlp_parameters_and_zero_grad():
    nn = importlib.import_module("minigrad.nn")
    m = nn.MLP(2, [4, 4, 1])
    assert len(m.parameters()) == 37
    out = m([1.0, -2.0])
    out.backward()
    assert any(p.grad != 0 for p in m.parameters())
    m.zero_grad()
    assert all(p.grad == 0 for p in m.parameters())

@test(5)
def layer_shapes():
    nn = importlib.import_module("minigrad.nn")
    assert len(nn.Layer(3, 5)([1.0, 2.0, 3.0])) == 5 and len(nn.Neuron(3).parameters()) == 4

@test(6)
def training_reduces_loss():
    nn, loss, optim = (importlib.import_module("minigrad." + m) for m in ("nn", "loss", "optim"))
    random.seed(0)
    xs, ys = [[0.0, 1.0], [1.0, 0.0], [1.0, 1.0], [0.0, 0.0]], [1.0, 1.0, 1.0, -1.0]      # OR: linearly separable
    m = nn.MLP(2, [4, 1])
    opt = optim.SGD(m.parameters(), lr=0.05)
    first = last = None
    for _ in range(80):
        l = loss.mse_loss([m(x) for x in xs], ys)
        opt.zero_grad(); l.backward(); opt.step()
        first = l.data if first is None else first
        last = l.data
    assert last < first * 0.8, (first, last)

@test(7)
def grad_check_uses_documented_defaults():
    check = importlib.import_module("minigrad.check")
    assert check.grad_check(lambda a, b: (a * b + a).tanh(), [0.5, -1.2]) is True

@test(7)
def grad_check_accepts_explicit_eps_tol():
    check = importlib.import_module("minigrad.check")
    assert check.grad_check(lambda a: a ** 2 + a.exp(), [0.3], eps=1e-5, tol=1e-3) is True

@test(8)
def no_grad_context():
    eng = importlib.import_module("minigrad.engine")
    with eng.no_grad():
        v = eng.Value(2) * eng.Value(3)
        assert v._prev == set() and v.data == 6
    w = eng.Value(2) * eng.Value(3)
    assert len(w._prev) == 2

@test(8)
def values_are_floats():
    assert type(V(3).data) is float and V(1 / 3).data == 1 / 3 and type((V(2) * V(3)).data) is float


class Timeout(Exception):
    pass


def _alarm(*a):
    raise Timeout()


signal.signal(signal.SIGALRM, _alarm)
results = []
for task, name, fn in TESTS:
    if task > ntasks:
        continue
    signal.alarm(5)
    try:
        fn()
        ok, err = True, ""
    except BaseException as e:
        ok, err = False, f"{type(e).__name__}: {str(e)[:120]}"
    signal.alarm(0)
    results.append({"task": task, "test": name, "passed": ok, "error": err})
passed = sum(r["passed"] for r in results)
print(json.dumps({"passed": passed, "total": len(results), "pass_rate": passed / max(1, len(results)), "results": results}))
