import math
import numpy as np
from utils.Vector import Vector3

class Camera():
    def __init__(self, 
                camera_origin=Vector3(0,0,0),
                camera_forward=Vector3(0,0,1),
                camera_right=Vector3(1,0,0),
                camera_down=Vector3(0,-1,0), 
                fov=65, 
                render_size=(640,480), 
                samples=1
                ):

        self.origin = camera_origin
        self.forward = camera_forward
        self.right = camera_right
        self.down = camera_down
        self.fov = fov

        self.render_size = render_size
        self.canvas_size = (self.render_size[0]*samples, self.render_size[1]*samples, 3)
        self.canvas = np.zeros((self.canvas_size[1], self.canvas_size[0], 3), dtype=np.uint8)

        self.canvas_distance = (self.canvas_size[0]/2)/math.tan(math.radians(self.fov/2))
        self.canvas_origin = self.origin + (self.forward * self.canvas_distance)