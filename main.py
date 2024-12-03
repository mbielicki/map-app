import pygame
import pygame_gui
import sys

from events import process_events
from app import App

def loop(app: App):
    time_delta = app.clock.tick(60)/1000.0
    
    process_events(app)

    # Update UI manager
    app.ui_manager.update(time_delta)
    
    # Clear screen
    app.screen.fill((240, 240, 240))
    
    # Draw dogs
    for dog in app.dogs:
        # Convert dog's world coordinates to screen coordinates
        screen_x, screen_y = app.world_to_screen_coords(dog.x, dog.y)
        
        # Determine dog color (selected or default)
        color = (255, 100, 100) if dog == app.selected_dog else dog.color
        
        # Draw dog circle
        pygame.draw.circle(
            app.screen, 
            color, 
            (int(screen_x), int(screen_y)), 
            int(dog.radius * app.zoom)
        )
        
        # Draw dog name
        font = pygame.font.Font(None, int(20 * app.zoom))
        text = font.render(dog.name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(int(screen_x), int(screen_y + dog.radius * app.zoom + 15)))
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