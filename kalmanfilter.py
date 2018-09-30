from cars import Car

class KalmanFilterCar(Car):
    def init(self):
        self.sigmav = 0.1
        self.sigmaw = 0.5
        self.V0= 0.1

    def filter_distances(self):

        for cid in self.rec_distances:
            if len(self.rec_distances[cid]) == 0:
                break

            if cid not in self.filt_distances:
                # initialize by setting variance to 0.1 and mean to observation
                self.filt_distances[cid] = [self.rec_distances[cid][-1], self.V0]

            y = self.rec_distances[cid][-1]
            m = self.filt_distances[cid][0]
            V = self.filt_distances[cid][1]

            # compute new mean and variance
            self.filt_distances[cid][0] = m + (V + self.sigmaw)*(y-m)/(V + self.sigmav + self.sigmaw)
            self.filt_distances[cid][1] = (V + self.sigmaw) - (V + self.sigmaw)**2 / (V + self.sigmaw + self.sigmav)
        print(self.filt_distances)



