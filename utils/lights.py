class pointLight():
    def __init__(self, position, color, intensity=1):
        self.type = 'Point'
        self.position = position
        self.color = color
        self.intensity = intensity

class directionalLight():
    def __init__(self, position, direction, color, intensity=1):
        self.type = 'Directional'
        self.position = position
        self.direction = direction
        self.color = color
        self.intensity = intensity

