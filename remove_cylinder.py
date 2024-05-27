import pydicom
import glob
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os

# Specify the path to your DICOM directory and a sample DICOM file for adjustment
dicom_dir = '/Users/tonganze/Desktop/Cam IIA/GG2/Low resolution reconstructed CT data-20240527/recon_data_b'
dicom_file = '/Users/tonganze/Desktop/Cam IIA/GG2/Low resolution reconstructed CT data-20240527/recon_data_b/recon_data_b_0028.dcm'

# Initial guess for the parameters
x, y, r = 64, 64, 50  # Adjusted initial values for a smaller circle

def visualize_circle(image, x, y, r):
    # Create a copy of the image
    img_copy = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # Draw the circle on the image copy
    cv2.circle(img_copy, (x, y), r, (0, 255, 0), thickness=2)
    return img_copy

def remove_outer_circle(image, x, y, r):
    # Directly remove the outer circle by setting the pixels to 0
    mask = np.zeros_like(image, dtype=np.uint8)
    cv2.circle(mask, (x, y), r, (255, 255, 255), thickness=-1)
    mask = mask == 0
    image[mask] = 0
    return image

def process_dicom(file_path, x, y, r, preview=False):
    # Read the DICOM file
    dicom_dataset = pydicom.dcmread(file_path)

    # Extract the image data
    if hasattr(dicom_dataset, 'pixel_array'):
        pixel_array = dicom_dataset.pixel_array

        # Remove the outer circle
        processed_image = remove_outer_circle(pixel_array, x, y, r)

        if preview:
            return processed_image, pixel_array

        # Save the modified image as a new DICOM file
        dicom_dataset.PixelData = processed_image.tobytes()
        output_path = os.path.join(dicom_dir, 'processed_' + os.path.basename(file_path))
        dicom_dataset.save_as(output_path)
        print(f"Processed file saved to: {output_path}")

    else:
        print(f"No image data found in {file_path}")

# Read the DICOM file and get the image
image = process_dicom(dicom_file, x, y, r, preview=True)

if image is not None:
    processed_image, original_image = image
    while True:
        # Display the image with the current circle overlay
        img_with_circle = visualize_circle(original_image, x, y, r)
        plt.imshow(img_with_circle, cmap='gray')
        plt.title("Adjust the circle parameters")
        plt.show()

        # Interactive input for adjusting the parameters
        adjust = input("Adjust (x/y/r) or done? ").strip().lower()
        if adjust == 'x':
            x = int(input("Enter new x coordinate: "))
        elif adjust == 'y':
            y = int(input("Enter new y coordinate: "))
        elif adjust == 'r':
            r = int(input("Enter new radius: "))
        elif adjust == 'done':
            break
        else:
            print("Invalid input. Please enter 'x', 'y', 'r', or 'done'.")

    # Apply the final parameters to all images in the directory
    dicom_files = glob.glob(f"{dicom_dir}/*.dcm")
    for dicom_file in dicom_files:
        process_dicom(dicom_file, x, y, r)
else:
    print("Failed to read the DICOM file.")
