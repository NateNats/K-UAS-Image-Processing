import tkinter as tk
from tkinter import ttk, filedialog

import cv2
import numpy as np
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
        self.title = ttk.Label(self.title_frame, text="Segmentasi Cabai", font=("Arial", 24, "bold"), padding=10)
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
        self.clear_button.place(relx=0.2, rely=0.9, anchor="center")
        self.clear_button.state(["disabled"])

        self.upload_button = ttk.Button(self.canvas, text="Upload Gambar", command=self.upload_image)
        self.upload_button.place(relx=0.4, rely=0.9, anchor="center")

        self.process_button = ttk.Button(self.canvas, text="Proses Gambar", command=self.process_image)
        self.process_button.place(relx=0.6, rely=0.9, anchor="center")
        self.process_button.state(["disabled"])

        self.result_button = ttk.Button(self.canvas, text="Tampilkan Hasil", command=self.show_result)
        self.result_button.place(relx=0.8, rely=0.9, anchor="center")
        self.result_button.state(["disabled"])

        self.file_path = None  # Untuk menyimpan path file gambar yang diupload

    def show_result(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("Hasil proses")
        result_window.geometry("1000x800")
        result_window.configure(bg="#e7f1fd")
        result_window.resizable(False, False)

        card_frame = ttk.Frame(result_window, padding=10)
        card_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # resize image
        img_resize = Image.open("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/resized/resized.jpg")
        img_resize = img_resize.resize((300, 300), Image.Resampling.LANCZOS)
        self.tk_resize = ImageTk.PhotoImage(img_resize)
        image_label = ttk.Label(card_frame, image=self.tk_resize)
        image_label.grid(row=0, column=0, padx=10, pady=10)
        image_label.bind("<Button-1>", lambda e: self.show_large_image(img_resize, "Resized Image"))
        resize_label = ttk.Label(card_frame, text=f"Resized Image {img_resize.width}x{img_resize.height}")
        resize_label.grid(row=1, column=0, padx=10, pady=10)

        # reduce noise
        img_noise = Image.open("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/denoised/denoised.jpg")
        img_noise = img_noise.resize((300, 300), Image.Resampling.LANCZOS)
        self.tk_noise = ImageTk.PhotoImage(img_noise)
        noise_label = ttk.Label(card_frame, image=self.tk_noise)
        noise_label.grid(row=0, column=1, padx=10, pady=10)
        noise_label.bind("<Button-1>", lambda e: self.show_large_image(img_noise, "Denoised Image"))
        noise_label = ttk.Label(card_frame, text="Denoised Image")
        noise_label.grid(row=1, column=1, padx=10, pady=10)

        # adjust brightness contrast
        img_brightness = Image.open("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/brightness/brightness.jpg")
        img_brightness = img_brightness.resize((300, 300), Image.Resampling.LANCZOS)
        self.tk_brightness = ImageTk.PhotoImage(img_brightness)
        brightness_label = ttk.Label(card_frame, image=self.tk_brightness)
        brightness_label.grid(row=0, column=2, padx=10, pady=10)
        brightness_label.bind("<Button-1>", lambda e: self.show_large_image(img_brightness, "Brightness Image"))
        brightness_label = ttk.Label(card_frame, text="Brightness Image")
        brightness_label.grid(row=1, column=2, padx=10, pady=10)

        # mask image
        img_mask = Image.open("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/masked/masked.jpg")
        img_mask = img_mask.resize((300, 300), Image.Resampling.LANCZOS)
        self.tk_mask = ImageTk.PhotoImage(img_mask)
        mask_label = ttk.Label(card_frame, image=self.tk_mask)
        mask_label.grid(row=2, column=0, padx=10, pady=10)
        mask_label.bind("<Button-1>", lambda e: self.show_large_image(img_mask, "Masked Image"))
        mask_label = ttk.Label(card_frame, text="Masked Image")
        mask_label.grid(row=3, column=0, padx=10, pady=10)

        # segment image
        img_segment = Image.open("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/segment/segmented.jpg")
        img_segment = img_segment.resize((300, 300), Image.Resampling.LANCZOS)
        self.tk_segment = ImageTk.PhotoImage(img_segment)
        segment_label = ttk.Label(card_frame, image=self.tk_segment)
        segment_label.grid(row=2, column=1, padx=10, pady=10)
        segment_label.bind("<Button-1>", lambda e: self.show_large_image(img_segment, "Segmented Image"))
        segment_label = ttk.Label(card_frame, text="Segmented Image")
        segment_label.grid(row=3, column=1, padx=10, pady=10)

        # normalize image
        img_normalize = Image.open("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/normalize/normalized.jpg")
        img_normalize = img_normalize.resize((300, 300), Image.Resampling.LANCZOS)
        self.tk_normalize = ImageTk.PhotoImage(img_normalize)
        normalize_label = ttk.Label(card_frame, image=self.tk_normalize)
        normalize_label.grid(row=2, column=2, padx=10, pady=10)
        normalize_label.bind("<Button-1>", lambda e: self.show_large_image(img_normalize, "Normalized Image"))
        normalize_label = ttk.Label(card_frame, text="Normalized Image")
        normalize_label.grid(row=3, column=2, padx=10, pady=10)


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
            self.image_label.config(image=self.displayed_image, text=f"size: {image.width}x{image.height}")
            self.clear_button.state(["!disabled"])
            self.process_button.state(["!disabled"])

    def clear_image(self):
        """Fungsi untuk menghapus gambar dari GUI."""
        self.image_label.config(image="", text="Masukan gambar disini...")
        self.clear_button.state(["disabled"])
        self.process_button.state(["disabled"])
        self.result_button.state(["disabled"])
        self.file_path = None

    def process_image(self):
        if self.file_path:
            # resize image
            img = Image.open(self.file_path)
            pw = np.array(img)
            preprocessing.resize_image(pw,"resized.jpg",  300, 300)

            # reduce noise
            img2 = Image.open("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/resized/resized.jpg")
            pw2 = np.array(img2)
            preprocessing.reduce_noise(pw2,"denoised.jpg")

            # adjust brightness contrast
            img3 = Image.open("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/denoised/denoised.jpg")
            pw3 = np.array(img3)
            preprocessing.adjust_brightness_contrast(pw3,"brightness.jpg")

            # segment image

            img4 = cv2.imread("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/brightness/brightness.jpg")
            preprocessing.segment_image(img4,"segmented.jpg")

            # img4 = Image.open("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/brightness/brightness.jpg")
            # pw4 = np.array(img4)
            # preprocessing.segment_image(pw4,"segmented.jpg")

            #normalize image
            img5 = Image.open("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/segment/segmented.jpg")
            pw5 = np.array(img5)
            preprocessing.normalize_image(pw5, "normalized.jpg")

            # img5 = cv2.imread("C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/segment/segmented.jpg")
            # preprocessing.normalize_image(img5,"normalized.jpg")

            self.result_button.state(["!disabled"])

    def show_large_image(self, image, title):
        large_img_window = tk.Toplevel(self.root)
        large_img_window.geometry("800x800")
        large_img_window.title(title)
        large_img_window.resizable(False, False)
        large_img_window.configure(bg="#f0f0f0")

        image = image.resize((800, 800), Image.Resampling.LANCZOS)
        self.tk_large = ImageTk.PhotoImage(image)

        img_label = ttk.Label(large_img_window, image=self.tk_large)
        img_label.pack(fill="both", expand=True, padx=10, pady=10, anchor="center")

        close_button = ttk.Button(large_img_window, text="Close", command=large_img_window.destroy)
        close_button.pack(pady=10)