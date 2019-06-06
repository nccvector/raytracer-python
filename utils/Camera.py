import math
import numpy as np
from utils.Vector import Vector3

class Camera():
    def __init__(self, 
                position=Vector3(0,0,0),
                forward=Vector3(0,0,1),
                right=Vector3(1,0,0),
                down=Vector3(0,-1,0),
                fov=65, 
                render_size=(640,480)
                ):

        self.position = position
        self.forward = forward
        self.right = right
        self.down = down
        self.fov = fov
        self.render_size = render_size

        self.canvas = np.zeros((self.render_size[1], self.render_size[0], 3), dtype=np.uint8)
        self.canvas_distance = (self.render_size[0]/2)/math.tan(math.radians(self.fov/2))
        self.canvas_origin = self.position + (self.forward*self.canvas_distance)