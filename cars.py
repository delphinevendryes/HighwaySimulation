import numpy as np
from carinfo import CarInfo

class Car:
    """Car Class
    """
    def __init__(self, id, x_0, p_0, a_0, l_0, n_lanes):
        self.id = id
        self.x, self.p, self.a, self.lane = x_0, p_0, a_0, l_0
        self.time_elapsed = 0
        self.n_lanes = n_lanes
        # Storing
        self.info = CarInfo()

    def __repr__(self):
        return "Car(id = %s, x=%f, p=%f, a =%f, l=%d)" % (
            self.id, self.x, self.p, self.a, self.lane)

    def init(self):
        pass

    def update_positions(self, messages):
        for m in messages:
            # if m.from_id not in self.rec_distances:
            #     self.info.received_positions[m.from_id] = []
            self.info.received_positions[m.from_id] = [m.r, m.theta]

    def filter_distances(self):
        self.info.saved_filtered_distances = self.info.filtered_distances.copy()
        for id in self.info.received_positions:
            if len(self.info.received_positions[id]) > 0:
                self.info.filtered_distances[id] = [self.info.received_positions[id][0]]

    def update_speed(self, dt):
        info = self.info
        for cid in info.filtered_distances:
            if cid in info.saved_filtered_distances:
                info.filtered_speed[cid] = (info.filtered_distances[cid][0] - info.saved_filtered_distances[cid][0]) / dt

    def position(self):
        return self.lane, self.x

    def change_lane_left(self):
        if self.lane > 0:
            self.lane -= 1

    def change_lane_right(self):
        if self.lane < self.n_lanes:
            self.lane += 1

    def step(self, dt):
        """execute one time step of length dt and update state"""
        self.a = np.random.normal(self.a, 0.1)

        for cid in self.info.filtered_distances:
            if (self.info.received_positions[cid][1] == 0) & (self.info.filtered_distances[cid][0] < 20) & (cid in self.info.filtered_speed):
                if np.random.uniform(0, 1) < 0.9:
                    self.a = (self.info.filtered_speed[cid] - self.p) * 0.1
                else:
                    self.change_lane_left()
                    self.a += 3

        self.p += self.a * dt
        self.p = max(self.p, 20)
        self.x += self.p * dt
        self.time_elapsed += dt