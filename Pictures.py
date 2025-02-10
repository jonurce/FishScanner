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


def is_integrated_camera_active():
    """Check if the integrated camera is active using PowerShell."""
    camera_name = "*Integrated Camera*"
    check_command = f'powershell "Get-PnpDevice -FriendlyName \'{camera_name}\' | Where-Object {{ $_.Status -eq \'OK\' }}"'

    try:
        print("Checking if the integrated camera is active...")
        result_check = subprocess.run(
            check_command, shell=True, check=True, capture_output=True, text=True
        )
        if "OK" in result_check.stdout:
            print("Integrated camera is active.")
            return True
        else:
            print("Integrated camera is not active or not found.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Failed to check the status of the integrated camera: {e}")
        print(f"Error output: {e.stderr}")
        return False


def disable_integrated_camera():
    """Disables the integrated camera using PowerShell."""
    camera_name = "*Integrated Camera*"
    disable_command = f'powershell "Get-PnpDevice -FriendlyName \'{camera_name}\' | Disable-PnpDevice -Confirm:$false"'

    try:
        print("Disabling the integrated camera...")
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

def capture_images_from_cameras(output_folder="captured_images"):
    """Captures images from all available cameras and saves them to the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cameras = get_available_cameras()
    if not cameras:
        print("No cameras available.")
        return

    # Desired resolution
    desired_width = 3840
    desired_height = 2160

    print(f"Available cameras: {cameras}")
    for cam_index in cameras:
        cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            print(f"Unable to access camera {cam_index}")
            continue

        # Set the resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

        ret, frame = cap.read()
        if ret:
            filename = os.path.join(output_folder, f"camera_{cam_index}.png")
            cv2.imwrite(filename, frame)
            print(f"Image captured from camera {cam_index} and saved as {filename}")

        else:
            print(f"Failed to capture image from camera {cam_index}")

        cap.release()

    print("Image capture complete.")


if __name__ == "__main__":
    # Ensure the script runs as admin
    run_as_admin()

    # Check and disable the integrated camera if it is active
    if is_integrated_camera_active():
        disabled = disable_integrated_camera()
        if disabled:
            print("Integrated camera disabled successfully.")
        else:
            print("Failed to disable the integrated camera.")
    else:
        print("Integrated camera is not active. Skipping deactivation.")

    # Output folder for captured images
    output_folder = "Testing"

    # Capture images from all available cameras
    capture_images_from_cameras(output_folder)