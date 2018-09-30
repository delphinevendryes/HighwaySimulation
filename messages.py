from numpy import random
from util import highway_location_to_polar

class Message:
    def __init__(self, from_id, to_id, x, delta_lane):
        self.from_id = from_id
        self.to_id = to_id
        r, theta = highway_location_to_polar(x, delta_lane)
        self.r = r + random.normal(0, r**2 / 750)
        self.theta = theta

    def __repr__(self):
        return "Message(from_id = %s, to_id=%s, r=%f, theta=%f)" % (
            self.from_id, self.to_id, self.r, self.theta)