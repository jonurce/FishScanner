import os
import subprocess


def run_colmap(image_folder, output_folder):
    # Check if COLMAP is installed
    colmap_path = 'colmap'  # Adjust if COLMAP is not in your PATH

    # Step 1: Create a new project directory
    os.makedirs(output_folder, exist_ok=True)

    # Step 2: Feature extraction
    feature_extraction_cmd = [
        colmap_path, 'feature_extractor',
        '--database_path', os.path.join(output_folder, 'database.db'),
        '--image_path', image_folder
    ]
    subprocess.run(feature_extraction_cmd)

    # Step 3: Match features
    feature_matching_cmd = [
        colmap_path, 'exhaustive_matcher',
        '--database_path', os.path.join(output_folder, 'database.db')
    ]
    subprocess.run(feature_matching_cmd)

    # Step 4: Structure-from-Motion (SfM)
    sparse_model_cmd = [
        colmap_path, 'mapper',
        '--database_path', os.path.join(output_folder, 'database.db'),
        '--image_path', image_folder,
        '--output_path', os.path.join(output_folder, 'sparse')
    ]
    subprocess.run(sparse_model_cmd)

    # Step 5: Convert sparse model to dense model (optional)
    dense_model_cmd = [
        colmap_path, 'patch_match_stereo',
        '--workspace_path', os.path.join(output_folder, 'dense'),
        '--workspace_format', 'COLMAP',
        '--PatchMatchStereo.geom_consistency', '1'
    ]
    subprocess.run(dense_model_cmd)

    # Step 6: Export model to .obj format
    export_model_cmd = [
        colmap_path, 'model_converter',
        '--input_path', os.path.join(output_folder, 'sparse', '0'),
        '--output_path', os.path.join(output_folder, 'model.obj'),
        '--output_type', 'OBJ'
    ]
    subprocess.run(export_model_cmd)

    print("3D model has been generated and saved as model.obj")


# Usage
image_folder = 'Pictures/SmallPlastic'
output_folder = 'output_3d_model'
run_colmap(image_folder, output_folder)
