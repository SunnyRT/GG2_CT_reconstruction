import os

# Modify this directory to your own local dir
directory = '/Users/tonganze/Desktop/Cam IIA/GG2/processed_dicom_data/dicom_processed_data_b'

# Define the starting count and the prefix for the new filenames
start_count = 582
prefix = 'processed_a_'

# Get a sorted list of files in the directory that match the pattern
files = sorted([f for f in os.listdir(directory) if f.startswith('processed_b_') and f.endswith('.dcm')])

# Rename each file
for i, filename in enumerate(files):
    new_filename = f"{prefix}{start_count + i}.dcm"
    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
    print(f"Renamed {filename} to {new_filename}")

print("All files have been renamed.")
