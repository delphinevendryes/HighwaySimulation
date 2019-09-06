from typing import NamedTuple, Dict
from .car import CarId, MotionDescriptor
from .navigation_system import NavigationSystem
from .highway import HighwayNavigationSystem


class Round(NamedTuple):
    round_info: Dict[CarId, MotionDescriptor]


def get_single_navigation_system_round_info(navigation_system: NavigationSystem):
    car_id = navigation_system.car.car_id
    motion_descriptor = navigation_system.car.motion
    return car_id, motion_descriptor


def get_round_from_highway_navigation_systems(highway_navigation_system: HighwayNavigationSystem):
    navigation_systems = highway_navigation_system.navigation_systems
    round_info = {}
    for navigation_system in navigation_systems:
        car_id, motion_descriptor = get_single_navigation_system_round_info(navigation_system)
        round_info.update({car_id: motion_descriptor})
    return Round(round_info=round_info)


class History:
    def __init__(self):
        """The history keeps track of true positions."""
        self._rounds = []

    def update(self, new_round: Round):
        self._rounds.append(new_round)
