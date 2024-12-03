import pygame
import pygame_gui

from anchor import Anchor
from app import App
from process_rtt import start_rtt

def process_events(app: App):
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            app.running = False
            break
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == app.delete_button:
                delete_selected_anchor(app)
            elif event.ui_element == app.rtt_button:
                start_rtt(app)
        
        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            on_props_edit(app, event)
        
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_sx, click_sy = event.pos

            if click_sx < app.SIDEBAR_X:
                click_x, click_y = app.screen_to_world_coords(click_sx, click_sy)

                if event.button == 1:  # Left mouse button
                    clicked_anchor: Anchor | None = app.get_anchor_at_position(click_x, click_y)

                    app.selected_anchor = clicked_anchor
                    app.update_sidebar(app.selected_anchor)
                    
                    if app.selected_anchor:
                        start_dragging(app, click_x, click_y)
                    else:
                        start_panning(app, click_x, click_y)
                
                elif event.button == 2:  # Middle mouse button
                    app.add_anchor(f"{len(app.anchors) + 1}", click_x, click_y)
        
        # Dragging and panning
        elif event.type == pygame.MOUSEMOTION:
            if app.dragging and app.selected_anchor:
                drag_selected_anchor(app, event)
            elif app.panning:
                pan_view(app, event)
            
        
        # Stop dragging or panning
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                stop_dragging(app)
                stop_panning(app)
        
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

def stop_panning(app):
    app.panning = False
    app.pan_start_x = None
    app.pan_start_y = None

def stop_dragging(app):
    app.dragging = False

def drag_selected_anchor(app: App, event):
    mouse_x, mouse_y = app.screen_to_world_coords(event.pos[0], event.pos[1])
    app.selected_anchor.x = mouse_x - app.drag_start_x
    app.selected_anchor.y = mouse_y - app.drag_start_y
    app.update_sidebar(app.selected_anchor)

def pan_view(app: App, event):
    mouse_x, mouse_y = app.screen_to_world_coords(event.pos[0], event.pos[1])
    app.view_x -= mouse_x - app.pan_start_x
    app.view_y -= mouse_y - app.pan_start_y

def start_panning(app: App, click_x, click_y):
    app.panning = True
    app.pan_start_x = click_x 
    app.pan_start_y = click_y

def start_dragging(app: App, click_x, click_y):
    app.dragging = True
    app.drag_start_x = click_x - app.selected_anchor.x
    app.drag_start_y = click_y - app.selected_anchor.y

def on_props_edit(app: App, event):
    if app.selected_anchor:
        if event.ui_element == app.name_input:
            app.selected_anchor.name = event.text
        elif event.ui_element == app.x_input:
            try:
                app.selected_anchor.x = float(event.text)
            except ValueError:
                pass
        elif event.ui_element == app.y_input:
            try:
                app.selected_anchor.y = float(event.text)
            except ValueError:
                pass

def delete_selected_anchor(app: App):
    if app.selected_anchor:
        app.anchors.remove(app.selected_anchor)
        app.selected_anchor = None
        app.update_sidebar()
    