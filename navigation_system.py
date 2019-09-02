from .car import Car

import numpy as np

from typing import List, NamedTuple, Dict, Tuple
from .car import Vector2d
from .message import Message


LANE_WIDTH = 1


def build_empty_car_information():
    return DistanceTracker(
        received_positions=[],
        filtered_distances=[],
        filtered_speed=[],
    )


class DistanceTracker(NamedTuple):
    received_positions: List[Vector2d]
    filtered_distances: List[Vector2d]
    filtered_speed: List[Vector2d]

    def update(self, position: Vector2d, dt: float):
        previous_position = self.received_positions[-1]
        self.received_positions.append(position)
        # TODO implement filtering
        self.filtered_distances.append(position)
        # TODO implement filtering
        speed = position.subtract(previous_position).divide(dt)
        self.filtered_speed.append(speed)


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

    def change_lane(self, right: bool):
        self.car.motion.position.x += right * LANE_WIDTH

    def step(self, dt):
        """execute one time step of length dt and update state"""
        acceleration, _ = self.car.motion.position.acceleration
        self.car.motion.position.acceleration = np.random.normal(acceleration, 0.1), 0

        if np.random.uniform(0, 1) < 0.9:
            pass
        else:
            self.change_lane(right=False)
            self.car.motion.position.acceleration += 3

        self.car.motion.speed += self.car.motion.acceleration.x * dt
        self.car.motion.speed = max(self.car.motion.speed.x, 20)
        self.car.motion.position += self.car.motion.speed * dt
        self.time_elapsed += dt
