import cv2
import time
import os
from multiprocessing import Process, Queue
import numpy as np

# Folder to save the images
save_folder = 'Buck6x3Aligned'

# Create the folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Number of cameras
number_of_cameras = 18
camera_indices = np.arange(0, number_of_cameras, 1)


# Camera capture worker function
def camera_worker(camera_id, queue):
    # Initialize camera
    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}.")
        return

    # Set camera properties once
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

    while True:
        try:
            # Get instruction from queue
            if not queue.empty():
                command = queue.get_nowait()
                if command == "capture":
                    ret, frame = cap.read()
                    if ret:
                        filename = os.path.join(save_folder,
                                                f"camera_{camera_id}_image_{int(time.time())}.png")
                        cv2.imwrite(filename, frame)
                        print(f"Captured image from camera {camera_id}.")
                elif command == "exit":
                    break
        except Exception as e:
            print(f"Error in camera {camera_id}: {e}")

    # Cleanup
    cap.release()


if __name__ == "__main__":
    # Create queues for each camera
    queues = [Queue() for _ in range(number_of_cameras)]

    # Start camera processes
    processes = []
    for i, camera_id in enumerate(camera_indices):
        p = Process(target=camera_worker, args=(camera_id, queues[i]))
        processes.append(p)
        p.start()

    try:
        while True:
            # Trigger capture from all cameras simultaneously
            start_time = time.time()
            for q in queues:
                q.put("capture")

            # Wait a bit between captures (adjust as needed)
            time.sleep(1)

            # Optional: Print capture rate
            print(f"Capture cycle took {time.time() - start_time:.2f} seconds")

    except KeyboardInterrupt:
        print("\nImage capture process interrupted. Exiting...")

        # Send exit command to all processes
        for q in queues:
            q.put("exit")

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Clean up
    cv2.destroyAllWindows()