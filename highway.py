from .navigation_system import NavigationSystem
from typing import NamedTuple, List


class HighWay(NamedTuple):
    length: float
    lane_number: int
    lane_width: float


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
        car_positions = [navigation_system.car.motion.position.y for navigation_system in self.navigation_systems]
        return all(car_position > highway_length for car_position in car_positions)

    def step(self, dt):
        for navigation_system in self.navigation_systems:
            navigation_system.step(dt, lane_width=self.highway.lane_width, n_lanes=self.highway.lane_number)
