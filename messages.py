from numpy import random, abs

class Message:
    def __init__(self, from_id, to_id, x_rel):
        self.from_id = from_id
        self.to_id = to_id
        self.x_meas = x_rel + random.normal(0, 0.1)

    def __repr__(self):
        return "Message(from_id = %s, to_id=%s, x_meas=%f)" % (
            self.from_id, self.to_id, self.x_meas)