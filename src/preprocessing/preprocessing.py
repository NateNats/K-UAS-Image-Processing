from PIL import Image
import os
import numpy as np
import cv2
import torch
from ultralytics import YOLO

model = YOLO("./models/yolov8s.pt")

def resize_image(image, image_name, target_width, target_height, result_dir="C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/resized"):
    height, width, _ = image.shape
    resized_image = np.zeros((target_height, target_width, 3), dtype=np.uint8)

    scale_x = width / target_width
    scale_y = height / target_height

    for y in range(target_height):
        for x in range(target_width):
            resized_image[y, x] = image[int(y * scale_y), int(x * scale_x)]

    resized_pillow_image = Image.fromarray(resized_image)
    result_path = os.path.join(result_dir, image_name)
    try:
        resized_pillow_image.save(result_path, "JPEG")
        print(f"Image saved to {result_path}")
    except:
        print("Error saving image")


def reduce_noise(image, image_name, kernel_size=3, result_dir="C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/denoised"):
    padded_image = np.pad(image, ((kernel_size//2, kernel_size//2), (kernel_size//2, kernel_size//2), (0, 0)), mode='constant', constant_values=0)
    denoised_image = np.zeros_like(image)

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(3):
                kernel = padded_image[y:y+kernel_size, x:x+kernel_size, c]
                denoised_image[y, x, c] = np.median(kernel)

    reduce_pillow_img = Image.fromarray(denoised_image)
    result_path = os.path.join(result_dir, image_name)

    try:
        reduce_pillow_img.save(result_path, "JPEG")
        print(f"Image saved to {result_path}")
    except:
        print("Error saving image")


def adjust_brightness_contrast(image, image_name, brightness=20, contrast=1.1, result_dir="C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/brightness"):
    adjusted_image = np.clip(contrast * image + brightness, 0, 255).astype(np.uint8)

    adjusted_pillow_image = Image.fromarray(adjusted_image)
    result_path = os.path.join(result_dir, image_name)

    try:
        adjusted_pillow_image.save(result_path, "JPEG")
        print(f"Image saved to {result_path}")
    except:
        print("Error saving image")


# def segment_image(image, image_name, result_dir="C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/segment/"): --> yang asli
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, mask = cv2.threshold(gray, 255, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#     segmented_image = cv2.bitwise_and(image, image, mask=mask)
#
#     segmented_pillow = Image.fromarray(segmented_image)
#     result_path = os.path.join(result_dir, image_name)
#
#     try:
#         segmented_pillow.save(result_path, "JPEG")
#         print(f"Image saved to {result_path}")
#     except:
#         print("Error saving image")


def segment_image(image, image_name, result_dir="C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/segment/", result_dir_mask="C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/masked/"):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    kernel = np.ones((5, 5), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_OPEN, kernel)

    segmented_img = cv2.bitwise_and(image, image, mask=mask_cleaned)

    segmented_pillow = Image.fromarray(cv2.cvtColor(segmented_img, cv2.COLOR_BGR2RGB))
    result_path = os.path.join(result_dir, image_name)

    masked = Image.fromarray(cv2.cvtColor(mask_cleaned, cv2.COLOR_BGR2RGB))
    masked_path = os.path.join(result_dir_mask, "masked.jpg")

    try:
        segmented_pillow.save(result_path, "JPEG")
        print(f"Image saved to {result_path}")

        masked.save(masked_path, "JPEG")
        print(f"Mask saved to {masked_path}")
    except:
        print("Error saving image")


def normalize_image(image, image_name, result_dir="C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/normalize/"):
    normalized_img = image / 255.0
    normalized_uint8 = (normalized_img * 255).astype(np.uint8)
    normalized_pilow = Image.fromarray(normalized_uint8)
    result_path = os.path.join(result_dir, image_name)

    try:
        normalized_pilow.save(result_path, "JPEG")
        print(f"Image saved to {result_path}")
    except:
        print("Error saving image")

def detect_objects(image, image_name, result_dir="C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/detected/"):
    results = model(image)
    detected_image = results.render()
    detected_pillow = Image.fromarray(detected_image)
    result_path = os.path.join(result_dir, image_name)

    try:
        detected_pillow.save(result_path, "JPEG")
        print(f"Image saved to {result_path}")
    except:
        print("Error saving image")