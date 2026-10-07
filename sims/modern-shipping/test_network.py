import json
from pathlib import Path

import pytest

from network import Network, haversine_nm

CFG = json.loads((Path(__file__).parent / "config.json").read_text())
NET = Network(CFG)


def test_all_ports_connected_both_ways():
    for policy in ("shortest", "no_canals"):
        for a in NET.ports:
            for b in NET.ports:
                if a != b:
                    assert NET.route(a, b, policy), (a, b, policy)


@pytest.mark.parametrize("a,b,policy,real,canal", [
    ("Shanghai", "Rotterdam", "shortest", 10500, "Suez"),
    ("Shanghai", "Rotterdam", "no_canals", 14000, None),
    ("Houston", "Shanghai", "shortest", 10000, "Panama"),
    ("Port Hedland", "Shanghai", "shortest", 3600, None),
    ("New York", "Rotterdam", "shortest", 3400, None),
    ("Los Angeles", "Yokohama", "shortest", 4800, None),
])
def test_distances_close_to_real(a, b, policy, real, canal):
    r = NET.route(a, b, policy)
    assert abs(r.nm / real - 1) < 0.15
    assert (canal in r.canals) if canal else not r.canals


def test_avoiding_canals_is_longer_when_it_matters():
    assert NET.route("Shanghai", "Rotterdam", "no_canals").nm > NET.route("Shanghai", "Rotterdam").nm
    assert NET.route("Houston", "Shanghai", "no_canals").nm > NET.route("Houston", "Shanghai").nm


def test_haversine():
    assert haversine_nm((0, 0), (0, 1)) == pytest.approx(60.04, rel=0.01)   # 1 degree of latitude ≈ 60 nm
