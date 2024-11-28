import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class InteractivePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal', adjustable='datalim')
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

        # Add two circles
        self.circle1 = Circle((0, 0), 2, color='blue', alpha=0.5)
        self.circle2 = Circle((5, 5), 3, color='red', alpha=0.5)
        self.ax.add_patch(self.circle1)
        self.ax.add_patch(self.circle2)

        # Connect event handlers
        self.press = None
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)

        plt.show()

    def on_press(self, event):
        """Record mouse press for panning."""
        if event.button == 1:  # Left mouse button
            self.press = (event.xdata, event.ydata)

    def on_release(self, event):
        """Release mouse button."""
        self.press = None

    def on_motion(self, event):
        """Handle panning by moving the plot."""
        if self.press is not None and event.xdata is not None and event.ydata is not None:
            dx = self.press[0] - event.xdata
            dy = self.press[1] - event.ydata
            self.press = (event.xdata, event.ydata)
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            self.ax.set_xlim(xlim[0] + dx, xlim[1] + dx)
            self.ax.set_ylim(ylim[0] + dy, ylim[1] + dy)
            self.ax.figure.canvas.draw()

    def on_scroll(self, event):
        """Handle zooming using the mouse wheel."""
        base_scale = 1.1
        if event.button == 'up':  # Zoom in
            scale_factor = 1 / base_scale
        elif event.button == 'down':  # Zoom out
            scale_factor = base_scale
        else:
            return

        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        x_range = (xlim[1] - xlim[0]) * scale_factor
        y_range = (ylim[1] - ylim[0]) * scale_factor

        x_center = event.xdata
        y_center = event.ydata

        self.ax.set_xlim([x_center - x_range / 2, x_center + x_range / 2])
        self.ax.set_ylim([y_center - y_range / 2, y_center + y_range / 2])
        self.ax.figure.canvas.draw()

if __name__ == '__main__':
    InteractivePlot()
