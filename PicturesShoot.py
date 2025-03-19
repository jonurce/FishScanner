import cv2
import time
import os
import numpy as np

# Folder to save the images
save_folder = '96images'

# Create the folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# List of camera indices (0, 1, 2, ..., 5 for 6 cameras)
#camera_indices = [0,1,2,3,4,5]
number_of_cameras = 6
camera_indices = np.arange(0,number_of_cameras,1)


# Function to capture images from a single camera
def capture_images_from_camera(camera_id):
    cap = cv2.VideoCapture(camera_id)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    #cap.set(cv2.CAP_PROP_AUTO_WB, 1)
    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print(f"Error: Failed to capture image from camera {camera_id}.")
        return

    # Save the frame as an image file in the specified folder
    filename = os.path.join(save_folder, f"camera_{camera_id}_image_{int(time.time())}.png")
    #cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
    cv2.imwrite(filename, frame)
    print(f"Captured image from camera {camera_id}.")

    # Release the camera when don
    cap.release()


# Continuous loop to capture from each camera repeatedly
if __name__ == "__main__":
    try:
        while True:
            # Capture from each camera
            for camera_id in camera_indices:
                capture_images_from_camera(camera_id)
            # Optional: Wait before starting the next loop, if needed
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nImage capture process interrupted. Exiting...")

    # Clean up
    cv2.destroyAllWindows()
