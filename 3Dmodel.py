import subprocess
import os

# Set paths to COLMAP executable and your images
colmap_path = '/path/to/colmap'  # Path to the COLMAP binary (replace with actual path)
image_dir = 'Pictures/SmallPlastic'  # Path to the directory containing the 2D images
output_dir = 'output_3d_model'  # Directory to store the 3D model


# Step 1: Feature extraction
def extract_features():
    subprocess.run([
        colmap_path, 'feature_extractor',
        '--database_path', os.path.join(output_dir, 'database.db'),
        '--image_path', image_dir
    ])


# Step 2: Feature matching
def match_features():
    subprocess.run([
        colmap_path, 'exhaustive_matcher',
        '--database_path', os.path.join(output_dir, 'database.db')
    ])


# Step 3: Structure from Motion (SfM)
def run_sfm():
    subprocess.run([
        colmap_path, 'mapper',
        '--database_path', os.path.join(output_dir, 'database.db'),
        '--image_path', image_dir,
        '--output_path', os.path.join(output_dir, 'sfm_output')
    ])


# Step 4: Multi-View Stereo (MVS) - Dense reconstruction
def run_mvs():
    subprocess.run([
        colmap_path, 'patch_match_stereo',
        '--workspace_path', os.path.join(output_dir, 'sfm_output'),
        '--workspace_format', 'COLMAP',
        '--PatchMatchStereo.geom_consistency', '1'
    ])

    subprocess.run([
        colmap_path, 'stereo_fusion',
        '--workspace_path', os.path.join(output_dir, 'sfm_output'),
        '--workspace_format', 'COLMAP',
        '--output_path', os.path.join(output_dir, 'fused.ply')
    ])


# Step 5: Export the 3D model as an .obj file
def export_3d_model():
    subprocess.run([
        colmap_path, 'model_converter',
        '--input_path', os.path.join(output_dir, 'sfm_output', '0'),
        '--output_path', os.path.join(output_dir, 'model.obj'),
        '--output_type', 'OBJ'
    ])


# Running the functions step by step
def create_3d_model():
    extract_features()
    match_features()
    run_sfm()
    run_mvs()
    export_3d_model()
    print("3D model creation complete! The model is saved as 'model.obj'.")


# Execute the 3D model creation process
if __name__ == "__main__":
    create_3d_model()
