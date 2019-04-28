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

    def invert(self):
        return ray(self.origin, self.direction.invert())


class color():

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


    def __add__(self, other):  # Operator +
        '''
        Returns: 
        
            vector3

        Description:

            If passed with vector3, adds the two vectors

            If passed with scalar, adds the scalar to all components of the vector

        '''

        if type(other).__name__ == 'color':
            return color(self.r+other.r, self.g+other.g, self.b+other.b)
        else:
            return color(self.r+other, self.g+other, self.b+other)


    def __mul__(self, other):  # Operator *
        '''
        Returns: 
        
            scalar if passed with vector3

            vector3 if passed with scalar

        Description:

            if passed with vector3, performs dot product of the two

            if passed with scalar, multiplies scalar with all components of vector

        '''

        if type(other).__name__ == 'color':
            return color(self.r*other.r, self.g*other.g, self.b*other.b)
        else:
            return color(self.r*other, self.g*other, self.b*other)


class sphere():
    def __init__(self, center, radius, color, material_type=None):
        self.center = center
        self.radius = radius
        self.color = color
        self.material_type = material_type
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

            if t0 > 0 and t1 > 0:
                if t0 < t1:
                    return r.origin + (r.direction * t0)
                else:
                    return r.origin + (r.direction * t1)

            if t0 > 0 and t1 < 0:
                return r.origin + (r.direction * t0)
            elif t1 > 0 and t0 < 0:
                return r.origin + (r.direction * t1)

        return None


class sky():
    def __init__(self, center, radius, color, material_type=None):
        self.center = center
        self.radius = radius
        self.color = color
        self.material_type = material_type
        self.type = 'Sky'

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

            if t0 > 0 and t1 > 0:
                if t0 < t1:
                    return r.origin + (r.direction * t0)
                else:
                    return r.origin + (r.direction * t1)

            if t0 > 0 and t1 < 0:
                return r.origin + (r.direction * t0)
            elif t1 > 0 and t0 < 0:
                return r.origin + (r.direction * t1)

        return None


class pointLight():
    def __init__(self, center, color):
        self.center = center
        self.color = color
        self.type = 'Light'


class plane():
    def __init__(self, point, normal, color, material_type=None):
        self.point = point
        self.normal = normal
        self.color = color
        self.material_type = material_type
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


# objects
objects = [
    sphere(vector3(-100.0,0.0,50.0), 100.0, color(0.1,0.1,0.8), material_type='Reflective'), 
    sphere(vector3(100.0,0.0,50.0), 100.0, color(0.8,0.1,0.1), material_type='Reflective'), 
    sky(vector3(0.0,0.0,0.0), 100000.0, color(1.0,1.0,1.0)), 
    plane(vector3(0.0,-100.0, 0.0), vector3(0.0,1.0,0.0), color(0.1,0.8,0.1), material_type='Reflective'),
]

lights = [
    pointLight(vector3(0.0,99999.0,-150.0), color(1.0,1.0,1.0)),
    # pointLight(vector3(50.0,500.0,150.0), color(1.0,1.0,1.0)),
]


def trace(r, bounces):
    bounces -= 1
    # Reflection ray
    # Finding closes object on ray
    min_dist = math.inf
    closest_object = None
    closest_hit_point = None
    for object in objects:
        hit_point = object.hit(r)
        if hit_point:
            distance = vector3.magnitude(hit_point - r.origin)
            if distance < min_dist:
                min_dist = distance
                closest_object = object
                closest_hit_point = hit_point

    # Reflect another ray if found closest object            
    if closest_object:
        if closest_object.type == 'Sky':
            return closest_object.color
        elif closest_object.type == 'Plane':
            object_normal = closest_object.normal
        else:
            object_normal = closest_object.normal(closest_hit_point)

        if bounces == 0 or not closest_object.material_type == "Reflective":
            color_to_return = closest_object.color
        else:
            ray_inv = r.invert()
            color_to_return = color(0,0,0)
            for i in range(-3,4):
                direction = ray_inv.direction + i/3
                reflected_ray_direction = ((object_normal *(object_normal * direction)) * 2) - direction
                reflected_ray = ray(closest_hit_point, reflected_ray_direction)

                color_to_return += trace(reflected_ray, bounces) * ((object_normal * reflected_ray_direction) * 0.025)

            color_to_return += closest_object.color * 0.25

        # # Checking Shadow ray against all light sources
        # interacted_lights = []
        # for light in lights:
        #     object_in_way = False
        #     shadow_ray_direction = vector3.unit_vector(light.center - closest_hit_point)
        #     shadow_ray = ray(closest_hit_point, shadow_ray_direction)
        #     min_dist = vector3.magnitude(light.center - closest_hit_point)
        #     # Checking Shadow ray against all objects
        #     for object in objects:
        #         hit_point = object.hit(shadow_ray)
        #         if hit_point:
        #             distance = vector3.magnitude(hit_point - shadow_ray.origin)
        #             if distance < min_dist:
        #                 min_dist = distance
        #                 object_in_way = True
        #                 break

        #     if not object_in_way:
        #         interacted_lights.append(light)
        
        # intensity = 0
        # for light in interacted_lights:
        #     if reflected_object is not None and reflected_object.type == 'Sky':
        #         intensity = 1
        #     else:
        #         angle = shadow_ray_direction.unit_vector()
        #         diff_angle = angle * object_normal
        #         intensity = intensity + diff_angle

        return color_to_return

    return color(0,0,0)
    

if __name__ == "__main__":
    # image canvas parameters
    render_size = (640,480)
    samples = 1

    image_shape = (render_size[1]*samples, render_size[0]*samples, 3)
    image = np.zeros(image_shape,dtype=np.uint8)

    # ray and canvas coordinates
    ray_origin = vector3(0.0,0.0,-500.0)
    frame_origin = vector3(0.0,0.0,200.0)

    # Initialize blank frame
    image_area = cv2.resize(image, render_size)
    cv2.imshow('Area', image_area)
    cv2.waitKey(5)
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
            
            col = trace(r, 3)

            image[y,x,2] = col.r * 255
            image[y,x,1] = col.g * 255
            image[y,x,0] = col.b * 255

        # Update after every 50th part completes
        if (x+1)%int(image_shape[1]/100) == 0 or x+1 == image_shape[1]:
            image_area = cv2.resize(image, render_size, interpolation=cv2.INTER_AREA)
            cv2.imshow('Area', image_area)
            cv2.waitKey(5)
    cv2.waitKey(0)