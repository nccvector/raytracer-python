class ray:

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def invert(self):
        return ray(self.origin, self.direction.invert())