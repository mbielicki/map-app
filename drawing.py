import pygame

from app import App

def draw_grid(app: App):
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