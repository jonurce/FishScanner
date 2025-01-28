"""
import open3d as o3d

# Load the .ply file
mesh = o3d.io.read_triangle_mesh("output_model.ply")

# Visualize the mesh
o3d.visualization.draw_geometries([mesh])
"""
import open3d as o3d

# Load the point cloud from the .ply file
point_cloud = o3d.io.read_point_cloud("output_model.ply")

# Visualize the point cloud
o3d.visualization.draw_geometries([point_cloud])



