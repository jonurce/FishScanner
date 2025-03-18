import cv2
import time
import os

# Folder to save images
save_folder = 'TestBucket18Aligned90deg'
os.makedirs(save_folder, exist_ok=True)

# Function to capture image from a camera
def capture_image(camera_id):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"Camera {camera_id} not accessible")
        return False
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    ret, frame = cap.read()
    if ret:
        filename = os.path.join(save_folder, f"camera_{camera_id}_image_{int(time.time())}.jpg")
        cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
        print(f"Captured image from camera {camera_id}")
    else:
        print(f"Failed to capture from camera {camera_id}")
    cap.release()
    return ret

# Scan for cameras (try indices 0 to 9, adjust if needed)
max_index = 28  # Increase if you suspect more devices
active_cameras = []
for i in range(max_index):
    if capture_image(i):
        active_cameras.append(i)

# Main loop to capture from all detected cameras
if active_cameras:
    try:
        while True:
            for camera_id in active_cameras:
                capture_image(camera_id)
            time.sleep(1)  # Adjust delay as needed
    except KeyboardInterrupt:
        print("\nStopped by user")
else:
    print("No cameras found")

cv2.destroyAllWindows()