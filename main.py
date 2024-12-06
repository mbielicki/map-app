import pygame
import pygame_gui
import sys

from drawing import draw_anchors, draw_grid, draw_nodes
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
    
    draw_grid(app)
    draw_anchors(app)
    draw_nodes(app)
    
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