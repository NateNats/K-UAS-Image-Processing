import cv2
import numpy as np

def segment_red_chili(image, output_path="segmented_chili.jpg"):
    # Konversi gambar ke ruang warna HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Rentang warna merah dalam HSV
    lower_red1 = np.array([0, 100, 100])      # Rentang merah terang
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])   # Rentang merah gelap
    upper_red2 = np.array([180, 255, 255])

    # Masking untuk warna merah
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2  # Gabungkan kedua mask

    # Operasi morfologi untuk membersihkan noise
    kernel = np.ones((5, 5), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Tutup lubang kecil
    mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_OPEN, kernel)  # Hilangkan noise kecil

    # Terapkan mask ke gambar asli
    segmented_image = cv2.bitwise_and(image, image, mask=mask_cleaned)

    # Simpan hasil segmentasi
    cv2.imwrite(output_path, segmented_image)
    print(f"Hasil segmentasi disimpan di: {output_path}")

    return segmented_image, mask_cleaned

# Contoh Penggunaan
if __name__ == "__main__":
    # Path gambar input
    image_path = "C:/Kuliah/Semester 5/UAS Pemrosesan Citra/result/brightness/brightness.jpg"

    # Baca gambar
    image = cv2.imread(image_path)
    if image is None:
        print("Gagal membaca gambar. Periksa path!")
    else:
        # Segmentasi cabai merah
        segmented_image, mask = segment_red_chili(image, output_path="segmented_chili.jpg")

        # Tampilkan hasil
        cv2.imshow("Original Image", image)
        cv2.imshow("Mask", mask)
        cv2.imshow("Segmented Image", segmented_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
