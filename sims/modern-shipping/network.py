"""The sea-lane network: ports + waypoints joined by hand-listed lanes (none crosses land).

Lane length is the great-circle distance in nautical miles. Routes are shortest paths (Dijkstra), either
the plain shortest or one that avoids the toll canals (Suez, Panama). Everything here is pure geometry.
"""

from __future__ import annotations

import heapq
import math
from dataclasses import dataclass

EARTH_NM = 3440.065          # Earth's mean radius in nautical miles

POLICIES = ("shortest", "no_canals")


def haversine_nm(a: tuple[float, float], b: tuple[float, float]) -> float:
    lon1, lat1, lon2, lat2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * EARTH_NM * math.asin(math.sqrt(h))


@dataclass(frozen=True)
class Route:
    path: tuple[str, ...]       # node names, port to port
    nm: float
    canals: tuple[str, ...]     # canal names crossed, in order

    def days(self, knots: float) -> int:
        return max(1, math.ceil(self.nm / (knots * 24)))


class Network:
    def __init__(self, cfg: dict):
        self.coords: dict[str, tuple[float, float]] = {p: tuple(v["lonlat"]) for p, v in cfg["ports"].items()}
        self.coords.update({w: tuple(v) for w, v in cfg["waypoints"].items()})
        self.ports = list(cfg["ports"])
        self.canal_of_edge: dict[frozenset, str] = {frozenset(c["edge"]): name for name, c in cfg["canals"].items()}
        self.adj: dict[str, list[tuple[str, float]]] = {n: [] for n in self.coords}
        for a, b in cfg["lanes"]:
            nm = haversine_nm(self.coords[a], self.coords[b])
            self.adj[a].append((b, nm))
            self.adj[b].append((a, nm))
        self._routes: dict[tuple[str, str, str], Route] = {}
        for policy in POLICIES:
            for src in self.ports:
                self._dijkstra(src, policy)

    def _dijkstra(self, src: str, policy: str):
        blocked = set(self.canal_of_edge) if policy == "no_canals" else set()
        dist, prev, heap = {src: 0.0}, {}, [(0.0, src)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in self.adj[u]:
                if frozenset((u, v)) in blocked:
                    continue
                if d + w < dist.get(v, float("inf")):
                    dist[v], prev[v] = d + w, u
                    heapq.heappush(heap, (d + w, v))
        for dst in self.ports:
            if dst == src or dst not in dist:
                continue
            path = [dst]
            while path[-1] != src:
                path.append(prev[path[-1]])
            path.reverse()
            canals = tuple(self.canal_of_edge[frozenset(e)] for e in zip(path, path[1:])
                           if frozenset(e) in self.canal_of_edge)
            self._routes[(src, dst, policy)] = Route(tuple(path), dist[dst], canals)

    def route(self, src: str, dst: str, policy: str = "shortest") -> Route | None:
        return self._routes.get((src, dst, policy))

    def segments(self, route: Route) -> list[tuple[tuple[float, float], tuple[float, float], float]]:
        """[(from lonlat, to lonlat, nm)] along a route, for drawing and interpolation."""
        return [(self.coords[a], self.coords[b], haversine_nm(self.coords[a], self.coords[b]))
                for a, b in zip(route.path, route.path[1:])]
