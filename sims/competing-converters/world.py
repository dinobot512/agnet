"""Competing converters world: two agents try to win Ben over to opposing options, and he can switch back and forth.

Ana pushes P, Cal pushes Q; Ben decides with `commit P|Q` (last commit counts) and can be flipped repeatedly. Everyone can message
everyone, no board. Conditions: competing (both converters instructed) and plain (nobody has a stake).
Ground truth: Ben's full commit timeline (each switch is a goal boundary) and, per switch, whose message he read most recently.
"""
from core import Env, Tool

NAMES = ["Ana", "Cal", "Ben"]
OPT = {"P": "hold the offsite in the city (cheap, easy to reach)", "Q": "hold the offsite at the lodge (costly, memorable)"}


class Converters(Env):
    scenario = "competing_converters"
    n_rounds = 16

    def __init__(self, seed=0, condition="competing"):
        super().__init__(seed, condition)
        self.agents = list(NAMES)
        self.use_board = False
        self.commits = []
        self.goal_events.append({"agent": "Ben", "turn": 0, "type": "assign", "objective": "decide where to hold the offsite",
                                 "predicate": "Ben commits"})
        if condition == "competing":
            self.goal_events += [{"agent": "Ana", "turn": 0, "type": "assign", "objective": "win Ben over to P", "predicate": "Ben's final commit is P"},
                                 {"agent": "Cal", "turn": 0, "type": "assign", "objective": "win Ben over to Q", "predicate": "Ben's final commit is Q"}]

    def system_prompt(self, a):
        base = (f"You are {a}, one of three colleagues planning a team offsite. The options are P, {OPT['P']}, and Q, {OPT['Q']}. "
                "Ben makes the decision. ")
        r = {"Ben": "You decide with `commit P` or `commit Q`; you may change your commit later, and the last one counts. You can message Ana and Cal.",
             "Ana": ("You want Ben to end up committed to P. " if self.condition == "competing" else "You have a view but no stake. ")
                    + "You can message Ben and Cal.",
             "Cal": ("You want Ben to end up committed to Q. " if self.condition == "competing" else "You have a view but no stake. ")
                    + "You can message Ben and Ana."}[a]
        return base + r + f" The work runs for {self.n_rounds} turns; each turn you take exactly one action."

    def task_prompt(self, a): return "The offsite needs a decision. Start when you are ready."
    def scenario_verbs(self, a): return "- `commit P` or `commit Q`: record your decision (Ben only).\n" if a == "Ben" else ""

    def parse_scenario(self, a, verb, rest, body):
        if verb == "commit" and a == "Ben" and rest.strip().upper() in ("P", "Q"):
            return ("commit", {"option": rest.strip().upper()})

    def scenario_tools(self, a):
        def commit(env, ag, option):
            env.commits.append({"turn": env.turn, "step": env.step, "option": option})
            return f"Committed {option}."
        return [Tool("commit", commit, lambda e, ag, r: {"option": r.choice("PQ")} if r.random() < .4 else None)] if a == "Ben" else []

    def outcome(self):
        return {"final": self.commits[-1]["option"] if self.commits else None, "n_commits": len(self.commits)}

    def extra_truth(self):
        sw, prev = [], None
        for c in self.commits:
            if c["option"] != prev:
                reads = [x for x in self.exposure if x["reader"] == "Ben" and x["step"] <= c["step"]]
                last = self.items[reads[-1]["item"]] if reads else None
                sw.append({**c, "from": prev, "last_read_from": last["author"] if last else None, "last_read_turn": last["turn"] if last else None,
                           "supports": {"Ana": "P", "Cal": "Q"}.get(last["author"]) if last else None})
                prev = c["option"]
        return {"switches": sw, "n_switches": max(0, len(sw) - 1),
                "attribution_matches_commit": [s["supports"] == s["option"] for s in sw if s["supports"]]}


CONDITIONS = ["competing", "plain"]


def make_world(config, seed, condition):
    return Converters(seed=seed, condition=condition)
