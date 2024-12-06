class Anchor:
    def __init__(self, name, x, y, radius=20):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (24, 116, 152)  # Default blue color
        self.color_selected = (235, 83, 83)  # Red color
