class Node:
    def __init__(self, name, radius=20):
        self.name = name
        self.x = None
        self.y = None
        self.radius = radius
        self.color = (0, 128, 255)  # Default blue color

        self.distances = {}

    def add_distance(self, info: dict):
        self.distances[info['to']] = info['dist']
        # TODO distance data timeout

        self.trilaterate()

    def trilaterate(self):
        """
        Try to trilaterate the position of the node given the distances
        measured from other nodes.

        If the node can be trilaterated, self.x and self.y are set to the
        calculated coordinates. Otherwise, both are set to None.
        """
        # TODO trilaterate
        pass
        