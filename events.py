import pygame
import pygame_gui

def process_events(app):
    for event in pygame.event.get():
        
        # Pygame event handling
        if event.type == pygame.QUIT:
            app.running = False
            break
        
        # UI event handling
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == app.delete_button:
                # Delete selected dog
                if app.selected_dog:
                    app.dogs.remove(app.selected_dog)
                    app.selected_dog = None
                    app.update_sidebar()
        
        # Text input events
        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if app.selected_dog:
                if event.ui_element == app.name_input:
                    app.selected_dog.name = event.text
                elif event.ui_element == app.x_input:
                    try:
                        app.selected_dog.x = float(event.text)
                    except ValueError:
                        pass
                elif event.ui_element == app.y_input:
                    try:
                        app.selected_dog.y = float(event.text)
                    except ValueError:
                        pass
        
        
        # Panning view
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if clicking on a dog
                world_x, world_y = app.screen_to_world_coords(event.pos[0], event.pos[1])
                clicked_dog = app.get_dog_at_position(world_x, world_y)
                
                # Deselect previous dog and select new dog
                if app.selected_dog:
                    app.selected_dog.selected = False
                
                app.selected_dog = clicked_dog
                
                if app.selected_dog:
                    app.selected_dog.selected = True
                    app.update_sidebar(app.selected_dog)
                    # Prepare for dragging
                    app.dragging = True
                    app.drag_offset_x = world_x - app.selected_dog.x
                    app.drag_offset_y = world_y - app.selected_dog.y
                else:
                    # Start panning if no dog is selected
                    app.pan_start_x, app.pan_start_y = event.pos
                    app.update_sidebar()
            
            # Add a new dog with middle mouse button
            elif event.button == 2:
                world_x, world_y = app.screen_to_world_coords(event.pos[0], event.pos[1])
                app.add_dog(f"Dog {len(app.dogs) + 1}", world_x, world_y)
        
        # Dragging
        elif event.type == pygame.MOUSEMOTION:
            if app.dragging and app.selected_dog:
                # Move selected dog
                world_x, world_y = app.screen_to_world_coords(event.pos[0], event.pos[1])
                app.selected_dog.x = world_x - app.drag_offset_x
                app.selected_dog.y = world_y - app.drag_offset_y
                app.update_sidebar(app.selected_dog)
            
        # Panning view
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not app.selected_dog:
            if hasattr(app, 'pan_start_x'):
                dx = event.pos[0] - app.pan_start_x
                dy = event.pos[1] - app.pan_start_y
                app.view_x += dx
                app.view_y += dy
                app.pan_start_x, app.pan_start_y = event.pos
        
        # Stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                app.dragging = False
        
        # Zooming
        elif event.type == pygame.MOUSEWHEEL:
            # Zoom towards mouse cursor
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Calculate zoom factor
            zoom_factor = 1.1 if event.y > 0 else 0.9
            new_zoom = app.zoom * zoom_factor
            
            # Limit zoom
            if 0.1 <= new_zoom <= 10:
                # Adjust view to zoom towards cursor
                app.view_x = mouse_x - (mouse_x - app.view_x) * zoom_factor
                app.view_y = mouse_y - (mouse_y - app.view_y) * zoom_factor
                app.zoom = new_zoom
        
        # Pass events to UI manager
        app.ui_manager.process_events(event)
    