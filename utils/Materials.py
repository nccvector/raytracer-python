from utils.Vector import Vector3

class StandardMaterial():
    def __init__(self, color, roughness, base_reflection):
        self.color = color
        self.roughness = roughness
        self.base_reflection = base_reflection