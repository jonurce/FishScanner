import cv2
import os
import time

# Create the directory if it doesn't exist
output_dir = "3Dcam"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Camera indices for the cameras you want to use
camera_indices = [0]  # Update with actual camera indices

# Set desired resolution (example: 4K resolution)
desired_width = 4096
desired_height = 2160

# Set the capture interval (in seconds)
capture_interval = 0.5

# Open all cameras and set resolution
caps = []
for idx in camera_indices:
    cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print(f"Error: Could not open video stream from camera {idx}.")
        continue

    # Set maximum resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

    caps.append(cap)

# Start capturing images
try:
    while True:
        frames = []

        # Capture frame-by-frame from each camera
        for idx, cap in enumerate(caps):
            ret, frame = cap.read()
            if not ret:
                print(f"Failed to grab frame from camera {camera_indices[idx]}.")
                break
            frames.append(frame)

        # Check if all frames were captured successfully
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
    # Release the cameras and close any OpenCV windows
    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()
