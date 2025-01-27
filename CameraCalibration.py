import cv2
import numpy as np
import os


def calibrate_camera(images_dir, pattern_size=(9, 6), square_size=0.025):
    """
    Calibrate the camera using checkerboard images.

    Args:
        images_dir (str): Directory containing calibration images.
        pattern_size (tuple): Number of internal corners per a chessboard row and column (cols, rows).
        square_size (float): Size of a square in your defined unit (e.g., meters).

    Returns:
        dict: Calibration results containing intrinsic matrix, distortion coefficients, and more.
    """
    # Termination criteria for corner subpixel refinement
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Prepare object points, e.g., (0,0,0), (1,0,0), ..., (8,5,0)
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    objp *= square_size

    # Arrays to store object points and image points
    objpoints = []  # 3D points in real-world space
    imgpoints = []  # 2D points in image plane

    # Load images
    images = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.endswith(".jpg")]

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        if ret:
            objpoints.append(objp)

            # Refine corner locations
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, pattern_size, corners2, ret)
            cv2.imshow("Corners", img)
            cv2.waitKey(100)

    cv2.destroyAllWindows()

    # Perform camera calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    if ret:
        print("Camera calibrated successfully.")
        print("Intrinsic Matrix (K):")
        print(mtx)
        print("Distortion Coefficients:")
        print(dist)
        return {"mtx": mtx, "dist": dist, "rvecs": rvecs, "tvecs": tvecs}
    else:
        print("Camera calibration failed.")
        return None


if __name__ == "__main__":
    # Directory containing your checkerboard images
    calibration_images_dir = "calibration_images"

    # Perform calibration
    results = calibrate_camera(calibration_images_dir)

    if results:
        intrinsic_matrix = results["mtx"]
        print("Intrinsic Matrix:")
        print(intrinsic_matrix)
