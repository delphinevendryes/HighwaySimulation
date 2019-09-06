import unittest
import numpy as np
from ..filtering.kalman_filter import KalmanFilter


class TestKalmanFilter(unittest.TestCase):
    def test_kalman_filter_with_no_noise(self):
        sigma_w = np.zeros((3, 3))
        sigma_v = np.zeros((3, 3))

        psi = np.identity(3)
        phi = np.identity(3)

        kalman_filter = KalmanFilter(phi, psi, sigma_v, sigma_w)

        time_series = [np.ones(3), np.ones(3), np.ones(3)]
        filtered_time_series = kalman_filter.filter(time_series)
        filtered_mean = [list(filtered_info.compile()) for filtered_info in filtered_time_series]
        self.assertEqual(
            filtered_mean,
            [list(observation) for observation in time_series],
        )

        time_series = [np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3)]
        filtered_time_series = kalman_filter.filter(time_series)
        filtered_mean = [list(filtered_info.compile()) for filtered_info in filtered_time_series]
        self.assertEqual(
            filtered_mean,
            [list(observation) for observation in time_series],
        )

        phi = np.identity(3) / 2
        kalman_filter = KalmanFilter(phi, psi, sigma_v, sigma_w)

        time_series = [np.ones(3), np.ones(3) / 2, np.ones(3) / 4]
        filtered_time_series = kalman_filter.filter(time_series)
        filtered_mean = [list(filtered_info.compile()) for filtered_info in filtered_time_series]
        self.assertEqual(
            filtered_mean,
            [list(observation) for observation in time_series],
        )

        phi = np.identity(3) / 3
        kalman_filter = KalmanFilter(phi, psi, sigma_v, sigma_w)

        time_series = [np.ones(3), np.ones(3) / 3, np.ones(3) / 9, np.ones(3) / 27]
        filtered_time_series = kalman_filter.filter(time_series)
        filtered_mean = [list(filtered_info.compile()) for filtered_info in filtered_time_series]
        self.assertEqual(
            filtered_mean,
            [list(observation) for observation in time_series],
        )
