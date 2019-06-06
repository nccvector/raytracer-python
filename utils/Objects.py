import math
from utils.Materials import StandardMaterial
from utils.Vector import Vector3

class Plane():
    def __init__(self, position, normal, material):
        self.type = 'Object'
        self.subtype = 'Plane'
        self.position = position
        self.normal = normal
        self.material = material

    def calculate_normal(self, _):
        """The surface normal at the given point on the plane"""
        return self.normal
    
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

class Sphere():
    def __init__(self, position, radius, material):
        self.type = 'Object'
        self.subtype = 'Sphere'
        self.position = position
        self.radius = radius
        self.material = material

    def calculate_normal(self, p):
        """The surface normal at the given point on the sphere"""
        return Vector3.normalize(p - self.position)

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