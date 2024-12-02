import pygame
import pygame_gui
import sys

from events import process_events

# Generated with prompt:

# Write a Python app that displays the location of dogs in a park. Dogs are shown as circles labeled with names. The app must have the following functionalities:
# 1. Pan the view with the mouse.
# 2. Zoom in and out using the mouse wheel.
# 3. Add a dog.
# 4. Select a dog by clicking on it, the dog should change color to show that it is selected.
# 5. Show selected dog's properties on a sidebar as editable fields (coordinates and name).
# 6. Move a dog by dragging and dropping.
# 7. Delete selected dog.

class Dog:
    def __init__(self, name, x, y, radius=20):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (0, 128, 255)  # Default blue color
        self.selected = False

class App:
    def __init__(self):
        pygame.init()
        
        # Screen and view settings
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Dog Park Tracker")
        
        # View translation and scaling
        self.view_x = 0
        self.view_y = 0
        self.zoom = 1.0
        
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
        world_x = (screen_x - self.view_x) / self.zoom
        world_y = (screen_y - self.view_y) / self.zoom
        return world_x, world_y
    
    def world_to_screen_coords(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        screen_x = world_x * self.zoom + self.view_x
        screen_y = world_y * self.zoom + self.view_y
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
 
    def run(self):
        """Main game loop"""
        self.running = True
        while self.running:
            time_delta = self.clock.tick(60)/1000.0
            
            process_events(self)

            # Update UI manager
            self.ui_manager.update(time_delta)
            
            # Clear screen
            self.screen.fill((240, 240, 240))
            
            # Draw dogs
            for dog in self.dogs:
                # Convert dog's world coordinates to screen coordinates
                screen_x, screen_y = self.world_to_screen_coords(dog.x, dog.y)
                
                # Determine dog color (selected or default)
                color = (255, 100, 100) if dog.selected else dog.color
                
                # Draw dog circle
                pygame.draw.circle(
                    self.screen, 
                    color, 
                    (int(screen_x), int(screen_y)), 
                    int(dog.radius * self.zoom)
                )
                
                # Draw dog name
                font = pygame.font.Font(None, int(20 * self.zoom))
                text = font.render(dog.name, True, (0, 0, 0))
                text_rect = text.get_rect(center=(int(screen_x), int(screen_y + dog.radius * self.zoom + 15)))
                self.screen.blit(text, text_rect)
            
            # Draw UI
            self.ui_manager.draw_ui(self.screen)
            
            # Update display
            pygame.display.update()
        
        # Quit the game
        pygame.quit()
        sys.exit()

def main():
    dog_park = App()
    dog_park.run()

if __name__ == "__main__":
    main()

# Dependencies:
# pip install pygame pygame_gui