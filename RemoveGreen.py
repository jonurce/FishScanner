import os
from PIL import Image
import numpy as np
import cv2
from multiprocessing import Pool
from functools import partial

# Define folders
input_folder = "FishGreenTest"
output_folder = "FishGreenNoBack"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def remove_green_background(filename, input_folder, output_folder):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    # Read image with OpenCV (faster than PIL for this)
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return f"Failed to load: {filename}"

    # Convert BGR to RGBA if needed
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

    # Convert to HSV (vectorized with OpenCV)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Define green range in HSV (adjust as needed)
    lower_green = np.array([65 // 2, 10 * 255 // 100, 10 * 255 // 100])  # H/2, S%, V% to OpenCV scale
    upper_green = np.array([180 // 2, 255, 255])  # H/2, 100%, 100%

    # Create mask (fast with OpenCV)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # Apply mask to alpha channel
    img[:, :, 3] = np.where(green_mask == 255, 0, img[:, :, 3])

    # Save with PIL (for PNG support)
    result = Image.fromarray(img)
    result.save(output_path, 'PNG')


def process_images():
    png_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]

    with Pool() as pool:
        process_func = partial(remove_green_background,
                               input_folder=input_folder,
                               output_folder=output_folder)
        results = pool.map(process_func, png_files)

    print("All images processed!")


if __name__ == '__main__':
    process_images()