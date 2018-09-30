

from numpy import sin, cos
from kalmanfilter import KalmanFilterCar
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import queue
from cars import Car

class HighWay:

    def __init__(self, length, n_lanes, n_cars, dt):
        self.length = length
        self.n_lanes = n_lanes
        self.n_cars = n_cars
        self.cars = list()
        self.dt = dt
        for i in range(n_cars):
            x_0 = np.random.uniform(0, length)
            p_0 = np.random.normal(30, 5)
            l_0 = n_lanes
            car = Car(id='Car'+str(i), x_0=x_0, p_0=p_0, a_0=0, l_0=l_0, n_lanes=self.n_lanes)
            self.cars.append(car)

    def step(self, dt):
        for car in self.cars:
            car.step(dt)
