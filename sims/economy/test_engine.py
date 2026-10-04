import copy
import json
from pathlib import Path

import pytest

from engine import Game
from fake_agent import FakePlayer
from engine import PHASES

BASE = json.loads((Path(__file__).parent / "config.json").read_text())


def make(earners=("a", "b"), agents="abcdefghij", **over):
    cfg = copy.deepcopy(BASE)
    cfg.update(agents=list(agents), earners=list(earners), **over)
    return Game(cfg, seed=0)


def prop(direction="i_pay", amount=1, duration=3, time_limit=2, signing_limit=1):
    return {"direction": direction, "amount": amount, "duration": duration,
            "time_limit": time_limit, "signing_limit": signing_limit}


def sign(g, proposer, signer, phase_pair=("propose1", "deal1"), **p):
    g.apply_phase(phase_pair[0], {proposer: {"propose": prop(**p)}})
    pid = list(g.proposals)[-1]
    g.apply_phase(phase_pair[1], {signer: {"accept": pid}})
    return [c for c in g.contracts.values() if c.proposal_id == pid]


def test_basic_payment_and_score():
    g = make()
    (c,) = sign(g, "a", "c", amount=2)
    assert (c.payer, c.payee) == ("a", "c")
    g.settle()
    # a: 3 + 4 income - 2 - 1 upkeep; c: 3 + 2 - 1
    assert g.agents["a"].balance == 4 and g.agents["c"].balance == 4
    assert g.agents["a"].score == 2 and c.remaining == 2


def test_you_pay_direction():
    g = make()
    (c,) = sign(g, "c", "d", direction="you_pay", amount=1)
    assert (c.payer, c.payee) == ("d", "c")


def test_earner_to_earner_does_not_score():
    g = make()
    sign(g, "a", "b", amount=1)
    g.settle()
    assert g.agents["a"].score == 0


def test_no_income_agent_dies_after_start_balance_runs_out():
    g = make()
    for _ in range(3):
        g.settle()
    assert g.agents["c"].alive and g.agents["c"].balance == 0
    g.settle()
    assert not g.agents["c"].alive and g.agents["c"].eliminated_turn == 4


def test_insolvent_payer_eliminated_and_balance_destroyed():
    g = make()
    (c,) = sign(g, "c", "d", amount=5)        # c (non-earner, 3 credits) promises 5/turn
    g.settle()
    assert not g.agents["c"].alive
    assert g.destroyed == 3
    assert c.status == "voided"
    assert g.agents["d"].balance == 2         # got nothing, paid upkeep


def test_cascade():
    g = make()
    # c pays d 3/turn (c can't afford it); d relies on that to pay e 4/turn.
    sign(g, "c", "d", amount=3)
    sign(g, "d", "e", phase_pair=("propose2", "deal2"), amount=4)
    s = g.settle()
    # c: 3 < 3+1 -> out. Then d: 3 + 0 < 4 + 1 -> out. e survives.
    assert set(s["eliminated"]) == {"c", "d"}
    assert g.agents["e"].alive and g.agents["e"].balance == 2


def test_incoming_from_solvent_payer_covers_outgoing():
    g = make()
    sign(g, "a", "c", amount=3)                     # earner pays c 3
    sign(g, "c", "d", phase_pair=("propose2", "deal2"), amount=5)   # c pays d 5: 3 + 3 >= 5 + 1
    s = g.settle()
    assert s["eliminated"] == []
    assert g.agents["c"].balance == 0 and g.agents["d"].balance == 7


def test_tie_break_respects_signing_limit():
    g = make()
    g.apply_phase("propose1", {"a": {"propose": prop(signing_limit=2)}})
    g.apply_phase("deal1", {n: {"accept": "P1"} for n in "cdefg"})
    assert len(g.proposals["P1"].signers) == 2
    assert not g.proposals["P1"].open
    failed = [e for e in g.events if e["event"] == "accept_failed"]
    assert len(failed) == 3 and all("slot filled" in e["reason"] for e in failed)


def test_cannot_accept_own_or_twice():
    g = make()
    g.apply_phase("propose1", {"a": {"propose": prop(signing_limit=3, time_limit=2)}})
    assert g.validate_accept("a", "P1")
    g.apply_phase("deal1", {"c": {"accept": "P1"}})
    assert g.validate_accept("c", "P1")


def test_time_limit_expiry():
    g = make()
    g.apply_phase("propose1", {"a": {"propose": prop(time_limit=1)}})
    g.apply_phase("deal1", {})
    assert not g.proposals["P1"].open
    g.apply_phase("propose2", {"a": {"propose": prop(time_limit=2)}})
    g.apply_phase("deal2", {})
    g.settle()
    assert g.proposals["P2"].open and g.proposals["P2"].time_limit == 1


def test_mutual_termination_needs_both_same_turn():
    g = make()
    (c,) = sign(g, "a", "c")
    g.apply_phase("deal2", {"a": {"terminate": [c.id]}})
    assert c.status == "active"
    g.settle()
    g.apply_phase("deal1", {"c": {"terminate": [c.id]}})
    assert c.status == "active"                # a's request was last turn
    g.apply_phase("deal2", {"a": {"terminate": [c.id]}})
    assert c.status == "terminated"


def test_contract_completes():
    g = make()
    (c,) = sign(g, "a", "c", duration=2)
    g.settle()
    g.settle()
    assert c.status == "completed" and g.agents["a"].score == 2


def test_validation_limits():
    g = make()
    assert g.validate_post("c", "   ")
    assert g.validate_post("c", "x" * 80) is None          # too long is cut, not rejected
    assert g.validate_proposal("c", prop(amount=0))
    assert g.validate_proposal("c", prop(duration=11))
    assert g.validate_proposal("c", prop(signing_limit=6))
    assert g.validate_proposal("c", prop(direction="gift"))
    assert g.validate_proposal("c", prop()) is None


def test_view_hides_secrets_from_non_earners():
    g = make()
    g.apply_phase("board", {"c": {"post": "hi all"}})
    v = g.view_for("d", "propose1")
    assert "hi all" in v and "(c)" not in v           # board is anonymous
    assert "score" not in v.lower() and "income" not in v.lower()
    assert "score" in g.view_for("a", "propose1").lower()


@pytest.mark.parametrize("seed", range(5))
def test_fake_game_conserves_credits(seed):
    cfg = copy.deepcopy(BASE)
    g = Game(cfg, seed=seed)
    player = FakePlayer(g, seed=seed)
    while not g.is_over():
        for phase in PHASES:
            g.apply_phase(phase, {n: player.act(n, phase) for n in g.alive()})
        g.settle()
        r = g.results()["credits"]
        assert r["final"] == r["start"] + r["income"] - r["upkeep"] - r["destroyed"]
        assert all(a.balance >= 0 for a in g.agents.values())


def test_worst_case_exposure_in_view():
    g = make()
    g.apply_phase("propose1", {"c": {"propose": prop(amount=2, signing_limit=3)}})
    v = g.view_for("c", "deal1")
    # c: balance 3, owes upkeep 1 now; worst case 1 + 2*3 = 7 > 3
    assert "you would owe 7 this turn against 3 available" in v and "YOU COULD BE ELIMINATED" in v
    assert "YOU COULD BE ELIMINATED" not in g.view_for("d", "deal1")


def test_events_stream_to_sink_with_phase():
    seen = []
    cfg = copy.deepcopy(BASE)
    cfg["earners"] = ["a", "b"]
    g = Game(cfg, seed=0, event_sink=seen.append)
    g.apply_phase("board", {"c": {"post": "hi"}})
    g.settle()
    kinds = {e["event"] for e in seen}
    assert {"setup", "action", "board", "income", "upkeep", "notice", "settled"} <= kinds
    assert seen == g.events
    assert all("phase" in e for e in seen)


def test_long_posts_are_cut_and_logged():
    g = make()
    g.apply_phase("board", {"c": {"post": "y" * 70}})
    assert g.board[-1]["text"] == "y" * 50
    (t,) = [e for e in g.events if e["event"] == "truncated"]
    assert t["original"] == "y" * 70 and t["where"] == "board"


def test_config_signing_limit_is_one():
    g = make()
    assert g.validate_proposal("c", prop(signing_limit=2))
    assert g.validate_proposal("c", prop(signing_limit=1)) is None


def test_new_contract_cap_counts_signing_and_being_signed():
    g = make()
    g.apply_phase("propose1", {"a": {"propose": prop()}, "b": {"propose": prop(time_limit=4)}})
    g.apply_phase("deal1", {"c": {"accept": "P1"}})            # a: 1 (being signed)
    g.apply_phase("propose2", {"a": {"propose": prop()}})
    g.apply_phase("deal2", {"d": {"accept": "P3"}})            # a: 2
    assert g.new_contracts["a"] == 2
    assert "maximum" in g.validate_accept("a", "P2")          # a can't sign more
    g.apply_phase("propose2", {"a": {"propose": prop()}})      # P4
    g.apply_phase("deal2", {"e": {"accept": "P4"}})            # nobody can sign a's proposals either
    (fail,) = [e for e in g.events if e["event"] == "accept_failed"]
    assert fail["agent"] == "e" and "maximum" in fail["reason"]
    g.settle()
    assert g.new_contracts["a"] == 0 and g.validate_accept("a", "P2") is None


def test_proposals_described_from_reader_side():
    g = make()
    g.apply_phase("propose1", {"c": {"propose": prop(direction="you_pay")}, "d": {"propose": prop()}})
    v = g.view_for("e", "deal1")
    assert "P1 by c: if you sign, YOU PAY c" in v and "P2 by d: if you sign, d PAYS YOU" in v
    assert "YOUR offer: each signer pays you" in g.view_for("c", "deal1")


def test_projection_runway():
    g = make()
    assert g.projection("c") == (-1, 4)            # 3 credits, upkeep 1: 0 left after turn 3, eliminated in turn 4
    assert g.projection("a")[1] is None            # earner with no contracts survives
    sign(g, "a", "c", amount=5, duration=10)       # a: +4 income - 5 - 1 = -2/turn from 3 credits
    net, dies = g.projection("a")
    assert net == -2 and dies == 2
    assert g.projection("c") == (4, None)
    assert "ELIMINATED at the end of turn 2" in g.view_for("a", "deal2")
