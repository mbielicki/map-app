import pygame
import pygame_gui
import sys

class Dog:
    def __init__(self, name, x, y, radius=20):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (0, 128, 255)  # Default blue color
        self.selected = False

class DogParkTracker:
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
            starting_height=4,
            manager=self.ui_manager
        )
        
        # Sidebar elements
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.SCREEN_WIDTH - 240, 50, 230, 30),
            manager=self.ui_manager,
            container=self.sidebar
        )
        self.name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.SCREEN_WIDTH - 240, 20, 230, 30),
            text="Dog Name:",
            manager=self.ui_manager,
            container=self.sidebar
        )
        
        self.x_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.SCREEN_WIDTH - 240, 130, 230, 30),
            manager=self.ui_manager,
            container=self.sidebar
        )
        self.x_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.SCREEN_WIDTH - 240, 100, 230, 30),
            text="X Coordinate:",
            manager=self.ui_manager,
            container=self.sidebar
        )
        
        self.y_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.SCREEN_WIDTH - 240, 210, 230, 30),
            manager=self.ui_manager,
            container=self.sidebar
        )
        self.y_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.SCREEN_WIDTH - 240, 180, 230, 30),
            text="Y Coordinate:",
            manager=self.ui_manager,
            container=self.sidebar
        )
        
        self.delete_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.SCREEN_WIDTH - 240, 260, 230, 50),
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
        running = True
        while running:
            time_delta = self.clock.tick(60)/1000.0
            
            # Event handling
            for event in pygame.event.get():
                # UI event handling
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.delete_button:
                        # Delete selected dog
                        if self.selected_dog:
                            self.dogs.remove(self.selected_dog)
                            self.selected_dog = None
                            self.update_sidebar()
                
                # Text input events
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if self.selected_dog:
                        if event.ui_element == self.name_input:
                            self.selected_dog.name = event.text
                        elif event.ui_element == self.x_input:
                            try:
                                self.selected_dog.x = float(event.text)
                            except ValueError:
                                pass
                        elif event.ui_element == self.y_input:
                            try:
                                self.selected_dog.y = float(event.text)
                            except ValueError:
                                pass
                
                # Pygame event handling
                if event.type == pygame.QUIT:
                    running = False
                
                # Panning view
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Check if clicking on a dog
                        world_x, world_y = self.screen_to_world_coords(event.pos[0], event.pos[1])
                        clicked_dog = self.get_dog_at_position(world_x, world_y)
                        
                        # Deselect previous dog and select new dog
                        if self.selected_dog:
                            self.selected_dog.selected = False
                        
                        self.selected_dog = clicked_dog
                        
                        if self.selected_dog:
                            self.selected_dog.selected = True
                            self.update_sidebar(self.selected_dog)
                            # Prepare for dragging
                            self.dragging = True
                            self.drag_offset_x = world_x - self.selected_dog.x
                            self.drag_offset_y = world_y - self.selected_dog.y
                        else:
                            # Start panning if no dog is selected
                            self.pan_start_x, self.pan_start_y = event.pos
                            self.update_sidebar()
                    
                    # Add a new dog with middle mouse button
                    elif event.button == 2:
                        world_x, world_y = self.screen_to_world_coords(event.pos[0], event.pos[1])
                        self.add_dog(f"Dog {len(self.dogs) + 1}", world_x, world_y)
                
                # Dragging
                if event.type == pygame.MOUSEMOTION:
                    if self.dragging and self.selected_dog:
                        # Move selected dog
                        world_x, world_y = self.screen_to_world_coords(event.pos[0], event.pos[1])
                        self.selected_dog.x = world_x - self.drag_offset_x
                        self.selected_dog.y = world_y - self.drag_offset_y
                        self.update_sidebar(self.selected_dog)
                    
                    # Panning view
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.selected_dog:
                        if hasattr(self, 'pan_start_x'):
                            dx = event.pos[0] - self.pan_start_x
                            dy = event.pos[1] - self.pan_start_y
                            self.view_x += dx
                            self.view_y += dy
                            self.pan_start_x, self.pan_start_y = event.pos
                
                # Stop dragging
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging = False
                
                # Zooming
                if event.type == pygame.MOUSEWHEEL:
                    # Zoom towards mouse cursor
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Calculate zoom factor
                    zoom_factor = 1.1 if event.y > 0 else 0.9
                    new_zoom = self.zoom * zoom_factor
                    
                    # Limit zoom
                    if 0.1 <= new_zoom <= 10:
                        # Adjust view to zoom towards cursor
                        self.view_x = mouse_x - (mouse_x - self.view_x) * zoom_factor
                        self.view_y = mouse_y - (mouse_y - self.view_y) * zoom_factor
                        self.zoom = new_zoom
                
                # Pass events to UI manager
                self.ui_manager.process_events(event)
            
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
    dog_park = DogParkTracker()
    dog_park.run()

if __name__ == "__main__":
    main()

# Dependencies:
# pip install pygame pygame_gui