import tkinter as tk
from tkinter import simpledialog, messagebox
import math

class Dog:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.radius = 20
        self.color = 'blue'
        self.selected = False

class DogParkApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Dog Park Tracker")
        
        # Main frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Canvas for drawing
        self.canvas = tk.Canvas(self.main_frame, bg='lightgreen', width=800, height=600)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        # Sidebar frame
        self.sidebar = tk.Frame(master, width=250, bg='lightgray')
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sidebar contents
        self.dog_info_label = tk.Label(self.sidebar, text="No Dog Selected", bg='lightgray')
        self.dog_info_label.pack(pady=10)
        
        self.edit_name_button = tk.Button(self.sidebar, text="Edit Name", command=self.edit_dog_name)
        self.edit_name_button.pack(pady=5)
        
        self.delete_dog_button = tk.Button(self.sidebar, text="Delete Dog", command=self.delete_selected_dog)
        self.delete_dog_button.pack(pady=5)
        
        self.add_dog_button = tk.Button(self.sidebar, text="Add Dog", command=self.add_dog)
        self.add_dog_button.pack(pady=5)
        
        # Dogs list
        self.dogs = []
        
        # Pan and zoom variables
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.zoom_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
        # Bind events
        self.canvas.bind('<ButtonPress-1>', self.on_canvas_click)
        self.canvas.bind('<B1-Motion>', self.on_pan)
        self.canvas.bind('<MouseWheel>', self.on_zoom)  # Windows and MacOS
        self.canvas.bind('<Button-4>', self.on_zoom)    # Linux scroll up
        self.canvas.bind('<Button-5>', self.on_zoom)    # Linux scroll down
        
        # Add initial info text
        self.canvas.create_text(400, 300, 
            text="Right-click to add a dog\nScroll to zoom\nClick and drag to pan", 
            font=('Arial', 12), fill='gray')

    def add_dog(self, x=None, y=None):
        """Add a new dog to the park"""
        # If x and y are not provided, prompt user
        if x is None or y is None:
            # Use canvas center as default
            canvas_center_x = self.canvas.winfo_width() / 2
            canvas_center_y = self.canvas.winfo_height() / 2
            
            # Ask for dog name
            name = simpledialog.askstring("Add Dog", "Enter dog's name:")
            if not name:
                return
            
            # Create dog at canvas center or mouse position
            x = canvas_center_x
            y = canvas_center_y
        
        # Create dog object
        new_dog = Dog(name, x, y)
        self.dogs.append(new_dog)
        
        # Deselect all other dogs
        for dog in self.dogs:
            dog.selected = False
        
        # Select the new dog
        new_dog.selected = True
        
        # Redraw everything
        self.redraw_canvas()
        
        # Update sidebar
        self.update_sidebar()

    def on_canvas_click(self, event):
        """Handle canvas click events"""
        # Deselect all dogs first
        for dog in self.dogs:
            dog.selected = False
        
        # Check if any dog was clicked
        for dog in self.dogs:
            # Calculate distance from click to dog center
            dist = math.sqrt((event.x - dog.x)**2 + (event.y - dog.y)**2)
            if dist <= dog.radius:
                dog.selected = True
                break
        
        # Redraw canvas to show selection
        self.redraw_canvas()
        
        # Update sidebar
        self.update_sidebar()

    def on_pan(self, event):
        """Pan the canvas"""
        if not hasattr(self, 'pan_start_x'):
            self.pan_start_x = event.x
            self.pan_start_y = event.y
            return
        
        # Calculate pan delta
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        
        # Update offset
        self.offset_x += dx
        self.offset_y += dy
        
        # Update pan start
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        
        # Redraw canvas
        self.redraw_canvas()

    def on_zoom(self, event):
        """Zoom in or out"""
        # Determine zoom direction
        if event.num == 5 or event.delta < 0:  # Scroll down
            self.zoom_factor *= 0.9
        elif event.num == 4 or event.delta > 0:  # Scroll up
            self.zoom_factor *= 1.1
        
        # Limit zoom
        self.zoom_factor = max(0.1, min(self.zoom_factor, 5.0))
        
        # Redraw canvas
        self.redraw_canvas()

    def redraw_canvas(self):
        """Redraw all dogs on the canvas"""
        # Clear canvas
        self.canvas.delete('all')
        
        # Redraw dogs
        for dog in self.dogs:
            # Determine color based on selection
            color = 'red' if dog.selected else 'blue'
            
            # Draw dog
            self.canvas.create_oval(
                dog.x - dog.radius, 
                dog.y - dog.radius, 
                dog.x + dog.radius, 
                dog.y + dog.radius, 
                fill=color, 
                outline='black'
            )
            
            # Draw dog name
            self.canvas.create_text(
                dog.x, 
                dog.y + dog.radius + 10, 
                text=dog.name, 
                fill='black'
            )

    def update_sidebar(self):
        """Update sidebar with selected dog's information"""
        # Find selected dog
        selected_dog = next((dog for dog in self.dogs if dog.selected), None)
        
        if selected_dog:
            # Update dog info
            info_text = f"Dog Name: {selected_dog.name}\n"
            info_text += f"X Coordinate: {selected_dog.x}\n"
            info_text += f"Y Coordinate: {selected_dog.y}"
            
            self.dog_info_label.config(text=info_text)
            
            # Enable buttons
            self.edit_name_button.config(state=tk.NORMAL)
            self.delete_dog_button.config(state=tk.NORMAL)
        else:
            # No dog selected
            self.dog_info_label.config(text="No Dog Selected")
            
            # Disable buttons
            self.edit_name_button.config(state=tk.DISABLED)
            self.delete_dog_button.config(state=tk.DISABLED)

    def edit_dog_name(self):
        """Edit name of selected dog"""
        # Find selected dog
        selected_dog = next((dog for dog in self.dogs if dog.selected), None)
        
        if selected_dog:
            # Prompt for new name
            new_name = simpledialog.askstring(
                "Edit Dog", 
                "Enter new name for the dog:", 
                initialvalue=selected_dog.name
            )
            
            if new_name:
                selected_dog.name = new_name
                
                # Redraw canvas
                self.redraw_canvas()
                
                # Update sidebar
                self.update_sidebar()

    def delete_selected_dog(self):
        """Delete the selected dog"""
        # Find selected dog
        selected_dog = next((dog for dog in self.dogs if dog.selected), None)
        
        if selected_dog:
            # Confirm deletion
            confirm = messagebox.askyesno(
                "Delete Dog", 
                f"Are you sure you want to delete {selected_dog.name}?"
            )
            
            if confirm:
                # Remove dog from list
                self.dogs.remove(selected_dog)
                
                # Redraw canvas
                self.redraw_canvas()
                
                # Update sidebar
                self.update_sidebar()

def main():
    root = tk.Tk()
    root.geometry('1000x600')
    app = DogParkApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()