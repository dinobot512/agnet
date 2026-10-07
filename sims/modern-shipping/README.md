# Modern shipping sim

Independent shipping captains trading across today's world: 31 real ports, 29 goods, 13 supply chains, real sea lanes with the Suez and Panama canals. Market information is perfect; other captains are invisible. **The rules are in [RULES.md](RULES.md).** Predetermined strategies only, for now: no AI agents, no API calls.

## Setup

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt     # only pytest; the sim itself is plain Python
```

## Run

```bash
.venv/bin/python run.py                         # 150 captains, 365 days, the default strategy mix (~3 s)
.venv/bin/python run.py --strategy greedy       # everyone plays one strategy
.venv/bin/python run.py --captains 60 --days 730 --seed 7
.venv/bin/python viewer.py                      # (re)build the playback page for the latest run
.venv/bin/python sweep.py                       # tune the economy (all cores)
.venv/bin/python -m pytest -q                   # tests
```

| Flag | Effect |
|---|---|
| `--seed N` | Fixes everything: fleet assignment, start ports, wake order, demand drift. Random if omitted, and always recorded. |
| `--captains N`, `--days N` | Fleet size (port flows scale with it) and game length |
| `--strategy greedy\|liner\|random` | Give every captain this strategy instead of the config's mix |
| `--config PATH` | Use another config, e.g. `runs/<timestamp>/config.json` to replay a run's world |
| `--quiet` | Don't print every voyage |

Every run writes a playback page, `runs/<timestamp>/viewer.html`.

## Files

| File | What it does |
|---|---|
| `config.json` | Everything about the world: ship types, costs, canals and tolls, goods (base price and ship class), recipes, 31 ports (lon/lat, production, consumption, factories), ~100 sea waypoints and the lanes between them, market settings, fleet mix, liner lanes, captain names |
| `network.py` | Sea-lane graph; great-circle lane lengths; shortest routes with or without canals |
| `world.py` | `Market`: prices, unit-by-unit price impact, daily production, `Recipe` factories (fractional batches; they record why they're idle), drifting consumption |
| `engine.py` | `Sim`: the day loop, wake-ups, actions (`buy`, `sell`, `refuel`, `sail`, `wait`), costs, emergency bunkers, bankruptcy, `View` (what a strategy may see), daily market history, scoring |
| `strategies/` | `greedy.py`, `liner.py`, `random_player.py`, plus `common.py` (closed-form price-impact estimates, voyage costs, refuelling) |
| `run.py` | Command line; writes the run folder and the viewer |
| `viewer.py`, `viewer_template.html` | Playback page (below) |
| `sweep.py` | Economy tuning over a grid of settings with mixed fleets |
| `test_*.py` | World, network, engine and strategy tests |

### Writing a new strategy
A strategy is any object with `act(sim, cid)`. It reads `view = sim.view(cid)`:
- **Its own ship:** `cash`, `fuel`, `tank`, `cargo`, `capacity`, `carries`, `port`, `spec`
- **Any market, live:** `market(port)`
- **Routes:** `route(dest, policy)` and `leg(a, b, policy)`

Then it calls `sim.buy / sell / refuel`, and must end with `sim.sail(cid, dest, policy)` or `sim.wait(cid, days)`. Register it in `run.players()` and the fleet mix in `config.json`.

## Playback viewer
- **Map:** a world map you can zoom and pan, with sea lanes and the canals in red. Ships are shaped by type (● bulk, ◆ tanker, ■ container) and colored by strategy. They glide along their real routes and sit in rings at ports; a dashed outline means waiting.
- **Hover a ship** for its strategy, type, status (including canal), cash, net worth, fuel and hold. **Click** it to follow it and see its route.
- **Left panel (any port):** what it produces and consumes; its factories, with batches made in the last 7 days and **why they're idle** (e.g. "idle: no coal"); ships in port and inbound; the true market each day, with demand and 7-day price changes.
- **Right panel:** strategy standings now; a ranked, scrollable leaderboard by net worth; recent voyages.

## Output: `runs/<timestamp>/`
| File | Contents |
|---|---|
| `events.jsonl` | Every event: `setup` (fleet), `arrive`, `wake`, `trade`, `refuel` (with emergency units), `sail` (route, canals, tolls, fuel), `wait`, `default_wait`, `bankrupt`, `finish` |
| `markets.json` | Daily history of every port's prices, stock and demand; batches made and idle reasons per factory per day |
| `results.json` | Final scores and stats per captain; batches made per factory |
| `summary.md` | Results by strategy and ship type, supply-chain output, leaderboard |
| `console.log`, `config.json`, `viewer.html` | Log, the config and seed used, and the playback page |
