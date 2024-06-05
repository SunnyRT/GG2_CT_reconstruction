import os
import pydicom
import uuid

def modify_dicom_uids(directory, new_study_uid, new_series_uid):
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file name starts with "rectified_processed_a_"
            if not file.startswith("processed_processed_a_"):
                continue
            
            file_path = os.path.join(root, file)
            
            try:
                dicom_dataset = pydicom.dcmread(file_path)
                
                if hasattr(dicom_dataset, 'StudyInstanceUID') and hasattr(dicom_dataset, 'SeriesInstanceUID'):
                    # Print original UIDs
                    print(f"Original StudyInstanceUID for {file_path}: {dicom_dataset.StudyInstanceUID}")
                    print(f"Original SeriesInstanceUID for {file_path}: {dicom_dataset.SeriesInstanceUID}")
                    
                    # Modify UIDs
                    dicom_dataset.StudyInstanceUID = new_study_uid
                    dicom_dataset.SeriesInstanceUID = new_series_uid
                    
                    # Print new UIDs
                    print(f"New StudyInstanceUID for {file_path}: {dicom_dataset.StudyInstanceUID}")
                    print(f"New SeriesInstanceUID for {file_path}: {dicom_dataset.SeriesInstanceUID}")
                    
                    # Save modified DICOM file
                    dicom_dataset.save_as(file_path)
                    print(f"DICOM file {file_path} saved with new UIDs.")
                else:
                    print(f"{file_path} is not a valid DICOM file or does not contain the required UIDs.")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# Directory path and new UIDs
directory_path = '/Users/tonganze/Desktop/Cam IIA/GG2/processed_dicom_data/processed_merged_a-b'  # Update this path
new_study_uid = "GG2 20240529"  # Example StudyInstanceUID, update with your UID
new_series_uid = str(uuid.uuid4())  # Generate a new SeriesInstanceUID

# Modify the UIDs
modify_dicom_uids(directory_path, new_study_uid, new_series_uid)
