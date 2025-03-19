import cv2
import numpy as np

# Settings
camera_index = 5
# Change for each camera (0, 1, 2, 3, 4, 5)
n_images = 15
checkerboard_size = (8, 6)
square_size = 35

# Prepare object points
objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2) * square_size

objpoints = []
imgpoints = []

# Open camera
cap = cv2.VideoCapture(camera_index)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

# Capture images
for i in range(n_images):
    print(f"Camera {camera_index} - Capture {i+1}/{n_images}: Position checkerboard and press 'c'")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)
            if ret:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                           (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
                imgpoints.append(corners2)
                break

# Calibrate and save
if len(objpoints) > 0:
    ret, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    np.savez(f"calibration_cam_{camera_index}.npz", mtx=mtx, dist=dist)
    print(f"Camera {camera_index} calibrated. Saved to calibration_cam_{camera_index}.npz")
else:
    print("Calibration failed - not enough valid images")

cap.release()
cv2.destroyAllWindows()