from .filter import Filter
import numpy as np

DELTA_T = 1/30

SIGMA_W = np.zeros((3, 3))
SIGMA_V = np.diag(0.1, 3)
PSI = np.diag(1, 3)
PHI = np.matrix(
            [
                [1, DELTA_T, 0.5 * DELTA_T ** 2],
                [0, 1, DELTA_T],
                [0, 0, 1]
            ]
        )


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

        temp_mean = (
                old_mean + (old_variance * psi_transpose) * np.linalg.pinv(psi * old_variance * psi_transpose + sigma_v) * (new_observation - psi * old_mean)
        )
        return phi * temp_mean

    def _compute_new_variance(self, old_parameters):
        old_mean, old_variance = old_parameters

        psi = self.psi
        phi = self.phi
        sigma_v = self.sigma_v
        sigma_w = self.sigma_w

        psi_transpose = np.transpose(psi)

        tmp_variance = (
                old_variance - old_variance * psi_transpose * np.linalg.pinv(psi * old_variance * psi_transpose + sigma_v) * psi * old_variance
        )
        return phi * tmp_variance * np.transpose(phi) + sigma_w

    def recursion_step(self, new_observation, old_parameters):
        new_mean = self._compute_new_mean(new_observation, old_parameters)
        new_variance = self._compute_new_variance(old_parameters)
        return new_mean, new_variance

    def filter(self, time_series):
        filtered_series = []
        mean = 0
        variance = 0
        parameters = mean, variance
        for time_step in time_series:
            filtered_series.append(parameters)
            parameters = self.recursion_step(time_step, parameters)
        return filtered_series
