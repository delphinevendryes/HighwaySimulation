from .car import Car
import numpy as np
from .navigation_system import DistanceTracker


NORMALIZATION_CONSTANT = 750


class Message:
    def __init__(self, source: Car, target: Car):
        self.source = source
        self.target = target

    def compile(self):
        difference = self.source.motion.position.subtract(self.target.motion.position)
        distance, theta = difference.to_polar()
        distance += np.random.normal(0, distance**2 / NORMALIZATION_CONSTANT)
        return distance, theta

    def __repr__(self):
        return "Message(from_id = %s, to_id=%s)" % (
            self.source.car_id, self.target.car_id)
