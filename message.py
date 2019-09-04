from .car import Car, Vector2d
import numpy as np


NORMALIZATION_CONSTANT = 750


def get_random_noise(distance):
    return np.random.normal(0, distance**2 / NORMALIZATION_CONSTANT)


class Message:
    def __init__(self, source: Car, target: Car):
        self.source = source
        self.target = target

    def compile(self):
        difference = self.source.motion.position.subtract(self.target.motion.position)
        distance, theta = difference.to_polar()
        noise = get_random_noise(distance)
        distance += noise
        return Vector2d.from_polar(distance, theta)

    def __repr__(self):
        return "Message(from_id = %s, to_id=%s)" % (
            self.source.car_id, self.target.car_id)