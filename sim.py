from .highway import HighWay, HighwayNavigationSystem
from .message import Message
from .navigation_system import NavigationSystem, build_empty_information_manager
from .car import Car, initialize_random_motion_descriptor_from_highway_config
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

def get_color(i: int, n: int) -> List[float]:
    return [(i + 1) / n, 0, 0]


def init_visualization(n_lanes: int, n_cars: int, highway_length: float):
    fig = plt.figure()
    ax = fig.add_subplot(
        111,
        autoscale_on=False,
        xlim=(-1, n_lanes),
        ylim=(0, highway_length),
    )
    ax.grid()
    ax.set_xlabel('Lanes')
    ax.set_ylabel('Highway length (m)')
    ax.set_xticks(np.arange(n_lanes + 1))
    car_points = [ax.plot([], 'o', color=get_color(i, n_cars))[0] for i in range(n_cars)]
    time_str = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    return fig, ax, car_points, time_str


def run_sim_once(highway_config):
    n_cars = highway_config["n_cars"]
    n_lanes = highway_config["n_lanes"]
    highway_length = highway_config["length"]
    dt = highway_config["delta"]
    lane_width = highway_config["lane_width"]

    def animate(time: float):
        """Perform animation step"""
        for i_car, navigation_system in enumerate(highway_navigation_system.navigation_systems):
            position = navigation_system.car.motion.position.to_cartesian()
            points[i_car].set_data(*position)
            time_text.set_text('time = %.1f' % time)
        return points, time_text

    # def update_scores():
    #     for car in highway.cars:
    #         for cid in car.info.received_positions:
    #             if cid in car.info.filtered_distances:
    #                 true_r, _= highway_location_to_polar((car.x - cars_by_id[cid].x), (car.lane - cars_by_id[cid].lane))
    #                 score[car.id] += (car.info.filtered_distances[cid][0] - true_r)**2
    #                 noise[car.id] += (car.info.received_positions[cid][0] - true_r)**2

    print("Starting simulation")

    highway = HighWay(length=highway_length, lane_number=n_lanes, lane_width=lane_width)

    motions = [
        initialize_random_motion_descriptor_from_highway_config(highway_config) for _ in range(n_cars)
    ]
    cars = [Car(car_id=str(uuid.uuid4()), motion=motion) for motion in motions]

    debug_car_id = cars[0].car_id

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

    # for car in highway.cars:
    #     score[car.id] = 0
    #     noise[car.id] = 0

    # Visualization
    fig, ax, points, time_text = init_visualization(n_lanes, n_cars, highway_length)

    round = 0
    time_elapsed = 0
    plot_distance = np.zeros(500)

    # Begin the event loop
    while True:
        print("======= Round %d ========" % round)
        if highway_navigation_system.is_done():
            break

        for target in highway_navigation_system.navigation_systems:
            messages = []
            target_car = target.car
            for source in highway_navigation_system.navigation_systems:
                source_car = source.car
                message = Message(source_car, target_car)
                messages.append(message)
            target.information_manager.update_positions(messages, dt)
            if target.car.car_id == debug_car_id:
                print(target.information_manager.distance_trackers)

        highway_navigation_system.step(dt)
        points, time_text = animate(time_elapsed)

        plt.draw()
        plt.pause(0.01)

        # update_scores()
        round += 1
        time_elapsed = round * dt

    print("======= SUMMARY STATS ========")
    print('Filtering', score)
    print('Noise', noise)
    plt.plot(plot_distance[:round])
    plt.show()
