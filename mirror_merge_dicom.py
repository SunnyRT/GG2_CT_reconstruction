import pydicom
import numpy as np
import os

def mirror_and_rename_dicom_series(input_directory, output_directory, input_prefix='b_', output_prefix='a_', start=1, end=434, new_start=582):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    total_files = end - start + 1
    new_end = new_start + total_files - 1

    for i in range(start, end + 1):
        # Generate input file name with leading zeros
        input_file_number = str(i).zfill(4)
        input_file_name = f"{input_prefix}{input_file_number}.dcm"
        input_path = os.path.join(input_directory, input_file_name)

        # Calculate the new file number for inversion and renaming
        new_file_number = str(new_start + (total_files - (i - start + 1))).zfill(4)
        output_file_name = f"{output_prefix}{new_file_number}.dcm"
        output_path = os.path.join(output_directory, output_file_name)

        try:
            # Load the DICOM file
            ds = pydicom.dcmread(input_path)

            # Extract the image data
            image_data = ds.pixel_array

            # Mirror the image data (horizontal flip)
            mirrored_image_data = np.fliplr(image_data)

            # Update the pixel data in the DICOM dataset
            ds.PixelData = mirrored_image_data.tobytes()

            # Save the modified DICOM file with the new name
            ds.save_as(output_path)

            print(f"Processed and saved: {output_path}")

        except Exception as e:
            print(f"Failed to process {input_path}: {e}")

# Define the input and output directories
input_directory = 'mirror_b'
output_directory = 'mirrored_b'

# Mirror and rename the DICOM series
#mirror_and_rename_dicom_series(input_directory, output_directory)

