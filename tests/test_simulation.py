from ..sim import run_sim_once
from ..constants import HIGHWAY_CONFIG
import unittest


class TestSimulation(unittest.TestCase):
    def test_simulation(self):
        run_sim_once(HIGHWAY_CONFIG)
        self.assertTrue(True)
