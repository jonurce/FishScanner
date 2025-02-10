import cv2
import os
import time

# Create the directory if it doesn't exist
output_dir = "3cams30"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Camera indices for the three cameras
camera_indices = [0, 1, 2]  # Adjust these indices if necessary

# Set the capture interval (in seconds)
capture_interval = 0.5

# Start capturing images
try:
    while True:
        frames = []

        # Open, capture, and release each camera sequentially
        for idx in camera_indices:
            cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)

            if not cap.isOpened():
                print(f"Error: Could not open video stream from camera {idx}.")
                continue

            ret, frame = cap.read()
            if not ret:
                print(f"Failed to grab frame from camera {idx}.")
                cap.release()
                continue

            frames.append(frame)
            cap.release()  # Close the camera after capturing the frame

        # Check if frames were captured successfully
        if len(frames) != len(camera_indices):
            print("Not all frames were captured.")
            break

        # Generate a unique filename for each image
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        for idx, frame in enumerate(frames):
            image_filename = os.path.join(output_dir, f"camera{camera_indices[idx]}_image_{timestamp}.png")
            cv2.imwrite(image_filename, frame)
            print(f"Captured and saved: {image_filename}")

        # Wait for the specified time before capturing the next set of images
        time.sleep(capture_interval)

except KeyboardInterrupt:
    print("Image capture stopped by user.")
finally:
    cv2.destroyAllWindows()
