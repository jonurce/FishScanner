import cv2
import time
import os

# Folder to save the images
save_folder = 'LotsSingle'

# Create the folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# List of camera indices (0, 1, 2, ..., 5 for 6 cameras)
camera_indices = [0]


# Function to capture images from a single camera
def capture_images_from_camera(camera_id):
    cap = cv2.VideoCapture(camera_id)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}.")
        return

    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print(f"Error: Failed to capture image from camera {camera_id}.")
        return

    # Save the frame as an image file in the specified folder
    filename = os.path.join(save_folder, f"camera_{camera_id}_image_{int(time.time())}.png")
    cv2.imwrite(filename, frame)

    # Release the camera when don
    cap.release()


# Continuous loop to capture from each camera repeatedly
if __name__ == "__main__":
    try:
        while True:
            # Capture from each camera
            for camera_id in camera_indices:
                capture_images_from_camera(camera_id)
                print(f"Captured image from camera {camera_id}.")

            # Optional: Wait before starting the next loop, if needed
            # time.sleep(1)

    except KeyboardInterrupt:
        print("\nImage capture process interrupted. Exiting...")

    # Clean up
    cv2.destroyAllWindows()
