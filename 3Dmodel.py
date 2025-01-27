import cv2
import numpy as np
import open3d as o3d
import os


def detect_and_match_features(image1, image2):
    """Detect and match features between two images using SIFT."""
    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and compute descriptors
    kp1, des1 = sift.detectAndCompute(image1, None)
    kp2, des2 = sift.detectAndCompute(image2, None)

    # Use FLANN-based matcher
    index_params = dict(algorithm=1, trees=5)  # KD-Tree
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Filter matches using Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    return kp1, kp2, good_matches


def compute_point_cloud(matches, kp1, kp2, K):
    """Compute a sparse point cloud using matched features and camera matrix K."""
    # Extract matched keypoints
    points1 = np.array([kp1[m.queryIdx].pt for m in matches])
    points2 = np.array([kp2[m.trainIdx].pt for m in matches])

    # Estimate the essential matrix
    E, mask = cv2.findEssentialMat(points1, points2, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)

    # Recover the relative camera pose
    _, R, t, mask_pose = cv2.recoverPose(E, points1, points2, K)

    # Triangulate points to generate a sparse point cloud
    points1_hom = cv2.convertPointsToHomogeneous(points1).reshape(-1, 3).T
    points2_hom = cv2.convertPointsToHomogeneous(points2).reshape(-1, 3).T

    P1 = np.dot(K, np.hstack((np.eye(3), np.zeros((3, 1)))))  # Projection matrix of camera 1
    P2 = np.dot(K, np.hstack((R, t)))  # Projection matrix of camera 2

    points_4d = cv2.triangulatePoints(P1, P2, points1.T, points2.T)
    points_3d = points_4d[:3] / points_4d[3]  # Convert to 3D

    return points_3d.T


def generate_dense_point_cloud(sparse_cloud):
    """Convert sparse cloud into dense point cloud (dummy example for now)."""
    # This function can be enhanced with a real densification algorithm
    dense_cloud = sparse_cloud  # Placeholder: You can use MVS libraries for densification
    return dense_cloud


def create_3d_mesh(point_cloud):
    """Create a 3D mesh from a point cloud using Open3D."""
    # Convert point cloud to Open3D format
    o3d_cloud = o3d.geometry.PointCloud()
    o3d_cloud.points = o3d.utility.Vector3dVector(point_cloud)

    # Estimate normals for better meshing
    o3d_cloud.estimate_normals()

    # Create a mesh using Poisson reconstruction
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(o3d_cloud, depth=8)
    return mesh


def save_mesh(mesh, output_file="output_mesh.obj"):
    """Save the mesh to a file."""
    o3d.io.write_triangle_mesh(output_file, mesh)
    print(f"3D model saved as {output_file}")


def main(image_folder, K):
    """Main pipeline for 3D reconstruction."""
    # Load images
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(".jpg")]
    images = [cv2.imread(f) for f in sorted(image_files)]

    if len(images) < 2:
        print("At least two images are required for 3D reconstruction.")
        return

    # Detect and match features between the first two images
    kp1, kp2, matches = detect_and_match_features(images[0], images[1])

    # Compute sparse point cloud
    sparse_cloud = compute_point_cloud(matches, kp1, kp2, K)

    # Generate dense point cloud
    dense_cloud = generate_dense_point_cloud(sparse_cloud)

    # Create a 3D mesh
    mesh = create_3d_mesh(dense_cloud)

    # Save the mesh to a file
    save_mesh(mesh)


if __name__ == "__main__":
    # Folder containing captured images
    image_folder = "test_images"

    # Camera intrinsic matrix (example values, adjust based on your camera)
    K = np.array([[495.21153939, 0, 335.75450282], [0, 504.81851369, 179.00894773], [0, 0, 1]])

    # Run the reconstruction pipeline
    main(image_folder, K)
