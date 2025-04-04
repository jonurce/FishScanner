import cv2
import time
import os
import numpy as np
import pyttsx3
import pyrealsense2 as rs

engine = pyttsx3.init()

# Folder to save the images
save_folder = 'DepthMask'

# Create the folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)


# Function to remove background based on depth
def remove_depth_background(color_frame, depth_frame, depth_threshold=1.0):
    # Convert color frame to BGRA (adding alpha channel)
    frame_bgra = cv2.cvtColor(color_frame, cv2.COLOR_BGR2BGRA)

    # Get depth values in meters
    depth_data = np.array(depth_frame.get_data(), dtype=np.float32) / 1000.0  # Convert from mm to meters

    # Create mask where depth > threshold (or invalid depth = 0)
    mask = (depth_data > depth_threshold) | (depth_data == 0)

    # Set alpha channel to 0 (transparent) where depth exceeds threshold
    frame_bgra[mask, 3] = 0

    return frame_bgra


# Configure RealSense pipeline
def configure_pipeline():
    pipeline = rs.pipeline()
    config = rs.config()

    # Enable color and depth streams
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)

    return pipeline, config


try:
    # Initialize RealSense pipeline
    pipeline, config = configure_pipeline()

    # Start streaming
    profile = pipeline.start(config)

    # Get depth scale
    depth_sensor = profile.get_device().first_depth_sensor()

    # Number of captures (instead of multiple cameras)
    number_of_captures = 1
    capture_duration = 5  # Duration per capture in seconds
    frame_interval = 0.0  # Time between frames in seconds

    engine.say(f"Fish scanning process started! I will tell you when to spin that fish! Be ready!")
    engine.runAndWait()

    for capture_index in range(number_of_captures):
        print(f"Starting capture {capture_index}...")
        engine.say(f"Starting capture {capture_index}! Spin that fish!")
        engine.runAndWait()
        start_time = time.time()

        message_interval = 5
        while (time.time() - start_time) < capture_duration:
            # Wait for frames
            frames = pipeline.wait_for_frames()

            # Get color and depth frames
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            if not color_frame or not depth_frame:
                print(f"Error: Failed to capture frames in capture {capture_index}.")
                continue

            # Convert color frame to numpy array
            color_image = np.asanyarray(color_frame.get_data())

            # Remove background based on depth
            result_frame = remove_depth_background(color_image, depth_frame, depth_threshold=1.0)

            # Save the frame with capture index in the filename
            filename = os.path.join(save_folder, f"capture{capture_index}_image_{int(time.time() * 1000)}.png")
            cv2.imwrite(filename, result_frame)

            # Wait before capturing next frame
            time.sleep(frame_interval)

            if (time.time() - start_time) > message_interval:
                engine.say(f"Keep spinning that fish!")
                engine.runAndWait()
                message_interval += 5

        print(f"Finished capture {capture_index}.")
        engine.say(f"Finished capture {capture_index}. You can rest rotating the camera.")
        engine.runAndWait()

    engine.say(f"Fish scanning process finished! Hell yeah fish! Good fish job!")
    engine.runAndWait()

except KeyboardInterrupt:
    print("\nImage capture process interrupted. Exiting...")
finally:
    # Clean up
    pipeline.stop()
    cv2.destroyAllWindows()