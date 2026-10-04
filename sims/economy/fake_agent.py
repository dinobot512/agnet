"""Random but valid player, for testing the engine and runner without API calls (run.py --fake)."""

from __future__ import annotations

import random

from engine import Game


class FakePlayer:
    def __init__(self, game: Game, seed: int | None = None):
        self.game = game
        self.rng = random.Random(seed)

    def act(self, name: str, phase: str) -> dict:
        g, r = self.game, self.rng
        if phase == "board":
            return {"post": f"hello from {name}"} if r.random() < 0.5 else {}
        if phase in ("propose1", "propose2"):
            if r.random() < 0.4:
                return {"propose": {"direction": r.choice(["i_pay", "you_pay"]), "amount": r.randint(1, 2),
                                    "duration": r.randint(1, 5), "time_limit": r.randint(1, 3),
                                    "signing_limit": r.randint(1, g.cfg["limits"]["max_signing_limit"])}}
            return {}
        action: dict = {}
        mine = g.active_contracts(name)
        if mine and r.random() < 0.2:
            action["terminate"] = [r.choice(mine).id]
        options = [p.id for p in g.open_proposals() if g.validate_accept(name, p.id) is None]
        if options and r.random() < 0.6:
            action["accept"] = r.choice(options)
        elif options and phase == "deal1" and r.random() < 0.3:
            action["counteroffer"] = {"proposal_id": r.choice(options), "text": "make it 2/turn?"}
        return action
