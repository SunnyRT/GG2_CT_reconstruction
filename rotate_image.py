import cv2
import numpy as np
import pydicom
import os
from matplotlib import pyplot as plt

def read_dicom_image(file_path):
    dicom_file = pydicom.dcmread(file_path)
    image = dicom_file.pixel_array
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    return image, dicom_file

def transform_image(image, angle, dx, dy):
    h, w = image.shape
    center = (w / 2, h / 2)
    M_rot = cv2.getRotationMatrix2D(center, angle, 1.0)
    M_trans = np.float32([[1, 0, dx], [0, 1, dy]])
    rotated_image = cv2.warpAffine(image, M_rot, (w, h), flags=cv2.INTER_LINEAR)
    transformed_image = cv2.warpAffine(rotated_image, M_trans, (w, h), flags=cv2.INTER_LINEAR)
    return transformed_image

def save_dicom_image(dicom_file, image, output_path):
    original_shape = dicom_file.pixel_array.shape
    resized_image = cv2.resize(image, (original_shape[1], original_shape[0]), interpolation=cv2.INTER_LINEAR)
    dicom_file.PixelData = resized_image.tobytes()
    dicom_file.Rows, dicom_file.Columns = resized_image.shape
    dicom_file.save_as(output_path)

def measure_transformation(original_image, transformed_image):
    if original_image.dtype != np.uint8:
        original_image = cv2.normalize(original_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if transformed_image.dtype != np.uint8:
        transformed_image = cv2.normalize(transformed_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(original_image, None)
    kp2, des2 = orb.detectAndCompute(transformed_image, None)

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

def process_images(directory, start_number, rotation_angle, dx, dy, tolerance=0.5):
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".dcm"):
            continue
        
        try:
            parts = filename.split('_')
            if len(parts) != 3 or not parts[2].endswith('.dcm'):
                print(f"Skipping file with invalid format: {filename}")
                continue
            file_number = int(parts[2].split('.')[0])
        except ValueError:
            print(f"Skipping file with invalid format: {filename}")
            continue
        
        file_path = os.path.join(directory, filename)
        print(f"Processing {filename} with number {file_number}...")
        image, dicom_file = read_dicom_image(file_path)
        
        if file_number > start_number:
            print(f"Transforming image {filename} by {rotation_angle} degrees rotation and shift ({dx}, {dy}).")
            transformed_image = transform_image(image, rotation_angle, dx, dy)
            
            new_dx, new_dy, new_angle, kp1, kp2, matches = measure_transformation(image, transformed_image)
            if new_dx is not None and new_dy is not None and new_angle is not None:
                if abs(new_dx - dx) > tolerance or abs(new_dy - dy) > tolerance or abs(new_angle - rotation_angle) > tolerance:
                    print(f"Transformation failed for {filename}: dx={new_dx}, dy={new_dy}, angle={new_angle}")
                    #visualize_matches(image, transformed_image, kp1, kp2, matches)
                else:
                    print(f"Transformation succeeded for {filename}: dx={new_dx}, dy={new_dy}, angle={new_angle}")
            else:
                print(f"Unable to measure transformation for {filename}")

            output_filename = f"processed_{filename}"
            output_path = os.path.join(directory, output_filename)
            save_dicom_image(dicom_file, transformed_image, output_path)
            print(f"Saved processed image as {output_path}")
        else:
            print(f"No transformation applied to image {filename}. Saving without modification.")
            output_filename = f"processed_{filename}"
            output_path = os.path.join(directory, output_filename)
            save_dicom_image(dicom_file, image, output_path)
            print(f"Saved processed image as {output_path}")

# Example usage
directory = '/Users/tonganze/Desktop/Cam IIA/GG2/processed_dicom_data/processed_merged_a-b'
start_number = 581
rotation_angle = -0.036411110617445286
dx, dy = -0.847543051943298, -2.049354690739822
process_images(directory, start_number, rotation_angle, dx, dy)
