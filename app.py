import time
import pygame
import pygame_gui
import json
from anchor import Anchor
from node import Node


class App:
    def __init__(self):
        pygame.init()
        
        # Screen and view settings
        self.SCREEN_WIDTH = 1920 / 2
        self.SCREEN_HEIGHT = 1080 - 300
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("RTLS")

        
        self.start_time = time.time()
        self.running = True
        
        # RTT
        self.rtt_buffer = ''
        self.rtt = None
        
        # View translation and scaling
        self.view_x = 0
        self.view_y = 0
        self.zoom = 1.0
        
        # Dragging and panning
        self.dragging = False
        self.panning = False

        self.drag_start_x = 0
        self.drag_start_y = 0
        self.pan_start_x = 0
        self.pan_start_y = 0

        self.nodes = []
        
        self.init_anchors()
        self.init_sidebar()
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        
    def init_anchors(self):
        self.anchors = []
        self.selected_anchor = None

        # Load anchors from JSON file
        try:
            with open('data/anchor-config.json', 'r') as file:
                anchor_data = json.load(file)
                for anchor_entry in anchor_data:
                    name = anchor_entry.get("name")
                    x = anchor_entry.get("x")
                    y = anchor_entry.get("y")
                    if name and x is not None and y is not None:
                        self.add_anchor(name, x, y)
        except FileNotFoundError:
            print("Anchor configuration file not found.")
        except json.JSONDecodeError as e:
            print(f"Error decoding anchor configuration file: {e}")

    def init_sidebar(self):
        
        # UI Manager
        self.ui_manager = pygame_gui.UIManager((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Sidebar
        self.SIDEBAR_WIDTH = 250
        self.SIDEBAR_X = self.SCREEN_WIDTH - self.SIDEBAR_WIDTH

        sidebar_rect = pygame.Rect(self.SIDEBAR_X, 0, self.SIDEBAR_WIDTH, self.SCREEN_HEIGHT)
        self.sidebar = pygame_gui.elements.UIPanel(
            relative_rect=sidebar_rect,
            starting_height=1,
            manager=self.ui_manager
        )
        
        # Sidebar elements
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(50, 50, 100, 30),
            manager=self.ui_manager,
            container=self.sidebar
        )
        self.name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 20, 100, 30),
            text="Anchor Name:",
            manager=self.ui_manager,
            container=self.sidebar
        )
        
        self.x_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(50, 120, 100, 30),
            manager=self.ui_manager,
            container=self.sidebar
        )
        self.x_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 90, 100, 30),
            text="X Coordinate:",
            manager=self.ui_manager,
            container=self.sidebar
        )
        
        self.y_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(50, 190, 100, 30),
            manager=self.ui_manager,
            container=self.sidebar
        )
        self.y_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 160, 100, 30),
            text="Y Coordinate:",
            manager=self.ui_manager,
            container=self.sidebar
        )
        
        self.delete_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(50, 230, 100, 30),
            text="Delete",
            manager=self.ui_manager,
            container=self.sidebar
        )

        self.rtt_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(50, 300, 100, 30),
            text="Start RTT",
            manager=self.ui_manager,
            container=self.sidebar
        )
        self.update_sidebar()

    def now(self) -> str:
        return f'{(time.time() - self.start_time):.3f}'

    def update_nodes(self, info: dict):
        """
        Update nodes with distance information and ensure multilateration is performed in strict sequence.
        """
        # Update or add the node from the info
        for node in self.nodes:
            if node.name == info['from']:
                node.add_distance(info)
                break
        else:
            # Create a new node if it doesn't already exist
            new_node = Node(info['from'])
            new_node.add_distance(info)
            self.nodes.append(new_node)

        # Multilateration logic with strict order
        node_dict = {node.name: node for node in self.nodes}

        # Multilaterate nodes in strict order
        node_99 = node_dict.get("99")
        node_98 = node_dict.get("98")

        if node_99:
            print("Multilaterating Node 99...")
            node_99.multilaterate(self.anchors, self.nodes)

        # Only multilaterate Node 98 if Node 99 has a valid position
        if node_98 and node_99 and node_99.x is not None and node_99.y is not None:
            print("Multilaterating Node 98...")
            node_98.multilaterate(self.anchors, self.nodes)
        elif node_98:
            print("Skipping Node 98 multilateration: Node 99 has not been resolved yet.")

    def add_anchor(self, name, x, y):
        new_anchor = Anchor(name, x, y)
        self.anchors.append(new_anchor)
        print(f"Anchor added: {name} at ({x}, {y})")
        
    def screen_to_world_coords(self, screen_x: float, screen_y: float) -> tuple[float, float]:
        """Convert screen coordinates to world coordinates"""
        world_x = screen_x / self.zoom + self.view_x
        world_y = screen_y / self.zoom + self.view_y 
        return world_x, world_y
    
    def world_to_screen_coords(self, world_x: float, world_y: float) -> tuple[float, float]:
        """Convert world coordinates to screen coordinates"""
        screen_x = (world_x - self.view_x) * self.zoom
        screen_y = (world_y - self.view_y) * self.zoom
        return screen_x, screen_y
    
    def get_anchor_at_position(self, x, y):
        """Find an anchor at the given world coordinates"""
        for anchor in self.anchors:
            # Calculate distance from click to anchor center
            dist = ((x - anchor.x) ** 2 + (y - anchor.y) ** 2) ** 0.5
            if dist <= anchor.radius / self.zoom:
                return anchor
        return None
    
    def update_sidebar(self, anchor=None):
        """Update sidebar with selected anchor's information"""
        if anchor:
            self.name_input.set_text(anchor.name)
            self.x_input.set_text(str(int(anchor.x)))
            self.y_input.set_text(str(int(anchor.y)))
            self.name_input.enable()
            self.x_input.enable()
            self.y_input.enable()
            self.delete_button.enable()
        else:
            self.name_input.set_text("")
            self.x_input.set_text("")
            self.y_input.set_text("")
            self.name_input.disable()
            self.x_input.disable()
            self.y_input.disable()
            self.delete_button.disable()
 
 
    def log_node_position(self, node_name, x, y, elapsed_time):
        """Logs calculated node position and elapsed time to a file."""
        log_entry = {
            "node": node_name,
            "x": x,
            "y": y,
            "time": f"{elapsed_time:.3f}"
        }
        with open("data/node_positions.log", "a") as log_file: 
            log_file.write(json.dumps(log_entry) + "\n")
        
    