import numpy as np

from typing import NamedTuple, Tuple, Optional


def validate_angle(theta):
    if not - np.pi < theta <= np.pi:
        raise ValueError(
            "theta must be in -pi, pi found {}".format(theta)
        )


class Vector2d:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return "x={}, y={}".format(self.x, self.y)

    def to_cartesian(self):
        return self.x, self.y

    def set_x(self, x: float):
        self.x = x

    def set_y(self, y: float):
        self.y = y

    @classmethod
    def from_polar(cls, distance, theta):
        x = distance * np.cos(theta)
        y = distance * np.sin(theta)
        return cls(x, y)

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

    def subtract(self, vector: "Vector2d"):
        return Vector2d(self.x - vector.x, self.y - vector.y)

    def divide(self, t: float):
        return Vector2d(self.x / t, self.y / t)


def initialize_random_vector_2d(range_x: Tuple[float, float], range_y: Tuple[float, float]) -> Vector2d:
    x_low, x_high = range_x
    y_low, y_high = range_y
    x = np.random.uniform(x_low, x_high)
    y = np.random.uniform(y_low, y_high)
    return Vector2d(x, y)


def initialize_random_motion_descriptor(position_range, speed_range, acceleration_range=(0, 0)):
    position = initialize_random_vector_2d(range_x=(0, 0), range_y=position_range)
    speed = initialize_random_vector_2d(range_x=(0, 0), range_y=speed_range)
    acceleration = initialize_random_vector_2d(range_x=(0, 0), range_y=acceleration_range)

    return MotionDescriptor(
        position,
        speed,
        acceleration,
    )


def project_position_on_closest_inferior_lane(position, lane_width):
    x, y = position.to_cartesian()
    position.set_x(np.floor(x / lane_width) * lane_width)


def initialize_random_motion_descriptor_from_highway_config(highway_config):
    width = highway_config["n_lanes"]
    length = highway_config["length"]
    speed_limit = highway_config["speed_limit"]
    lane_width = highway_config["lane_width"]

    position_range_x = (0, width)
    position_range_y = (0, length)
    speed_range_y = (speed_limit - 20, speed_limit + 15)

    position = initialize_random_vector_2d(range_x=position_range_x, range_y=position_range_y)
    speed = initialize_random_vector_2d(range_x=(0, 0), range_y=speed_range_y)
    acceleration = initialize_random_vector_2d(range_x=(0, 0), range_y=(0, 0))

    project_position_on_closest_inferior_lane(position, lane_width)

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

    def set_cartesian_position(self, *, x: Optional[float] = None, y: Optional[float] = None):
        if x is not None and y is not None:
            self.motion.position.set_x(x)
            self.motion.position.set_y(y)
        elif x is not None:
            self.motion.position.set_x(x)
        elif y is not None:
            self.motion.position.set_y(y)
        else:
            raise ValueError("Cannot set car position coordinates to None.")

    def cartesian_position(self):
        return self.motion.position.to_cartesian()

    def is_in_leftmost_lane(self):
        x, y = self.cartesian_position()
        return x == 0

    def is_in_rightmost_lane(self, n_lanes, lane_width):
        x, y = self.cartesian_position()
        return x == (n_lanes - 1) * lane_width

    def __repr__(self):
        return "Car(id=%s)" % self.car_id
