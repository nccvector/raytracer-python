import numpy as np
import cv2
import math

image_shape = (480,640,3)

image = np.zeros(image_shape,dtype=np.uint8)

class vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def unit_vector(v):
    k = 1/math.sqrt(v.x**2 + v.y**2 + v.z**2)
    return vector3(v.x*k,v.y*k,v.z*k)
def add_vector(v1, v2):
    return vector3(v1.x+v2.x,v1.y+v2.y,v1.z+v2.z)
def subtract_vector(v1, v2):
    return vector3(v1.x-v2.x,v1.y-v2.y,v1.z-v2.z)
def magnitude(v):
    return math.sqrt(v.x**2 + v.y**2 + v.z**2)
def product(v, n):
    return vector3(v.x*n,v.y*n,v.z*n)
def dot_product(v1, v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z
def cross_product(v1, v2):
    return vector3(v1.y*v2.z-v1.z*v2.y,-(v1.x*v2.z-v1.z-v2.x),v1.x*v2.y-v1.y-v2.x)

class ray:
    def __init__(self, originVector, directionVector):
        self.origin = originVector
        self.direction = directionVector

def hit_sphere(center, radius, r):
    oc = subtract_vector(center, r.origin)
    a = dot_product(r.direction, r.direction)
    b = 2.0 * dot_product(oc, r.direction)
    c = dot_product(oc, oc) - radius**2
    root = b**2 - 4*a*c
    if root>0:
        return product(r.direction,root)
    return None

ray_origin = vector3(0,0,0)
frame_origin = vector3(0,0,100)
light_origin = vector3(0,500,200)
for x in range(0, image_shape[1]):
    for y in range(0, image_shape[0]):
        frame_point = vector3(x-(image_shape[1]/2), y-(image_shape[0]/2), frame_origin.z)
        ray_direction = unit_vector(subtract_vector(frame_point,ray_origin))
        r = ray(ray_origin, ray_direction)
        next_point = hit_sphere(vector3(0,0,200),100,r)
        if next_point is not None:
            ray_direction = unit_vector(subtract_vector(light_origin,next_point))
            r = ray(next_point, ray_direction)
            next_next_point = hit_sphere(light_origin,0.001,r)
            if next_next_point is not None:
                diff = subtract_vector(light_origin, next_point)
                intensity = (magnitude(diff)/100000)**2
                print(intensity)
                if intensity > 1:
                    intensity = 1
                intensity = vector3(intensity, intensity, intensity)
                col = vector3(0.25,0,0)
                col = add_vector(col, intensity)
            else:
                col = vector3(0,0,0)
        else:
            col = vector3(1,1,1)
        image[y,x,2] = col.x * 255
        image[y,x,1] = col.y * 255
        image[y,x,0] = col.z * 255

cv2.imshow('Rendered image', image)
cv2.waitKey(0)