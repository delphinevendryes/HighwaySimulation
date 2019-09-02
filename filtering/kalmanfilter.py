from cars import Car


class KalmanFilterCar(Car):
    def init(self):
        self.sigmav = 0.1
        self.sigmaw = 0.1
        self.V0= 10

    def filter_distances(self):
        self.saved_filt_distances = self.info.info.received_positions.copy()
        for cid in self.info.received_positions:
            if len(self.info.received_positions[cid]) == 0:
                break

            if cid not in self.info.filtered_distances:
                # initialize by setting variance to 0.1 and mean to observation
                self.info.filtered_distances[cid] = [self.info.received_positions[cid][0], self.V0]

            y = self.info.received_positions[cid][0]
            m = self.info.filtered_distances[cid][0]
            V = self.info.filtered_distances[cid][1]

            # compute new mean and variance
            self.info.filtered_distances[cid][0] = m + (V + self.sigmaw)*(y-m)/(V + self.sigmav + self.sigmaw)
            self.info.filtered_distances[cid][1] = (V + self.sigmaw) - (V + self.sigmaw)**2/(V + self.sigmaw + self.sigmav)
