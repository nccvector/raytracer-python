class Ray:

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def invert(self):
        return Ray(self.origin, self.direction.invert())