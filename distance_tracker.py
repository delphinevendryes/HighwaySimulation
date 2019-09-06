from typing import List

from .car import Vector2d
from .filtering.filter import FilteredInfo, Filter
import numpy as np


def get_new_observation(received_positions: List[Vector2d], new_position: Vector2d, delta_t: float):
    distance, _ = new_position.to_polar()
    positions = received_positions.copy()

    if len(positions) > 0:
        previous_position = positions.pop()
        previous_distance, _ = previous_position.to_polar()
        speed = get_approx_time_derivative(distance, previous_distance, delta_t)

        if len(positions) > 1:
            pre_previous_position = positions.pop()
            pre_previous_distance, _ = pre_previous_position.to_polar()
            previous_speed = get_approx_time_derivative(previous_distance, pre_previous_distance, delta_t)
            acceleration = get_approx_time_derivative(speed, previous_speed, delta_t)
        else:
            acceleration = 0

    else:
        speed = 0
        acceleration = 0

    return np.array([distance, speed, acceleration])


def get_approx_time_derivative(distance, previous_distance, delta_t):
    return (distance - previous_distance) / delta_t


class DistanceTracker:
    def __init__(self, distance_filter: [Filter, None]):
        self.received_positions = []
        self.filtered_info_list = []
        self.distance_filter = distance_filter

    def update(self, position: Vector2d, dt: float):
        self.received_positions.append(position.copy())

        if self.distance_filter is not None:
            observation = get_new_observation(self.received_positions, position, dt)
            if len(self.filtered_info_list) > 0:
                last_filtered_info = self.filtered_info_list.copy().pop()
            else:
                last_filtered_info = None
            filtered_info = self.distance_filter.do_recursion_step(new_observation=observation, filtered_info=last_filtered_info)
            self.filtered_info_list.append(filtered_info)
