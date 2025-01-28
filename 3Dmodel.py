import os
import cv2
import numpy as np
import open3d as o3d


# Function to load images from the folder
def load_images_from_folder(folder):
    images = []
    for filename in sorted(os.listdir(folder)):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img)
    return images


# Detect and match features
def detect_and_match_features(images):
    sift = cv2.SIFT_create(nfeatures=3000)
    orb = cv2.ORB_create(nfeatures=10000)
    keypoints = []
    descriptors = []
    matches = []

    for i in range(len(images) - 1):
        # Convert to grayscale
        gray1 = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(images[i+1], cv2.COLOR_BGR2GRAY)

        #Equalize histograms
        equalized1 = cv2.equalizeHist(gray1)
        equalized2 = cv2.equalizeHist(gray2)

        #Blur the images
        blurred1 = cv2.GaussianBlur(equalized1, (5, 5), 0)
        blurred2 = cv2.GaussianBlur(equalized2, (5, 5), 0)

        # Detect ORB features and descriptors
        kp1, des1 = sift.detectAndCompute(images[i], None)
        kp2, des2 = sift.detectAndCompute(images[i+1], None)

        #kp1, des1 = sift.detectAndCompute(images[i], None)
        #kp2, des2 = sift.detectAndCompute(images[i+1], None)

        # Match features
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        raw_matches = bf.match(des1, des2)
        raw_matches = sorted(raw_matches, key=lambda x: x.distance)

        # Store results
        keypoints.append((kp1, kp2))
        descriptors.append((des1, des2))
        matches.append(raw_matches)

        #Debug: draw matches
        #img_matches = cv2.drawMatches(images[i], kp1, images[i + 1], kp2, raw_matches[:50], None)
        #cv2.imshow("Matches", img_matches)
        #cv2.waitKey(0)

    #Debug:
    print(f"Number of matches: {[len(m) for m in matches]}")

    return keypoints, descriptors, matches


# Reconstruct sparse 3D point cloud
def reconstruct_3d(matches, keypoints, images):
    # Placeholder for SfM pipeline. This is typically complex and may require tools like COLMAP or OpenMVG.
    # Intrinsic matrix:
    K = np.array([[495.21153939, 0, 335.75450282], [0, 504.81851369, 179.00894773], [0, 0, 1]])
    points_3d = []

    print(f"Starting 3D reconstruction with {len(matches)} image pairs.")

    for i, match_set in enumerate(matches):
        print(f"Processing Image pair {i}")
        print(f"Number of matches: {len(match_set)}")

        kp1, kp2 = keypoints[i]
        pts1 = np.float32([kp1[m.queryIdx].pt for m in match_set])
        pts2 = np.float32([kp2[m.trainIdx].pt for m in match_set])

        print(f"Triangulating {len(pts1)} points.")

        if len(pts1) < 8:  # Not enough points for essential matrix calculation
            print(f"Skipping frame {i} -> {i + 1}: Not enough matches.")
            continue

        E, _ = cv2.findEssentialMat(pts1, pts2, K, method=cv2.RANSAC, prob=0.999, threshold=2.0)
        _, R, t, _ = cv2.recoverPose(E, pts1, pts2, K)

        # Essential Matrix Debugging
        print(f"Essential matrix inliers: {np.sum(_)}")

        # Triangulate points (example)
        P1 = np.dot(K, np.hstack((np.eye(3), np.zeros((3, 1)))))
        P2 = np.dot(K, np.hstack((R, t)))
        points_hom = cv2.triangulatePoints(P1, P2, pts1.T, pts2.T)
        points_3d.append(cv2.convertPointsFromHomogeneous(points_hom.T))

        print(f"Triangulating {len(pts1)} points.")
        print(f"Triangulated points (homogeneous): {points_hom.shape}")

        points = cv2.convertPointsFromHomogeneous(points_hom.T).reshape(-1, 3)
        valid_points = points[np.isfinite(points).all(axis=1)]
        print(f"Image pair {i}: {valid_points.shape[0]} valid 3D points.")

        if points_hom.size == 0:
            print(f"Triangulation failed for Image pair {i}.")
            continue

        if len(points_3d) == 0:
            print("No 3D points reconstructed.")
        return np.array([])

        print(f"Image pair {i}: {points_3d.shape[0]} points reconstructed.")

    return np.vstack(points_3d)


# Save 3D model as .ply file
def save_point_cloud(points, output_file):
    # Check:
    if points.shape[0] == 0:
        print("No points to save. Point cloud is empty.")
        return

    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud(output_file, cloud)
    print(f"3D model saved to {output_file}")


# Main function
def main():
    input_folder = ("Gingy")
    output_file = "output_model.ply"

    images = load_images_from_folder(input_folder)
    if not images:
        print("No images found in the folder.")
        return

    keypoints, descriptors, matches = detect_and_match_features(images)
    points_3d = reconstruct_3d(matches, keypoints, images)

    if points_3d.size == 0:
        print("Failed to generate 3D points.")
        return

    save_point_cloud(points_3d.reshape(-1, 3), output_file)


if __name__ == "__main__":
    main()
