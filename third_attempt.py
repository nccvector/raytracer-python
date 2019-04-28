import numpy as np
import cv2
import math


class vector3():

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


    def unit_vector(self):
        '''
        Returns: 
        
            vector3

        Description: 
            
            returns unit vector

        '''
        
        k = 1/math.sqrt(self.x**2 + self.y**2 + self.z**2)
        return vector3(self.x*k, self.y*k, self.z*k)


    def magnitude(self):
        '''
        Returns: 
        
            scalar

        Description: 
            
            returns magnitude of the vector

        '''

        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    
    def invert(self):  # Operator -
        '''
        Returns: 
        
            vector3

        Description:

            inverts all the components

        '''

        return vector3(-self.x, -self.y, -self.z)


    def __add__(self, other):  # Operator +
        '''
        Returns: 
        
            vector3

        Description:

            If passed with vector3, adds the two vectors

            If passed with scalar, adds the scalar to all components of the vector

        '''

        if type(other).__name__ == 'vector3':
            return vector3(self.x+other.x, self.y+other.y, self.z+other.z)
        else:
            return vector3(self.x+other, self.y+other, self.z+other)

    
    def __sub__(self, other):  # Operator -
        '''
        Returns: 
        
            vector3

        Description:

            If passed with vector3, subtracts the two vectors

            If passed with scalar, subtracts the scalar to all components of the vector

        '''

        if type(other).__name__ == 'vector3':
            return vector3(self.x-other.x, self.y-other.y, self.z-other.z)
        else:
            return vector3(self.x-other, self.y-other, self.z-other)


    def __mul__(self, other):  # Operator *
        '''
        Returns: 
        
            scalar if passed with vector3

            vector3 if passed with scalar

        Description:

            if passed with vector3, performs dot product of the two

            if passed with scalar, multiplies scalar with all components of vector

        '''

        if type(other).__name__ == 'vector3':
            return self.x*other.x + self.y*other.y + self.z*other.z
        else:
            return vector3(self.x*other, self.y*other, self.z*other)


    def __mod__(self, other):  # Operator %
        '''
        Returns: 
        
            vector3

        Description:

            performs cross product

        '''

        return vector3(self.y*other.z-self.z*other.y, -(self.x*other.z-self.z-other.x), self.x*other.y-self.y-other.x)


class ray:

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class color():

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


    def __mul__(self, other):  # Operator *
        '''
        Returns: 
        
            color

        Description:

            multiplies with all components of color

        '''
        
        return color(self.r*other, self.g*other, self.b*other)


class sphere():
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color
        self.type = 'Sphere'

    def normal(self, p):
        """The surface normal at the given point on the sphere"""
        return vector3.unit_vector(p - self.center)

    def hit(self, r):
        """The ray t value of the first intersection point of the
        ray with self, or None if no intersection occurs"""
        q = self.center - r.origin
        vDotQ = r.direction * q
        squareDiffs = (q * q) - (self.radius*self.radius)
        discrim = (vDotQ * vDotQ) - squareDiffs
        if discrim >= 0:
            root = math.sqrt(discrim)
            t0 = (vDotQ - root)
            t1 = (vDotQ + root)
            if t0 < t1 and t1 > 0:
                return r.origin + (r.direction * t0)
            elif t1 < t0 and t0 > 0:
                return r.origin + (r.direction * t1)

        return None


class pointLight():
    def __init__(self, center, color):
        self.center = center
        self.color = color
        self.type = 'Light'


class plane():
    def __init__(self, point, normal, color):
        self.point = point
        self.normal = normal
        self.color = color
        self.type = 'Plane'
    
    def hit(self, r):
        d = self.point * self.normal
        denom = (r.direction * self.normal.invert())

        if denom == 0:
            t = -math.inf
        else:
            t = -(d + r.origin * self.normal) / denom

        if t < 0:
            return None
        else:
            return r.origin + (r.direction * t)


if __name__ == "__main__":
    # image canvas parameters
    image_shape = (480,640,3)
    image = np.zeros(image_shape,dtype=np.uint8)

    # ray and canvas coordinates
    ray_origin = vector3(0.0,0.0,-500.0)
    frame_origin = vector3(0.0,0.0,100.0)

    # objects
    objects = [
        sphere(vector3(-50.0,0.0,160.0), 50.0, color(0.1,0.1,0.8)), 
        sphere(vector3(50.0,0.0,160.0), 50.0, color(0.8,0.1,0.1)), 
        plane(vector3(0.0,-50.0, 0.0), vector3(0.0,1.0,0.0), color(0.1,0.8,0.1)),
    ]

    lights = [
        pointLight(vector3(250.0,500.0,-1500.0), color(1.0,1.0,1.0)),
    ]


    for x in range(0, image_shape[1]):
        for y in range(0, image_shape[0]):
            col = color(0,0,0)
            frame_point = vector3(x-(image_shape[1]/2), (image_shape[0]/2)-y, frame_origin.z)
            ray_direction = vector3.unit_vector(frame_point - ray_origin)
            r = ray(ray_origin, ray_direction)

            # check ray with all objects to find closest one
            min_distance = math.inf
            closest_object = None
            closest_int_point = None
            for obj in objects:                
                int_point = obj.hit(r)

                if int_point is not None:
                    distance = vector3.magnitude(int_point - r.origin)
                    if distance < min_distance:
                        min_distance = distance
                        closest_object = obj
                        closest_int_point = int_point

            # Apply color of closest object
            if closest_object is not None:

                # Trace shadow ray from closest intersection point to all light sources
                for light in lights:
                    angle = vector3.unit_vector(light.center - closest_int_point)
                    if closest_object.type == "Plane":
                        diff_angle = angle * closest_object.normal
                    else:
                        diff_angle = angle * closest_object.normal(closest_int_point)
                    col = closest_object.color * diff_angle
                    shadow_ray_direction = vector3.unit_vector(light.center - closest_int_point)
                    shadow_ray = ray(closest_int_point, shadow_ray_direction)

                    # check ray with all objects to find closest one
                    min_distance = vector3.magnitude(light.center - shadow_ray.origin)
                    for obj in objects:
                        int_point = obj.hit(shadow_ray)
                        
                        if int_point is not None:
                            distance = vector3.magnitude(int_point - shadow_ray.origin)
                            if int_point is not None and distance < min_distance:
                                col = color(0,0,0)
                                break

            image[y,x,2] = col.r * 255
            image[y,x,1] = col.g * 255
            image[y,x,0] = col.b * 255

    cv2.imshow('Rendered image', image)
    cv2.waitKey(0)