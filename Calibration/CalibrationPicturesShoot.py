import cv2
import os
import time

# Create the directory if it doesn't exist
output_dir = "RotatingCup"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open the external camera (use the appropriate index for your camera)
# Typically, the first camera will have index 0, second camera 1, and so on.
camera_index = 0  # Change this if your external camera is at a different index
cap = cv2.VideoCapture(camera_index)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream from camera.")
    exit()

# Set the capture interval (in seconds)
capture_interval = 0.5

# Start capturing images
try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame.")
            break

        # Generate a unique filename for each image
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        image_filename = os.path.join(output_dir, f"image_{timestamp}.jpg")

        # Save the captured image
        cv2.imwrite(image_filename, frame)
        print(f"Captured and saved: {image_filename}")

        # Wait for the specified time before capturing the next image
        time.sleep(capture_interval)

except KeyboardInterrupt:
    print("Image capture stopped by user.")

finally:
    # Release the camera and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
