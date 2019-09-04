from typing import NamedTuple, List

from .car import Vector2d


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
