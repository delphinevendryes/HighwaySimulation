from .car import Car, Vector2d
from .constants import NOISE_NORMALIZATION_CONSTANT
import numpy as np


def get_random_noise(distance):
    return np.random.normal(0, distance**2 / NOISE_NORMALIZATION_CONSTANT)


class Message:
    def __init__(self, source: Car, target: Car):
        """A message is broadcast between a source and a target car."""
        self.source = source
        self.target = target

    def compile(self) -> Vector2d:
        """A message compiles to a noisy vector."""
        difference = self.source.motion.position.subtract(self.target.motion.position)
        distance, theta = difference.to_polar()
        noise = get_random_noise(distance)
        distance += noise
        return Vector2d.from_polar(distance, theta)

    def __repr__(self) -> str:
        """For debugging purposes."""
        return "Message(from_id = %s, to_id=%s)" % (
            self.source.car_id, self.target.car_id)
