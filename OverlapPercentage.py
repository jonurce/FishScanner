from skimage.metrics import structural_similarity as ssim
import cv2

# Load images in grayscale
image1 = cv2.imread("SmallPlastic/IMG_3472.JPG", cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread("SmallPlastic/IMG_3473.JPG", cv2.IMREAD_GRAYSCALE)

# Resize to match dimensions
image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

# Compute SSIM
score, _ = ssim(image1, image2, full=True)
print(f"SSIM Overlap Percentage: {score * 100:.2f}%")
