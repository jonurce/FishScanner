import cv2

index = 0  # Replace with the index of the problematic camera
cap = cv2.VideoCapture(index)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        print(f"Successfully captured a frame from Camera {index}.")
    else:
        print(f"Failed to read a frame from Camera {index}.")
    cap.release()
else:
    print(f"Camera {index} is not accessible.")
