import unittest
import numpy as np
from ..filtering.kalman_filter import KalmanFilter


class TestKalmanFilter(unittest.TestCase):
    def test_kalman_filter_with_no_noise(self):
        SIGMA_W = np.zeros((3, 3))
        SIGMA_V = np.zeros((3, 3))
        
        PSI = np.identity(3)
        PHI = np.identity(3)

        kalman_filter = KalmanFilter(PHI, PSI, SIGMA_V, SIGMA_W)

        time_series = [np.ones(3), np.ones(3), np.ones(3)]
        filtered_time_series = kalman_filter.filter(time_series)
        filtered_mean = [list(mean) for mean, variance in filtered_time_series]
        self.assertEqual(
            filtered_mean,
            [list(observation) for observation in time_series],
        )

        time_series = [np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3)]
        filtered_time_series = kalman_filter.filter(time_series)
        filtered_mean = [list(mean) for mean, variance in filtered_time_series]
        self.assertEqual(
            filtered_mean,
            [list(observation) for observation in time_series],
        )


        PHI = np.identity(3) / 2
        kalman_filter = KalmanFilter(PHI, PSI, SIGMA_V, SIGMA_W)

        time_series = [np.ones(3), np.ones(3) / 2, np.ones(3) / 4]
        filtered_time_series = kalman_filter.filter(time_series)
        filtered_mean = [list(mean) for mean, variance in filtered_time_series]
        self.assertEqual(
            filtered_mean,
            [list(observation) for observation in time_series],
        )

        PHI = np.identity(3) / 3
        kalman_filter = KalmanFilter(PHI, PSI, SIGMA_V, SIGMA_W)

        time_series = [np.ones(3), np.ones(3) / 3, np.ones(3) / 9, np.ones(3) / 27]
        filtered_time_series = kalman_filter.filter(time_series)
        filtered_mean = [list(mean) for mean, variance in filtered_time_series]
        self.assertEqual(
            filtered_mean,
            [list(observation) for observation in time_series],
        )
