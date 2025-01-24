import os
import ctypes
import subprocess
import sys
import cv2


def is_admin():
    """Check if the script is running as an administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """Re-run the script as administrator."""
    if not is_admin():
        print("Requesting administrator privileges...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()


def disable_integrated_camera():
    """Disables the integrated camera using PowerShell."""
    check_command = 'powershell "Get-PnpDevice -FriendlyName \'*Integrated Camera*\'"'
    disable_command = (
        'powershell "Get-PnpDevice -FriendlyName \'*Integrated Camera*\' | '
        'Disable-PnpDevice -Confirm:$false"'
    )
    try:
        print("Checking for the integrated camera...")
        result_check = subprocess.run(
            check_command, shell=True, check=True, capture_output=True, text=True
        )
        if "*Integrated Camera*" not in result_check.stdout:
            print("No integrated camera found. Skipping disable step.")
            return False

        print("Integrated camera detected. Disabling it now...")
        result_disable = subprocess.run(
            disable_command, shell=True, check=True, capture_output=True, text=True
        )
        print(result_disable.stdout)
        print("Integrated camera disabled successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable the integrated camera: {e}")
        print(f"Error output: {e.stderr}")
        return False


def get_available_cameras():
    """Returns a list of indexes for available cameras."""
    index = 0
    available_cameras = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        available_cameras.append(index)
        cap.release()
        index += 1
    return available_cameras


def capture_images_from_cameras(output_folder):
    """Captures images from all available cameras and saves them to the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cameras = get_available_cameras()
    if not cameras:
        print("No cameras available to capture images.")
        return

    print(f"Available cameras: {cameras}")
    for cam_index in cameras:
        cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            print(f"Unable to access camera {cam_index}")
            continue

        ret, frame = cap.read()
        if ret:
            filename = os.path.join(output_folder, f"camera_{cam_index}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Image saved from camera {cam_index} as {filename}")
        else:
            print(f"Failed to capture image from camera {cam_index}")

        cap.release()

    print("Done capturing images.")


def create_3d_model_with_alicevision(images_folder, output_folder):
    """Creates a 3D model using AliceVision from the captured images."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        # Step 1: Initialize the camera parameters
        print("Initializing camera parameters...")
        camera_init_output = os.path.join(output_folder, "cameraInit.sfm")
        subprocess.run(
            [
                "aliceVision_cameraInit",
                "--input", images_folder,
                "--output", camera_init_output,
                "--allowSingleView", "1"
            ],
            check=True,
        )

        # Step 2: Feature extraction
        print("Extracting features...")
        feature_output = os.path.join(output_folder, "features")
        subprocess.run(
            [
                "aliceVision_featureExtraction",
                "--input", camera_init_output,
                "--output", feature_output,
            ],
            check=True,
        )

        # Step 3: Create a 3D model
        print("Generating 3D model...")
        model_output = os.path.join(output_folder, "3D_model.obj")
        subprocess.run(
            [
                "aliceVision_sfmAlignment",
                "--input", feature_output,
                "--output", model_output,
            ],
            check=True,
        )

        print(f"3D model created successfully. Saved at {model_output}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to process images with AliceVision: {e}")
        print(f"Command output: {e.stderr}")


if __name__ == "__main__":
    # Ensure the script runs as admin
    run_as_admin()

    # Disable the integrated camera
    disabled = disable_integrated_camera()

    if disabled:
        print("Integrated camera disabled successfully. Proceeding to capture images...")
    else:
        print("Could not disable the integrated camera. Proceeding anyway...")

    # Output folders
    images_folder = "captured_images"
    model_output_folder = "3d_model_output"

    # Step 1: Capture images from cameras
    print("Capturing images from cameras...")
    capture_images_from_cameras(images_folder)

    # Step 2: Create a 3D model from the captured images using AliceVision
    print("Creating a 3D model from the captured images...")
    create_3d_model_with_alicevision(images_folder, model_output_folder)
