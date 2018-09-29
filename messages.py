from numpy import random

class Message:
    def __init__(self, from_id, to_id, x_rel):
        self.from_id = from_id
        self.to_id = to_id
        self.x_rel = x_rel
        # self.noise = random.normal(0, 1.0, 1)

    def __repr__(self):
        return "Message(from_id = %s, to_id=%s, x_rel=%f)" % (
            self.from_id, self.to_id, self.x_rel)