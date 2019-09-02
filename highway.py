from .navigation_system import NavigationSystem
from typing import NamedTuple, List


class HighWay(NamedTuple):
    length: float
    lane_number: int


class HighwayNavigationSystem:
    def __init__(
            self,
            highway: HighWay,
            navigation_systems: List[NavigationSystem],
            delta: float
    ):
        self.highway = highway
        self.navigation_systems = navigation_systems
        self.delta = delta

    def is_done(self):
        highway_length = self.highway.length
        car_positions = [navigation_system.car.motion.y for navigation_system in self.navigation_systems]
        return all(car_position > highway_length for car_position in car_positions)

    def step(self, dt):
        for navigation_system in self.navigation_systems:
            navigation_system.step(dt)
