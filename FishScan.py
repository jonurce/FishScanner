
import cv2
import os

# Create an output directory for images
output_dir = "captured_images"
os.makedirs(output_dir, exist_ok=True)

# Function to find available cameras
def list_available_cameras(max_cameras=10):
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras

# List all connected cameras
camera_indices = list_available_cameras()
print(f"Available Cameras: {camera_indices}")

# Capture images from each camera
for camera_index in camera_indices:
    cap = cv2.VideoCapture(camera_index)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Save the captured image
            image_path = os.path.join(output_dir, f"camera_{camera_index}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Image saved from Camera {camera_index} at {image_path}")
        else:
            print(f"Failed to capture image from Camera {camera_index}")
        cap.release()
    else:
        print(f"Unable to open Camera {camera_index}")

# Optional: Inform the user about completion
print("Image capture completed!")
