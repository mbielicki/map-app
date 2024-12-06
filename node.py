import numpy as np

class Node:
    def __init__(self, name, radius=20):
        self.name = name
        self.x = None
        self.y = None
        self.radius = radius
        self.color = (0, 128, 255)  # Default blue color

        self.distances = {}

    def add_distance(self, info: dict, anchors: list):
        # Find the anchor object based on the name in `info['to']`
        anchor = next((a for a in anchors if a.name == info['to']), None)
        if anchor:
            self.distances[anchor] = float(info['dist'])
            self.trilaterate()
        else:
            print(f"Anchor {info['to']} not found.")

    def trilaterate(self):
        if len(self.distances) < 3:
            # Not enough anchors to trilaterate
            self.x, self.y = None, None
            return

        # Extract the first three anchors and their distances
        anchors = list(self.distances.keys())
        try:
            p1 = np.array((anchors[0].x, anchors[0].y))
            p2 = np.array((anchors[1].x, anchors[1].y))
            p3 = np.array((anchors[2].x, anchors[2].y))
            d1, d2, d3 = self.distances[anchors[0]], self.distances[anchors[1]], self.distances[anchors[2]]

            # Calculate intermediate variables
            ex = (p2 - p1) / np.linalg.norm(p2 - p1)
            i = np.dot(ex, p3 - p1)
            ey = (p3 - p1 - i * ex) / np.linalg.norm(p3 - p1 - i * ex)
            d = np.linalg.norm(p2 - p1)
            j = np.dot(ey, p3 - p1)

            # Calculate x, y coordinates relative to the reference frame defined by p1, p2, p3
            x = (d1**2 - d2**2 + d**2) / (2 * d)
            y = (d1**2 - d3**2 + i**2 + j**2) / (2 * j) - (i / j) * x

            # Convert back to absolute coordinates
            final_pos = p1 + x * ex + y * ey
            self.x, self.y = final_pos[0], final_pos[1]

        except Exception as e:
            # Handle calculation errors gracefully
            print(f"Trilateration failed: {e}")
            self.x, self.y = None, None
        