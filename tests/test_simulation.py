from ..sim import run_sim_once
import unittest

HIGHWAY_CONFIG = {
    "n_lanes": 2,
    "length": 500,
    "speed_limit": 5,
    "n_cars": 20,
    "delta": 1./30,
    "lane_width": 1,
}


class TestSimulation(unittest.TestCase):
    def test_simulation(self):
        run_sim_once(HIGHWAY_CONFIG)
        self.assertTrue(True)
