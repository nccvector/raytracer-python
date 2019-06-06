from cv2 import cv2
import numpy as np
import random
import multiprocessing

# Modules from utils directory
from utils.Tracer import Trace
from utils.Vector import Vector3
from utils.Ray import Ray
from utils.Camera import Camera
from utils.Objects import *
from utils.Lights import PointLight
from utils.Materials import *

sphere_mat = StandardMaterial(
                                color=Vector3(0.8, 0.3, 0.3),
                                roughness=0.3,
                                base_reflection=0.3
                                )   
floor_mat = StandardMaterial(
                                color=Vector3(0.6, 0.6, 0.6),
                                roughness=1.00,
                                base_reflection=0.3
                                ) 

# Defining list of objects
floor = Plane(
            position=Vector3(0.0,-30.0, 0.0),
            normal=Vector3(0.0,1.0,0.0), 
            material=floor_mat
            )

wall = Plane(
            position=Vector3(-50.0,0.0, 0.0),
            normal=Vector3(1.0,0.0,0.0), 
            material=floor_mat
            )

objects = [
    floor,
    wall,
    Sphere(position=Vector3(0.0,0.0,0.0), radius=30.0, material=sphere_mat), 
    PointLight(position=Vector3(0,0,0), radius=1000, color=Vector3(1,1,1))
]

# Custom Camera params
render_size = (640, 480)

camera_position = Vector3(0,0,-100)
look_at_position = Vector3(0,0,100)
forward = Vector3(0,0,1)
right = Vector3.cross(forward,floor.normal)
down = Vector3.cross(forward,right)

# Defining Camera objects
cam = Camera(
    position=camera_position,
    forward=forward,
    right=right,
    down=down,
    fov=90,
    render_size=render_size,
)

# Tracing parameters
bounces = 3
antialiasing_samples = 1
bounce_samples = 5
energy = 2

def color_from_trace(x, y):
    # Getting coordinate on canvas
    frame_point = cam.canvas_origin + (cam.right * (cam.render_size[0]/2 - x) + (cam.down * (y-cam.render_size[1]/2)))

    # initializing total color with ambient color
    final_color = Vector3(0.1,0.1,0.1)

    # Creating initial ray
    r = Ray(cam.position, Vector3.normalize(frame_point-cam.position))
    ret_col = Trace(r, objects, bounce_samples, bounces=bounces)

    if ret_col is not None:
        final_color += ret_col
    
    # Clipping total color
    final_color.x = 1 if final_color.x > 1 else final_color.x
    final_color.y = 1 if final_color.y > 1 else final_color.y
    final_color.z = 1 if final_color.z > 1 else final_color.z

    cam.canvas[y,x,2] = final_color.x * 255
    cam.canvas[y,x,1] = final_color.y * 255
    cam.canvas[y,x,0] = final_color.z * 255

    return cam.canvas

def Thread_function(quadruple):
    start_x = quadruple[0]
    end_x = quadruple[1]
    start_y = quadruple[2]
    end_y = quadruple[3]
    # Rendering loop
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            results = color_from_trace(x, y)

    return results

if __name__ == "__main__":
    num_threads = 10
    divs = 10

    bucket_size = (int(cam.render_size[0]/divs), int(cam.render_size[1]/divs))
    bucket_list = []
    for u in range(0,divs):
        for v in range(0,divs):
            bucket_list.append((bucket_size[0]*u,bucket_size[0]*(u+1),bucket_size[1]*v,bucket_size[1]*(v+1)))
    random.shuffle(bucket_list)

    temp_image = np.zeros((cam.render_size[1], cam.render_size[0],3), dtype=np.uint8)
    for b in range(0,int(len(bucket_list)/num_threads)):
        pool = multiprocessing.Pool(num_threads)
        if (b+1)==int(len(bucket_list)/num_threads):
            results = pool.map(Thread_function, bucket_list[b*num_threads:])
        else:
            results = pool.map(Thread_function, bucket_list[b*num_threads:(b+1)*num_threads])
        for result in results:
            temp_image += result

        cv2.imshow('Area', temp_image)
        cv2.waitKey(5)
        pool.close()

    # When render finished, press any key to exit
    cv2.waitKey(0)

    # Uncomment next line to save image after render
    # cv2.imwrite('./output.jpg', image)