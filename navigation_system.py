from .car import Car

import numpy as np

from typing import List, NamedTuple, Dict, Tuple
from .car import Vector2d
from .message import Message


class DistanceTracker(NamedTuple):
    received_positions: List[Vector2d]
    filtered_distances: List[Vector2d]
    filtered_speed: List[Vector2d]

    def update(self, position: Vector2d, dt: float):
        self.received_positions.append(position)
        # TODO implement filtering
        self.filtered_distances.append(position)
        # TODO implement filtering
        if len(self.received_positions) > 1:
            previous_position = self.received_positions[-1]
            speed = position.subtract(previous_position).divide(dt)
            self.filtered_speed.append(speed)


def build_empty_car_information():
    return DistanceTracker(
        received_positions=[],
        filtered_distances=[],
        filtered_speed=[],
    )


class InformationManager(NamedTuple):
    distance_trackers: Dict[str, DistanceTracker]

    def update_positions(self, received_messages: List[Message], dt: float):
        for message in received_messages:
            source_id = message.source.car_id
            tracker = self.distance_trackers.get(source_id, build_empty_car_information())
            tracker.update(message.compile(), dt)
            self.distance_trackers.update({source_id: tracker})


def build_empty_information_manager() -> InformationManager:
    return InformationManager(distance_trackers={})


class NavigationSystem:

    def __init__(self, car: Car, information_manager: InformationManager):
        self.car = car
        self.information_manager = information_manager
        self.time_elapsed = 0

    def change_lane(self, right: bool, lane_width):
        x, y = self.car.cartesian_position()
        if right:
            self.car.motion.position.set_x(x + lane_width)
        else:
            self.car.motion.position.set_x(x - lane_width)

    def step(self, dt: float, lane_width: float, n_lanes: int):
        """Execute one time step of length dt and update state."""
        _, acceleration_y = self.car.motion.acceleration.to_cartesian()
        _, speed_y = self.car.motion.speed.to_cartesian()
        _, position_y = self.car.cartesian_position()

        self.car.motion.acceleration.set_y(np.random.normal(acceleration_y, 0.1))

        u = np.random.uniform(0, 1)
        if u > 0.99:
            if not self.car.is_in_rightmost_lane(n_lanes, lane_width):
                self.change_lane(right=True, lane_width=lane_width)
                self.car.motion.acceleration.set_y(acceleration_y - 3)
        elif u < 0.01:
            if not self.car.is_in_leftmost_lane():
                self.change_lane(right=False, lane_width=lane_width)
                self.car.motion.acceleration.set_y(acceleration_y + 3)

        speed_y += acceleration_y * dt
        speed_y = max(speed_y, 20)
        self.car.motion.speed.set_y(speed_y)

        position_y += speed_y * dt
        self.car.set_cartesian_position(y=position_y)
        self.time_elapsed += dt
