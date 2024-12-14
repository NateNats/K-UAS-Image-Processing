import tkinter as tk
from tkinter import filedialog, Label, Button, Canvas, PhotoImage
from PIL import Image, ImageTk, ImageEnhance
import cv2
import numpy as np
import torch

# Load YOLOv5 model
yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

# Preprocessing functions
def preprocess_image(image_path):
    """Perform preprocessing on the input image."""
    # Read image
    image = cv2.imread(image_path)
    
    # Resize to 640x640
    image = cv2.resize(image, (640, 640))

    # Noise reduction
    image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    # Convert to HSV for brightness and contrast adjustments
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.equalizeHist(v)
    hsv = cv2.merge((h, s, v))
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Segmentation (convert to grayscale and apply thresholding)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    segmented = cv2.bitwise_and(image, image, mask=mask)

    # Normalization
    normalized = cv2.normalize(segmented, None, 0, 255, cv2.NORM_MINMAX)

    return normalized

# Detection function
def detect_disease(image_path):
    """Use YOLOv5 model to detect diseases in chili images."""
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)

    # Convert to RGB and prepare for YOLOv5
    image_rgb = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB)
    results = yolo_model(image_rgb)

    return results

# GUI Application
def open_file():
    """Open file dialog to select an image."""
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        # Display selected image
        img = Image.open(file_path)
        img = img.resize((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        canvas.image = img_tk
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

        # Perform detection
        results = detect_disease(file_path)

        # Show results
        results_label.config(text=str(results.pandas().xyxy[0]))

# Create main window
window = tk.Tk()
window.title("Chili Disease Detection")
window.geometry("800x600")

# Widgets
canvas = Canvas(window, width=400, height=400, bg="white")
canvas.pack(pady=20)

upload_btn = Button(window, text="Upload Image", command=open_file)
upload_btn.pack(pady=10)

results_label = Label(window, text="Detection Results will appear here.", wraplength=400, justify="left")
results_label.pack(pady=10)

# Run the application
window.mainloop()
