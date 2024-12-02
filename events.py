import pygame
import pygame_gui

def process_events(game):
    for event in pygame.event.get():
        
        # Pygame event handling
        if event.type == pygame.QUIT:
            game.running = False
            break
        
        # UI event handling
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == game.delete_button:
                # Delete selected dog
                if game.selected_dog:
                    game.dogs.remove(game.selected_dog)
                    game.selected_dog = None
                    game.update_sidebar()
        
        # Text input events
        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if game.selected_dog:
                if event.ui_element == game.name_input:
                    game.selected_dog.name = event.text
                elif event.ui_element == game.x_input:
                    try:
                        game.selected_dog.x = float(event.text)
                    except ValueError:
                        pass
                elif event.ui_element == game.y_input:
                    try:
                        game.selected_dog.y = float(event.text)
                    except ValueError:
                        pass
        
        
        # Panning view
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if clicking on a dog
                world_x, world_y = game.screen_to_world_coords(event.pos[0], event.pos[1])
                clicked_dog = game.get_dog_at_position(world_x, world_y)
                
                # Deselect previous dog and select new dog
                if game.selected_dog:
                    game.selected_dog.selected = False
                
                game.selected_dog = clicked_dog
                
                if game.selected_dog:
                    game.selected_dog.selected = True
                    game.update_sidebar(game.selected_dog)
                    # Prepare for dragging
                    game.dragging = True
                    game.drag_offset_x = world_x - game.selected_dog.x
                    game.drag_offset_y = world_y - game.selected_dog.y
                else:
                    # Start panning if no dog is selected
                    game.pan_start_x, game.pan_start_y = event.pos
                    game.update_sidebar()
            
            # Add a new dog with middle mouse button
            elif event.button == 2:
                world_x, world_y = game.screen_to_world_coords(event.pos[0], event.pos[1])
                game.add_dog(f"Dog {len(game.dogs) + 1}", world_x, world_y)
        
        # Dragging
        elif event.type == pygame.MOUSEMOTION:
            if game.dragging and game.selected_dog:
                # Move selected dog
                world_x, world_y = game.screen_to_world_coords(event.pos[0], event.pos[1])
                game.selected_dog.x = world_x - game.drag_offset_x
                game.selected_dog.y = world_y - game.drag_offset_y
                game.update_sidebar(game.selected_dog)
            
        # Panning view
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game.selected_dog:
            if hasattr(game, 'pan_start_x'):
                dx = event.pos[0] - game.pan_start_x
                dy = event.pos[1] - game.pan_start_y
                game.view_x += dx
                game.view_y += dy
                game.pan_start_x, game.pan_start_y = event.pos
        
        # Stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                game.dragging = False
        
        # Zooming
        elif event.type == pygame.MOUSEWHEEL:
            # Zoom towards mouse cursor
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Calculate zoom factor
            zoom_factor = 1.1 if event.y > 0 else 0.9
            new_zoom = game.zoom * zoom_factor
            
            # Limit zoom
            if 0.1 <= new_zoom <= 10:
                # Adjust view to zoom towards cursor
                game.view_x = mouse_x - (mouse_x - game.view_x) * zoom_factor
                game.view_y = mouse_y - (mouse_y - game.view_y) * zoom_factor
                game.zoom = new_zoom
        
        # Pass events to UI manager
        game.ui_manager.process_events(event)
    