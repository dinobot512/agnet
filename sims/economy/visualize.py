"""Draw one network graph per turn from a finished run's events.jsonl.

    .venv/bin/python visualize.py                      # most recent run in runs/
    .venv/bin/python visualize.py runs/<timestamp>     # a specific run

Writes runs/<timestamp>/graphs/turn_NN.png plus overview.png (all turns side by side).

Each graph shows the state after that turn's settlement:
- bubble = agent; area scales with balance. Earners are gold, non-earners blue,
  eliminated agents small and grey (marked with the turn they died).
- arrow = a contract payment made at this turn's settlement, payer -> payee; width = credits paid.
- the INCOME node in the middle has an arrow to each earner; width = that turn's income.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

HERE = Path(__file__).parent

EARNER, OTHER, DEAD, INCOME = "#e0a526", "#4a7fc1", "#b8b8b8", "#3a9a5b"
PAY = "#555555"


def load(run_dir: Path) -> dict:
    events = [json.loads(line) for line in (run_dir / "events.jsonl").read_text().splitlines() if line.strip()]
    setup = next(e for e in events if e["event"] == "setup")
    turns = {}
    for e in events:
        t = turns.setdefault(e["turn"], {"payments": [], "income": {}, "balances": None, "eliminated": []})
        if e["event"] == "payment":
            t["payments"].append((e["payer"], e["payee"], e["amount"]))
        elif e["event"] == "income":
            t["income"][e["agent"]] = e["amount"]
        elif e["event"] == "eliminated":
            t["eliminated"].append(e["agent"])
        elif e["event"] == "settled":
            t["balances"] = e["balances"]
    turns = {n: t for n, t in turns.items() if t["balances"] is not None}   # only fully settled turns
    return {"agents": list(setup["balances"]), "earners": set(setup["earners"]),
            "start": setup["balances"], "turns": dict(sorted(turns.items()))}


def bubble_area(balance: int) -> float:
    return 650 + 200 * balance              # points^2


def radius_pts(area: float) -> float:
    return math.sqrt(area) / 2


def draw_turn(ax, data: dict, turn: int, positions: dict, max_balance: int):
    t = data["turns"][turn]
    died_at = {a: n for n, tt in data["turns"].items() if n <= turn for a in tt["eliminated"]}
    balances = t["balances"]

    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect("equal")
    ax.axis("off")
    total_income = sum(t["income"].values())
    alive = len(balances)
    ax.set_title(f"Turn {turn} — after settlement\n{alive} alive · income {total_income} · "
                 f"{sum(p[2] for p in t['payments'])} credits paid in contracts", fontsize=11)

    areas = {}
    for a in data["agents"]:
        areas[a] = bubble_area(balances[a]) if a in balances else 160
    areas["INCOME"] = 1500

    def arrow(src, dst, width, color, rad):
        ax.add_patch(FancyArrowPatch(
            positions[src], positions[dst], arrowstyle="-|>", mutation_scale=10 + 3 * width,
            linewidth=0.8 + 1.6 * width, color=color, alpha=0.75, connectionstyle=f"arc3,rad={rad}",
            shrinkA=radius_pts(areas[src]) + 2, shrinkB=radius_pts(areas[dst]) + 3, zorder=1))

    # income arrows
    for earner, amount in t["income"].items():
        arrow("INCOME", earner, amount, INCOME, 0.0)
        mx, my = [(positions["INCOME"][i] + positions[earner][i]) / 2 for i in (0, 1)]
        ax.text(mx, my, f"+{amount}", color=INCOME, fontsize=9, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8), zorder=4)

    # contract payments (merge duplicates between the same pair; curve so A->B and B->A don't overlap)
    flows: dict[tuple[str, str], int] = {}
    for payer, payee, amount in t["payments"]:
        flows[(payer, payee)] = flows.get((payer, payee), 0) + amount
    for (payer, payee), amount in flows.items():
        (x1, y1), (x2, y2) = positions[payer], positions[payee]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        # Bend away from the centre (where the INCOME node sits): arc3 offsets its control point by
        # rad * (dy, -dx), so pick the sign that points outward, and bend more the closer the straight
        # line passes to the centre. The reverse direction of a pair gets extra bend so they don't overlap.
        outward = 1 if (dy * mx - dx * my) >= 0 else -1
        rad = outward * (0.15 + 0.45 * (1 - min(1.0, math.hypot(mx, my))))
        if (payee, payer) in flows and payer > payee:
            rad += 0.2 * outward
        arrow(payer, payee, amount, PAY, rad)
        # label at the arc's midpoint (half the control-point offset for a quadratic Bezier)
        mx, my = mx + 0.5 * rad * dy, my - 0.5 * rad * dx
        ax.text(mx, my, str(amount), fontsize=8, ha="center", va="center", color=PAY,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8), zorder=4)

    # nodes
    ix, iy = positions["INCOME"]
    ax.scatter([ix], [iy], s=areas["INCOME"], c=INCOME, marker="s", zorder=2, edgecolors="white")
    ax.text(ix, iy, "INCOME", color="white", fontsize=6.5, fontweight="bold", ha="center", va="center", zorder=3)
    for a in data["agents"]:
        x, y = positions[a]
        if a in balances:
            color = EARNER if a in data["earners"] else OTHER
            ax.scatter([x], [y], s=areas[a], c=color, zorder=2, edgecolors="white", linewidths=1.5)
            ax.text(x, y, f"{a}\n{balances[a]}", color="white", fontsize=9, fontweight="bold",
                    ha="center", va="center", zorder=3)
        else:
            ax.scatter([x], [y], s=areas[a], c=DEAD, zorder=2, edgecolors="white")
            ax.text(x, y, a, color="white", fontsize=8, ha="center", va="center", zorder=3)
            ax.text(x, y - 0.13, f"† t{died_at[a]}", color="#888888", fontsize=7, ha="center", va="top", zorder=3)


def legend(fig):
    from matplotlib.lines import Line2D
    handles = [
        Line2D([], [], marker="o", ls="", color=EARNER, markersize=10, label="earner (size = balance)"),
        Line2D([], [], marker="o", ls="", color=OTHER, markersize=10, label="non-earner (size = balance)"),
        Line2D([], [], marker="o", ls="", color=DEAD, markersize=7, label="eliminated († turn)"),
        Line2D([], [], color=INCOME, lw=2.5, label="income (width = credits)"),
        Line2D([], [], color=PAY, lw=2.5, label="contract payment this turn (width = credits)"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=8, frameon=False)


def main():
    if len(sys.argv) > 1:
        run_dir = Path(sys.argv[1])
    else:
        runs = sorted(p for p in (HERE / "runs").iterdir() if (p / "events.jsonl").exists())
        run_dir = runs[-1]
    data = load(run_dir)
    out = run_dir / "graphs"
    out.mkdir(exist_ok=True)

    agents = data["agents"]
    positions = {a: (math.cos(math.pi / 2 - 2 * math.pi * i / len(agents)),
                     math.sin(math.pi / 2 - 2 * math.pi * i / len(agents))) for i, a in enumerate(agents)}
    positions["INCOME"] = (0.0, 0.0)
    max_balance = max(max(t["balances"].values(), default=0) for t in data["turns"].values())

    for turn in data["turns"]:
        fig, ax = plt.subplots(figsize=(7, 7.6))
        draw_turn(ax, data, turn, positions, max_balance)
        legend(fig)
        fig.savefig(out / f"turn_{turn:02d}.png", dpi=130, bbox_inches="tight")
        plt.close(fig)

    n = len(data["turns"])
    cols = min(n, 5)
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5.3 * rows), squeeze=False)
    for ax in axes.flat:
        ax.axis("off")
    for ax, turn in zip(axes.flat, data["turns"]):
        draw_turn(ax, data, turn, positions, max_balance)
    legend(fig)
    fig.savefig(out / "overview.png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {n} turn graphs + overview.png to {out}")


if __name__ == "__main__":
    main()
