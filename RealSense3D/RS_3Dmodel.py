import os
import numpy as np
import open3d as o3d
import cv2
import pyrealsense2 as rs

# Load the saved images from the folder
output_folder = '../Main program/RS_captured_images'
depth_files = sorted([f for f in os.listdir(output_folder) if 'depth' in f])
color_files = sorted([f for f in os.listdir(output_folder) if 'color' in f])

# Check if there are matching depth and color images
assert len(depth_files) == len(color_files), "Mismatch in number of depth and color images."

# Initialize pointcloud object
pc = rs.pointcloud()

# Create Open3D point cloud object
points_o3d = o3d.geometry.PointCloud()

for i in range(len(depth_files)):
    # Load depth and color images
    depth_image_path = os.path.join(output_folder, depth_files[i])
    color_image_path = os.path.join(output_folder, color_files[i])

    # Load the images using OpenCV
    depth_image_o3d_loaded  = o3d.io.read_image(depth_image_path)  # Depth as 16-bit image
    color_image = cv2.imread(color_image_path)  # Color image as 8-bit

    # Convert the depth image to RealSense format (16-bit unsigned integers)
    depth_frame = rs.frame()
    depth_frame = rs.depth_frame(np.asarray(depth_image_o3d_loaded))

    # Convert the depth frame to a point cloud
    points = pc.calculate(depth_frame)

    # Extract 3D vertices (X, Y, Z) from the point cloud
    vtx = np.asanyarray(points.get_vertices())

    # Add the new points to the Open3D point cloud
    points_o3d.points.extend(vtx)

    print(f"Processed image {i+1}/{len(depth_files)}")

# Visualize the point cloud
o3d.visualization.draw_geometries([points_o3d])

# Save the final point cloud to a PLY file
o3d.io.write_point_cloud("final_fish_pointcloud.ply", points_o3d)