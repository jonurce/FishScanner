import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time

# Create a RealSense pipeline
pipeline = rs.pipeline()

# Create a config object to configure the pipeline
config = rs.config()

# Enable depth and color streams with maximum resolutions
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)  # Depth stream (1280x720)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.rgb8, 30)  # Color stream (1920x1080)

# Start the pipeline
pipeline.start(config)

# Define output folder for storing images
output_folder = 'captured_images'
os.makedirs(output_folder, exist_ok=True)

try:
    frame_count = 0
    while True:
        # Wait for a new set of frames
        frames = pipeline.wait_for_frames()

        # Get depth and color frames
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # If frames are valid, process them
        if not depth_frame or not color_frame:
            continue

        # Convert depth and color frames to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Save depth and color images as PNG
        depth_image_path = os.path.join(output_folder, f"depth_{frame_count:04d}.png")
        color_image_path = os.path.join(output_folder, f"color_{frame_count:04d}.png")

        cv2.imwrite(depth_image_path, depth_image)
        cv2.imwrite(color_image_path, color_image)

        print(f"Saved frame {frame_count}")

        frame_count += 1
        time.sleep(1)  # Capture an image every second

finally:
    # Stop the pipeline when done
    pipeline.stop()