import torch
import os
import numpy as np
from imageio import imread
from nerf import NERF  # Import your NeRF model class from the repo (this may vary based on the repo)
import matplotlib.pyplot as plt

# 1. Prepare your images
image_folder = 'Pictures/SmallPlastic'  # Set the path to your images folder
image_files = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.JPG', '.JPEG'))])

# Read the images and convert them to tensors
images = []
for img_file in image_files:
    img = imread(img_file)
    img = torch.tensor(img).float()  # Convert image to tensor
    images.append(img)

# Convert list to tensor
images = torch.stack(images)

# 2. Load pre-trained NeRF model
# Make sure to replace this with the appropriate class or function to load the model
model = NERF()  # This will depend on the repo you're using
model.load_state_dict(torch.load('.venv/Lib/site-packages/nerf/data/6a5j_model_1.pdb'))  # Replace with actual model path

# Set model to evaluation mode
model.eval()

# 3. Prepare camera parameters (intrinsics and extrinsics)
# For simplicity, we're assuming you have intrinsic parameters (K matrix)
# You can use OpenCV or other tools to estimate the extrinsics (camera positions and orientations)
K = np.array([[495.21153939, 0, 335.75450282], [0, 504.81851369, 179.00894773], [0, 0, 1]])

# Assuming you've either estimated or approximated camera extrinsics (positions and orientations)
# You can set them manually or use photogrammetry methods (like OpenCV) to estimate them.
extrinsics = np.eye(4)  # Placeholder, replace with actual extrinsics

# 4. Generate 3D reconstruction using NeRF
# Assuming the model takes images and camera parameters and returns 3D points or a rendered scene
output = model.forward(images, K, extrinsics)

# 5. Convert the output to a 3D model (point cloud)
# Assuming the model output contains 3D points or depth information
depth_map = output['depth_map']  # Replace with actual output from the model

# Convert the depth map to 3D points
# This is a simple conversion assuming a basic camera model
# For more complex models, you'd need to apply the correct transformation based on your camera parameters
points_3d = []
for i in range(depth_map.shape[0]):
    for j in range(depth_map.shape[1]):
        z = depth_map[i, j]
        x = (j - K[0, 2]) * z / K[0, 0]
        y = (i - K[1, 2]) * z / K[1, 1]
        points_3d.append([x, y, z])

# Convert points_3d to a NumPy array
points_3d = np.array(points_3d)


# 6. Save the 3D points as an OBJ file
def save_as_obj(points, output_path):
    with open(output_path, 'w') as file:
        # Write vertices
        for point in points:
            file.write(f"v {point[0]} {point[1]} {point[2]}\n")

        # Optionally, you can write faces here if you want to connect points (triangles)
        # For simplicity, we're not doing this here, but you can use Delaunay triangulation or other methods


# Save the 3D points as an OBJ file
save_as_obj(points_3d, 'output_model.obj')

print("3D model saved as 'output_model.obj'")
