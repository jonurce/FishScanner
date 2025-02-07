import cv2
import os
import time
from datetime import datetime

# Create the directory if it doesn't exist
output_dir = "calibration_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define the range of camera indices
camera_indices = range(0, 4)  # Adjust the range as needed

# Open all cameras with DirectShow backend for better multi-camera support
cameras = []
for index in camera_indices:
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if cap.isOpened():
        cameras.append((index, cap))
        print(f"Camera {index} opened successfully.")
        time.sleep(1)  # Allow the camera to warm up
    else:
        print(f"Error: Could not open camera {index}.")

if not cameras:
    print("Error: No cameras opened successfully.")
    exit()

# Set the capture interval (in seconds)
capture_interval = 3

# Start capturing images
try:
    while True:
        for index, cap in cameras:
            cap.grab()  # Force frame capture refresh
            ret, frame = cap.read()
            if ret:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                image_filename = os.path.join(output_dir, f"camera_{index}_image_{timestamp}.jpg")
                cv2.imwrite(image_filename, frame)
                print(f"Captured and saved: {image_filename}")
            else:
                print(f"Failed to grab frame from camera {index}.")

        time.sleep(capture_interval)

except KeyboardInterrupt:
    print("Image capture stopped by user.")

finally:
    for index, cap in cameras:
        cap.release()
    cv2.destroyAllWindows()
