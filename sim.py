from highway import HighWay
from messages import Message
import matplotlib.pyplot as plt
import numpy as np
from util import highway_location_to_polar
import scipy.integrate as integrate
import matplotlib.animation as animation
import queue
import logging
from time import time


# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
# ani.save('double_pendulum.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

def run_sim_once(n_cars=20, n_lanes=4, length=200, dt=1./30):

    def init_visualization():
        fig = plt.figure()
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1, n_lanes + 1), ylim=(0, length))
        ax.grid()
        ax.set_xlabel('Lanes')
        ax.set_ylabel('Highway stretch (m)')
        ax.set_xticks(np.arange(n_lanes+1))
        points = [ax.plot([], 'o', color=[(i + 1) / n_cars, 0, 0])[0] for i in range(n_cars)]
        time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
        return fig, ax, points, time_text

    def animate():
        """perform animation step"""
        for j in range(highway.n_cars):
            points[j].set_data(*highway.cars[j].position())
            time_text.set_text('time = %.1f' % highway.cars[0].time_elapsed)
        return points, time_text

    def update_car_beliefs(messages):
        # TODO : check
        for car in highway.cars:
            car.update_positions(messages[car.id])
            car.filter_distances()
            car.update_speed(dt=dt)

    def update_scores():
        for car in highway.cars:
            for cid in car.info.received_positions:
                if cid in car.info.filtered_distances:
                    true_r, _= highway_location_to_polar((car.x - cars_by_id[cid].x), (car.lane - cars_by_id[cid].lane))
                    score[car.id] += (car.info.filtered_distances[cid][0] - true_r)**2
                    noise[car.id] += (car.info.received_positions[cid][0] - true_r)**2

    def get_car_position_message(to_id):
        mess = list()
        for from_id in car_ids:
            if from_id != to_id:
                x = cars_by_id[from_id].x - cars_by_id[to_id].x
                delta_lane = cars_by_id[from_id].lane - cars_by_id[to_id].lane
                mess.append(Message(from_id=from_id, to_id=to_id, x=x, delta_lane=delta_lane))
        return mess

    def car_done(positions, car_id):
        if positions[car_id] > length:
            return True
        return False

    def all_done(positions):
        # Check all peers to update done status
        for position in positions:
            assert position > 0, print('Car going backwards')
            if position < length:
                return False
        return True

    print("Starting simulation")
    highway = HighWay(length=length, n_lanes=n_lanes, n_cars=n_cars, dt=dt)

    car_ids = [car.id for car in highway.cars]
    cars_by_id = dict((car.id, car) for car in highway.cars)

    score = dict()
    noise = dict()

    for car in highway.cars:
        car.init()
        score[car.id] = 0
        noise[car.id] = 0

    # Visualization
    #fig, ax, points, time_text = init_visualization()

    round = 0
    plot_distance = np.zeros(500)

    # Begin the event loop
    while True:
        print("======= Round %d ========" % round)
        test_done = all_done([car.x for car in highway.cars])
        messages = dict() # car_id -> list of messages

        for c_rec in highway.cars:
            messages[c_rec.id] = get_car_position_message(to_id=c_rec.id)
            if c_rec.id == 'Car0':
                plot_distance[round] = [m.r for m in messages[c_rec.id] if m.from_id == 'Car1'][0]
            # print(messages)

        update_car_beliefs(messages)

        highway.step(highway.dt)
        #points, time_text = animate()

        #plt.draw()
        #plt.pause(0.01)

        update_scores()

        if test_done:
            break
        round += 1

    print("======= SUMMARY STATS ========")
    print('Filtering', score)
    print('Noise', noise)
    plt.plot(plot_distance[:round])
    plt.show()

run_sim_once()