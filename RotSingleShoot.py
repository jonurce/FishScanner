import cv2
import time
import os
import numpy as np

# Folder to save the images
save_folder = 'FishNoBackg3'

# Create the folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Open the camera (0 is usually the default camera)
cap = cv2.VideoCapture(1)

# Set resolution to 1280x720 (Note: your original was 3264x2448)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()


def remove_white_background(frame):
    # Convert BGR to HSV color space (better for color detection)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range for white color in HSV
    lower_white = np.array([0, 0, 150])  # Lower bound for white
    upper_white = np.array([180, 50, 255])  # Upper bound for white

    # Create a mask for white areas
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Invert the mask (white becomes black, non-white becomes white)
    mask_inv = cv2.bitwise_not(mask)

    # Convert the original image to BGRA (adding alpha channel)
    frame_bgra = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    # Set alpha channel to 0 (transparent) where mask is white
    frame_bgra[:, :, 3] = mask_inv

    return frame_bgra


try:
    while True:
        ret, frame = cap.read()  # Capture frame from the camera
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Remove white background
        frame_processed = remove_white_background(frame)

        # Save the frame as a PNG file (PNG supports transparency)
        filename = os.path.join(save_folder, f"image_{int(time.time() * 1000)}.png")
        cv2.imwrite(filename, frame_processed)

        # Wait for 500 milliseconds (0.5 seconds) before capturing the next image
        # time.sleep(0.5)

except KeyboardInterrupt:
    print("\nImage capture process interrupted. Exiting...")

# Release the camera and clean up
cap.release()
cv2.destroyAllWindows()