import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

class GridImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid Image App")

        # Initialize image and canvas
        self.image = None
        self.photo_image = None  # Reference to display image

        # Sliders to control grid
        self.rows = tk.IntVar(value=5)
        self.columns = tk.IntVar(value=5)

        # Canvas to display the image
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.grid(row=0, column=0, columnspan=3)

        # Slider to adjust number of rows
        tk.Label(self.root, text="Rows").grid(row=1, column=0)
        self.row_slider = tk.Scale(self.root, from_=2, to=20, orient=tk.HORIZONTAL, variable=self.rows, command=self.update_grid)
        self.row_slider.grid(row=1, column=1)

        # Slider to adjust number of columns
        tk.Label(self.root, text="Columns").grid(row=2, column=0)
        self.column_slider = tk.Scale(self.root, from_=2, to=20, orient=tk.HORIZONTAL, variable=self.columns, command=self.update_grid)
        self.column_slider.grid(row=2, column=1)

        # Button to load image
        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.grid(row=3, column=0)

        # Button to save the image with grid
        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_button.grid(row=3, column=2)

    def load_image(self):
        # Open file dialog to choose an image
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                # Open the image
                self.image = Image.open(file_path)
                self.image.thumbnail((500, 500))  # Resize for display

                # Display the image on the canvas
                self.photo_image = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

                # Draw the initial grid
                self.update_grid()
            except Exception as e:
                print(f"Error loading image: {e}")

    def update_grid(self, event=None):
        # Check if an image is loaded
        if self.image is None:
            return

        # Clear the canvas
        self.canvas.delete("all")

        # Redraw the image
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        # Get the current number of rows and columns
        num_rows = self.rows.get()
        num_columns = self.columns.get()

        # Get image dimensions
        width, height = self.image.size

        # Draw the grid lines
        for i in range(1, num_rows):
            y = i * height / num_rows
            self.canvas.create_line(0, y, width, y, fill="red")
        for j in range(1, num_columns):
            x = j * width / num_columns
            self.canvas.create_line(x, 0, x, height, fill="red")

    def save_image(self):
        if self.image is None:
            print("No image loaded.")
            return

        try:
            # Create a copy of the image to draw the grid
            grid_image = self.image.copy()
            draw = ImageDraw.Draw(grid_image)

            # Get the current number of rows and columns
            num_rows = self.rows.get()
            num_columns = self.columns.get()

            # Get image dimensions
            width, height = grid_image.size

            # Draw the grid lines
            for i in range(1, num_rows):
                y = i * height / num_rows
                draw.line([(0, y), (width, y)], fill="red")
            for j in range(1, num_columns):
                x = j * width / num_columns
                draw.line([(x, 0), (x, height)], fill="red")

            # Save the image with the grid overlay
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                grid_image.save(save_path)
                print(f"Image saved as {save_path}")
        except Exception as e:
            print(f"Error saving image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GridImageApp(root)
    root.mainloop()