from PIL import Image
import os
import numpy as np
import cv2
# import torch

# yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def resize_image(image, target_width, target_height, output_path="result/resized/resized_image.jpg"):
    height, width, _ = image.shape
    resized_image = np.zeros((target_height, target_width, 3), dtype=np.uint8)

    scale_x = width / target_width
    scale_y = height / target_height

    for y in range(target_height):
        for x in range(target_width):
            resized_image[y, x] = image[int(y * scale_y), int(x * scale_x)]

    resized_pillow_image = Image.fromarray(resized_image)
    directory = os.path.dirname(output_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    resized_pillow_image.save(output_path)
    print(f"Resized image saved to: {output_path}")

def reduce_noise(image, kernel_size=3, output_path="result/denoised/denoised_image.jpg"):
    padded_image = np.pad(image, ((kernel_size//2, kernel_size//2), (kernel_size//2, kernel_size//2), (0, 0)), mode='constant', constant_values=0)
    denoised_image = np.zeros_like(image)

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(3):
                kernel = padded_image[y:y+kernel_size, x:x+kernel_size, c]
                denoised_image[y, x, c] = np.median(kernel)

    reduce_pillow_img = Image.fromarray(denoised_image)
    directory = os.path.dirname(output_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    reduce_pillow_img.save(output_path)

def adjust_brightness_contrast(image, brightness=30, contrast=1.2, output_path="result/adjusted/adjusted_image.jpg"):
    adjusted_image = np.clip(contrast * image + brightness, 0, 255).astype(np.uint8)
    adjusted_pillow_image = Image.fromarray(adjusted_image)

    directory = os.path.dirname(output_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    adjusted_pillow_image.save(output_path)

def segment_image(image, output_path="result/segmented/segmented_image.jpg"):
    gray = cv2.cvtColorTwoPlane(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    segmented_image = cv2.bitwise_and(image, image, mask=mask)
    segmented_pillow = Image.fromarray(segmented_image)
    directory = os.path.dirname(output_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    segmented_pillow.save(output_path)

def normalize_image(image, output_path="result/normalize/normalized_image.jpg"):
    normalized_img = image / 255.0
    if not os.path.exists(dir):
        os.makedirs(dir)

    normalized_pilow = Image.fromarray(normalized_img * 255).astype(np.uint8)
    normalized_pilow.save(output_path)



def chillie_disease_detection(image):

    pass