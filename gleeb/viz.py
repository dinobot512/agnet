"""Summary image: each agent's goal partitions (expressed and behavioral lanes) on the shared event axis,
with flow edges drawn between agents. Requires matplotlib (pip install "gleeb[viz]")."""

from __future__ import annotations

import textwrap

from gleeb.schema import FlowEdge, GoalStream, Trace

LANES = ("expressed", "behavioral")
EDGE_STYLE = {"transfer": dict(color="#1f4e9c", lw=1.6, ls="-"),
              "carry": dict(color="#7a7a7a", lw=0.9, ls=":"),
              "unexplained": dict(color="#c0392b", lw=1.6, ls="--"),
              "unknown": dict(color="#b0b0b0", lw=0.8, ls="-")}


def summary_image(trace: Trace, streams: list[GoalStream], edges: list[FlowEdge], path: str,
                  title: str = "", show_carry: bool = True, show_unknown: bool = True) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, Rectangle

    agents = list(trace.agents)
    n = len(trace.events)
    band = {a: (len(agents) - 1 - i) * 3.0 for i, a in enumerate(agents)}      # bottom y of each agent
    lane_y = {(a, l): band[a] + (1.1 if l == "expressed" else 0.0) for a in agents for l in LANES}
    palette = plt.get_cmap("Set3").colors + plt.get_cmap("Pastel1").colors

    legend_lines: list[str] = []
    fig_h = 1.6 + 1.9 * len(agents)
    n_lines = sum(len(s.spans) for s in streams if s.stream in LANES)
    fig = plt.figure(figsize=(16, fig_h + 0.16 * n_lines + 0.5))
    ax = fig.add_axes([0.11, 1 - (fig_h - 0.4) / fig.get_figheight(), 0.87, (fig_h - 1.2) / fig.get_figheight()])

    # activity ticks: where each agent acted
    for e in trace.events:
        ax.plot([e.seq, e.seq], [band[e.agent] - 0.15, band[e.agent] - 0.05], color="#999", lw=0.5)

    for s in streams:
        if s.stream not in LANES or s.agent not in band:
            continue
        y = lane_y[s.agent, s.stream]
        for k, sp in enumerate(s.spans):
            tag = f"{s.agent.upper()}-{'E' if s.stream == 'expressed' else 'B'}{k + 1}"
            x0, x1 = sp.start[0] - 0.5, sp.end[1] + 0.5
            c = palette[(k + (0 if s.stream == "expressed" else 4)) % len(palette)]
            ax.add_patch(Rectangle((x0, y), x1 - x0, 0.9, fc=c, ec="#333", lw=0.6))
            if sp.start[1] > sp.start[0]:                                       # uncertain boundary
                ax.add_patch(Rectangle((sp.start[0] - 0.5, y), sp.start[1] - sp.start[0], 0.9,
                                       fc="none", ec="#333", hatch="///", lw=0))
            width = x1 - x0
            label = tag if width < n * 0.08 else f"{tag}: {sp.goal}"
            label = textwrap.shorten(label, width=max(len(tag), int(width / max(n, 1) * 190)), placeholder="…")
            ax.text(x0 + 0.4, y + 0.45, label, va="center", fontsize=7, clip_on=True)
            legend_lines.append(f"{tag}  [{sp.start[0]}–{sp.end[1]}]  {sp.goal}")

    def arrow(x0, y0, x1, y1, style, rad=0.0):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=9,
                                     connectionstyle=f"arc3,rad={rad}", **style))

    for e in edges:
        if e.kind == "carry":
            if show_carry and e.dst_seq > e.src_seq:
                y = band[e.from_agent] - 0.1
                arrow(e.src_seq, y, e.dst_seq, y, EDGE_STYLE["carry"], rad=0.35)
        elif e.from_agent == "?":
            if show_unknown:
                y = band[e.to_agent] + 2.15
                arrow(e.dst_seq, y + 0.5, e.dst_seq, y, EDGE_STYLE["unknown"])
        elif e.from_agent in band and e.to_agent in band:
            style = EDGE_STYLE["unexplained" if e.kind == "unexplained" else "transfer"]
            y0, y1 = band[e.from_agent] + 1.0, band[e.to_agent] + 1.0
            arrow(e.src_seq, y0, e.dst_seq, y1, style, rad=0.15)
            ax.text((e.src_seq + e.dst_seq) / 2, (y0 + y1) / 2 + 0.25,
                    e.blackboard_id.removeprefix("file:"), fontsize=7, color=style["color"], ha="center")

    ax.set_xlim(-1, n)
    ax.set_ylim(-0.8, band[agents[0]] + 3.0)
    ax.set_yticks([lane_y[a, l] + 0.45 for a in agents for l in LANES])
    ax.set_yticklabels([f"{trace.agents[a].name or a}  {l}" for a in agents for l in LANES], fontsize=8)
    ax.set_xlabel("event seq (shared axis)")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_title(title or f"gleeb summary: {trace.id}", fontsize=11, loc="left")
    handles = [plt.Line2D([], [], **{k: v for k, v in st.items()}, label=name)
               for name, st in (("transfer", EDGE_STYLE["transfer"]), ("carry (within agent)", EDGE_STYLE["carry"]),
                                ("unexplained", EDGE_STYLE["unexplained"]), ("unknown source", EDGE_STYLE["unknown"]))]
    ax.legend(handles=handles, loc="upper right", fontsize=7, frameon=False, ncol=4, bbox_to_anchor=(1, 1.08))

    fig.text(0.11, (0.16 * len(legend_lines) + 0.3) / fig.get_figheight(),
             "\n".join(textwrap.shorten(l, 200, placeholder="…") for l in legend_lines),
             fontsize=7, va="top", family="monospace")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
