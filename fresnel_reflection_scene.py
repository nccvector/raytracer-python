import cv2

# Modules from utils directory
from utils.Tracer import RecursiveTrace
from utils.Vector import Vector3
from utils.Ray import Ray
from utils.Color import Color
from utils.Camera import Camera
from utils.Objects import *
from utils.Lights import *
    

if __name__ == "__main__":

    # Defining list of objects
    reflectness = 1
    objects = [
        Sphere(Vector3(-300.0,0.0,300.0), 100.0, Color(0.5,0.5,0.5), material_type='Reflective', reflectness=reflectness), 
        Sphere(Vector3(-150.0,0.0,150.0), 100.0, Color(0.9,0.9,0.9), material_type='Reflective', reflectness=reflectness), 
        Sphere(Vector3(0.0,0.0,0.0), 100.0, Color(1.0,0.1,0.1), material_type='Reflective', reflectness=reflectness), 
        Sphere(Vector3(150.0,0.0,150.0), 100.0, Color(0.1,0.1,1.0), material_type='Reflective', reflectness=reflectness), 
        Sphere(Vector3(300.0,0.0,300.0), 100.0, Color(0.1,1.0,0.1), material_type='Reflective', reflectness=reflectness), 
        Plane(Vector3(0.0,-100.0, 0.0), Vector3(0.0,1.0,0.0), Color(1.0,1.0,1.0), material_type='Reflective', reflectness=reflectness),
    ]

    # Defining list of lights
    lights = [
        PointLight(Vector3(500.0, 500.0, -500.0), Color(1.0, 1.0, 1.0), intensity=0.5),
        DirectionalLight(Vector3(0.0, 1000.0, 0.0), Vector3(0.3, -0.7, 0), Color(1.0, 1.0, 1.0), intensity=0.5),
    ]

    # Custom Camera params
    render_size = (640, 480)
    samples = 1
    down_look_param = 0.15
    camera_forward = Vector3(0, -down_look_param, 1-down_look_param)
    camera_right = Vector3(1, 0, 0)
    camera_down = camera_forward % camera_right

    # Defining Camera objects
    cam = Camera(
        camera_origin=Vector3(0.0,90.0,-400.0),
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

            ray_direction = Vector3.normalize(frame_point - cam.origin)
            r = Ray(cam.origin, ray_direction)
            
            col = RecursiveTrace(r, objects, lights, bounces=5, energy=1) # Recursive Reflective trace

            cam.canvas[y,x,2] = col.r * 255
            cam.canvas[y,x,1] = col.g * 255
            cam.canvas[y,x,0] = col.b * 255

        if (x+1)%int(cam.canvas_size[0]/100) == 0 or (x+1) == cam.canvas_size[0]:
            image = cv2.resize(cam.canvas, render_size, interpolation=cv2.INTER_AREA)
            cv2.imshow('Render window', image)
            cv2.waitKey(20)

    # When render finished, press any key to exit
    cv2.waitKey(0)

    # Uncomment next line to save image after render
    # cv2.imwrite('./output.jpg', image)