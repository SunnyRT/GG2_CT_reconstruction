import cv2
import numpy as np
import pydicom
import matplotlib.pyplot as plt

def read_dicom_image(file_path):
    # Read the DICOM file
    dicom_file = pydicom.dcmread(file_path)
    # Extract the image data as a numpy array
    image = dicom_file.pixel_array
    # Convert the image to 8-bit grayscale (if necessary)
    image = cv2.convertScaleAbs(image, alpha=(255.0/image.max()))
    return image

def find_rotation_and_visualize(image1_path, image2_path):
    # Read the images from DICOM files
    img1 = read_dicom_image(image1_path)
    img2 = read_dicom_image(image2_path)
    
    # Check if images are loaded correctly
    if img1 is None or img2 is None:
        print("Error: One of the images didn't load correctly.")
        return

    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Detect SIFT features and compute descriptors
    keypoints1, descriptors1 = sift.detectAndCompute(img1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(img2, None)

    # Initialize the FLANN-based matcher
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Match the descriptors
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    # Apply ratio test to get the good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Extract the matched keypoints
    if len(good_matches) > 4:
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Find the homography matrix
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # Define the intrinsic camera matrix
        h, w = img1.shape
        K = np.array([[w, 0, w / 2],
                      [0, h, h / 2],
                      [0, 0, 1]])

        # Decompose the homography matrix to get the rotation angle
        _, Rs, Ts, Ns = cv2.decomposeHomographyMat(M, K)

        # Assuming the first rotation matrix
        R = Rs[0]

        # Calculate the rotation angle from the rotation matrix
        rotation_angle = np.degrees(np.arctan2(R[1, 0], R[0, 0]))

        print(f"Estimated rotation angle: {rotation_angle} degrees")

        # Rotate the second image to align it with the first image
        center = (w / 2, h / 2)
        M_rot = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
        img2_rotated = cv2.warpAffine(img2, M_rot, (w, h))

        # Visualize the difference
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 3, 1)
        plt.title("Image 1")
        plt.imshow(img1, cmap='gray')
        plt.subplot(1, 3, 2)
        plt.title("Image 2 (Rotated)")
        plt.imshow(img2_rotated, cmap='gray')
        plt.subplot(1, 3, 3)
        plt.title("Overlay")
        overlay = cv2.addWeighted(img1, 0.5, img2_rotated, 0.5, 0)
        plt.imshow(overlay, cmap='gray')
        plt.show()
    else:
        print("Not enough matches are found - {}/{}".format(len(good_matches), 4))
        rotation_angle = None

    return rotation_angle

dicom_file1 = '/Users/tonganze/Desktop/Cam IIA/GG2/processed_dicom_data/processed_merged_a-b/rectified2_processed_a_0581.dcm'
dicom_file2 = '/Users/tonganze/Desktop/Cam IIA/GG2/processed_dicom_data/processed_merged_a-b/rectified2_processed_a_0582.dcm'

rotation_angle = find_rotation_and_visualize(dicom_file1, dicom_file2)

if rotation_angle is not None:
    print(f"Rotation angle between the images: {rotation_angle} degrees")
else:
    print("Could not determine the rotation angle.")
