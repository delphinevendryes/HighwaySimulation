"""
General Numerical Solver for the 1D Time-Dependent Schrodinger's equation.

adapted from code at http://matplotlib.sourceforge.net/examples/animation/double_pendulum_animated.py

Double pendulum formula translated from the C code at
http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import queue

class Car:
    """Double Pendulum Class

    init_state is [theta1, omega1, theta2, omega2] in degrees,
    where theta1, omega1 is the angular position and velocity of the first
    pendulum arm, and theta2, omega2 is that of the second pendulum arm
    """
    def __init__(self, id, x_0, v_0, a_0, l_0, n_lanes):
        self.id = id
        self.x = x_0
        self.p = v_0
        self.a = a_0
        self.lane = l_0
        self.time_elapsed = 0
        self.n_lanes = n_lanes
        self.rec_distances = dict()
        self.filt_distances = dict()
        self.bel_speed = dict()

    def __repr__(self):
        return "Car(id = %s, x=%d, p=%d, a =%d, l=%s)" % (
            self.id, self.x, self.p, self.a, self.lane)

    def init(self):
        pass

    def update_distances(self, messages):
        for m in messages:
            if m.from_id not in self.rec_distances:
                self.rec_distances[m.from_id] = []
            else: self.rec_distances[m.from_id].append(m.x_meas)

    def filter_distances(self):
        for id in self.rec_distances:
            if len(self.rec_distances[id]) > 0:
                self.filt_distances[id] = self.rec_distances[id][-1]

    def update_bel_speed(self, dt):
        # for car in self.rec_distances:
        #    self.bel_speeds[car] = (self.prev_bel_distances[car] - self.rec_distances[car]) / dt
        pass

    def position(self):
        return self.lane, self.x

    def change_lane(self):
        if (self.lane < self.n_lanes) & (self.lane > 0):
            self.lane += 2 * np.random.binomial(1, 0.5, 1) - 1
        elif self.lane < self.n_lanes:
            self.lane += 1
        elif self.lane > 0:
            self.lane += -1

    def step(self, dt):
        """execute one time step of length dt and update state"""
        self.a = np.random.normal(self.a, 0.1)
        if self.p + self.a * dt < 0.1:
             self.a = - self.p / dt + 0.1 / dt
        self.p += self.a * dt

        self.p = max(self.p, 1)
        self.p = min(self.p, 3)

        self.x += self.p * dt
        if np.random.uniform(0, 1) < 0.01:
            self.change_lane()
        self.time_elapsed += dt