import cv2
import time
import os
import numpy as np
import pyttsx3

engine = pyttsx3.init()

# Folder to save the images
save_folder = 'FishTest'

# Create the folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)


# Function to remove white/gray background
def remove_green_background(frame):
    # Convert BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define HSV range for green color
    lower_green = np.array([35, 40, 130])  # Adjusted lower bound for green
    upper_green = np.array([85, 255, 255])  # Adjusted upper bound for green

    # Create a mask for green areas
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Invert the mask (green becomes black, non-green becomes white)
    mask_inv = cv2.bitwise_not(mask)

    # Convert the original image to BGRA (adding alpha channel)
    frame_bgra = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    # Set alpha channel to 0 (transparent) where mask is green
    frame_bgra[:, :, 3] = mask_inv

    return frame_bgra


# List of camera indices (adjust if your cameras have different indices)
number_of_cameras = 8
camera_indices = np.arange(0,number_of_cameras,1)
capture_duration = 5  # Duration per camera in seconds
frame_interval = 0.0  # Time between frames in seconds

try:
    for cam_index in camera_indices:
        if cam_index == 0:
            engine.say(f"Fish scanning process started! I will tell you when to spin that fish! Be ready!")
            engine.runAndWait()

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
        engine.say(f"Starting capture with camera {cam_index}! Spin that fish!")
        engine.runAndWait()
        start_time = time.time()

        message_interval = 5;
        while (time.time() - start_time) < capture_duration:
            ret, frame = cap.read()  # Capture frame from the camera
            if not ret:
                print(f"Error: Failed to capture image from camera {cam_index}.")
                break

            # Remove white/gray background
            frame = remove_green_background(frame)

            # Save the frame with camera index in the filename
            filename = os.path.join(save_folder, f"cam{cam_index}_image_{int(time.time() * 1000)}.png")
            cv2.imwrite(filename, frame)

            # Wait for 500 milliseconds (0.5 seconds) before capturing the next image
            time.sleep(frame_interval)

            if (time.time() - start_time) > message_interval:
                engine.say(f"Keep spinning that fish!")
                engine.runAndWait()
                message_interval += 5;

        # Release the current camera before switching
        cap.release()
        print(f"Finished capture with camera {cam_index}.")
        engine.say(f"Finished capture with camera {cam_index}. You can rest rotating the camera.")
        engine.runAndWait()

        if cam_index == number_of_cameras-1:
            engine.say(f"Fish scanning process finished! Hell yeah fish! Good fish job!")
            engine.runAndWait()

except KeyboardInterrupt:
    print("\nImage capture process interrupted. Exiting...")

# Clean up any open cameras (in case of interruption)
cv2.destroyAllWindows()