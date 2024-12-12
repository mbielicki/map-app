import numpy as np
from scipy.optimize import least_squares
from scipy.optimize import minimize


class Node:
    def __init__(self, name, radius=20):
        self.name = name
        self.x = None
        self.y = None
        self.radius = radius
        self.color = (0, 128, 255)  # Default blue color
        self.distances = {}

    def add_distance(self, info: dict):
        target_name = info.get('to')
        distance = info.get('distance') or info.get('dist')  # Handle both 'distance' and 'dist' keys

        if distance is None:
            print(f"Error: 'distance' key not found in info for node {self.name}")
            return  # Exit the function if distance is not found

        # Add or update the distance for the target node/anchor
        self.distances[target_name] = float(distance)  # Convert to float if necessary

    def multilaterate(self, anchors: list, other_nodes: list) -> bool:
        # Collect all points and distances
        points = []
        distances = []

        # Map anchor names to coordinates
        anchor_dict = {anchor.name: anchor for anchor in anchors}
        node_dict = {node.name: node for node in other_nodes if node.x is not None and node.y is not None}

        for target_name, dist in self.distances.items():
            if target_name in anchor_dict:  # It's an anchor
                anchor = anchor_dict[target_name]
                points.append((anchor.x, anchor.y))
                distances.append(dist)
            elif target_name in node_dict:  # It's another node
                node = node_dict[target_name]
                points.append((node.x, node.y))
                distances.append(dist)

        if len(points) < 3:
            print(f"Multilateration failed for {self.name}: Not enough valid points.")
            self.x = self.y = None
            return False

        # Objective function for optimization
        def objective(pos):
            px, py = pos
            return sum(
                (np.sqrt((px - x) ** 2 + (py - y) ** 2) - d) ** 2
                for (x, y), d in zip(points, distances)
            )

        # Initial guess for the position
        initial_guess = (0, 0)

        # Optimize using scipy
        result = minimize(objective, initial_guess, method='L-BFGS-B')

        if result.success:
            self.x, self.y = result.x
            return True
        else:
            print(f"Multilateration failed for {self.name}: {result.message}")
            self.x = self.y = None
            return False