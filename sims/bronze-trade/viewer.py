"""Build a self-contained playback page for a run: runs/<timestamp>/viewer.html

    .venv/bin/python viewer.py                      # most recent run
    .venv/bin/python viewer.py runs/<timestamp>     # a specific run

Replays events.jsonl into per-captain state snapshots (where, status, silver, cargo, destination), plus
tavern statements and the market prices captains saw, and embeds them in viewer_template.html.
The page loads d3 from a CDN. The coastline (world-atlas, Natural Earth 1:50m) is downloaded once into
assets/ and embedded in each page, so playback works offline once d3 is cached.
"""

from __future__ import annotations

import heapq
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_URL = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json"
ATLAS_FILE = HERE / "assets" / "countries-50m.json"

# Home port -> colour group. Rhodes shares the Achaean (Mycenae) colour: the validated palette has 8 hues.
GROUPS = ["Avaris", "Byblos", "Ugarit", "Enkomi", "Mycenae", "Knossos", "Miletus", "Sardinia"]
GROUP_OF = {**{g: g for g in GROUPS}, "Rhodes": "Mycenae"}
GROUP_LABEL = {"Mycenae": "Mycenae & Rhodes (Achaeans)"}

# Drawing-only waypoints (lon, lat) so lanes go around land instead of straight through it.
# Sailing times in the game are unaffected.
WAYPOINTS = {
    ("Mycenae", "Sardinia"): [[23.05, 37.25], [23.3, 36.3], [21.5, 36.1], [15.2, 36.3], [12.2, 37.2]],
    ("Knossos", "Sardinia"): [[23.6, 35.75], [15.2, 36.3], [12.2, 37.2]],
    ("Enkomi", "Rhodes"): [[34.15, 34.95], [32.9, 34.45], [32.1, 34.75]],
    ("Enkomi", "Avaris"): [[34.15, 34.95]],
}


def lane_path(a: str, b: str, ports: dict) -> list:
    if (a, b) in WAYPOINTS:
        mid = WAYPOINTS[(a, b)]
    elif (b, a) in WAYPOINTS:
        mid = WAYPOINTS[(b, a)][::-1]
    else:
        mid = []
    return [ports[a]["lonlat"], *mid, ports[b]["lonlat"]]


def latest_run() -> Path:
    runs = sorted(p for p in (HERE / "runs").iterdir() if (p / "events.jsonl").exists())
    if not runs:
        sys.exit("no runs found in runs/")
    return runs[-1]


def routes(ports: list[str], lanes: list) -> dict[str, list[str]]:
    """Shortest sea route (by nautical miles) between every pair of ports, as a list of port names."""
    adj = {p: [] for p in ports}
    for a, b, nm in lanes:
        adj[a].append((b, nm))
        adj[b].append((a, nm))
    out = {}
    for src in ports:
        dist, prev, heap = {src: 0}, {}, [(0, src)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                if d + w < dist.get(v, float("inf")):
                    dist[v], prev[v] = d + w, u
                    heapq.heappush(heap, (d + w, v))
        for dst in ports:
            if dst == src or dst not in dist:
                continue
            path = [dst]
            while path[-1] != src:
                path.append(prev[path[-1]])
            out[f"{src}|{dst}"] = path[::-1]
    return out


def replay_markets(cfg: dict, seed: int, days: int, events: list[dict]) -> tuple[dict, int]:
    """Rebuild every port's true market for every day by replaying the logged trades against the run's
    config and seed (markets are deterministic). Returns ({port: [[day, {good: [buy, sell, stock, demand]}]]},
    number of logged session stocks that didn't match the replay)."""
    sys.path.insert(0, str(HERE))
    from world import build_markets
    markets = build_markets(cfg, seed or 0)
    trades: dict[int, list[dict]] = {}
    sessions: dict[int, list[dict]] = {}
    for e in events:
        if e["event"] == "trade":
            trades.setdefault(e["day"], []).append(e)
        elif e["event"] == "session":
            sessions.setdefault(e["day"], []).append(e)
    out = {p: [] for p in markets}
    mismatches = 0
    for day in range(days + 1):
        for mk in markets.values():
            mk.advance(day)
        for e in sessions.get(day, []):                      # check: stock at session start matches the log
            stock = {g: round(v, 1) for g, v in markets[e["port"]].stock.items()}
            if any(abs(stock[g] - v) > 0.2 for g, v in e["stock"].items()):
                mismatches += 1
        for e in trades.get(day, []):
            mk = markets[e["port"]]
            (mk.buy if e["side"] == "buy" else mk.sell)(e["good"], e["qty"])
        for port, mk in markets.items():
            out[port].append([day, {g: [round(mk.buy_price(g), 2), round(mk.sell_price(g), 2), int(mk.stock[g]),
                                        round(mk.demand.get(g, 1.0), 2)] for g in mk.goods}])
    return out, mismatches


def build(run_dir: Path) -> dict:
    cfg = json.loads((run_dir / "config.json").read_text())
    current = json.loads((HERE / "config.json").read_text())
    events = [json.loads(line) for line in (run_dir / "events.jsonl").read_text().splitlines() if line.strip()]
    results = json.loads((run_dir / "results.json").read_text()) if (run_dir / "results.json").exists() else {}

    ports = {}
    for name, p in cfg["ports"].items():
        lonlat = p.get("lonlat") or current["ports"].get(name, {}).get("lonlat")
        ports[name] = {"lonlat": lonlat, "region": p.get("region", ""), "produce": p.get("produce", {}),
                       "consume": p.get("consume", {}), "bronze": p.get("bronze_batches", 0)}

    setup = next(e for e in events if e["event"] == "setup")
    captains = []
    for i, (cid, info) in enumerate(setup["captains"].items(), 1):
        group = GROUP_OF.get(info["home"], info["home"])
        captains.append({"id": cid, "name": info["name"], "home": info["home"],
                         "label": f"{info['name'][0]}{i}", "group": GROUPS.index(group) if group in GROUPS else 0})

    start = cfg["ship"]["start_silver"]
    state = {c["id"]: {"status": "sea", "port": None, "from": None, "dest": c["home"], "depart": 0, "arrive": 0,
                       "until": None, "silver": start, "cargo": {}} for c in captains}
    snaps = {c["id"]: [] for c in captains}
    statements, quotes = [], {p: [] for p in ports}

    for e in events:
        kind, day = e["event"], e["day"]
        if kind == "statement":
            statements.append([day, e["port"], e["speaker"], e["name"], e["round"], e["text"], len(e["listeners"])])
            continue
        if kind == "observe":
            q = quotes[e["port"]]
            if q and q[-1][0] == day:
                q[-1] = [day, e["quote"]]
            else:
                q.append([day, e["quote"]])
            continue
        cid = e.get("captain")
        if cid not in state:
            continue
        s = state[cid]
        if kind == "arrive":
            s.update(status="port", port=e["port"], dest=None, silver=e["silver"], cargo=e["cargo"])
        elif kind == "wake":
            s.update(status="port", silver=e.get("silver", s["silver"]), cargo=e.get("cargo", s["cargo"]))
        elif kind == "trade":
            if "silver" in e:
                s.update(silver=e["silver"], cargo=e["cargo"])
            else:                                                  # older runs: apply the trade ourselves
                cargo = dict(s["cargo"])
                sign = 1 if e["side"] == "buy" else -1
                cargo[e["good"]] = cargo.get(e["good"], 0) + sign * e["qty"]
                cargo = {g: q for g, q in cargo.items() if q}
                s.update(silver=round(s["silver"] - sign * e["total"], 2), cargo=cargo)
        elif kind == "sail":
            s.update(status="sea", port=None, **{"from": e["origin"]}, dest=e["dest"], depart=day,
                     arrive=e["arrive_day"], silver=e["silver"], cargo=e["cargo"])
        elif kind == "wait":
            s.update(status="waiting", until=e["until"], silver=e.get("silver", s["silver"]),
                     cargo=e.get("cargo", s["cargo"]))
        elif kind == "stranded":
            s.update(status="stranded")
        else:
            continue
        snaps[cid].append([day, s["status"], s["port"], s["from"], s["dest"], s["depart"], s["arrive"],
                           s["until"], round(s["silver"], 2), dict(s["cargo"])])

    days = cfg.get("days") or max(e["day"] for e in events)
    market, mismatches = replay_markets(cfg, cfg.get("seed"), days, events)
    if mismatches:
        print(f"(warning: replayed markets differ from the log at {mismatches} sessions)")
    return {
        "meta": {"run": run_dir.name, "seed": cfg.get("seed"), "days": cfg.get("days"),
                 "aborted": results.get("aborted"), "market_mismatches": mismatches},
        "market": market,
        "ports": ports,
        "lanes": {f"{a}|{b}": lane_path(a, b, ports) for a, b, _ in cfg["lanes"]}
                 | {f"{b}|{a}": lane_path(b, a, ports) for a, b, _ in cfg["lanes"]},
        "routes": routes(list(ports), cfg["lanes"]),
        "groups": [GROUP_LABEL.get(g, g) for g in GROUPS],
        "captains": captains,
        "snaps": snaps,
        "statements": statements,
        "quotes": quotes,
        "scores": results.get("scores", {}),
    }


def coastline() -> str:
    """The world-atlas TopoJSON, cached in assets/. Returns 'null' if it can't be had (page then tries the CDN)."""
    if not ATLAS_FILE.exists():
        try:
            ATLAS_FILE.parent.mkdir(exist_ok=True)
            with urllib.request.urlopen(ATLAS_URL, timeout=30) as r:
                ATLAS_FILE.write_bytes(r.read())
        except OSError as e:
            print(f"(couldn't download the coastline, the page will try the CDN: {e})")
            return "null"
    return ATLAS_FILE.read_text()


def write_viewer(run_dir: Path) -> Path:
    data = build(run_dir)
    html = (HERE / "viewer_template.html").read_text()
    payload = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    out = run_dir / "viewer.html"
    out.write_text(html.replace("/*__RUN_DATA__*/null", payload).replace("/*__ATLAS__*/null", coastline()))
    return out


def main():
    out = write_viewer(Path(sys.argv[1]) if len(sys.argv) > 1 else latest_run())
    print(f"Wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
