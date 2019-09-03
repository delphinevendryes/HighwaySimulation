class KalmanFilter:
    def __init__(self):
        self.sigma_v = 0.1
        self.sigma_w = 0.1
        self.v_0 = 10

    def filter_distances(self, distances, filtered_information):
        most_recent_position = distances[-1]

        if len(filtered_information) == 0:
            old_mean = most_recent_position
            old_variance = self.v_0
        else:
            old_mean, old_variance = filtered_information[-1]

        new_mean = (
            old_mean + (old_variance + self.sigma_w) * (most_recent_position - old_mean) / (old_variance + self.sigma_v + self.sigma_w)
        )
        new_variance = (
            (old_variance + self.sigma_w) - (old_variance + self.sigma_w)**2 / (old_variance + self.sigma_w + self.sigma_v)
        )
        return new_mean, new_variance
