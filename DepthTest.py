import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Define folders
input_folder = "FishNpyDepth"  # Your folder with .npy files
output_folder = "FishDepthColormapped"  # Where to save colormapped plots

# Create output folder if it doesn’t exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def visualize_depth_with_colormap(depth_filename):
    depth_path = os.path.join(input_folder, depth_filename)
    output_path = os.path.join(output_folder, depth_filename.replace(".npy", "_plot.png"))

    # Load depth array
    try:
        depth_array = np.load(depth_path)
    except Exception as e:
        print(f"Failed to load {depth_filename}: {str(e)}")
        return

    # Normalize depth to 0-255 range for colormap (if not already uint8)
    if depth_array.dtype != np.uint8:
        depth_normalized = cv2.normalize(depth_array, None, 0, 255, cv2.NORM_MINMAX)
        depth_normalized = depth_normalized.astype(np.uint8)
    else:
        depth_normalized = depth_array

    # Apply colormap (JET: blue = low, red = high)
    depth_colored = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_JET)

    # Convert BGR (OpenCV format) to RGB for correct display/saving
    depth_colored_rgb = cv2.cvtColor(depth_colored, cv2.COLOR_BGR2RGB)

    # Create plot with colorbar
    plt.figure(figsize=(10, 6))  # Adjust size as needed
    plt.imshow(depth_colored_rgb)
    plt.title(f"Depth Map: {depth_filename}", fontsize=12, pad=10)
    plt.colorbar(label="Depth (normalized 0-255)")
    plt.axis('off')  # Hide axes for cleaner look

    # Save the plot as PNG
    try:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')  # High DPI for clarity
        print(f"Saved plot to {output_path}")
    except Exception as e:
        print(f"Failed to save {output_path}: {str(e)}")
    finally:
        plt.close()  # Close the figure to free memory

    # Optional: Display the plot (comment out if not needed)
    # plt.show()

def process_depth_images():
    # Find all depth files
    depth_files = [f for f in os.listdir(input_folder)
                   if f.lower().startswith('depth_') and f.lower().endswith('.npy')]

    # Process each file
    for depth_file in depth_files:
        visualize_depth_with_colormap(depth_file)

if __name__ == '__main__':
    process_depth_images()