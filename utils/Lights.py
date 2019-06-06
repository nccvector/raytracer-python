import math
from utils.Vector import Vector3

class PointLight():
    def __init__(self, position, radius, color):
        self.type = 'Light'
        self.subtype = 'Point'
        self.position = position
        self.radius = radius
        self.color = color

    def hit(self, r):
        """The ray t value of the first intersection point of the
        ray with self, or None if no intersection occurs"""
        a = Vector3.dot(r.direction, r.direction)
        f = r.origin - self.position
        b = 2 * Vector3.dot(f, r.direction)
        c = Vector3.dot(f, f) - self.radius * self.radius

        discriminant = b * b - 4 * a * c

        if discriminant >= 0:
            root = math.sqrt(discriminant)
            t0 = (-b - root)/(2*a)
            t1 = (-b + root)/(2*a)

            if t0 >= 0:
                return r.origin + (r.direction * t0)
            elif t1 >= 0:
                return r.origin + (r.direction * t1)

        return None

class DirectionalLight():
    def __init__(self, position, direction, color):
        self.type = 'Light'
        self.subtype = 'Directional'
        self.position = position
        self.direction = direction
        self.color = color

    def hit(self, r):
        d = Vector3.dot(self.position, self.normal.invert())
        denom = Vector3.dot(r.direction, self.normal)

        if denom == 0:
            t = -math.inf
        else:
            t = -(d + Vector3.dot(r.origin, self.normal)) / denom

        if t < 0:
            return None
        else:
            return r.origin + (r.direction * t)

