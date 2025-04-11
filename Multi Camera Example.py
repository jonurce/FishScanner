# Python program to run multiple USB cameras with OpenCV
# Author: Evan Juras, EJ Technology Consultants (https://ejtech.io)

# Import necessary packages
import sys
import cv2

### User-defined parameters
# Number of cameras to run
num_cameras = 1

# Specify each camera resolution in (Width, Height)
cam1_res = (1280, 720)
cam2_res = (1280, 720)
cam3_res = (1280, 720)
cam4_res = (1280, 720)

cam_resolutions = [cam1_res, cam2_res, cam3_res, cam4_res]
enable_thresholding = [False, False, False,
                       False]  # Set to "True" to enable black-and-white thresholding on each camera

### Initialize cameras
caps = []  # Array to hold camera VideoCapture objects

for i in range(num_cameras):
    cam_index = i  # 0, 1, 2, etc
    # cam_index = i * 2 # 0, 2, 4, etc (uncomment this if using Linux)
    cap = cv2.VideoCapture(cam_index)  # Initialize camera by its device index
    ret = cap.set(3, cam_resolutions[i][0])  # Set camera resolution width
    ret = cap.set(4, cam_resolutions[i][1])  # Set camera resolution height
    caps.append(cap)

### Continously grab and display frames from each camera
while True:

    # Loop through each camera
    for i in range(num_cameras):

        # Grab frame from camera
        hasFrame, frame = caps[i].read()
        if not hasFrame or len(frame) == 0:
            print(
                f'Unable to read frame from camera {i + 1}! This usually means the camera is not connected or is not working. Exiting program.')
            sys.exit()

        # Perform desired processing on each camera frame here. For this example, we will run adpative thresholding on frame if enabled
        if enable_thresholding[i] == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
            frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25,
                                          2)  # Threshold frame

        # Display camera frame
        cv2.imshow(f'Camera {i + 1}', frame)

    # Wait for user keypress
    key = cv2.waitKey(5)
    if key == ord('q'):  # Press 'q' to quit
        break

# Clean up
cv2.destroyAllWindows()
cap.release()