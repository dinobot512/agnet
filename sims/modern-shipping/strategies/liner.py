"""Liner: a fixed shuttle on one lane for its ship type (config liner_routes), e.g. iron ore
Port Hedland → Shanghai. Loads as much as it can afford at the loading port, sells everything at the
unloading port, and sails back empty. A specialist to compare against the opportunistic greedy captain.
It only loads when the lane pays: expected sale at the unloading port must cover the purchase plus both legs'
costs. Otherwise it waits 2 days at the loading port for prices to recover."""

from __future__ import annotations

from strategies.common import affordable, ensure_fuel, est_buy, est_sell, fuel_price, leg_cost


class LinerPlayer:
    name = "liner"

    def act(self, sim, cid: str):
        v = sim.view(cid)
        lane = sim.cfg["liner_routes"][v.ship_type]
        load, unload, good = lane["load"], lane["unload"], lane["good"]
        mk = v.market(v.port)
        for g, q in v.cargo.items():                         # sell anything sellable that isn't the lane good,
            if g in mk.goods and (g != good or v.port == unload):   # and the lane good at the unloading port
                sim.sell(cid, g, q)
        v = sim.view(cid)
        if v.port == load:
            dest = unload
        elif v.port == unload:
            dest = load
        else:
            dest = load                                      # get back onto the lane
        cost, days, policy = leg_cost(v, v.port, dest, fuel_price(v, v.port))
        need = v.leg(v.port, dest, policy)["fuel"]
        if not ensure_fuel(sim, cid, v, need):
            sim.wait(cid, 1)
            return
        v = sim.view(cid)
        if v.port == load and good in mk.goods:
            budget = v.cash - (cost - need * fuel_price(v, v.port)) - 20       # keep tolls, crew and dues
            qty = affordable(mk, good, budget, v.capacity - sum(v.cargo.values()))
            back = leg_cost(v, unload, load, fuel_price(v, unload))[0]
            margin = est_sell(v.market(unload), good, qty) - est_buy(mk, good, qty) - cost - back
            if qty <= 0 or margin <= 0:
                sim.wait(cid, 2)                             # lane doesn't pay right now
                return
            sim.buy(cid, good, qty)
        result = sim.sail(cid, dest, policy)
        if result.startswith("error"):
            sim.wait(cid, 1)
