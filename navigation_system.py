from highway_simulation.distance_tracker import DistanceTracker
from .car import Car, CarId

import numpy as np

from typing import List, NamedTuple, Dict
from .message import Message
from .filtering.kalman_filter import KalmanFilter
from .constants import MIN_SPEED, ACCELERATION_STD, ACCELERATION_CHANGE_WITH_LANE_CHANGE


def build_kalman_distance_tracker():
    """Build a distance tracker that uses Kalman filtering."""
    sigma_w = np.identity(3) * 0.1
    sigma_v = np.identity(3) * 1

    psi = np.identity(3)
    phi = np.identity(3)
    kalman_filter = KalmanFilter(phi, psi, sigma_v, sigma_w)
    return DistanceTracker(distance_filter=kalman_filter)


class InformationManager(NamedTuple):
    """An information manager holds on to a dictionary that maps all car ids on the road to a distance tracker."""
    distance_trackers: Dict[CarId, DistanceTracker]

    def update_positions(self, received_messages: List[Message], dt: float):
        """Update distance trackers according to received messages."""
        for message in received_messages:
            source_id = message.source.car_id
            tracker = self.distance_trackers.get(source_id, build_kalman_distance_tracker())
            tracker.update(message.compile(), dt)
            self.distance_trackers.update({source_id: tracker})


def build_empty_information_manager() -> InformationManager:
    """Build empty information manager."""
    return InformationManager(distance_trackers={})


class NavigationSystem:
    def __init__(self, car: Car, information_manager: InformationManager):
        """A navigation system holds on to a car and the meta information that helps a car navigate."""
        self.car = car
        self.information_manager = information_manager
        self.time_elapsed = 0

    def change_lane(self, right: bool, lane_width: float):
        x, y = self.car.get_cartesian_position()
        if right:
            self.car.set_cartesian_position(x=x + lane_width)
        else:
            self.car.set_cartesian_position(x=x - lane_width)

    def step(self, delta_t: float, lane_width: float, n_lanes: int):
        """Execute one time step of length dt and update state."""
        _, acceleration_y = self.car.motion.acceleration.to_cartesian()
        _, speed_y = self.car.motion.speed.to_cartesian()
        _, position_y = self.car.get_cartesian_position()

        self.car.motion.acceleration.set_y(np.random.normal(acceleration_y, ACCELERATION_STD))

        u = np.random.uniform(0, 1)
        if u > 0.99:
            if not self.car.is_in_rightmost_lane(n_lanes, lane_width):
                self.change_lane(right=True, lane_width=lane_width)
                self.car.motion.acceleration.set_y(acceleration_y - ACCELERATION_CHANGE_WITH_LANE_CHANGE)
        elif u < 0.01:
            if not self.car.is_in_leftmost_lane():
                self.change_lane(right=False, lane_width=lane_width)
                self.car.motion.acceleration.set_y(acceleration_y + ACCELERATION_CHANGE_WITH_LANE_CHANGE)

        speed_y += acceleration_y * delta_t
        speed_y = max(speed_y, MIN_SPEED)
        self.car.motion.speed.set_y(speed_y)

        position_y += speed_y * delta_t
        self.car.set_cartesian_position(y=position_y)
        self.time_elapsed += delta_t
