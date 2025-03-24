import cv2
import time
import os
import numpy as np

# Folder to save the images
save_folder = 'FishNoBack_2cams'

# Create the folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)


# Function to remove white/gray background
def remove_white_background(frame):
    # Convert BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Adjusted range for white/grayish colors in HSV
    lower_white = np.array([0, 0, 100])  # Lower brightness threshold to include grays
    upper_white = np.array([180, 50, 255])  # Broader saturation range for grayish tones

    # Create a mask for white/gray areas
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Invert the mask (white/gray becomes black, non-white becomes white)
    mask_inv = cv2.bitwise_not(mask)

    # Convert the original image to BGRA (adding alpha channel)
    frame_bgra = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    # Set alpha channel to 0 (transparent) where mask is white/gray
    frame_bgra[:, :, 3] = mask_inv

    return frame_bgra


# List of camera indices (adjust if your cameras have different indices)
number_of_cameras = 2
camera_indices = np.arange(0,number_of_cameras,1)
capture_duration = 30  # Duration per camera in seconds
frame_interval = 0.0  # Time between frames in seconds

try:
    for cam_index in camera_indices:
        # Open the current camera
        cap = cv2.VideoCapture(cam_index)

        # Set resolution to 3264x2448
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)

        # Check if the camera is opened successfully
        if not cap.isOpened():
            print(f"Error: Could not open camera {cam_index}.")
            continue  # Skip to the next camera if this one fails

        print(f"Starting capture with camera {cam_index}...")
        start_time = time.time()

        while (time.time() - start_time) < capture_duration:
            ret, frame = cap.read()  # Capture frame from the camera
            if not ret:
                print(f"Error: Failed to capture image from camera {cam_index}.")
                break

            # Remove white/gray background
            frame_processed = remove_white_background(frame)

            # Save the frame with camera index in the filename
            filename = os.path.join(save_folder, f"cam{cam_index}_image_{int(time.time() * 1000)}.png")
            cv2.imwrite(filename, frame_processed)

            # Wait for 500 milliseconds (0.5 seconds) before capturing the next image
            time.sleep(frame_interval)

        # Release the current camera before switching
        cap.release()
        print(f"Finished capture with camera {cam_index}.")

except KeyboardInterrupt:
    print("\nImage capture process interrupted. Exiting...")

# Clean up any open cameras (in case of interruption)
cv2.destroyAllWindows()