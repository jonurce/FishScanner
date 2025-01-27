
import open3d as o3d

# Load the .ply file
mesh = o3d.io.read_triangle_mesh("output_mesh.ply")

# Visualize the mesh
o3d.visualization.draw_geometries([mesh])

