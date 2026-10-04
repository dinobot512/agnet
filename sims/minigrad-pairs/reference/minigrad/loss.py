from minigrad.engine import Value


def mse_loss(preds, targets):
    total = Value(0.0)
    for p, t in zip(preds, targets):
        total = total + (p - t) ** 2
    return total * (1.0 / len(targets))
