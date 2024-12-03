import pygame
import pygame_gui
from dog import Dog


class App:
    def __init__(self):
        pygame.init()
        
        # Screen and view settings
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Dog Park Tracker")

        
        self.running = True
        
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
        
        # Dogs management
        self.dogs = []
        self.selected_dog = None
        
        # UI Manager
        self.ui_manager = pygame_gui.UIManager((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Sidebar
        sidebar_rect = pygame.Rect(self.SCREEN_WIDTH - 250, 0, 250, self.SCREEN_HEIGHT)
        self.sidebar = pygame_gui.elements.UIPanel(
            relative_rect=sidebar_rect,
            starting_height=1,
            manager=self.ui_manager
        )
        
        # Sidebar elements
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(50, 50, 50, 30),
            manager=self.ui_manager,
            container=self.sidebar
        )
        self.name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 20, 50, 30),
            text="Dog Name:",
            manager=self.ui_manager,
            container=self.sidebar
        )
        
        self.x_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(50, 100, 50, 30),
            manager=self.ui_manager,
            container=self.sidebar
        )
        self.x_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 70, 50, 30),
            text="X Coordinate:",
            manager=self.ui_manager,
            container=self.sidebar
        )
        
        self.y_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(50, 150, 50, 30),
            manager=self.ui_manager,
            container=self.sidebar
        )
        self.y_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 120, 50, 30),
            text="Y Coordinate:",
            manager=self.ui_manager,
            container=self.sidebar
        )
        
        self.delete_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(50, 200, 50, 30),
            text="Delete Selected Dog",
            manager=self.ui_manager,
            container=self.sidebar
        )
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        
        # Dragging state
        self.dragging = False
        
    def add_dog(self, name, x, y):
        """Add a new dog to the park"""
        new_dog = Dog(name, x, y)
        self.dogs.append(new_dog)
        
    def screen_to_world_coords(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        world_x = (screen_x + self.view_x) / self.zoom
        world_y = (screen_y + self.view_y) / self.zoom
        return world_x, world_y
    
    def world_to_screen_coords(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        screen_x = world_x * self.zoom - self.view_x
        screen_y = world_y * self.zoom - self.view_y
        return screen_x, screen_y
    
    def get_dog_at_position(self, x, y):
        """Find a dog at the given world coordinates"""
        for dog in self.dogs:
            # Calculate distance from click to dog center
            dist = ((x - dog.x) ** 2 + (y - dog.y) ** 2) ** 0.5
            if dist <= dog.radius / self.zoom:
                return dog
        return None
    
    def update_sidebar(self, dog=None):
        """Update sidebar with selected dog's information"""
        if dog:
            self.name_input.set_text(dog.name)
            self.x_input.set_text(str(int(dog.x)))
            self.y_input.set_text(str(int(dog.y)))
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
 
    