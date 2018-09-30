

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
            v_0=np.random.normal(2, 0.01)
            l_0=n_lanes
            car = KalmanFilterCar(id='Car'+str(i), x_0=x_0, v_0=v_0, a_0=0, l_0=l_0, n_lanes=self.n_lanes)
            self.cars.append(car)

        # for car in self.cars:
        #     for carr in [carr for carr in self.cars if car != carr]:
        #         car.add_neighbor(carr)
        # Figure
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect='equal', autoscale_on=False,
                             xlim=(-1, n_lanes + 1), ylim=(0, length))
        self.ax.grid()

        self.points = [self.ax.plot([], 'o', color = [(i+1)/n_cars, 0, 0])[0] for i in range(n_cars)]
        self.time_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes)

    def step(self, dt):
        for car in self.cars:
            car.step(dt)

    def init(self):
        """initialize animation"""
        for point in self.points:
            point.set_data([], [])
        self.time_text.set_text('')
        return self.points, self.time_text

    def animate(self, i):
        """perform animation step"""
        self.step(self.dt)
        for j in range(self.n_cars):
            self.points[j].set_data(*self.cars[j].x)
        self.time_text.set_text('time = %.1f' % self.cars[0].time_elapsed)
        return self.points, self.time_text
