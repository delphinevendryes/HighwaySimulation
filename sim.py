from .highway import HighWay, HighwayNavigationSystem
from .message import Message
from .navigation_system import NavigationSystem, build_empty_information_manager
from .car import Car, initialize_random_motion_descriptor
import matplotlib.pyplot as plt
import numpy as np
import uuid

from typing import List


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


    def update_scores():
        for car in highway.cars:
            for cid in car.info.received_positions:
                if cid in car.info.filtered_distances:
                    true_r, _= highway_location_to_polar((car.x - cars_by_id[cid].x), (car.lane - cars_by_id[cid].lane))
                    score[car.id] += (car.info.filtered_distances[cid][0] - true_r)**2
                    noise[car.id] += (car.info.received_positions[cid][0] - true_r)**2

    def get_car_position_message(target_id: str, source_ids: List[str]) -> List[Message]:
        """Get a list of messages received by target car"""
        mess = list()
        for from_id in car_ids:
            if from_id != to_id:
                x = cars_by_id[from_id].x - cars_by_id[to_id].x
                delta_lane = cars_by_id[from_id].lane - cars_by_id[to_id].lane
                mess.append(Message(source=from_id, target=to_id, x=x, delta_lane=delta_lane))
        return mess

    def car_done(positions, car_id):
        if positions[car_id] > length:
            return True
        return False

    print("Starting simulation")

    highway = HighWay(length=500, lane_number=1)
    motions = [initialize_random_motion_descriptor() for _ in range(n_cars)]
    cars = [Car(car_id=str(uuid.uuid4()), motion=motion) for motion in motions]
    navigation_systems = [
        NavigationSystem(
            car=car,
            information_manager=build_empty_information_manager()
        ) for car in cars
    ]

    highway_navigation_system = HighwayNavigationSystem(
        highway=highway,
        navigation_systems=navigation_systems,
        delta=dt,
    )
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
        if highway_navigation_system.is_done():
            break

        # messages = dict()  # car_id -> list of messages

        for target in highway_navigation_system.navigation_systems:
            messages = []
            for source in highway_navigation_system.navigation_systems:
                source_car = source.car
                target_car = target.car
                message = Message(source_car, target_car)
                messages.append(message)
            source.information_manager.update_positions(received_messages=messages)

        highway_navigation_system.step(dt)
        #points, time_text = animate()

        #plt.draw()
        #plt.pause(0.01)

        update_scores()
        round += 1

    print("======= SUMMARY STATS ========")
    print('Filtering', score)
    print('Noise', noise)
    plt.plot(plot_distance[:round])
    plt.show()


run_sim_once()
