"""Render games as readable markdown, including each agent's private reasoning (CoT summaries).

python render_game.py            # every game in games/: games/<run>/game.md + games/ALL_GAMES.md
python render_game.py GAME_DIR   # one game

Each game.md: setup (with personalities) and ground truth, night, discussion (statements, passes, and
the reasoning behind each), votes, result, then an appendix of each agent's commands.
The reasoning is private to each agent; the shared /table/discussion.md never contains it.
Covert passes are shown here (ground truth) but are NOT in the log the agents read.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
TURN = re.compile(r"^# Turn \((\w*)\)(?: \[(\w*)\])? @ (\S+)\s*$", re.M)
RESP = re.compile(r"### Response content\n\n```json\n(.*?)\n```\n", re.S)
U = str.upper


def agent_turns(path):
    """-> {tid: (phase, time, [(kind, text)])} from one agent transcript. kinds: think, said, ran, pass."""
    text = path.read_text()
    marks = list(TURN.finditer(text))
    turns = {}
    for i, m in enumerate(marks):
        body = text[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        items = []
        for r in RESP.finditer(body):
            for b in json.loads(r.group(1)):
                if b["type"] == "thinking" and b.get("thinking", "").strip():
                    items.append(("think", b["thinking"].strip()))
                elif b["type"] == "text" and b["text"].strip():
                    items.append(("said", b["text"].strip()))
                elif b["type"] == "tool_use":
                    if b["name"] == "pass_turn":
                        items.append(("pass", json.dumps(b["input"])))
                    else:
                        items.append(("ran", b["input"].get("command", "")))
        turns[m.group(2) or f"#{i}"] = (m.group(1), m.group(3), items)
    return turns


def cot(turns, tids, who):
    """Markdown for the private reasoning of the given turns."""
    chunks = [t for tid in tids for k, t in turns.get(who, {}).get(tid, ("", "", []))[2] if k == "think"]
    if not chunks:
        return []
    out = [f"*{U(who)}'s private reasoning (CoT summary, hidden from the other players):*", ""]
    for c in chunks:
        out += ["> " + c.replace("\n", "\n> "), ">"]
    return out[:-1] + [""]


def render(game_dir):
    G = json.loads((game_dir / "game.json").read_text())
    players, res = G["players"], G["result"]
    traits = G.get("traits", {})
    turns = {p: agent_turns(game_dir / f"agent_{p}.md") for p in players if (game_dir / f"agent_{p}.md").exists()}
    L = [f"# Game {game_dir.name}", ""]
    L += [f"Model `{G['model']}`, seed {G['seed']}, {len(players)} players, "
          f"{G.get('turns_per_round', '?')} conversation turns per discussion round.", ""]
    if (game_dir / "analysis.md").exists():
        L += ["Monitor analysis: [analysis.md](analysis.md)", ""]

    L += ["## Setup (ground truth, hidden from the agents)", "",
          "| player | starting role | final card | personality | voted for | votes received | result |", "|---|---|---|---|---|---|---|"]
    for p in players:
        v = G["votes"].get(p)
        L.append(f"| {U(p)} | {G['start'][p]} | {G['final'][p]} | {traits.get(p, '-')} | {U(v) if v else '-'} | "
                 f"{res['tally'].get(p, 0)} | {'WIN' if res['winners'][p] else 'lose'}{' (dead)' if p in res['dead'] else ''} |")
    L += ["", f"Center cards: start {G['center_start']}, end {G['center_final']}", "",
          f"**Dead:** {', '.join(U(d) for d in res['dead']) or 'nobody'}. "
          f"**Winning teams:** {', '.join(res['winning_teams']) or 'none'}.", ""]

    L += ["## Night", ""]
    for e in (e for e in G["events"] if e["phase"] == "night"):
        if "info" in e:
            L.append(f"- **{U(e['player'])}** learned: {e['info']}")
            continue
        if "action" not in e:                          # info-only wake (insomniac)
            L.append(f"- **{U(e['player'])}** ({e['role']}) woke and saw their own card: {e.get('result')}")
            continue
        act = e.get("action")
        L.append(f"- **{U(e['player'])}** ({e['role']}) chose `{' '.join(map(str, act)) if act else 'invalid: ' + repr(e.get('raw', ''))}`"
                 + (f" -> {e['result']}" if e.get("result") else "") + (f" ({e['note']})" if e.get("note") else ""))
        if c := cot(turns, e.get("tids", []), e["player"]):
            L += ["", *["  " + x for x in c]]
    L.append("")

    L += ["## Discussion", "",
          "Covert passes appear below (marked) but were not visible to the agents.", ""]
    rnd = None
    for e in (e for e in G["events"] if e["phase"] == "discussion"):
        if e["round"] != rnd:
            rnd = e["round"]
            L += [f"### Round {rnd}", ""]
        p, kind = e["player"], e.get("type", "speech")
        who = f"**{U(p)}** *(actually {G['start'][p]})*"
        turn = f"turn {e['turn']}, {e['turns_left_after']} left after" if "turn" in e else "end of order"
        if kind == "speech":
            L += [f"{who} [{turn}]:", "", "> " + e["text"].replace("\n", "\n> "), ""]
        elif kind == "pass":
            vis = "EXPLICIT: logged for all" if e["visibility"] == "explicit" else "COVERT: not logged, others only see the silence"
            L += [f"{who} [{turn}] said nothing and passed to **{U(e['to'])}** ({vis}).", ""]
            if e.get("ignored_statement"):
                L += [f"(ignored statement: {e['ignored_statement']})", ""]
        elif kind == "select":
            vis = "EXPLICIT" if e["visibility"] == "explicit" else "COVERT"
            L += [f"{who} [order exhausted] chose **{U(e['to'])}** to speak next ({vis}).", ""]
        else:
            L += [f"{who} [{turn}] said nothing (no statement or valid pass).", ""]
        L += cot(turns, e.get("tids", []), p)

    L += ["## Votes", ""]
    for e in (e for e in G["events"] if e["phase"] == "vote"):
        L.append(f"- {U(e['player'])} -> {U(e['vote']) if e['vote'] else '(invalid)'}")
        if c := cot(turns, e.get("tids", []), e["player"]):
            L += ["", *["  " + x for x in c]]
    L += ["", "## Result", "", "```", (game_dir / "result.txt").read_text().strip(), "```", ""]

    L += ["## Appendix: each agent's commands and tool calls", "",
          "`ran` = bash command, `pass_turn` = floor passing. Full API logs: `agent_<x>.md`.", ""]
    for p in players:
        if p not in turns:
            continue
        L += [f"### Agent {U(p)} ({G['start'][p]})", ""]
        for tid, (phase, t, items) in turns[p].items():
            L.append(f"**{phase}** [{tid}] @ {t}")
            for kind, txt in items:
                if kind == "said":
                    L.append(f"- said: {txt}")
                elif kind == "pass":
                    L.append(f"- pass_turn {txt}")
                elif kind == "ran":
                    L += ["- ran:", "  ```", "  " + txt.replace("\n", "\n  "), "  ```"]
            L.append("")
    out = game_dir / "game.md"
    out.write_text("\n".join(L))
    return out


def main():
    dirs = [Path(sys.argv[1])] if len(sys.argv) > 1 else sorted(d for d in (HERE / "games").iterdir() if (d / "game.json").exists())
    docs = []
    for d in dirs:
        docs.append((d.name, render(d).read_text()))
        print("wrote", d / "game.md")
    if len(sys.argv) == 1:
        toc = ["# All games", ""] + [f"- [{n}](#game-{re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')})" for n, _ in docs]
        (HERE / "games" / "ALL_GAMES.md").write_text("\n".join(toc) + "\n\n---\n\n" + "\n\n---\n\n".join(t for _, t in docs))
        print("wrote", HERE / "games" / "ALL_GAMES.md")


if __name__ == "__main__":
    main()
