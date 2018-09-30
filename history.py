

class History:
    def __init__(self):
        # every dictionary has same structure
        # keys = car that *received* information
        # mapped to a dictionary: cars -> information about speed (true / noisy / filtered)
        self.true_distances = dict()
        self.received_noisy_distances = dict()
        self.filtered_distances = dict()

    def update_true_history(self):
        pass

    def update_noisy_history(self):
        pass

    def update_filtered_history(self):
        pass