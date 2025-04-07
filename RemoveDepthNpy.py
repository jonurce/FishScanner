import os
import numpy as np
from multiprocessing import Pool
from functools import partial
from PIL import Image

# Define folders
input_folder = "FishNpyDepth"  # Update this to your new folder
output_folder = "0.FishDepthNoBackNpy"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def remove_background_using_depth(filename, input_folder, output_folder):
    # Extract the number part and construct depth filename
    if filename.startswith("color_") and filename.endswith(".npy"):
        number = filename[len("color_"):-len(".npy")]
        depth_filename = f"depth_{number}.npy"
    else:
        return f"Skipping invalid filename: {filename}"

    rgb_path = os.path.join(input_folder, filename)
    depth_path = os.path.join(input_folder, depth_filename)
    output_path = os.path.join(output_folder, filename.replace(".npy", ".png"))  # Save as PNG

    # Load RGB and depth arrays from .npy files
    try:
        rgb_array = np.load(rgb_path)
        depth_array = np.load(depth_path)
    except Exception as e:
        return f"Failed to load files for {filename}: {str(e)}"

    # Ensure RGB array is in correct format (H, W, C) and has alpha channel
    if rgb_array.ndim == 3 and rgb_array.shape[2] == 3:  # If RGB only
        rgb_array = np.dstack((rgb_array, np.full(rgb_array.shape[:2], 255, dtype=rgb_array.dtype)))  # Add alpha
    elif rgb_array.ndim != 3 or rgb_array.shape[2] != 4:
        return f"Invalid RGB array shape for {filename}: {rgb_array.shape}"

    # Ensure depth array matches RGB dimensions
    if depth_array.shape != rgb_array.shape[:2]:
        return f"Depth shape {depth_array.shape} doesn't match RGB shape {rgb_array.shape[:2]} for {filename}"

    # Create mask based on depth threshold
    depth_lower_threshold = 20
    depth_upper_threshold = 50
    background_mask = (depth_array < depth_lower_threshold) & (depth_array > depth_upper_threshold)

    # Apply mask to alpha channel
    rgb_array[:, :, 3] = np.where(background_mask, 0, rgb_array[:, :, 3])

    # Save as PNG using PIL
    try:
        result = Image.fromarray(rgb_array)
        result.save(output_path, 'PNG')
    except Exception as e:
        return f"Failed to save {output_path}: {str(e)}"


def process_images():
    # Only process color files
    color_files = [f for f in os.listdir(input_folder)
                   if f.lower().startswith('color_') and f.lower().endswith('.npy')]

    with Pool() as pool:
        process_func = partial(remove_background_using_depth,
                               input_folder=input_folder,
                               output_folder=output_folder)
        results = pool.map(process_func, color_files)

    # Print any errors
    for result in results:
        if isinstance(result, str):
            print(result)
    print("All images processed!")


if __name__ == '__main__':
    process_images()