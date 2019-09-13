from .analysis import get_analysis, plot_analysis
from .highway import HighWay, HighwayNavigationSystem
from .message import Message
from .navigation_system import NavigationSystem, build_empty_information_manager
from .car import Car, CarId, initialize_random_motion_descriptor_from_highway_config
from .history import History, get_round_from_highway_navigation_systems

import matplotlib.pyplot as plt
import numpy as np
import uuid

from typing import List, Optional


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
    ax.set_xlabel("Lanes")
    ax.set_ylabel("Highway length (m)")
    ax.set_xticks(np.arange(n_lanes + 1))
    car_points = [ax.plot([], 'o', color=get_color(i, n_cars))[0] for i in range(n_cars)]
    time_str = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    return fig, ax, car_points, time_str


def run_sim_once(highway_config, visualize: Optional[bool] = False):
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

    print("Starting simulation")
    history = History()

    highway = HighWay(length=highway_length, lane_number=n_lanes, lane_width=lane_width)

    motions = [
        initialize_random_motion_descriptor_from_highway_config(highway_config) for _ in range(n_cars)
    ]
    cars = [Car(car_id=CarId(str(uuid.uuid4())), motion=motion) for motion in motions]

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

    # Visualization
    if visualize:
        fig, ax, points, time_text = init_visualization(n_lanes, n_cars, highway_length)

    n_round = 0
    time_elapsed = 0

    # Begin the event loop
    while True:
        print("======= Round %d ========" % n_round)
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

        highway_navigation_system.step(dt)
        new_round = get_round_from_highway_navigation_systems(highway_navigation_system)
        history.update(new_round)

        if visualize:
            points, time_text = animate(time_elapsed)
            plt.draw()
            plt.pause(dt)

        # update_scores()
        n_round += 1
        time_elapsed = n_round * dt

    true_distances, noisy_distances, filtered_distances = get_analysis(
        source=navigation_systems[0], target=navigation_systems[1], history=history
    )
    plot_analysis(true_distances, noisy_distances, filtered_distances)

    print("======= SUMMARY STATS ========")
    print('Filtering', np.mean((filtered_distances - true_distances)**2))
    print('Noise', np.mean((noisy_distances - true_distances)**2))

