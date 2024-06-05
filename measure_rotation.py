import cv2
import numpy as np
import pydicom
from skimage import transform
import matplotlib.pyplot as plt

# Function to read DICOM images and convert to numpy arrays
def read_dicom_image(filepath):
    dicom = pydicom.dcmread(filepath)
    image = dicom.pixel_array
    return image

# Load the DICOM images
image1 = read_dicom_image('/Users/tonganze/Desktop/Cam IIA/GG2/processed_dicom_data/processed_merged_a-b/processed_a_0581.dcm')
image2 = read_dicom_image('/Users/tonganze/Desktop/Cam IIA/GG2/processed_dicom_data/processed_merged_a-b/processed_a_0582.dcm')

# Normalize the images to the range [0, 255]
image1 = cv2.normalize(image1, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
image2 = cv2.normalize(image2, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Convert the images to grayscale (if they are not already)
if len(image1.shape) == 3:
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
else:
    gray1 = image1

if len(image2.shape) == 3:
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
else:
    gray2 = image2

# Detect ORB keypoints and descriptors
orb = cv2.ORB_create()
keypoints1, descriptors1 = orb.detectAndCompute(gray1, None)
keypoints2, descriptors2 = orb.detectAndCompute(gray2, None)

# Match descriptors using BFMatcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors1, descriptors2)

# Sort matches by distance
matches = sorted(matches, key=lambda x: x.distance)

# Draw matches (for visualization)
matches_img = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Extract location of good matches
points1 = np.zeros((len(matches), 2), dtype=np.float32)
points2 = np.zeros((len(matches), 2), dtype=np.float32)

for i, match in enumerate(matches):
    points1[i, :] = keypoints1[match.queryIdx].pt
    points2[i, :] = keypoints2[match.trainIdx].pt

# Find homography
h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

# Use homography to warp image
height, width = image2.shape
image1_aligned = cv2.warpPerspective(image1, h, (width, height))

# Calculate the rotation and shift
dx, dy = h[0, 2], h[1, 2]
angle = -np.arctan2(h[1, 0], h[0, 0]) * 180 / np.pi

print(f"Shift: dx={dx}, dy={dy}")
print(f"Rotation: angle={angle} degrees")

# Show images (optional)
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title('Matches')
plt.imshow(matches_img)
plt.subplot(1, 2, 2)
plt.title('Aligned Image')
plt.imshow(image1_aligned, cmap='gray')
plt.show()
