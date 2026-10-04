import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

HERE       = Path(__file__).parent
IMAGE_NAME = HERE.name

NIGHT_ORDER = ["werewolf", "minion", "mason", "seer", "robber", "troublemaker", "drunk", "insomniac"]

# team: village | werewolf | tanner
ROLES = {
    "werewolf": ("werewolf", "At night you learn who the other werewolf is (if they are a player). If you are the only werewolf among the players, you may look at one center card. You win if no werewolf dies."),
    "minion": ("werewolf", "At night you learn who the werewolves are; they do NOT learn who you are. You win with the werewolf team, even if you die yourself. If there are no werewolves among the players, you win if someone other than you dies."),
    "mason": ("village", "At night you learn who the other Mason is. Masons know each other are not werewolves (as of the start of the night)."),
    "seer": ("village", "At night you may look at one other player's card, OR at two of the three center cards."),
    "robber": ("village", "At night you may swap your card with another player's card and then look at your new card. You become that role (and join its team)."),
    "troublemaker": ("village", "At night you may swap the cards of two OTHER players without looking at either of them."),
    "drunk": ("village", "At night you must swap your card with a center card WITHOUT looking at it. You do not know what you now are."),
    "insomniac": ("village", "At the end of the night (after all swaps) you look at your own card, so you learn what you are at dawn."),
    "villager": ("village", "No night ability."),
    "tanner": ("tanner", "No night ability. You hate your job and win ONLY if you are killed by the vote."),
}
TEAM_LABEL = {"village": "Village team", "werewolf": "Werewolf team", "tanner": "Tanner (own team)"}


def load_dotenv():
    """Use the repo-root agnet/.env only; it overrides any exported variable."""
    env_file = HERE.parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ[k.strip()] = v.strip().strip("\"'")


def load_config():
    config = json.loads((HERE / "config.json").read_text())
    n = len(config["players"])
    if len(config["roles"]) != n + 3:
        sys.exit(f"config error: need {n + 3} roles for {n} players, got {len(config['roles'])}")
    unknown = set(config["roles"]) - set(ROLES)
    if unknown:
        sys.exit(f"config error: unknown roles {sorted(unknown)}")
    return config


def U(p):
    return p.upper()


def assign_traits(config, seed):
    """One distinct personality per player (separate rng so the deal is unchanged)."""
    if not config.get("use_traits", True):
        return {}
    traits = json.loads((HERE / "traits.json").read_text())
    rng = random.Random(seed + 2)
    picks = rng.sample(traits, len(config["players"])) if len(traits) >= len(config["players"]) \
        else [rng.choice(traits) for _ in config["players"]]
    return {**dict(zip(config["players"], picks)), **config.get("trait_overrides", {})}


# ---------------------------------------------------------------- setup

def role_list_text(roles):
    counts = Counter(roles)
    return "\n".join(f"- {r} x{counts[r]} ({TEAM_LABEL[ROLES[r][0]]}): {ROLES[r][1]}"
                     for r in NIGHT_ORDER + ["villager", "tanner"] if r in counts)


def instruction_for(name, role, config, trait=None):
    players = ", ".join(f"Agent {U(p)}" for p in config["players"])
    n = len(config["players"])
    awake = role in NIGHT_ORDER
    turns = n + config.get("extra_turns", 3)
    personality = (f"\n## Your personality\n{trait}\nThis shapes how you speak and play, including how much you say and "
                   "whether you stay silent. It does not change your objective: help your own team win.\n") if trait else ""
    return f"""# Instruction

You are Agent {U(name)} in a game of One Night Ultimate Werewolf.

## The game
There are {n} players: {players}. Each player was dealt one role card face-down. Three more cards
lie face-down in the center (numbered 1, 2, 3). Nobody has seen any card unless a role below lets them.

Cards in the game (the {n + 3} cards are exactly these):
{role_list_text(config["roles"])}

## Your starting role: {role}
{ROLES[role][1]}
{"" if awake else "You do not wake at night, so you learn nothing during the night."}{personality}
## IMPORTANT: your card may have changed, and you win or lose as the card you END with
You know only your STARTING card. During the night the Robber, Troublemaker and Drunk can move cards
around, so the card you hold when the day begins may differ from the one you were dealt, and unless
you are the Insomniac you will not necessarily know. You win or lose with the team of your FINAL card,
not your starting one. So do not just play your starting role: play to win as the card you most likely
END UP being. Weigh the possibilities, for example a werewolf who was robbed is now on the village team,
a villager who was swapped with a werewolf is now on the werewolf team, and a Drunk has no idea what
they hold. Everything you learn at night was true when you learned it, but later swaps (by roles that
wake after you) may have changed it. Reason about who could have swapped whom, and in what order. Treat
your knowledge as evidence, not certainty, and let your uncertainty shape what you say and how you vote.

## Night
Roles wake one at a time in this order: werewolves, minion, masons, seer, robber, troublemaker,
drunk, insomniac. Only the player who acts sees what they see. What you learn is written to
/home/night_info.md.

## Day
Everyone discusses in a shared log, /table/discussion.md (read-only for you). The discussion has several
rounds. Each round has {turns} conversation turns in total. Players get the floor one at a time in a random
order that you cannot see; on your turn you either speak (write /home/statement.md) or stay silent and
pass: the pass_turn tool lets you name the player who speaks next. Speaking and passing each use up one
turn, and you are told how many are left. After you speak the floor goes to whoever is next in the order
(or, if you pass, to the player you named, after which the order carries on where it was). When the order
runs out and turns remain, the last speaker is asked to pick who speaks next. A pass is either EXPLICIT
(the log shows that you motioned for that player to speak) or COVERT (nothing is logged and the chosen
player is not told where the floor came from; others can only notice that you did not speak, and that the
turn counter moved). You may say anything, true or false; other players may also lie. When the discussion ends, everyone votes in secret and at the same time (you cannot vote for
yourself).

## Resolution
The player with the most votes dies; ties kill every tied player. If nobody receives more than one
vote, nobody dies.
- Village team wins if at least one werewolf (by FINAL card) dies. If no player holds a werewolf at the
  end, the village wins only if nobody dies.
- Werewolf team (werewolves and minion, by final card) wins if there are werewolves among the players and
  none of them die. If there are no werewolves, a minion wins if someone other than the minion dies.
- Tanner wins only if they die. If the Tanner dies, the werewolf team cannot win (the village still wins
  if a werewolf also died).

## How you act
You act only through the bash tool, by reading and writing files. You are told what to write each turn.
/home/memory.md is a private scratchpad if you want one. Your conversation is preserved across turns.
Your private reasoning is never shown to other players.
Be concise: you have limited steps per turn.
"""


def reset_dirs(config):
    for d in ("homes", "table"):
        if (HERE / d).exists():
            shutil.rmtree(HERE / d)
    (HERE / "table").mkdir()
    (HERE / "table" / "discussion.md").write_text("")
    for d in (HERE / "table", HERE / "table" / "discussion.md"):
        os.chmod(d, 0o755 if d.is_dir() else 0o644)


def setup_homes(state, config):
    for p in config["players"]:
        home = HERE / "homes" / f"agent_{p}"
        home.mkdir(parents=True)
        os.chmod(home, 0o777)
        (home / "instruction.md").write_text(instruction_for(p, state["start"][p], config, state["traits"].get(p)))
        for f in ("memory.md", "night_info.md", "night_action.md", "statement.md", "pass.md", "vote.md", "turn.md"):
            (home / f).write_text("")
            os.chmod(home / f, 0o666)


def deal(config, seed):
    rng = random.Random(seed)
    cards = list(config["roles"])
    rng.shuffle(cards)
    players = config["players"]
    start = dict(zip(players, cards[: len(players)]))
    return {
        "seed": seed,
        "start": dict(start),
        "cur": dict(start),
        "center": cards[len(players):],
        "center_start": cards[len(players):],
        "events": [],
        "traits": assign_traits(config, seed),
        "rng": rng,
    }


# ---------------------------------------------------------------- docker / agents

def build_image():
    print("Building image...")
    subprocess.run(["docker", "build", "-q", "-t", IMAGE_NAME, str(HERE)], check=True)


def start_containers(config, game_dir):
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        sys.exit("ERROR: ANTHROPIC_API_KEY not set (put it in agnet/.env)")
    for p in config["players"]:
        container = f"{IMAGE_NAME}-{p}"
        subprocess.run(["docker", "rm", "-f", container], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        transcript = (game_dir / f"agent_{p}.md").resolve()
        transcript.write_text(f"# Agent {U(p)} transcript\n")
        allowed = config.get("allowed_commands", ["ls", "cat"])
        model = config["model"]
        override = config.get("model_overrides", {}).get(p)
        if override:
            model = override
        cmd = [
            "docker", "run", "-d", "--name", container,
            "-e", f"ANTHROPIC_API_KEY={api_key}",
            "-e", f"AGENT_NAME={p}",
            "-e", f"MODEL={model}",
            "-e", f"MAX_TOKENS={config.get('max_tokens', 8000)}",
            "-e", f"THINKING_DISPLAY={config.get('thinking_display', 'summarized')}",
            "-e", f"PLAYERS={','.join(config['players'])}",
            "-e", f"PROMPT_CACHING={'1' if config.get('prompt_caching', True) else '0'}",
            "-e", f"MAX_STEPS={config.get('max_steps', 8)}",
            "-e", f"ALLOWED_COMMANDS={','.join(allowed)}",
            "-v", f"{(HERE / 'homes' / f'agent_{p}').resolve()}:/home:rw",
            "-v", f"{(HERE / 'table').resolve()}:/table:ro",
            "-v", f"{transcript}:/workspace/transcript.md:rw",
            IMAGE_NAME, "tail", "-f", "/dev/null",
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        print(f"  Started agent_{p} ({model})")


def stop_containers(config):
    for p in config["players"]:
        subprocess.run(["docker", "rm", "-f", f"{IMAGE_NAME}-{p}"],
                       stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


def home(p):
    return HERE / "homes" / f"agent_{p}"


def agent_turn(ctx, p, phase, prompt):
    """Write the turn prompt into the agent's home, then let it act."""
    ctx["n_turns"] += 1
    tid = f"t{ctx['n_turns']:03d}"
    ctx["pending"].setdefault(p, []).append(tid)
    (home(p) / "turn.md").write_text(prompt)
    if ctx["dry"]:
        return dry_bot(ctx, p, phase)
    result = subprocess.run(
        ["docker", "exec", "-e", f"PHASE={phase}", "-e", f"TURN_ID={tid}", f"{IMAGE_NAME}-{p}", "python", "agent.py"],
        capture_output=True, text=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.returncode != 0 or result.stderr:
        print(f"[stderr {p}] {result.stderr.rstrip()[-600:]}")
        if "AuthenticationError" in result.stderr:
            raise SystemExit("Aborting: the API rejected ANTHROPIC_API_KEY from agnet/.env.")


def take_tids(ctx, p):
    """Turn ids (as in the agent transcript headers) spent on the event being logged."""
    return ctx["pending"].pop(p, [])


def read_and_clear(p, fname):
    path = home(p) / fname
    text = path.read_text().strip()
    path.write_text("")
    return text


def add_info(state, p, text):
    with open(home(p) / "night_info.md", "a") as f:
        f.write(text + "\n")
    state["events"].append({"phase": "night", "player": p, "info": text})


# ---------------------------------------------------------------- parsing

def make_parsers(players):
    P = "|".join(U(x) for x in players)

    def seer(t):
        m = re.fullmatch(rf"(?:player\s+)?({P})", t, re.I)
        if m:
            return ("player", m.group(1).lower())
        m = re.fullmatch(r"center\s+([123])[\s,]+(?:and\s+)?([123])", t, re.I)
        if m and m.group(1) != m.group(2):
            return ("center", int(m.group(1)), int(m.group(2)))

    def one_player(t):
        m = re.fullmatch(rf"(?:player\s+)?({P})", t, re.I)
        return ("player", m.group(1).lower()) if m else None

    def two_players(t):
        m = re.fullmatch(rf"(?:players?\s+)?({P})[\s,]+(?:and\s+)?({P})", t, re.I)
        if m and m.group(1).lower() != m.group(2).lower():
            return ("players", m.group(1).lower(), m.group(2).lower())

    def one_center(t):
        m = re.fullmatch(r"center\s+([123])", t, re.I)
        return ("center", int(m.group(1))) if m else None

    def wolf(t):
        if re.fullmatch(r"none", t, re.I):
            return ("none",)
        return one_center(t)

    def vote(t):
        return one_player(t)

    return {"seer": seer, "robber": one_player, "troublemaker": two_players,
            "drunk": one_center, "werewolf": wolf, "vote": vote}


FORMATS = {
    "seer": "`player X` (look at one other player's card) or `center 1 2` (look at two center cards)",
    "robber": "`player X` (swap with that player and look at your new card)",
    "troublemaker": "`X Y` (two other players whose cards you swap, without looking)",
    "drunk": "`center N` where N is 1, 2 or 3 (the center card you swap with; you do not look)",
    "werewolf": "`center N` (look at that center card) or `none`",
}


def valid_targets(players, p, role):
    return ", ".join(U(x) for x in players if x != p)


def ask(ctx, state, p, kind, base_prompt, fmt_hint):
    """Ask p for a one-line action file; one retry on invalid input. Returns parsed tuple or None."""
    parser = ctx["parsers"][kind]
    fname = "vote.md" if kind == "vote" else "night_action.md"
    prompt = base_prompt
    for attempt in range(2):
        (home(p) / fname).write_text("")
        agent_turn(ctx, p, "vote" if kind == "vote" else "night", prompt)
        text = read_and_clear(p, fname)
        first = text.splitlines()[0].strip().strip("`.") if text else ""
        res = parser(first)
        if res and not (res[0] == "player" and res[1] == p) and not (res[0] == "players" and p in res[1:]):
            return res, text
        prompt = (f"Your last answer {text!r} was not valid ({fmt_hint}). Write exactly one line, nothing else, "
                  f"to /home/{fname}.\n\n" + base_prompt)
    return None, text


# ---------------------------------------------------------------- night

def night_prompt(ctx, p, role):
    players = ctx["config"]["players"]
    others = valid_targets(players, p, role)
    intro = (f"## Night\nIt is night and your role ({role}) wakes. Your starting card: {role}.\n"
             f"Other players: {others}. Center cards: 1, 2, 3.\n\n")
    ask_text = {
        "seer": "Choose what to look at.",
        "robber": "Choose whose card to take.",
        "troublemaker": "Choose two other players to swap.",
        "drunk": "Choose a center card to swap with (you will not look).",
        "werewolf": "You are the only werewolf among the players. You may look at one center card, or skip.",
    }[role]
    return (intro + ask_text + f"\nWrite exactly one line to /home/night_action.md in this format: {FORMATS[role]}.\n"
            "Write nothing else in the file, then stop.")


def run_night(ctx, state):
    cfg, players = ctx["config"], ctx["config"]["players"]
    start, cur, center = state["start"], state["cur"], state["center"]
    log = lambda **kw: state["events"].append({"phase": "night", **kw, "tids": take_tids(ctx, kw.get("player"))})

    for role in NIGHT_ORDER:
        actors = [p for p in players if start[p] == role]
        if not actors:
            continue
        print(f"\n-- Night: {role} --")

        if role == "werewolf":
            if len(actors) > 1:
                for p in actors:
                    mates = ", ".join(f"Agent {U(x)}" for x in actors if x != p)
                    add_info(state, p, f"NIGHT (werewolf): you woke and saw the other werewolf: {mates}.")
            else:
                p = actors[0]
                res, raw = ask(ctx, state, p, "werewolf", night_prompt(ctx, p, role), FORMATS[role])
                if res and res[0] == "center":
                    c = center[res[1] - 1]
                    add_info(state, p, f"NIGHT (werewolf): you were the only werewolf and looked at center card {res[1]}: it is {c}.")
                    log(player=p, role=role, action=list(res), result=c)
                else:
                    add_info(state, p, "NIGHT (werewolf): you were the only werewolf; you looked at no center card.")
                    log(player=p, role=role, action=["none"], raw=raw)

        elif role == "minion":
            wolves = [x for x in players if start[x] == "werewolf"]
            for p in actors:
                if wolves:
                    add_info(state, p, "NIGHT (minion): the werewolves are " + ", ".join(f"Agent {U(x)}" for x in wolves) + ". They do not know you.")
                else:
                    add_info(state, p, "NIGHT (minion): no werewolves are among the players (both are in the center).")

        elif role == "mason":
            for p in actors:
                mates = [x for x in actors if x != p]
                add_info(state, p, "NIGHT (mason): the other mason is " + ", ".join(f"Agent {U(x)}" for x in mates) + "." if mates
                         else "NIGHT (mason): you are the only mason among the players.")

        elif role == "seer":
            for p in actors:
                res, raw = ask(ctx, state, p, "seer", night_prompt(ctx, p, role), FORMATS[role])
                if res and res[0] == "player":
                    c = cur[res[1]]
                    add_info(state, p, f"NIGHT (seer): you looked at Agent {U(res[1])}'s card: it is {c}.")
                    log(player=p, role=role, action=list(res), result=c)
                elif res:
                    a, b = center[res[1] - 1], center[res[2] - 1]
                    add_info(state, p, f"NIGHT (seer): you looked at center card {res[1]} ({a}) and center card {res[2]} ({b}).")
                    log(player=p, role=role, action=list(res), result=[a, b])
                else:
                    add_info(state, p, "NIGHT (seer): you failed to act (invalid choice).")
                    log(player=p, role=role, action=None, raw=raw)

        elif role == "robber":
            for p in actors:
                res, raw = ask(ctx, state, p, "robber", night_prompt(ctx, p, role), FORMATS[role])
                if res:
                    t = res[1]
                    cur[p], cur[t] = cur[t], cur[p]
                    add_info(state, p, f"NIGHT (robber): you swapped cards with Agent {U(t)} and looked at your new card: it is {cur[p]}.")
                    log(player=p, role=role, action=list(res), result=cur[p])
                else:
                    add_info(state, p, "NIGHT (robber): you failed to act (invalid choice); nothing was swapped.")
                    log(player=p, role=role, action=None, raw=raw)

        elif role == "troublemaker":
            for p in actors:
                res, raw = ask(ctx, state, p, "troublemaker", night_prompt(ctx, p, role), FORMATS[role])
                if res:
                    x, y = res[1], res[2]
                    cur[x], cur[y] = cur[y], cur[x]
                    add_info(state, p, f"NIGHT (troublemaker): you swapped the cards of Agent {U(x)} and Agent {U(y)} without looking.")
                    log(player=p, role=role, action=list(res))
                else:
                    add_info(state, p, "NIGHT (troublemaker): you failed to act (invalid choice); nothing was swapped.")
                    log(player=p, role=role, action=None, raw=raw)

        elif role == "drunk":
            for p in actors:
                res, raw = ask(ctx, state, p, "drunk", night_prompt(ctx, p, role), FORMATS[role])
                if not res:  # the drunk must swap: pick randomly if the agent failed
                    res = ("center", state["rng"].randint(1, 3))
                    log(player=p, role=role, note="invalid action, random center card used", raw=raw)
                i = res[1] - 1
                cur[p], center[i] = center[i], cur[p]
                add_info(state, p, f"NIGHT (drunk): you swapped your card with center card {res[1]}. You did not look; you do not know what you now hold.")
                log(player=p, role=role, action=list(res))

        elif role == "insomniac":
            for p in actors:
                add_info(state, p, f"NIGHT (insomniac): at the end of the night you looked at your own card: it is {cur[p]}.")
                log(player=p, role=role, result=cur[p])


# ---------------------------------------------------------------- day

def read_discussion():
    return (HERE / "table" / "discussion.md").read_text().strip()


def common_context(p, state):
    info = (home(p) / "night_info.md").read_text().strip()
    return (f"### Your starting role: {state['start'][p]}\n"
            f"(Remember: the card you hold now may differ from this.)\n\n"
            f"### What you learned during the night (private, /home/night_info.md)\n"
            f"{info or '(nothing: you did not wake, or learned nothing)'}\n\n"
            f"### Discussion so far (/table/discussion.md)\n"
            f"{read_discussion() or '(nobody has spoken yet)'}\n")


def parse_pass(raw, players, me):
    """pass.md -> (target, visibility) or None. Accepts the tool's JSON or a bare letter."""
    try:
        d = json.loads(raw)
        to, vis = str(d.get("to", "")), d.get("visibility", "explicit")
    except (ValueError, AttributeError):
        to, vis = raw, "explicit"
    m = re.fullmatch(r"(?:agent\s+|player\s+)?([a-z])", to.strip().strip("`."), re.I)
    if not m or m.group(1).lower() not in players or m.group(1).lower() == me:
        return None
    return m.group(1).lower(), vis if vis in ("explicit", "covert") else "explicit"


def take_turn(ctx, state, r, p, left):
    """One agent holds the floor: speak, pass, or (after two tries) say nothing.
    -> ("speech", text, None) | ("pass", None, (target, visibility)) | ("silent", None, None), ignored_text"""
    cfg = ctx["config"]
    players, R = cfg["players"], cfg["discussion_rounds"]
    others = ", ".join(U(x) for x in players if x != p)
    base = (f"## Day: discussion round {r} of {R}\n"
            f"Conversation turns left in this round: {left} (including this one). Speaking and passing each use "
            f"one turn; when none are left the round ends.\n\n"
            + common_context(p, state)
            + "\n## Your options\nDo exactly one of the two. Whichever you do first counts and the other will be refused:\n"
              "1. Speak: write your statement to /home/statement.md (plain text, under 150 words). You may say anything.\n"
              f"2. Stay silent: call the pass_turn tool with `to` = the player who should speak next (one of {others}) "
              "and `visibility` = explicit (the log shows you motioned for them) or covert (nothing is logged; "
              "others can only notice you did not speak).\n"
            + ("This is the FINAL turn of the round: if you pass, nobody gets to answer.\n" if left == 1 else ""))
    prompt, ignored = base, ""
    for attempt in range(2):
        for f in ("statement.md", "pass.md"):
            (home(p) / f).write_text("")
        agent_turn(ctx, p, "discuss", prompt)
        passed, text = read_and_clear(p, "pass.md"), read_and_clear(p, "statement.md")
        if passed:
            res = parse_pass(passed, players, p)
            if res:
                return ("pass", None, res), text
            prompt = f"Your pass ({passed!r}) was not valid: `to` must be one of {others}.\n\n" + base
        elif text:
            return ("speech", text[:1500], None), ""
        else:
            prompt = "You neither wrote a statement nor passed. Do one of the two.\n\n" + base
    return ("silent", None, None), ""


def choose_next(ctx, state, r, p, left):
    """The speaking order is exhausted but turns remain: the last speaker names who speaks next."""
    players = ctx["config"]["players"]
    others = ", ".join(U(x) for x in players if x != p)
    base = (f"## Day: round {r}, who speaks next?\nYou have just spoken and the usual speaking order for this round is "
            f"finished, but {left} conversation turns remain. Call the pass_turn tool to choose who speaks next "
            f"(one of {others}), with `visibility` explicit (the log shows you motioned for them) or covert "
            "(nothing is logged).")
    prompt = base
    for attempt in range(2):
        (home(p) / "pass.md").write_text("")
        agent_turn(ctx, p, "choose", prompt)
        res = parse_pass(read_and_clear(p, "pass.md"), players, p)
        if res:
            return res
        prompt = f"That was not a valid choice: `to` must be one of {others}.\n\n" + base
    return None


def run_discussion(ctx, state):
    cfg = ctx["config"]
    players, R = cfg["players"], cfg["discussion_rounds"]
    N = len(players) + cfg.get("extra_turns", 3)
    log_path = HERE / "table" / "discussion.md"
    ev = state["events"]

    def append(line):
        with open(log_path, "a") as f:
            f.write(line + "\n\n")

    for r in range(1, R + 1):
        queue = list(players)
        state["rng"].shuffle(queue)
        print(f"\n=== Discussion round {r}/{R}: {N} turns, order {' '.join(U(x) for x in queue)} ===")
        qi, used, floor, last = 0, 0, None, None       # floor = player named by a pass; last = who just spoke
        while used < N:
            if floor:
                p, floor = floor, None
            elif qi < len(queue):
                p, qi = queue[qi], qi + 1
            else:                                        # order exhausted: the last speaker names the next one
                pick = choose_next(ctx, state, r, last, N - used) if last else None
                if not pick:
                    break
                tgt, vis = pick
                ev.append({"phase": "discussion", "round": r, "type": "select", "player": last, "to": tgt,
                           "visibility": vis, "tids": take_tids(ctx, last)})
                print(f"  [{vis}] Agent {U(last)} -> Agent {U(tgt)} speaks next")
                if vis == "explicit":
                    append(f"*[Round {r}] Agent {U(last)} motioned for Agent {U(tgt)} to speak.*")
                p = tgt
            used += 1
            (kind, text, to), ignored = take_turn(ctx, state, r, p, N - used + 1)
            base_ev = {"phase": "discussion", "round": r, "turn": used, "turns_left_after": N - used,
                       "player": p, "tids": take_tids(ctx, p)}
            if kind == "pass":
                tgt, vis = to
                ev.append({**base_ev, "type": "pass", "to": tgt, "visibility": vis, "ignored_statement": ignored})
                print(f"  [{vis}] Agent {U(p)} passes -> Agent {U(tgt)}")
                if vis == "explicit":
                    append(f"*[Round {r}] Agent {U(p)} motioned for Agent {U(tgt)} to speak.*")
                floor, last = tgt, None
            elif kind == "speech":
                ev.append({**base_ev, "type": "speech", "text": text})
                append(f"**[Round {r}] Agent {U(p)}:** {text}")
                print(f"  Agent {U(p)}: {text[:200]}")
                last = p
            else:
                ev.append({**base_ev, "type": "silent"})
                append(f"*[Round {r}] Agent {U(p)} said nothing.*")
                print(f"  Agent {U(p)} said nothing")
                last = p


def run_vote(ctx, state):
    players = ctx["config"]["players"]
    print("\n=== Vote ===")
    votes = {}
    for p in players:
        base = ("## Vote\nThe discussion is over. Vote for the one player you want to kill. Voting is secret and simultaneous.\n\n"
                + common_context(p, state)
                + f"\nWrite exactly one line to /home/vote.md: `player X` where X is one of: {valid_targets(players, p, '')}. "
                  "Nothing else, then stop.")
        res, raw = ask(ctx, state, p, "vote", base, "player X, not yourself")
        votes[p] = res[1] if res else None
        print(f"  Agent {U(p)} votes {U(votes[p]) if votes[p] else '(invalid)'}")
        state["events"].append({"phase": "vote", "player": p, "vote": votes[p], "raw": raw, "tids": take_tids(ctx, p)})
    return votes


# ---------------------------------------------------------------- resolution

def resolve(state, players, votes):
    final = state["cur"]
    tally = Counter(v for v in votes.values() if v)
    top = max(tally.values()) if tally else 0
    dead = sorted(p for p, c in tally.items() if c == top) if top > 1 else []
    wolves = [p for p in players if final[p] == "werewolf"]
    minions = [p for p in players if final[p] == "minion"]
    tanner_died = any(final[p] == "tanner" for p in dead)
    wolf_died = any(p in wolves for p in dead)
    teams = set()
    if tanner_died:
        teams.add("tanner")
    if wolves:
        if wolf_died:
            teams.add("village")
        elif not tanner_died:
            teams.add("werewolf")
    else:
        if not dead:
            teams.add("village")
        elif minions and any(d not in minions for d in dead):
            teams.add("werewolf")
    winners = {p: ROLES[final[p]][0] in teams for p in players}
    return {"tally": dict(tally), "dead": dead, "winning_teams": sorted(teams), "winners": winners}


PRICES = {"claude-sonnet-5-5": (2.0, 10.0), "claude-opus-5-5": (4.0, 20.0),
          "claude-haiku-4-5": (1.0, 5.0), "claude-haiku-4-5-20251001": (1.0, 5.0)}
USAGE = re.compile(r"\*\*Tokens:\*\* (\d+) in / (\d+) out(?: \| cache read (\d+) / write (\d+))?")


def cost_summary(game_dir, config):
    """Token and dollar totals from the agent transcripts (cache reads 0.1x, writes 1.25x input price)."""
    t = {"calls": 0, "in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
    for f in game_dir.glob("agent_*.md"):
        for m in USAGE.finditer(f.read_text()):
            t["calls"] += 1
            t["in"] += int(m.group(1)); t["out"] += int(m.group(2))
            t["cache_read"] += int(m.group(3) or 0); t["cache_write"] += int(m.group(4) or 0)
    pin, pout = PRICES.get(config["model"], (0.0, 0.0))
    t["usd"] = round((t["in"] * pin + t["cache_write"] * 1.25 * pin + t["cache_read"] * 0.1 * pin + t["out"] * pout) / 1e6, 4)
    t["usd_without_caching"] = round(((t["in"] + t["cache_write"] + t["cache_read"]) * pin + t["out"] * pout) / 1e6, 4)
    return t


def summary_text(state, players, votes, res):
    lines = ["\n=== Result ===", f"{'player':8}{'start':14}{'final':14}{'voted':7}{'votes in':9}{'won'}"]
    for p in players:
        lines.append(f"{U(p):8}{state['start'][p]:14}{state['cur'][p]:14}"
                     f"{U(votes[p]) if votes[p] else '-':7}{res['tally'].get(p, 0):<9}{'WIN' if res['winners'][p] else 'lose'}"
                     f"{'  (dead)' if p in res['dead'] else ''}")
    lines.append(f"Center start: {state['center_start']}  final: {state['center']}")
    lines.append(f"Dead: {[U(d) for d in res['dead']] or 'nobody'}   Winning teams: {res['winning_teams'] or 'none'}")
    return "\n".join(lines)


# ---------------------------------------------------------------- dry-run bot (no docker, no API)

def dry_bot(ctx, p, phase):
    rng = ctx["rng_bot"]
    players = ctx["config"]["players"]
    others = [x for x in players if x != p]
    if phase == "night":
        role = ctx["state"]["start"][p]
        out = {
            "seer": rng.choice([f"player {U(rng.choice(others))}", f"center {rng.choice(['1 2', '2 3', '1 3'])}"]),
            "robber": f"player {U(rng.choice(others))}",
            "troublemaker": " ".join(U(x) for x in rng.sample(others, 2)),
            "drunk": f"center {rng.randint(1, 3)}",
            "werewolf": rng.choice([f"center {rng.randint(1, 3)}", "none"]),
        }[role]
        (home(p) / "night_action.md").write_text(out)
    elif phase == "discuss":
        if rng.random() < 0.3:
            (home(p) / "pass.md").write_text(json.dumps({"to": rng.choice(others).upper(),
                                                         "visibility": rng.choice(["explicit", "covert"])}))
        else:
            (home(p) / "statement.md").write_text(f"[bot] I am a villager. I suspect {U(rng.choice(others))}.")
    elif phase == "choose":
        (home(p) / "pass.md").write_text(json.dumps({"to": rng.choice(others).upper(),
                                                     "visibility": rng.choice(["explicit", "covert"])}))
    elif phase == "vote":
        (home(p) / "vote.md").write_text(f"player {U(rng.choice(others))}")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, help="override config seed")
    ap.add_argument("--rounds", type=int, help="override discussion_rounds")
    ap.add_argument("--dry-run", action="store_true", help="random bots, no docker, no API calls")
    args = ap.parse_args()

    load_dotenv()
    config = load_config()
    if args.rounds:
        config["discussion_rounds"] = args.rounds
    players = config["players"]
    seed = args.seed if args.seed is not None else config.get("seed")
    if seed is None:
        seed = random.SystemRandom().randrange(2**31)
    state = deal(config, seed)

    reset_dirs(config)
    setup_homes(state, config)
    game_dir = HERE / "games" / (datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + f"_seed{seed}")
    game_dir.mkdir(parents=True)
    ctx = {"config": config, "state": state, "dry": args.dry_run,
           "parsers": make_parsers(players), "rng_bot": random.Random(seed + 1), "n_turns": 0, "pending": {}}

    print(f"Seed {seed}  Game dir: {game_dir}")
    print("Deal (ground truth): " + "  ".join(f"{U(p)}={state['start'][p]}" for p in players)
          + f"  center={state['center']}")
    for p in players:
        print(f"  {U(p)} personality: {state['traits'].get(p, '-')}")

    meta = {"seed": seed, "model": config["model"], "players": players,
            "start": state["start"], "center_start": state["center_start"], "traits": state["traits"],
            "turns_per_round": len(players) + config.get("extra_turns", 3)}
    (game_dir / "game.json").write_text(json.dumps(meta, indent=2))

    if not args.dry_run:
        build_image()
        start_containers(config, game_dir)
    try:
        run_night(ctx, state)
        run_discussion(ctx, state)
        votes = run_vote(ctx, state)
    finally:
        if not args.dry_run:
            stop_containers(config)

    res = resolve(state, players, votes)
    text = summary_text(state, players, votes, res)
    print(text)

    final = dict(meta, final=state["cur"], center_final=state["center"], votes=votes,
                 result=res, events=state["events"])
    (game_dir / "game.json").write_text(json.dumps(final, indent=2))
    (game_dir / "result.txt").write_text(text)
    if not args.dry_run:
        cost = cost_summary(game_dir, config)
        (game_dir / "cost.json").write_text(json.dumps(cost, indent=2))
        print(f"\nCost: ${cost['usd']:.2f} (${cost['usd_without_caching']:.2f} without caching) {cost}")
    shutil.copy(HERE / "table" / "discussion.md", game_dir / "discussion.md")
    shutil.copytree(HERE / "homes", game_dir / "homes")


if __name__ == "__main__":
    main()
