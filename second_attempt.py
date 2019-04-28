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


class sphere():
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color
        self.type = 'Sphere'

    def hit(self, r):
        oc = self.center - r.origin
        a = r.direction * r.direction
        b = oc * r.direction
        b = 2.0 * b
        c = (oc * oc) - self.radius**2
        root = b**2 - 4*a*c
        if root < 0:
            return None
        else:
            return r.origin + (r.direction * root)


class pointLight():
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color
        self.type = 'Light'

    def hit(self, r):
        oc = self.center - r.origin
        a = r.direction * r.direction
        b = oc * r.direction
        b = 2.0 * b
        c = (oc * oc) - self.radius**2
        root = b**2 - 4*a*c
        if root < 0:
            return None
        else:
            return r.origin + (r.direction * root)


class plane():
    def __init__(self, point, normal, color):
        self.point = point
        self.normal = normal
        self.color = color
        self.type = 'Plane'
    
    def hit(self, r):
        d = self.point * self.normal.invert()
        denom = (r.direction.z * self.normal.z + r.direction.y * self.normal.y + r.direction.x * self.normal.x)

        if denom == 0:
            t = -1
        else:
            t = -(d + r.origin.z * self.normal.z + r.origin.y * self.normal.y + r.origin.x * self.normal.x) / denom

        if t < 0:
            return None
        else:
            return r.origin + (r.direction * t)


if __name__ == "__main__":
    # image canvas parameters
    image_shape = (480,640,3)
    image = np.zeros(image_shape,dtype=np.uint8)

    # ray and canvas coordinates
    ray_origin = vector3(0.0,0.0,0.0)
    frame_origin = vector3(0.0,0.0,100.0)

    # objects
    objects = [
        sphere(vector3(0.0,-100.0,200.0), 50.0, color(1.0,0.0,0.0)), 
        sphere(vector3(0.0,-50.0,200.0), 50.0, color(1.0,0.0,0.0)), 
        plane(vector3(0.0,50.0,0.0), vector3(0.0,-1.0,0.0), color(0.5,0.5,0.5))
    ]

    lights = [
        pointLight(vector3(0.0,-200.0,200.0), 1, color(1.0,1.0,1.0))
    ]


    for x in range(0, image_shape[1]):
        for y in range(0, image_shape[0]):
            col = color(0,0,0)
            frame_point = vector3(x-(image_shape[1]/2), y-(image_shape[0]/2), frame_origin.z)
            ray_direction = frame_point - ray_origin
            ray_direction = ray_direction.unit_vector()
            r = ray(ray_origin, ray_direction)
            closest_distance = 10000000000.0
            closest_intersection_point = None
            closest_obj = None
            for obj in objects:
                intersection_point = obj.hit(r)
                if intersection_point is not None:
                    distance = intersection_point - r.origin
                    distance = distance.magnitude()
                    if distance < closest_distance and not obj.type == 'Light':
                        closest_distance = distance
                        closest_intersection_point = intersection_point
                        closest_obj = obj

            if closest_intersection_point is not None:
                for light in lights:
                    light_ray_direction = light.center - closest_intersection_point
                    light_ray_direction = light_ray_direction.unit_vector()
                    light_ray = ray(closest_intersection_point,  light_ray_direction)
                    closest_distance_2 = 10000000000.0
                    closest_intersection_point_2 = None
                    closest_obj_2 = None
                    for obj2 in objects+lights:
                        light_intersection_point = obj2.hit(light_ray)
                        if light_intersection_point is not None:
                            distance2 = light_intersection_point - light_ray.origin
                            distance2 = distance2.magnitude()
                            if distance2 < closest_distance_2:
                                closest_distance_2 = distance2
                                closest_intersection_point_2 = light_intersection_point
                                closest_obj_2 = obj2

                if closest_obj_2 and closest_obj_2 is not None and closest_obj_2.type == 'Light':
                    col = closest_obj.color
                


            image[y,x,2] = col.r * 255
            image[y,x,1] = col.g * 255
            image[y,x,0] = col.b * 255

    cv2.imshow('Rendered image', image)
    cv2.waitKey(0)