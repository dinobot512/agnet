"""Greedy: perfect-information arbitrage, one or two legs ahead.

At each port it
  1. sells cargo here if this pays at least ~95% of the best net price elsewhere,
  2. scores every destination by value per day:
       (cargo it holds sold there + the best good to buy here and sell there − voyage cost) / (days + 1)
     voyage cost = fuel at today's local fuel price + canal tolls + crew days + harbour dues, taking the
     cheaper of the canal and no-canal route;
  3. if that finds nothing, it considers repositioning empty: sail to port X and do X's best trade from
     there (cost of both legs, divided by both legs' days);
  4. refuels for the chosen leg (filling up when fuel here is cheap), buys, and sails. It waits only if
     every option loses more per day than waiting does (the crew's daily wage).

All prices come from the View (live markets everywhere). Price impact is estimated in closed form.
"""

from __future__ import annotations

import statistics

from strategies.common import affordable, ensure_fuel, est_buy, est_sell, fuel_price, leg_cost


class GreedyPlayer:
    name = "greedy"

    def __init__(self, sell_ratio: float = 0.95, reserve: float = 30.0):
        self.sell_ratio = sell_ratio
        self.reserve = reserve
        self._cache: dict = {}            # (day, ship_type) -> {port: (value, days, dest, good)}

    # ---------- the best trade starting from each port (shared by captains of one ship type, per day) ----------

    def _best_from(self, view) -> dict:
        key = (view.day, view.ship_type)
        if key in self._cache:
            return self._cache[key]
        self._cache = {k: v for k, v in self._cache.items() if k[0] == view.day}
        out = {}
        for x in view.ports:
            mx = view.market(x)
            fx = fuel_price(view, x)
            best = (0.0, 0, None, None)
            for g in view.carries:
                if g not in mx.goods or mx.stock[g] < 1:
                    continue
                qty = min(view.capacity, int(mx.stock[g]))
                buy = est_buy(mx, g, qty)
                for y in view.ports:
                    if y == x or g not in view.market(y).goods:
                        continue
                    cost, days, _ = leg_cost(view, x, y, fx)
                    value = est_sell(view.market(y), g, qty) - buy - cost
                    if value / (days + 1) > best[0] / (best[1] + 1 if best[2] else 1):
                        best = (value, days, y, g)
            out[x] = best
        self._cache[key] = out
        return out

    # ---------- decision ----------

    def act(self, sim, cid: str):
        v = sim.view(cid)
        here = v.port
        mk = v.market(here)
        fp_here = fuel_price(v, here)

        # 1. sell what pays well here
        for good, qty in v.cargo.items():
            if good not in mk.goods:
                continue
            here_value = est_sell(mk, good, qty)
            elsewhere = max((est_sell(v.market(p), good, qty) - leg_cost(v, here, p, fp_here)[0]
                             for p in v.ports if p != here), default=0.0)
            if here_value >= self.sell_ratio * elsewhere:
                sim.sell(cid, good, qty)
        v = sim.view(cid)

        # 2. direct options: carry what we hold + the best purchase here, to each destination
        room = v.capacity - sum(v.cargo.values())
        best = None                                   # (rate, dest, policy, good, qty)
        for dest in v.ports:
            if dest == here:
                continue
            cost, days, policy = leg_cost(v, here, dest, fp_here)
            md = v.market(dest)
            carried = sum(est_sell(md, g, q) for g, q in v.cargo.items())
            budget = v.cash - cost - self.reserve
            pick = (0.0, None, 0)
            for g in v.carries:
                if g not in mk.goods or g not in md.goods or room <= 0 or budget <= 0:
                    continue
                qty = affordable(mk, g, budget, room)
                if qty > 0:
                    gain = est_sell(md, g, qty) - est_buy(mk, g, qty)
                    if gain > pick[0]:
                        pick = (gain, g, qty)
            rate = (carried + pick[0] - cost) / (days + 1)
            if best is None or rate > best[0]:
                best = (rate, dest, policy, pick[1], pick[2])

        # Waiting isn't free: the crew is paid every day. A voyage losing less than that per day beats waiting.
        idle_cost = v.spec["crew"]

        # 3. reposition empty toward the best trade starting elsewhere
        if (best is None or best[0] <= 0) and not v.cargo:
            for x, (value, days2, y, g) in self._best_from(v).items():
                if x == here or not y:
                    continue
                cost1, days1, policy = leg_cost(v, here, x, fp_here)
                rate = (value - cost1) / (days1 + days2 + 1)
                if best is None or rate > best[0]:
                    best = (rate, x, policy, None, 0)

        if best is None or best[0] <= -idle_cost:
            sim.wait(cid, 2)
            return
        _, dest, policy, good, qty = best

        # 4. fuel, buy, sail
        need = v.leg(here, dest, policy)["fuel"] * 1.1
        prices = [fuel_price(v, p) for p in v.ports]
        cheap = fp_here < 0.9 * statistics.median(prices)
        if not ensure_fuel(sim, cid, v, min(need, v.tank), top_up=cheap and v.cash > 200):
            ensure_fuel(sim, cid, sim.view(cid), min(need, v.tank))
        if good:
            v = sim.view(cid)
            qty = min(qty, affordable(mk, good, v.cash - leg_cost(v, here, dest, fp_here)[0] - self.reserve,
                                      v.capacity - sum(v.cargo.values())))
            if qty > 0:
                sim.buy(cid, good, qty)
        if sim.sail(cid, dest, policy).startswith("error"):
            sim.wait(cid, 1)
