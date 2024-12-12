import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

from . import format_title, format_author

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(format_title())
        self.root.geometry("800x600")
        self.root.configure(bg="#e7f1fd")
        self.root.resizable(False, False)

        #bikin main frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=200)

        #bikin canvas yang ada titik-titiknya
        self.canvas = tk.Canvas(self.main_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.create_rectangle(
            20, 20, 230, 130,
            outline="gray",
            dash=(5, 4)
        )

        self.image_label = ttk.Label(self.canvas, text="Masukan gambar disini...", font=("Arial", 12))
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        self.upload_button = ttk.Button(self.canvas, text="upload Gambar", command=self.upload_image)
        self.upload_button.place(relx=0.5, rely=0.7, anchor="center")

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )

        if file_path:
            image = Image.open(file_path)
            image.thumbnail((200, 200))
            self.displayed_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.displayed_image, text="")