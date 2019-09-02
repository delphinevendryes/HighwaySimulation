import numpy as np

from typing import NamedTuple, Tuple


def validate_angle(theta):
    if not - np.pi < theta <= np.pi:
        raise ValueError(
            "theta must be in -pi, pi found {}".format(theta)
        )


class Vector2d(NamedTuple):
    x: float
    y: float

    def is_in_quadrant_2(self):
        return (self.x < 0) & (self.y >= 0)

    def is_in_quadrant_3(self):
        return (self.x < 0) & (self.y < 0)

    def get_distance_to_origin(self):
        return np.sqrt(self.x ** 2 + self.y ** 2)

    def is_on_y_axis(self):
        return self.x == 0

    def get_angle(self):
        theta = 0
        if self.is_on_y_axis():
            if self.y > 0:
                theta = np.pi / 2
            elif self.y < 0:
                theta = - np.pi / 2
            elif self.y == 0:
                theta = 0
        else:
            theta = np.arctan(self.y / self.x)
            if self.is_in_quadrant_2():
                theta += np.pi
            if self.is_in_quadrant_3():
                theta -= np.pi

        validate_angle(theta)

        return theta

    def to_polar(self):
        r = self.get_distance_to_origin()
        theta = self.get_angle()
        return r, theta

    def to_cartesian(self):
        return self.x, self.y

    def subtract(self, vector: "Vector2d"):
        self.x -= vector.x
        self.y -= vector.y

    def divide(self, t: float):
        self.x /= t
        self.y /= t


def initialize_random_vector_2d(range_x: Tuple[float, float], range_y: Tuple[float, float]) -> Vector2d:
    x_low, x_high = range_x
    y_low, y_high = range_y
    x = np.random.uniform(x_low, x_high)
    y = np.random.uniform(y_low, y_high)
    return Vector2d(x, y)


def initialize_random_motion_descriptor(position_range=0, speed_range=0, acceleration_range=0):
    position = initialize_random_vector_2d(range_x=(0,0), range_y=(0,0))
    speed = initialize_random_vector_2d(range_x=(0,0), range_y=(1,1))
    acceleration = initialize_random_vector_2d(range_x=(0,0), range_y=(0,0))

    return MotionDescriptor(
        position,
        speed,
        acceleration,
    )


class MotionDescriptor(NamedTuple):
    position: Vector2d
    speed: Vector2d
    acceleration: Vector2d


class Car(NamedTuple):
    """Car Class."""
    car_id: str
    motion: MotionDescriptor

    def __repr__(self):
        return "Car(id=%s)" % self.car_id
