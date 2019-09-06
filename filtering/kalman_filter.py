from .filter import Filter, FilteredInfo
from typing import Tuple, List
import numpy as np

DELTA_T = 1/30

SIGMA_W = np.zeros((3, 3))
SIGMA_V = np.diag([0.1 for _ in range(3)])
PSI = np.diag([1 for _ in range(3)])
PHI = np.matrix(
            [
                [1, DELTA_T, 0.5 * DELTA_T ** 2],
                [0, 1, DELTA_T],
                [0, 0, 1]
            ]
        )


class KalmanFilteredInfo(FilteredInfo):
    def __init__(self, normal_parameters: Tuple[np.array, np.array]):
        self._parameters = normal_parameters

    def get_normal_parameters(self) -> Tuple[np.array, np.array]:
        return self._parameters

    def compile(self) -> np.array:
        return self._parameters[0]


class KalmanFilter(Filter):
    def __init__(self, phi, psi, sigma_v, sigma_w):
        """We set up the model for the Kalman filter with:

        X_t = Phi * X_{t-1} + V_t  (transition model)
        Y_t = Psi * X_t + W_t  (observation model)
        V_t ~ N(0, Sigma_v) (i.i.d)
        W_t ~ N(0, Sigma_w) (i.i.d.)

        Phi = (1, DELTA_T, 0)
              (0, 1, DELTA_T)
              (0, 0, 0      )
        """
        self.phi = phi
        self.sigma_v = sigma_v
        self.sigma_w = sigma_w
        self.psi = psi

    def _compute_new_mean(self, new_observation, old_parameters):
        psi = self.psi
        phi = self.phi
        sigma_v = self.sigma_v

        old_mean, old_variance = old_parameters

        psi_transpose = np.transpose(psi)

        kalman_factor = old_variance * psi_transpose * np.linalg.pinv(psi * old_variance * psi_transpose + sigma_v)

        temp_mean = (
                old_mean + np.matmul(kalman_factor, new_observation - np.matmul(psi, old_mean))
        )
        return np.matmul(phi, temp_mean)

    def _compute_new_variance(self, old_parameters):
        old_mean, old_variance = old_parameters

        psi = self.psi
        phi = self.phi
        sigma_v = self.sigma_v
        sigma_w = self.sigma_w

        psi_transpose = np.transpose(psi)
        pinv = np.linalg.pinv(psi * old_variance * psi_transpose + sigma_v)

        kalman_factor = old_variance * psi_transpose * pinv

        tmp_variance = (
                old_variance - np.matmul(np.matmul(kalman_factor, psi), old_variance)
        )
        return np.matmul(np.matmul(phi, tmp_variance), np.transpose(phi)) + sigma_w

    def do_recursion_step(self, new_observation: np.array, filtered_info: KalmanFilteredInfo):
        parameters = filtered_info.get_normal_parameters()
        new_mean = self._compute_new_mean(new_observation, parameters)
        new_variance = self._compute_new_variance(parameters)

        return KalmanFilteredInfo((new_mean, new_variance))

    def filter(self, time_series) -> List[KalmanFilteredInfo]:
        filtered_series = []
        mean = time_series[0]
        variance = np.zeros((time_series[0].shape[0], time_series[0].shape[0]))
        parameters = KalmanFilteredInfo((mean, variance))
        for time_step in time_series:
            filtered_series.append(parameters)
            parameters = self.do_recursion_step(time_step, parameters)
        return filtered_series
