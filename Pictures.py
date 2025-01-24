import cv2
import os
from threading import Thread

def get_camera_indices():
    indices = []
    for i in range(10):  # Check up to 10 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            indices.append(i)
            cap.release()
    return indices

def capture_from_camera(index, folder_name):
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            filename = os.path.join(folder_name, f"camera_{index}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Image saved from Camera {index} as {filename}")
        else:
            print(f"Failed to capture image from Camera {index}")
        cap.release()
    else:
        print(f"Camera {index} is not accessible")

def capture_images_from_all_cameras(camera_indices, folder_name="3d_model_input"):
    if not os.path.exists(folder_name):
        try:
            os.makedirs(folder_name)
        except Exception as e:
            print(f"Error creating folder '{folder_name}': {e}")
            return

    threads = []
    for index in camera_indices:
        t = Thread(target=capture_from_camera, args=(index, folder_name))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    camera_indices = get_camera_indices()
    print("Detected cameras:", camera_indices)

    if camera_indices:
        capture_images_from_all_cameras(camera_indices, folder_name="3d_model_input")
    else:
        print("No cameras found.")
