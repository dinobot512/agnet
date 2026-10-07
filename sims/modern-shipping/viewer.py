"""Build a self-contained playback page for a run: runs/<timestamp>/viewer.html

    python viewer.py                      # most recent run
    python viewer.py runs/<timestamp>     # a specific run

Packs the world (ports, waypoints, lanes, canals, recipes), every captain's state changes (from events.jsonl)
and the daily true market history (markets.json) into viewer_template.html. The coastline is cached in
assets/ and embedded, so the page only needs a network connection for d3 itself.
"""

from __future__ import annotations

import json
import shutil
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_URL = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json"
ATLAS_FILE = HERE / "assets" / "countries-50m.json"
SIBLING_ATLAS = HERE.parent / "bronze-trade" / "assets" / "countries-50m.json"


def coastline() -> str:
    if not ATLAS_FILE.exists():
        ATLAS_FILE.parent.mkdir(exist_ok=True)
        if SIBLING_ATLAS.exists():
            shutil.copy(SIBLING_ATLAS, ATLAS_FILE)
        else:
            try:
                with urllib.request.urlopen(ATLAS_URL, timeout=30) as r:
                    ATLAS_FILE.write_bytes(r.read())
            except OSError as e:
                print(f"(couldn't get the coastline; the page will try the CDN: {e})")
                return "null"
    return ATLAS_FILE.read_text()


def latest_run() -> Path:
    runs = sorted(p for p in (HERE / "runs").iterdir() if (p / "events.jsonl").exists())
    if not runs:
        sys.exit("no runs found")
    return runs[-1]


def build(run_dir: Path) -> dict:
    cfg = json.loads((run_dir / "config.json").read_text())
    events = [json.loads(l) for l in (run_dir / "events.jsonl").read_text().splitlines() if l.strip()]
    markets = json.loads((run_dir / "markets.json").read_text()) if (run_dir / "markets.json").exists() else {}
    results = json.loads((run_dir / "results.json").read_text()) if (run_dir / "results.json").exists() else {}

    setup = next(e for e in events if e["event"] == "setup")
    captains = [{"id": cid, **info} for cid, info in setup["captains"].items()]
    snaps = {c["id"]: [] for c in captains}
    routes: dict[str, list[str]] = {}
    spec = cfg["ship_types"]
    for e in events:
        cid, kind, day = e.get("captain"), e["event"], e["day"]
        if cid not in snaps:
            continue
        if kind in ("arrive", "wake"):
            snaps[cid].append([day, "port", e["port"], None, None, 0, 0, 0, e["cash"], e["fuel"], e["cargo"], None])
        elif kind == "trade":
            last = snaps[cid][-1]
            snaps[cid].append([day, "port", last[2], None, None, 0, 0, 0, e["cash"], last[9], e["cargo"], None])
        elif kind == "refuel":
            last = snaps[cid][-1]
            snaps[cid].append([day, "port", last[2], None, None, 0, 0, 0, e["cash"], e["fuel"], last[10], None])
        elif kind == "wait":
            snaps[cid].append([day, "waiting", e["port"], None, None, 0, 0, e["until"], e["cash"], e["fuel"],
                               e["cargo"], None])
        elif kind == "sail":
            key = f"{e['origin']}|{e['dest']}|{e['policy']}"
            routes[key] = e["path"]
            snaps[cid].append([day, "sea", None, e["origin"], e["dest"], day, e["arrive_day"], 0, e["cash"],
                               e["fuel"], e["cargo"], key])
        elif kind == "bankrupt":
            last = snaps[cid][-1]
            snaps[cid].append([day, "bankrupt", e["port"], None, None, 0, 0, 0, e["cash"], last[9], {}, None])

    voyages = [[e["day"], e["captain"], e["origin"], e["dest"], e["arrive_day"], e["cargo"], e["canals"]]
               for e in events if e["event"] == "sail"]
    coords = {p: v["lonlat"] for p, v in cfg["ports"].items()}
    coords.update(cfg["waypoints"])
    return {
        "meta": {"run": run_dir.name, "seed": cfg.get("seed"), "days": cfg.get("days"), "captains": len(captains)},
        "ships": {k: {"name": v["name"], "capacity": v["capacity"], "tank": v["tank"] * v["burn"]} for k, v in spec.items()},
        "ports": {p: {"lonlat": v["lonlat"], "region": v["region"], "produce": v["produce"], "consume": v["consume"],
                      "recipes": v["recipes"]} for p, v in cfg["ports"].items()},
        "recipes": cfg["recipes"],
        "goods": {g: v["ship"] for g, v in cfg["goods"].items()},
        "coords": coords,
        "lanes": cfg["lanes"],
        "canals": {k: v["edge"] for k, v in cfg["canals"].items()},
        "captains": captains,
        "snaps": snaps,
        "routes": routes,
        "voyages": voyages,
        "history": markets.get("history", {}),
        "made": markets.get("made", {}),
        "blocked": markets.get("blocked", {}),
        "scores": results.get("scores", {}),
    }


def write_viewer(run_dir: Path) -> Path:
    data = build(run_dir)
    html = (HERE / "viewer_template.html").read_text()
    payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    out = run_dir / "viewer.html"
    out.write_text(html.replace("/*__RUN_DATA__*/null", payload).replace("/*__ATLAS__*/null", coastline()))
    return out


def main():
    out = write_viewer(Path(sys.argv[1]) if len(sys.argv) > 1 else latest_run())
    print(f"Wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
