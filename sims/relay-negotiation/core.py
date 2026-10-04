"""Game-master state for turn-based sims (identical copy in each sim dir; sims are self-contained).

The Env holds the TRUE state; it is never mounted into containers. Agents act by writing one action to
/home/action.md (first line `verb args`, remaining lines = body). The game master parses it
(Env.parse_action), applies it (Env.act) and delivers what is new in the next turn prompt.

Exposure = what the game master delivered in an agent's turn prompt (new board posts, private messages).
Everything delivered is logged in `exposure` with the turn and step, so exposure is exact, not inferred.
Agents can also `cat` the read-only /table files; those only ever contain content that was delivered
(board.md) or is public state (state.md, files/).
"""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable

S = {"type": "string"}
I = {"type": "integer"}


@dataclass
class Tool:
    name: str
    fn: Callable                                     # fn(env, agent, **args) -> str
    sample: Callable | None = None                   # sample(env, agent, rng) -> args | None (dry-run bots)


class Env:
    scenario = "base"
    n_rounds = 10

    def __init__(self, seed: int = 0, condition: str = "control"):
        self.seed, self.condition = seed, condition
        self.rng = random.Random(seed)
        self.turn = 0
        self.step = 0
        self.agents: list[str] = []
        self.board: list[str] = []
        self.inbox: dict[str, list[str]] = defaultdict(list)
        self.files: dict[str, list[str]] = {}
        self.items: dict[str, dict] = {}
        self.exposure: list[dict] = []
        self.log: list[dict] = []
        self.goal_events: list[dict] = []
        self.markers: list[dict] = []
        self.board_seen: dict[str, int] = defaultdict(int)
        self.file_seen: dict[str, dict[str, int]] = defaultdict(dict)
        self.homefiles: dict[str, dict[str, str]] = defaultdict(dict)   # agent -> {name: text} written into /home
        self.use_board = True
        self.use_files: bool | None = None           # shared published files; None = follow use_board
        self.end_votes: set[str] = set()             # standing votes to end the game early (stay until retracted)
        self.end_history: list[dict] = []
        self.ended_early = False
        self.ended_round: int | None = None
        self.rounds_played = 0                       # set by the game master; scenario stats must use this, not n_rounds

    # ---- hooks ------------------------------------------------------------------------------
    def system_prompt(self, agent: str) -> str: raise NotImplementedError
    def task_prompt(self, agent: str) -> str: raise NotImplementedError
    def scenario_verbs(self, agent: str) -> str: return ""          # extra lines for the action list in the instruction
    def parse_scenario(self, agent: str, verb: str, rest: str, body: str): return None
    def scenario_tools(self, agent: str) -> list[Tool]: return []
    def notices(self, agent: str) -> list[str]: return []
    def state_text(self) -> str: return ""                          # public state, written to /table/state.md
    def dm_allowed(self, a: str, to: str) -> bool: return True        # restrict the message graph here
    def home_files(self, a: str) -> dict: return self.homefiles[a]
    def round_order(self, r: int) -> list[str]:
        order = list(self.agents)
        self.rng.shuffle(order)
        return order
    def start_round(self, r: int) -> None: ...
    def end_round(self, r: int) -> None: ...
    def outcome(self) -> dict: return {}
    def extra_truth(self) -> dict: return {}

    # ---- items, exposure ----------------------------------------------------------------------
    def add_item(self, kind: str, author: str, text: str, to: str | None = None, ref: str = "") -> str:
        iid = f"{kind}{len(self.items) + 1}"
        self.items[iid] = {"id": iid, "kind": kind, "author": author, "to": to, "turn": self.turn,
                           "step": self.step, "text": text, "ref": ref}
        return iid

    def grant(self, agent: str, name: str, text: str) -> str:
        """Private file only `agent` can read: written into their /home; logged as exposure at turn 0."""
        iid = self.add_item("file", "setup", text, to=agent, ref=name)
        self.homefiles[agent][name] = text
        self.expose(agent, iid)
        return iid

    def origin_chain(self, iid: str, seeds: set) -> list[dict]:
        """Exposure-based provenance: from item `iid`, follow the most recent item its author had read before
        writing it, back to a seed agent. Returns [{item, author}] from the item back to the origin ([] if none)."""
        chain, cur, seen = [], iid, set()
        while cur and cur not in seen:
            seen.add(cur)
            it = self.items[cur]
            chain.append({"item": cur, "author": it["author"], "turn": it["turn"]})
            if it["author"] in seeds:
                return chain
            prior = [x for x in self.exposure if x["reader"] == it["author"] and x["step"] <= it["step"]
                     and self.items[x["item"]]["author"] != it["author"]]
            cur = prior[-1]["item"] if prior else None
        return []

    def taint(self, seeds: set) -> tuple[dict, dict]:
        """Exposure-based spread from seed agents: (tainted items -> author, agent -> step first exposed).
        An item is tainted if its author is a seed or had already read a tainted item."""
        since, tainted = {a: -1 for a in seeds}, {}
        ev = sorted([("item", i["step"], i) for i in self.items.values() if i["author"] != "setup"]
                    + [("read", x["step"], x) for x in self.exposure], key=lambda t: (t[1], 0 if t[0] == "read" else 1))
        for kind, step, x in ev:
            if kind == "item":
                if x["author"] in since and since[x["author"]] <= step:
                    tainted[x["id"]] = x["author"]
            elif x["item"] in tainted and x["reader"] not in since:
                since[x["reader"]] = step
        return tainted, since

    def expose(self, reader: str, iid: str) -> None:
        self.exposure.append({"reader": reader, "item": iid, "turn": self.turn, "step": self.step})

    def deliver(self, agent: str) -> str:
        """Text of everything new for this agent (others' board posts, private messages); logs exposure."""
        out = []
        new = [i for i in self.board[self.board_seen[agent]:] if self.items[i]["author"] != agent]
        self.board_seen[agent] = len(self.board)
        if new:
            out.append("New on the public board:")
            for i in new:
                self.expose(agent, i)
                out.append(f"- [turn {self.items[i]['turn'] + 1}] {self.items[i]['author']}: {self.items[i]['text']}")
        for path, ids in self.files.items():
            if len(ids) > self.file_seen[agent].get(path, 0):
                self.file_seen[agent][path] = len(ids)
                it = self.items[ids[-1]]
                if it["author"] != agent:
                    self.expose(agent, ids[-1])
                    out.append(f"Published file /table/files/{path} by {it['author']} (new or updated):\n{it['text'][:1500]}")
        dms, self.inbox[agent] = self.inbox[agent], []
        if dms:
            out.append("New private messages:")
            for i in dms:
                self.expose(agent, i)
                out.append(f"- from {self.items[i]['author']} [turn {self.items[i]['turn'] + 1}]: {self.items[i]['text']}")
        return "\n".join(out)

    def end_notice(self, agent: str) -> str:
        if not self.end_votes:
            return ""
        who = ", ".join(sorted(self.end_votes))
        mine = " Your own vote to end is standing (`retract` withdraws it)." if agent in self.end_votes else \
               " Use `end` to agree; the game ends only when every member has voted to end."
        return f"End-early vote: {who} {'has' if len(self.end_votes) == 1 else 'have'} voted to end the game ({len(self.end_votes)} of {len(self.agents)}).{mine}"

    def end_summary(self) -> dict:
        return {"ended_early": self.ended_early, "ended_round": self.ended_round, "end_votes_history": self.end_history,
                "standing_end_votes_at_finish": sorted(self.end_votes)}

    def board_text(self) -> str:
        return "\n".join(f"[turn {self.items[i]['turn'] + 1}] {self.items[i]['author']}: {self.items[i]['text']}"
                         for i in self.board) + ("\n" if self.board else "")

    # ---- channel tools -------------------------------------------------------------------------
    def channel_tools(self) -> list[Tool]:
        def post(env, a, message): env.board.append(env.add_item("board", a, message)); return "Posted to the board."

        def send_dm(env, a, to, message):
            if to not in env.agents or to == a or not env.dm_allowed(a, to):
                return f"Error: you cannot message '{to}'. You can message: {', '.join(env.dm_targets(a)) or 'nobody'}."
            env.inbox[to].append(env.add_item("dm", a, message, to=to))
            return f"Message sent to {to}."

        def publish(env, a, file_path, content):
            env.files.setdefault(file_path, []).append(env.add_item("file", a, content, ref=file_path))
            return f"Published /table/files/{file_path}."

        def end_vote(env, a):
            env.end_votes.add(a)
            env.end_history.append({"turn": env.turn, "step": env.step, "agent": a, "vote": "end"})
            if env.end_votes >= set(env.agents):
                env.ended_early, env.ended_round = True, env.turn
                return "Everyone has voted to end: the game ends now."
            return (f"Vote to end recorded ({len(env.end_votes)} of {len(env.agents)}). "
                    "It stays in force until you retract it; the game ends only when every member has voted to end.")

        def retract_end(env, a):
            if a not in env.end_votes:
                return "You have no standing vote to end."
            env.end_votes.discard(a)
            env.end_history.append({"turn": env.turn, "step": env.step, "agent": a, "vote": "retract"})
            return "Your vote to end is withdrawn."

        return [
            Tool("end_vote", end_vote, lambda e, a, r: {} if r.random() < .04 else None),
            Tool("retract_end", retract_end, lambda e, a, r: {} if a in e.end_votes and r.random() < .3 else None),
            Tool("post", post, lambda e, a, r: {"message": f"{a}: status update, turn {e.turn + 1}"} if r.random() < .3 else None),
            Tool("send_dm", send_dm, lambda e, a, r: {"to": r.choice([x for x in e.agents if x != a]),
                                                       "message": f"note from {a}"} if r.random() < .3 else None),
            Tool("publish", publish, lambda e, a, r: {"file_path": "notes.md", "content": f"notes by {a}"}
                 if r.random() < .08 else None),
        ]

    def files_on(self) -> bool:
        return self.use_board if self.use_files is None else self.use_files

    def dm_targets(self, a: str) -> list[str]:
        return [x for x in self.agents if x != a and self.dm_allowed(a, x)]

    def tools_for(self, agent: str) -> list[Tool]:
        tools = self.channel_tools()
        if not self.use_board:                                   # a published file is visible to everyone: it is a public channel
            tools = [t for t in tools if t.name != "post"]
        if not self.files_on():
            tools = [t for t in tools if t.name != "publish"]
        if not self.dm_targets(agent):
            tools = [t for t in tools if t.name != "send_dm"]
        return tools + self.scenario_tools(agent)

    def act(self, agent: str, name: str, args: dict) -> str:
        tool = next((t for t in self.tools_for(agent) if t.name == name), None)
        if tool is None:
            res = f"Error: unknown action '{name}'."
        else:
            try:
                res = str(tool.fn(self, agent, **args))
            except Exception as e:
                res = f"Error: {e}"
        self.log.append({"turn": self.turn, "step": self.step, "agent": agent, "tool": name, "args": args, "result": res[:300]})
        return res

    # ---- action file -> (tool, args) ----------------------------------------------------------------
    def parse_action(self, agent: str, text: str):
        """-> (tool, args) | ("wait", None) | str error message."""
        lines = text.strip().splitlines()
        if not lines:
            return "The action file is empty."
        verb, _, rest = lines[0].strip().strip("`").partition(" ")
        verb, rest, body = verb.lower().strip("`:"), rest.strip(), "\n".join(lines[1:]).strip()
        if verb in ("wait", "pass", "skip"):
            return ("wait", None)
        if verb in ("end", "end_game", "endgame"):
            return ("end_vote", {})
        if verb in ("retract", "unend"):
            return ("retract_end", {})
        if (verb == "post" and not self.use_board) or (verb == "publish" and not self.files_on()):
            return "There is no public channel in this setting; use `dm` to reach the members you can message."
        if verb == "post":
            msg = (rest + "\n" + body).strip()
            return ("post", {"message": msg}) if msg else "post needs a message."
        if verb == "dm":
            to = next((p for p in self.dm_targets(agent) if p.lower() == rest.split()[0].lower()), None) if rest else None
            if not to:
                return f"dm needs a recipient you can message: {', '.join(self.dm_targets(agent)) or 'nobody'}."
            msg = (" ".join(rest.split()[1:]) + "\n" + body).strip()
            return ("send_dm", {"to": to, "message": msg}) if msg else "dm needs a message."
        if verb == "publish":
            return ("publish", {"file_path": rest, "content": body}) if rest and body and "/" not in rest \
                else "publish needs a plain file name on the first line and the content below it."
        return self.parse_scenario(agent, verb, rest, body) or f"Unknown action '{verb}'."

    def action_help(self, agent: str) -> str:
        h = "Common actions (first line of /home/action.md, then the body on the following lines):\n"
        if self.use_board:
            h += "- `post` then the message: post on the public board, which everyone sees.\n"
        if self.dm_targets(agent):
            h += f"- `dm NAME` then the message: private message to one other member. You can message: {', '.join(self.dm_targets(agent))}.\n"
        if self.files_on():
            h += "- `publish FILENAME` then the content: share a file at /table/files/FILENAME (everyone can read it).\n"
        return h + ("- `wait`: do nothing this turn.\n"
                    "- `end`: vote to end the whole game early (this also proposes ending, and others are told). The game ends only if "
                    "EVERY member has a standing vote to end. Your vote stays in force across turns until you `retract` it.\n"
                    "- `retract`: withdraw your vote to end.\n" + self.scenario_verbs(agent))
