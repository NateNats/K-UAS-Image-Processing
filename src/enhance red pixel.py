import cv2
import numpy as np

def enhance_red_pixels(image):
    """
    Tingkatkan intensitas piksel merah dalam gambar.
    """
    # Konversi gambar ke ruang warna HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Rentang warna merah (dua rentang dalam HSV)
    lower_red1 = np.array([0, 25, 25])      # Rentang merah terang
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 25, 25])   # Rentang merah gelap
    upper_red2 = np.array([180, 255, 255])

    # Masking untuk warna merah
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Tingkatkan Saturasi dan Value di area merah
    hsv[:, :, 1] = np.where(mask > 0, hsv[:, :, 1] + 50, hsv[:, :, 1])  # Tingkatkan Saturasi
    hsv[:, :, 2] = np.where(mask > 0, hsv[:, :, 2] + 50, hsv[:, :, 2])  # Tingkatkan Value

    # Konversi kembali ke BGR
    enhanced_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return enhanced_image

# Contoh Penggunaan
if __name__ == "__main__":
    # Path gambar
    image_path = "C:/Users/nicol/Downloads/gambar cabai/baik/cabai_baik (21).jpg"

    # Baca gambar
    image = cv2.imread(image_path)

    if image is None:
        print("Gagal membaca gambar. Periksa path file!")
    else:
        # Tingkatkan intensitas piksel merah
        enhanced_image = enhance_red_pixels(image)

        # Tampilkan hasil
        cv2.imshow("Original Image", image)
        cv2.imshow("Enhanced Red Pixels", enhanced_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Simpan hasil
        cv2.imwrite("enhanced_red_pixels.jpg", enhanced_image)
