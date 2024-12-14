import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from src.preprocessing import preprocessing

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Deteksi Penyakit Cabai")
        self.root.geometry("1000x800")
        self.root.configure(bg="#e7f1fd")
        self.root.resizable(False, False)

        self.title_frame = tk.Frame(self.root, bg="#d3d3d3", padx=10, pady=10)
        self.title_frame.place(relx=0.5, rely=0.1, anchor="center")
        self.title = ttk.Label(self.title_frame, text="Deteksi Penyakit Cabai", font=("Arial", 24, "bold"), padding=10)
        self.title.pack()

        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.place(relx=0.5, rely=0.55, anchor="center", width=800, height=600)

        # Canvas untuk gambar
        self.canvas = tk.Canvas(self.main_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.create_rectangle(
            30, 20, 730, 530,
            outline="gray",
            dash=(5, 4)
        )

        self.image_label = ttk.Label(self.canvas, text="Masukan gambar disini...", font=("Arial", 12))
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        self.clear_button = ttk.Button(self.canvas, text="Hapus Gambar", command=self.clear_image)
        self.clear_button.place(relx=0.25, rely=0.9, anchor="center")
        self.clear_button.state(["disabled"])

        self.upload_button = ttk.Button(self.canvas, text="Upload Gambar", command=self.upload_image)
        self.upload_button.place(relx=0.5, rely=0.9, anchor="center")

        self.process_button = ttk.Button(self.canvas, text="Proses Gambar", command=self.process_image)
        self.process_button.place(relx=0.75, rely=0.9, anchor="center")
        self.process_button.state(["disabled"])

        self.file_path = None  # Untuk menyimpan path file gambar yang diupload

    def upload_image(self):
        """Fungsi untuk upload gambar."""
        file_path = filedialog.askopenfilename(
            title="Pilih gambar",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )

        if file_path:
            self.file_path = file_path  # Simpan path gambar
            image = Image.open(file_path)
            image.thumbnail((600, 400))
            self.displayed_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.displayed_image, text="")
            self.clear_button.state(["!disabled"])
            self.process_button.state(["!disabled"])

    def clear_image(self):
        """Fungsi untuk menghapus gambar dari GUI."""
        self.image_label.config(image="", text="Masukan gambar disini...")
        self.clear_button.state(["disabled"])
        self.process_button.state(["disabled"])
        self.file_path = None

    def process_image(self):
        if self.file_path:
            print(self.file_path)

            # # Jalankan deteksi dengan YOLOv5
            # results, preprocessed_image = detect_disease(self.file_path)
            #
            # # Gambarkan bounding boxes di gambar
            # image_with_boxes = draw_boxes(preprocessed_image.copy(), results)
            #
            # # Konversi gambar untuk ditampilkan di GUI
            # image_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB)))
            # self.image_label.config(image=image_tk)
            # self.image_label.image = image_tk  # Simpan referensi gambar agar tidak terhapus
            # print(results.pandas().xyxy[0].to_string())

