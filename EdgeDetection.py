import os
import cv2
import numpy as np
from multiprocessing import Pool
from functools import partial

# Define folders
input_folder = "FishGreenTest"  # Folder with PNG files
output_folder = "FishGreenTestEdges"  # Folder to save edge-detected images

# Create output folder if it doesn’t exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def detect_edges(filename, input_folder, output_folder):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    # Read the image
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if img is None:
        return f"Failed to load {filename}"

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise (optional but recommended for Canny)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Perform Canny edge detection
    edges = cv2.Canny(gray, threshold1=100, threshold2=200)

    # Save the edge-detected image
    cv2.imwrite(output_path, edges)
    return None  # No error, so return None

def process_images():
    # Find all PNG files
    png_files = [f for f in os.listdir(input_folder)
                 if f.lower().endswith('.png')]

    # Use multiprocessing to speed up processing
    with Pool() as pool:
        process_func = partial(detect_edges,
                              input_folder=input_folder,
                              output_folder=output_folder)
        results = pool.map(process_func, png_files)

    # Print any errors
    for result in results:
        if result is not None:
            print(result)
    print("All images processed!")

if __name__ == '__main__':
    detect_edges("cam0_image_1743762635255.png", input_folder, output_folder)
    #process_images()