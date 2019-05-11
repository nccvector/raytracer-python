import math
from utils.Vector import Vector3

class Plane():
    def __init__(self, position, normal, color, material_type=None):
        self.type = 'Plane'
        self.position = position
        self.normal = normal
        self.color = color
        self.material_type = material_type

    def calculate_normal(self, _):
        """The surface normal at the given point on the plane"""
        return self.normal
    
    def hit(self, r):
        d = self.position * self.normal.invert()
        denom = (r.direction * self.normal)

        if denom == 0:
            t = -math.inf
        else:
            t = -(d + r.origin * self.normal) / denom

        if t < 0:
            return None
        else:
            return r.origin + (r.direction * t)

class Sphere():
    def __init__(self, position, radius, color, material_type=None):
        self.type = 'Sphere'
        self.position = position
        self.radius = radius
        self.color = color
        self.material_type = material_type

    def calculate_normal(self, p):
        """The surface normal at the given point on the sphere"""
        return Vector3.normalize(p - self.position)

    def hit(self, r):
        """The ray t value of the first intersection point of the
        ray with self, or None if no intersection occurs"""
        a = r.direction * r.direction
        f = r.origin - self.position
        b = 2 * (f * r.direction)
        c = (f * f) - (self.radius * self.radius)

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