import cv2
import time
import os

# Folder to save the images
save_folder = 'RealSenseRot'

# Create the folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Open the camera (0 is usually the default camera)
cap = cv2.VideoCapture(1)

# Set resolution to 1280x720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

try:
    while True:
        ret, frame = cap.read()  # Capture frame from the camera
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Save the frame as an image file in the specified folder
        filename = os.path.join(save_folder, f"image_{int(time.time() * 1000)}.png")
        cv2.imwrite(filename, frame)

        # Wait for 500 milliseconds (0.5 seconds) before capturing the next image
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nImage capture process interrupted. Exiting...")

# Release the camera and clean up
cap.release()
cv2.destroyAllWindows()
