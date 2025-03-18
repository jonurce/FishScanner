import cv2
import time
import os
import numpy as np

# Folder to save the images
save_folder = 'TestBucket18Aligned90deg'

# Create the folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# List of camera indices (0, 1, 2, ..., 5 for 6 cameras)
camera_indices = [0, 1, 2, 3, 4, 5]

# Load calibration data for all cameras
calibration_data = {}
for cam_id in camera_indices:
    calib_file = f"calibration_cam_{cam_id}.npz"
    if os.path.exists(calib_file):
        data = np.load(calib_file)
        calibration_data[cam_id] = {"mtx": data["mtx"], "dist": data["dist"]}
        print(f"Loaded calibration data for camera {cam_id}")
    else:
        print(f"Warning: Calibration file {calib_file} not found. Images from camera {cam_id} will not be undistorted.")

# Function to capture and undistort images from a single camera
def capture_images_from_camera(camera_id):
    cap = cv2.VideoCapture(camera_id)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}.")
        return

    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # Note: Autofocus might interfere with calibration if it changes focus
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # Auto-exposure might vary; consider fixing it if needed

    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print(f"Error: Failed to capture image from camera {camera_id}.")
        cap.release()
        return

    # Apply undistortion if calibration data exists
    if camera_id in calibration_data:
        mtx = calibration_data[camera_id]["mtx"]
        dist = calibration_data[camera_id]["dist"]
        h, w = frame.shape[:2]
        # Get optimal new camera matrix and undistort
        new_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        undistorted_frame = cv2.undistort(frame, mtx, dist, None, new_mtx)
        # Crop to the valid region (optional, based on roi)
        x, y, w, h = roi
        undistorted_frame = undistorted_frame[y:y+h, x:x+w]
    else:
        undistorted_frame = frame  # Use raw frame if no calibration data

    # Save the undistorted frame as an image file
    filename = os.path.join(save_folder, f"camera_{camera_id}_image_{int(time.time())}.jpg")
    cv2.imwrite(filename, undistorted_frame, [cv2.IMWRITE_JPEG_QUALITY, 100])

    # Release the camera
    cap.release()

# Continuous loop to capture from each camera repeatedly
if __name__ == "__main__":
    try:
        while True:
            # Capture from each camera
            for camera_id in camera_indices:
                capture_images_from_camera(camera_id)
                print(f"Captured and processed image from camera {camera_id}.")

            # Optional: Wait before starting the next loop
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nImage capture process interrupted. Exiting...")

    # Clean up
    cv2.destroyAllWindows()