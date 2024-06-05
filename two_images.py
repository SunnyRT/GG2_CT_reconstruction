import cv2
import numpy as np
import pydicom
from matplotlib import pyplot as plt
from scipy.optimize import differential_evolution

# Function to read a DICOM image and convert it to grayscale if necessary
def read_dicom_image(file_path):
    dicom_file = pydicom.dcmread(file_path)
    image = dicom_file.pixel_array
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    return image, dicom_file

# Function to apply rotation and translation transformations to an image
def transform_image(image, angle, dx, dy):
    h, w = image.shape
    center = (w / 2, h / 2)
    M_rot = cv2.getRotationMatrix2D(center, angle, 1.0)
    M_trans = np.float32([[1, 0, dx], [0, 1, dy]])
    rotated_image = cv2.warpAffine(image, M_rot, (w, h), flags=cv2.INTER_LINEAR)
    transformed_image = cv2.warpAffine(rotated_image, M_trans, (w, h), flags=cv2.INTER_LINEAR)
    return transformed_image

# Function to measure the transformation between the original and transformed images using ORB features
def measure_transformation(original_image, transformed_image):
    if original_image.dtype != np.uint8:
        original_image = cv2.normalize(original_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if transformed_image.dtype != np.uint8:
        transformed_image = cv2.normalize(transformed_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(original_image, None)
    kp2, des2 = orb.detectAndCompute(transformed_image, None)

    if des1 is None or des2 is None:
        raise ValueError("Descriptors not found. Ensure the images have sufficient features.")

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    M, mask = cv2.estimateAffinePartial2D(src_pts, dst_pts)

    if M is not None:
        dx = M[0, 2]
        dy = M[1, 2]
        angle = np.arctan2(M[1, 0], M[0, 0]) * 180 / np.pi
    else:
        dx, dy, angle = None, None, None

    return dx, dy, angle, kp1, kp2, matches

# Function to visualize the matches between keypoints in the original and transformed images
def visualize_matches(original_image, transformed_image, kp1, kp2, matches):
    if original_image.dtype != np.uint8:
        original_image_vis = cv2.normalize(original_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    else:
        original_image_vis = original_image

    if transformed_image.dtype != np.uint8:
        transformed_image_vis = cv2.normalize(transformed_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    else:
        transformed_image_vis = transformed_image

    matched_image = cv2.drawMatches(original_image_vis, kp1, transformed_image_vis, kp2, matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    plt.figure(figsize=(15, 10))
    plt.imshow(matched_image, cmap='gray')
    plt.title("ORB Keypoint Matches")
    plt.show()

# Objective function for optimization, measuring the error between the applied transformation and the expected transformation
def objective_function(params, original_image, transformed_image):
    angle, dx, dy = params
    transformed_image = transform_image(transformed_image, angle, dx, dy)
    try:
        new_dx, new_dy, new_angle, _, _, _ = measure_transformation(original_image, transformed_image)
        if new_dx is None or new_dy is None or new_angle is None:
            return float('inf')
        error = np.sqrt((new_dx - dx)**2 + (new_dy - dy)**2 + (new_angle - angle)**2)
    except ValueError:
        return float('inf')
    return error

# Function to optimize the transformation parameters using differential evolution
def optimize_transformation(image1, image2, bounds):
    result = differential_evolution(lambda params: objective_function(params, image1, image2), 
                                    bounds=bounds, strategy='best1bin', maxiter=500, 
                                    popsize=10, tol=1e-6, mutation=(0.5, 1), recombination=0.9)

    optimal_angle, optimal_dx, optimal_dy = result.x
    transformed_image = transform_image(image2, optimal_angle, optimal_dx, optimal_dy)
    _, _, _, kp1, kp2, matches = measure_transformation(image1, transformed_image)

    print(f"Optimal transformation found: dx={optimal_dx}, dy={optimal_dy}, angle={optimal_angle}")
    visualize_matches(image1, transformed_image, kp1, kp2, matches)



# Load the two images
image1, _ = read_dicom_image('/Users/tonganze/Desktop/Cam IIA/GG2/processed_dicom_data/processed_merged_a-b/processed_a_0581.dcm')
image2, _ = read_dicom_image('/Users/tonganze/Desktop/Cam IIA/GG2/processed_dicom_data/processed_merged_a-b/processed_a_0581.dcm')

# Bounds for the transformation parameters: angle, dx, dy
# You can adjust these bounds based on your expectations for the transformations needed
bounds = [(-5, 5), (-20, 20), (-20, 20)]

# Optimize transformation
optimize_transformation(image1, image2, bounds)
