import cv2
import sys

# Appending utils to system paths
try:
    sys.path.append('./utils/')
except:
    pass

# Modules from utils directory
from trace_file import trace
from vector import vector3
from ray import ray
from color import color
from camera import camera
from objects import *
from lights import *
    

if __name__ == "__main__":

    # Defining list of objects
    objects = [
        sphere(vector3(-300.0,0.0,300.0), 100.0, color(0.5,0.5,0.5), material_type='Reflective'), 
        sphere(vector3(-150.0,0.0,150.0), 100.0, color(0.9,0.9,0.9), material_type='Reflective'), 
        sphere(vector3(0.0,0.0,0.0), 100.0, color(1.0,0.1,0.1), material_type='Lambertian'), 
        sphere(vector3(150.0,0.0,150.0), 100.0, color(0.1,0.1,1.0), material_type='Reflective'), 
        sphere(vector3(300.0,0.0,300.0), 100.0, color(0.1,1.0,0.1), material_type='Reflective'), 
        plane(vector3(0.0,-100.0, 0.0), vector3(0.0,1.0,0.0), color(1.0,1.0,1.0), material_type='Reflective'),
    ]

    # Defining list of lights
    lights = [
        pointLight(vector3(500.0, 500.0, -500.0), color(1.0, 1.0, 1.0), intensity=0.5),
        # directionalLight(vector3(0.0, 1000.0, 0.0), vector3(0.3, -0.7, 0), color(1.0, 1.0, 1.0), intensity=0.5),
    ]

    # Custom camera params
    render_size = (640, 480)
    samples = 1
    down_look_param = 0.15
    camera_forward = vector3(0, -down_look_param, 1-down_look_param)
    camera_right = vector3(1, 0, 0)
    camera_down = camera_forward % camera_right

    # Defining camera objects
    cam = camera(
        camera_origin=vector3(0.0,90.0,-400.0),
        camera_forward=camera_forward,
        camera_right=camera_right,
        camera_down=camera_down,
        fov=65,
        render_size=render_size,
        samples=samples
    )

    # Rendering loop
    for x in range(cam.canvas_size[0]):
        for y in range(cam.canvas_size[1]):

            frame_point = cam.canvas_origin + (cam.right * (x-cam.canvas_size[0]/2)) + (cam.down * (y-cam.canvas_size[1]/2))

            ray_direction = vector3.normalize(frame_point - cam.origin)
            r = ray(cam.origin, ray_direction)
            
            col = trace(r, objects, lights)

            cam.canvas[y,x,2] = col.r * 255
            cam.canvas[y,x,1] = col.g * 255
            cam.canvas[y,x,0] = col.b * 255

        if (x+1)%int(cam.canvas_size[0]/100) == 0 or (x+1) == cam.canvas_size[0]:
            image = cv2.resize(cam.canvas, render_size, interpolation=cv2.INTER_AREA)
            cv2.imshow('Render window', image)
            cv2.waitKey(20)

    # When render finished, press any key to exit
    cv2.waitKey(0)