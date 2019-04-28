import numpy as np
import cv2
import math
import random
import glob
import time
import multiprocessing


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
        
        k = 1/math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        return vector3(self.x*k, self.y*k, self.z*k)


    def magnitude(self):
        '''
        Returns: 
        
            scalar

        Description: 
            
            returns magnitude of the vector

        '''

        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    
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


class Camera():
    def __init__(self, 
                camera_origin=vector3(0,0,0),
                camera_direction=vector3(0,0,1), 
                fov=65, 
                render_size=(640,480), 
                samples=1
                ):

        self.origin = camera_origin
        self.direction = camera_direction
        self.horizontal = vector3(camera_direction.z, camera_direction.x, camera_direction.y)
        self.vertical = vector3(camera_direction.y, camera_direction.z, camera_direction.x)
        self.fov = fov

        self.render_size = render_size
        self.canvas_size = (self.render_size[0]*samples, self.render_size[1]*samples, 3)
        self.canvas = np.zeros((self.canvas_size[1], self.canvas_size[0], 3), dtype=np.uint8)

        self.canvas_distance = (self.canvas_size[0]/2)/math.tan(math.radians(fov/2))
        self.canvas_origin = self.origin + (self.direction * self.canvas_distance)


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

    def normal(self):
        """The surface normal at the given point on the sphere"""
        # return vector3.unit_vector(p - self.center)
        return vector3(0, 1, 0)

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
    sphere(vector3(-300.0,0.0,300.0), 100.0, color(0.2,0.2,0.2), material_type='Reflective'), 
    sphere(vector3(-150.0,0.0,150.0), 100.0, color(0.9,0.9,0.9), material_type='Reflective'), 
    sphere(vector3(0.0,0.0,0.0), 100.0, color(1.0,0.1,0.1), material_type='Lambertian'), 
    sphere(vector3(150.0,0.0,150.0), 100.0, color(0.1,0.1,1.0), material_type='Reflective'), 
    sphere(vector3(300.0,0.0,300.0), 100.0, color(0.1,1.0,0.1), material_type='Reflective'), 
    sky(vector3(0.0,0.0,0.0), 100000.0, color(1.0,1.0,1.0)), 
    plane(vector3(0.0,-100.0, 0.0), vector3(0.0,1.0,0.0), color(1.0,1.0,1.0), material_type='Reflective'),
]

lights = [
    pointLight(vector3(0.0,99999.0,-150.0), color(1.0,1.0,1.0)),
    # pointLight(vector3(50.0,500.0,150.0), color(1.0,1.0,1.0)),
]

render_size = (800,600)
samples = 2
# Initialize blank frame
num_threads = 8
# Generate_buckets
divs = 32
camera = Camera(camera_origin=vector3(0.0,0.0,-500.0),
                    camera_direction=vector3(0,0,1),
                    fov=65,
                    render_size=render_size,
                    samples=samples)


def trace(r, bounces, intensity=1):
    bounces -= 1
    intensity *= 0.5
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
    reflected_object = None         
    if closest_object:
        if closest_object.type == 'Sky':
            return closest_object.color, closest_object
        elif closest_object.type == 'Plane':
            object_normal = closest_object.normal
        else:
            object_normal = closest_object.normal(closest_hit_point)

        # Calculating color to return 
        if bounces == 0 or closest_object.type == "Sky":
            color_to_return = closest_object.color
        
        elif closest_object.material_type == "Lambertian":
            color_to_return = color(0,0,0)

            # generate unit sphere coordinates on the closest hit point
            unit_sphere_center = closest_hit_point + object_normal

            # generating random rays
            for _ in range(0,5):
                # generating random x, y and z

                x = random.randint(-10,11)
                y = random.randint(-10,11)
                z = random.randint(-10,11)

                if x == 0:
                    x = 0.001
                if y == 0:
                    y = 0.001
                if x == 0:
                    z = 0.001

                total_xyz = (x**2 + y**2 + z**2)**0.5

                x/=total_xyz
                y/=total_xyz
                z/=total_xyz

                diff_ray_direction = unit_sphere_center + vector3(x,y,z) - closest_hit_point
                diff_ray = ray(closest_hit_point, diff_ray_direction)
                reflected_color, reflected_object = trace(diff_ray, bounces, intensity)

                color_to_return += reflected_color * (object_normal * diff_ray_direction)
            color_to_return *= closest_object.color * intensity
        
        elif closest_object.material_type == "Reflective":
            ray_inv = r.invert()
            reflected_ray_direction = ((object_normal *(object_normal * ray_inv.direction)) * 2) - ray_inv.direction
            reflected_ray = ray(closest_hit_point, reflected_ray_direction)
            color_to_return, reflected_object = trace(reflected_ray, bounces)
            diff_angle = object_normal * ray_inv.direction
            color_to_return = color_to_return * (1-diff_angle) + closest_object.color * diff_angle


        # Checking Shadow ray against all light sources
        interacted_lights = []  # SKY NOT INCLUDED
        for light in lights:
            object_in_way = False
            shadow_ray_direction = vector3.unit_vector(light.center - closest_hit_point)
            shadow_ray = ray(closest_hit_point, shadow_ray_direction)
            min_dist = vector3.magnitude(light.center - closest_hit_point)
            # Checking Shadow ray against all objects
            for object in objects:
                hit_point = object.hit(shadow_ray)
                if hit_point:
                    distance = vector3.magnitude(hit_point - shadow_ray.origin)
                    if distance < min_dist:
                        min_dist = distance
                        object_in_way = True
                        break

            if not object_in_way:
                interacted_lights.append(light)
        
        intensity = 0
        for light in interacted_lights:
            if reflected_object is not None and reflected_object.type == 'Sky':
                diff_angle = reflected_object.normal() * object_normal
                if diff_angle > 0:
                    intensity += diff_angle
            # else:
            #     shadow_ray_direction = vector3.unit_vector(light.center - closest_hit_point)

            #     diff_angle = shadow_ray_direction * object_normal
            #     if diff_angle > 0:
            #         intensity += diff_angle
        if intensity > 1:
            intensity = 1

        if closest_object.material_type == "Lambertian":
            return color_to_return * intensity + color_to_return * 0.5, closest_object
        elif closest_object.material_type == "Reflective":
            return color_to_return * intensity * 0.5 + color_to_return * 0.5, closest_object

    return color(0,0,0), closest_object


def Thread_function(quadruple):
    start_x = quadruple[0]
    end_x = quadruple[1]
    start_y = quadruple[2]
    end_y = quadruple[3]

    global camera
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            col = color(0,0,0)
            frame_point = (camera.horizontal * (x-camera.canvas_size[0]/2)) + (camera.vertical * (camera.canvas_size[1]/2 - y)) + camera.canvas_origin

            ray_direction = vector3.unit_vector(frame_point - camera.origin)
            r = ray(camera.origin, ray_direction)
            
            col, _ = trace(r, 5)

            camera.canvas[y,x,2] = col.r * 255
            camera.canvas[y,x,1] = col.g * 255
            camera.canvas[y,x,0] = col.b * 255

    return camera.canvas
    

if __name__ == "__main__":

    bucket_size = (int(camera.canvas_size[0]/divs), int(camera.canvas_size[1]/divs))
    bucket_list = []
    for u in range(0,divs):
        for v in range(0,divs):
            bucket_list.append((bucket_size[0]*u,bucket_size[0]*(u+1),bucket_size[1]*v,bucket_size[1]*(v+1)))
    random.shuffle(bucket_list)

    start_time = time.time()

    temp_image = np.zeros((camera.canvas_size[1], camera.canvas_size[0],3), dtype=np.uint8)
    for b in range(0,int(len(bucket_list)/num_threads)):
        pool = multiprocessing.Pool(num_threads)
        if (b+1)==int(len(bucket_list)/num_threads):
            results = pool.map(Thread_function, bucket_list[b*num_threads:])
        else:
            results = pool.map(Thread_function, bucket_list[b*num_threads:(b+1)*num_threads])
        for result in results:
            temp_image += result

        final_image = cv2.resize(temp_image, (camera.render_size[0],camera.render_size[1]), interpolation=cv2.INTER_AREA)
        cv2.imshow('Area', final_image)
        cv2.waitKey(5)
        pool.close()

    print('Time taken ' + str(time.time()-start_time))

    # image_area = cv2.resize(final_image, camera.render_size, interpolation=cv2.INTER_AREA)
    # cv2.imshow('Area', image_area)
    total_saved_image = len(glob.glob('D:/vscode_workspaces/python_raytracer/render_output/*.jpg'))
    cv2.imwrite('D:/vscode_workspaces/python_raytracer/render_output/output_' + str(total_saved_image) + \
        '_size_' + str(render_size[0]) + 'x' + str(render_size[1]) + '_samples_' + str(samples) + \
        '.jpg', final_image)

    cv2.waitKey(0)