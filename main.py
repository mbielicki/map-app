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