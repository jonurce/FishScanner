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
    command = (
        'powershell "Get-PnpDevice -FriendlyName \'*Integrated Camera*\' | '
        'Disable-PnpDevice -Confirm:$false"'
    )
    try:
        print("Disabling the integrated camera...")
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        print(result.stdout)
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


def capture_images_from_cameras():
    """Captures images from all available cameras."""
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
            filename = f"camera_{cam_index}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Image saved from camera {cam_index} as {filename}")
        else:
            print(f"Failed to capture image from camera {cam_index}")

        cap.release()

    print("Done capturing images.")


if __name__ == "__main__":
    # Ensure the script runs as admin
    run_as_admin()

    # Disable the integrated camera
    disabled = disable_integrated_camera()

    if disabled:
        # Proceed to capture images from the remaining cameras
        capture_images_from_cameras()
    else:
        print("Unable to disable the integrated camera. Aborting.")
