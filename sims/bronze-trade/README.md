# Bronze Age trade sim

A swarm of independent ship captains trading across the Late Bronze Age Mediterranean. Captains only wake up in port, and **information travels only on ships**. **The rules are in [RULES.md](RULES.md).** This file covers how to run it.

## Setup

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

## Run

```bash
.venv/bin/python run.py --captains 10 --days 10   # small real game (~100 calls)
.venv/bin/python run.py                           # full game from config.json (50 captains, 120 days)
.venv/bin/python run.py --player random           # rule-of-thumb captains, no API calls (well under a second; --fake also works)
.venv/bin/python run.py --player informed         # rule-based captains with a parsable logbook and gossip (no API)
.venv/bin/python -m pytest -q                     # tests
.venv/bin/python viewer.py                        # playback page for the latest run (or pass runs/<timestamp>)
```

### Playback viewer
`viewer.py` turns a run into `runs/<timestamp>/viewer.html`, a single page you open in a browser:
- **The map:** the real Mediterranean, the ports and the sea lanes. Each ship is a small circle with its initial and number (e.g. `E14`), colored by home port. Rhodes shares the Mycenae color, since the palette has 8 hues; the label tells them apart.
- **Playback:** play/pause (space bar), ±1 day (arrow keys), a slider to jump to any day, and a speed from ½ to 8 days per second. Ships glide along the sea lanes between departure and arrival; ships in port sit in a ring around it. A dashed outline means the captain is asleep, waiting.
- **Hover a ship** to see its captain, home, status (in port / waiting until / sailing A → B, arriving day N), silver, hold, and the last thing it said. **Click** it to follow it: its route is drawn, and its stats stay in the side panel.
- **Hover a port** to see its market as last seen by a captain, and how many ships are there.
- **Side panel:** the 10 richest captains at the current day (click one to follow it), and the tavern talk up to that day, with who said it, where, and how many heard it.

The page loads d3 from a CDN. The coastline is downloaded once into `assets/` and embedded in each page.

| Flag | Effect |
|---|---|
| `--seed N` | Fixes all randomness: same-day trading order, talk order, names. Random if omitted, and always recorded in the run. |
| `--captains N`, `--days N` | Override `captains` / `days` |
| `--model ID` | Override `model` |
| `--player model\|random\|informed` | Who plays: Claude (default), the random rule-of-thumb player, or the informed rule-based player |
| `--fake` | Same as `--player random` |

Every run also writes its playback page, `runs/<timestamp>/viewer.html`.

**Cost:** each wake-up costs 1 call if the captain is alone, or 1 talk call per round plus about 2 decision calls in a meeting. Each call is about 3k input tokens. A 10-captain, 10-day test used about 115 calls (about $0.45 on Haiku). The cost grows with captains × days and with how much captains wait in busy ports, since every arrival wakes every captain waiting there.

**Aborts:** if the API reports a billing or authentication error, the run stops immediately and saves what it has, with `aborted` set in `results.json`.

## Files

| File | What it does |
|---|---|
| `world.py` | `Market`: per-port stock, prices (`base × (target/stock)^0.7`, clamped), unit-by-unit buying and selling, and lazy daily updates (production up to the storage cap, bronze-making only when both metals are there, consumption down to 0). `sailing_days`: shortest sea routes between ports. |
| `engine.py` | `Sim`: the calendar and event queue (arrivals, waiting deadlines), captains, port sessions (newcomers' first trade → wake waiters → talk rounds → final decisions), barkeep logs, logbooks, the briefing text, and scoring. Actions (`buy`, `sell`, `note`, `say`, `stay_silent`, `done_trading`, `sail`, `wait`) are validated and applied immediately. |
| `agent.py` | `CaptainPlayer`: model calls for each stage (`first`, `talk`, `final`), offering only that stage's tools. The system prompt is the rules plus the captain's persona. |
| `viewer.py`, `viewer_template.html` | Builds the playback page from a run's `events.jsonl` (see above). |
| `informed_agent.py` | `InformedPlayer`: a rule-based captain that uses only what it could know: the local market, its own logbook, and talk heard at its port. It logs every price as a parsable line (`PRICE port=Enkomi good=copper buy=4.06 sell=3.32 stock=400 day=10 src=seen`, where `src` is `seen` or the captain who told it). In the tavern it shares one record, chosen at random and weighted toward recent ones. It sells if this port pays at least 90% of the best net price it knows elsewhere. Then it picks the destination with the best expected profit per day of sailing (allowing for its own price impact and stale information), explores a port it knows nothing about, or waits 2 days. |
| `sweep.py` | Tunes the economy without API calls: runs random and informed captains over a grid of settings (`--grid broad` or `fine`, `--seeds N`, all CPU cores) and ranks the settings where random play roughly breaks even but informed play clearly wins. Results go to `sweeps/<timestamp>.json`. Re-check any winner on fresh seeds before adopting it: with many settings, the best few look better than they are. |
| `fake_agent.py` | `FakePlayer`: sells what the port buys, buys the cheapest good, repeats logbook prices in the tavern, sails at random. |
| `run.py` | Command line, runs the game, writes the outputs. |
| `config.json` | Goods and base prices, ports (production, consumption, bronze batches), sea lanes, ship and market numbers, captain origins (names and personas), and the rule text captains see. |
| `test_world.py`, `test_engine.py`, `test_informed.py` | Pricing, flows, bronze, sailing; newcomers trading first, deadlines, no calls at sea, information staying in its port, simultaneous talk, validation, stranding, silver accounting. |

## Output: `runs/<timestamp>/`

| File | Contents |
|---|---|
| `events.jsonl` | Written as events happen. Kinds: `setup`, `session` (newcomers, woken, still asleep, stock), `arrive`, `wake` (reason: arrival or deadline), `observe` (prices a captain saw), `trade`, `statement` (speaker, **listeners**, round), `note`, `sail`, `wait`, `default_wait`, `stranded`, `invalid_action`, `truncated`, `api_error`, `finish`. |
| `transcripts/captain_<id>.jsonl` | The captain's rules (a `system` line, once), then every briefing, response and tool result, tagged with day, port, stage and round. Same format as the economy sim; gleeb can read it. |
| `summary.md` | Leaderboard, plus everything each barkeep heard |
| `results.json` | Scores, ranking, token usage, and the abort reason if any |
| `console.log` | The console output |
| `config.json` | The config, seed, number of captains and days used |

The `statement` events (who said what, who heard it) and the `observe` events (who saw which prices, when) let you trace how a piece of news traveled from port to port.

## Tuning (2026-10-04)

Default fleet: **10 captains**. Economy (see RULES.md §9): provisions 1/day, harbor dues 2, 15% spread, buffers of 7 days, drifting demand, full-size port flows (`market.flow_scale` 1.0). At 10 ships, random captains end at a median of 263 and informed ones at 737; informed wins 10 of 10 games. `sweep.py --grid fleet10 --captains 10` reproduces the search.
