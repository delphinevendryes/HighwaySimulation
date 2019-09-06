import matplotlib.pyplot as plt

from .navigation_system import NavigationSystem
from .history import History

import numpy as np


def get_true_distances(history, source_id, target_id):
    source_motion = history.get_car_positions(source_id)
    target_motion = history.get_car_positions(target_id)

    distances = []
    for time_step in range(history.get_length()):
        relative_position = source_motion[time_step].position.subtract(
            target_motion[time_step].position
        )
        distance, _ = relative_position.to_polar()
        distances.append(distance)
    return distances


def get_noisy_distances(target, source):
    noisy_positions = target.information_manager.distance_trackers[source.car.car_id].received_positions
    distances = []
    for noisy_position in noisy_positions:
        distance, _ = noisy_position.to_polar()
        distances.append(distance)
    return distances


def get_filtered_distances(target, source):
    filtered_info_list = target.information_manager.distance_trackers[source.car.car_id].filtered_info_list
    filtered_positions = [filtered_info.compile() for filtered_info in filtered_info_list]
    distances = []
    for position in filtered_positions:
        distance = position[0]
        distances.append(distance)
    return distances


def get_analysis(source: NavigationSystem, target: NavigationSystem, history: History):
    """Analyze source target system"""
    # true distances
    true_distances = get_true_distances(history, target.car.car_id, source.car.car_id)

    # noisy distances received by target from source
    noisy_distances = get_noisy_distances(target, source)

    # filtered distances
    filtered_distances = get_filtered_distances(target, source)
    return np.array(true_distances), np.array(noisy_distances), np.array(filtered_distances)


def plot_analysis(true_distances, noisy_distances, filtered_distances):
    x_axis = [i for i in range(len(true_distances))]
    plt.plot(x_axis, true_distances, c='red', label="True distance")
    plt.plot(x_axis, noisy_distances, c='green', label="Noisy distance")
    plt.plot(x_axis, filtered_distances, c='orange', label="Filtered distance")
    plt.legend()
    plt.title("Distance between two cars")
    plt.xlabel("Time steps")
    plt.ylabel("Distance")
    plt.show()
    return
