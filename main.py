import pygame
import pygame_gui
import sys

from events import process_events
from app import App
from process_rtt import process_rtt

def loop(app: App):
    time_delta = app.clock.tick(60)/1000.0
    
    process_events(app)

    process_rtt(app)

    # Update UI manager
    app.ui_manager.update(time_delta)
    
    # Clear screen
    app.screen.fill((240, 240, 240))
    
    # Draw grid
    # Define grid spacing and color
    grid_spacing = 50  # Define grid spacing in world coordinates
    grid_color = (200, 200, 200)  # Light gray grid lines

    left_world_x, top_world_y = app.screen_to_world_coords(0, 0)
    right_world_x, bottom_world_y = app.screen_to_world_coords(app.SCREEN_WIDTH, app.SCREEN_HEIGHT)

    # Align the grid to the nearest grid line
    start_x = int(left_world_x // grid_spacing) * grid_spacing
    start_y = int(top_world_y // grid_spacing) * grid_spacing

    # Draw vertical lines
    x = start_x
    while x < right_world_x:
        screen_x, _ = app.world_to_screen_coords(x, 0)
        pygame.draw.line(app.screen, grid_color, (screen_x, 0), (screen_x, app.SCREEN_HEIGHT))
        x += grid_spacing

    # Draw horizontal lines
    y = start_y
    while y < bottom_world_y:
        _, screen_y = app.world_to_screen_coords(0, y)
        pygame.draw.line(app.screen, grid_color, (0, screen_y), (app.SCREEN_WIDTH, screen_y))
        y += grid_spacing

    # Draw anchors
    for anchor in app.anchors:
        # Convert anchor's world coordinates to screen coordinates
        screen_x, screen_y = app.world_to_screen_coords(anchor.x, anchor.y)
        
        # Determine anchor color (selected or default)
        color = (255, 100, 100) if anchor == app.selected_anchor else anchor.color
        
        # Draw anchor circle
        pygame.draw.circle(
            app.screen, 
            color, 
            (int(screen_x), int(screen_y)), 
            int(anchor.radius * app.zoom)
        )
        
        # Draw anchor name
        font = pygame.font.Font(None, int(20 * app.zoom))
        text = font.render(anchor.name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(int(screen_x), int(screen_y + anchor.radius * app.zoom + 15)))
        app.screen.blit(text, text_rect)
    
    # Draw nodes
    for node in app.nodes:
        if node.x is not None and node.y is not None:  # Ensure node position is valid
            screen_x, screen_y = app.world_to_screen_coords(node.x, node.y)
            
            pygame.draw.circle(
                app.screen, 
                node.color, 
                (int(screen_x), int(screen_y)), 
                int(node.radius * app.zoom)
            )
            
            font = pygame.font.Font(None, int(20 * app.zoom))
            text = font.render(node.name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(int(screen_x), int(screen_y + node.radius * app.zoom + 15)))
            app.screen.blit(text, text_rect)
    
    # Draw UI
    app.ui_manager.draw_ui(app.screen)
    
    # Update display
    pygame.display.update()



def main():
    app = App()
    
    while app.running:
        loop(app)

        
    # Quit the game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()