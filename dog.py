import tkinter as tk
from tkinter import simpledialog, messagebox
import math

class DogParkTracker:
    def __init__(self, master):
        self.master = master
        master.title("Dog Park Location Tracker")
        
        # Canvas setup
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, 
                                bg='lightgreen', highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        # Zoom and pan variables
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Dog storage
        self.dogs = []
        self.selected_dog = None
        
        # Bind events
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<ButtonPress-3>', self.start_pan)
        self.canvas.bind('<B3-Motion>', self.pan)
        self.canvas.bind('<MouseWheel>', self.zoom)  # Windows and MacOS
        self.canvas.bind('<Button-4>', self.zoom)    # Linux scroll up
        self.canvas.bind('<Button-5>', self.zoom)    # Linux scroll down
        
        # Keyboard bindings
        master.bind('<Delete>', self.delete_selected_dog)
        master.bind('<Control-e>', self.edit_dog)
        
        # Menu setup
        menubar = tk.Menu(master)
        master.config(menu=menubar)
        
        # Dog menu
        dog_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dogs", menu=dog_menu)
        dog_menu.add_command(label="Add Dog", command=self.add_dog_dialog)
        dog_menu.add_command(label="Edit Dog", command=self.edit_dog)
        dog_menu.add_command(label="Delete Dog", command=self.delete_selected_dog)
        
        # Context menu
        self.context_menu = tk.Menu(master, tearoff=0)
        self.context_menu.add_command(label="Add Dog", command=self.add_dog_dialog)
        
    def add_dog(self, x, y, name=None):
        """Add a dog to the park"""
        if name is None:
            name = simpledialog.askstring("Dog Name", "Enter dog's name:")
        
        if name:
            # Convert screen coordinates to park coordinates
            park_x = (x - self.pan_x) / self.zoom_factor
            park_y = (y - self.pan_y) / self.zoom_factor
            
            # Create dog object
            dog = {
                'name': name,
                'x': park_x,
                'y': park_y,
                'canvas_object': None
            }
            self.dogs.append(dog)
            self.draw_dog(dog)
    
    def draw_dog(self, dog):
        """Draw or redraw a dog on the canvas"""
        # Remove existing canvas object if it exists
        if dog['canvas_object']:
            self.canvas.delete(dog['canvas_object'])
        
        # Calculate screen coordinates
        screen_x = dog['x'] * self.zoom_factor + self.pan_x
        screen_y = dog['y'] * self.zoom_factor + self.pan_y
        
        # Draw dog as a circle with name
        radius = 20 * self.zoom_factor
        dog['canvas_object'] = [
            self.canvas.create_oval(
                screen_x - radius, screen_y - radius, 
                screen_x + radius, screen_y + radius, 
                fill='brown', outline='black'
            ),
            self.canvas.create_text(
                screen_x, screen_y + radius + 15, 
                text=dog['name'], fill='black'
            )
        ]
    
    def redraw_all_dogs(self):
        """Redraw all dogs when zooming or panning"""
        for dog in self.dogs:
            self.draw_dog(dog)
    
    def on_canvas_click(self, event):
        """Handle canvas click - add dog or select existing dog"""
        # Check if an existing dog is clicked
        for dog in self.dogs:
            screen_x = dog['x'] * self.zoom_factor + self.pan_x
            screen_y = dog['y'] * self.zoom_factor + self.pan_y
            
            # Calculate distance from click to dog center
            dist = math.sqrt((event.x - screen_x)**2 + (event.y - screen_y)**2)
            
            if dist < 25 * self.zoom_factor:
                # Dog selected
                self.selected_dog = dog
                return
        
        # If no dog selected, add a new dog
        self.add_dog(event.x, event.y)
    
    def add_dog_dialog(self):
        """Open dialog to add a dog with specific coordinates"""
        name = simpledialog.askstring("Dog Name", "Enter dog's name:")
        if name:
            x = simpledialog.askfloat("X Coordinate", "Enter X coordinate:")
            y = simpledialog.askfloat("Y Coordinate", "Enter Y coordinate:")
            
            if x is not None and y is not None:
                self.dogs.append({
                    'name': name,
                    'x': x,
                    'y': y,
                    'canvas_object': None
                })
                self.redraw_all_dogs()
    
    def edit_dog(self, event=None):
        """Edit selected dog's name or coordinates"""
        if not self.selected_dog:
            messagebox.showinfo("Edit Dog", "No dog selected. Click on a dog first.")
            return
        
        # Prompt for new name
        new_name = simpledialog.askstring(
            "Edit Dog", 
            f"Current name: {self.selected_dog['name']}", 
            initialvalue=self.selected_dog['name']
        )
        
        if new_name:
            self.selected_dog['name'] = new_name
        
        # Prompt for new coordinates
        new_x = simpledialog.askfloat(
            "X Coordinate", 
            "Enter new X coordinate:", 
            initialvalue=self.selected_dog['x']
        )
        new_y = simpledialog.askfloat(
            "Y Coordinate", 
            "Enter new Y coordinate:", 
            initialvalue=self.selected_dog['y']
        )
        
        if new_x is not None and new_y is not None:
            self.selected_dog['x'] = new_x
            self.selected_dog['y'] = new_y
        
        # Redraw to reflect changes
        self.redraw_all_dogs()
    
    def delete_selected_dog(self, event=None):
        """Delete the currently selected dog"""
        if not self.selected_dog:
            messagebox.showinfo("Delete Dog", "No dog selected. Click on a dog first.")
            return
        
        # Remove canvas objects
        if self.selected_dog['canvas_object']:
            for obj in self.selected_dog['canvas_object']:
                self.canvas.delete(obj)
        
        # Remove from dogs list
        self.dogs.remove(self.selected_dog)
        self.selected_dog = None
    
    def start_pan(self, event):
        """Start panning the canvas"""
        self.canvas.scan_mark(event.x, event.y)
    
    def pan(self, event):
        """Pan the canvas"""
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.pan_x = self.canvas.canvasx(0)
        self.pan_y = self.canvas.canvasy(0)
        self.redraw_all_dogs()
    
    def zoom(self, event):
        """Zoom in or out"""
        # Determine zoom direction
        if event.num == 5 or event.delta < 0:  # Zoom out
            new_zoom = max(0.1, self.zoom_factor * 0.9)
        else:  # Zoom in
            new_zoom = min(10, self.zoom_factor * 1.1)
        
        # Update zoom factor
        self.zoom_factor = new_zoom
        
        # Redraw dogs with new zoom
        self.redraw_all_dogs()

def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = DogParkTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()