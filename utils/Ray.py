class Ray:

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def inverse(self):
        """
        Returns the ray with its direction inverted
        
        Returns:
            Ray: inverted ray object

        """
        return Ray(self.origin, self.direction.invert())