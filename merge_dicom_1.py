import os
import pydicom
import numpy as np

# Directories containing the DICOM series
series_1_dir = 'merge_dicom_a'
series_2_dir = 'merge_dicom_b'
output_dir = 'merged_dicom'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to load DICOM files from a directory
def load_dicom_files(directory):
    dicom_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".dcm"):
            filepath = os.path.join(directory, filename)
            dicom_files.append(pydicom.dcmread(filepath))
    return dicom_files

# Load DICOM files from both series
series_1_files = load_dicom_files(series_1_dir)
series_2_files = load_dicom_files(series_2_dir)

# Combine the DICOM files into one list
combined_series_files = series_1_files + series_2_files

# Sort the combined list of DICOM files by Instance Number or another relevant attribute
def get_instance_number(dicom_file):
    return getattr(dicom_file, 'InstanceNumber', float('inf'))

combined_series_files.sort(key=get_instance_number)

# Get the position of the last image in the first series
last_image_series_1 = series_1_files[-1]
first_image_series_2 = series_2_files[0]

# Calculate the offset
last_position_series_1 = np.array(last_image_series_1.ImagePositionPatient, dtype=float)
first_position_series_2 = np.array(first_image_series_2.ImagePositionPatient, dtype=float)
offset = first_position_series_2 - last_position_series_1

# Adjust the ImagePositionPatient for the second series
def format_position_value(value):
    return "{:.10g}".format(value)  # Format value to fit within 16 characters

for dicom_file in series_2_files:
    position = np.array(dicom_file.ImagePositionPatient, dtype=float)
    adjusted_position = position - offset
    dicom_file.ImagePositionPatient = [format_position_value(coord) for coord in adjusted_position]

# Generate a new Series Instance UID for the merged series
new_series_instance_uid = pydicom.uid.generate_uid()

# Save the combined series to the output directory
for i, dicom_file in enumerate(combined_series_files, start=1):
    # Update the InstanceNumber and any other necessary metadata
    dicom_file.InstanceNumber = i
    dicom_file.SeriesInstanceUID = new_series_instance_uid
    
    # Define the output filename
    output_filename = f'a_{i:04d}.dcm'
    output_filepath = os.path.join(output_dir, output_filename)
    
    # Save the updated DICOM file
    dicom_file.save_as(output_filepath)

print("DICOM series merged and saved successfully.")