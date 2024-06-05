import os

# Modify this directory to your own local dir
directory = '/Users/tonganze/Desktop/Cam IIA/GG2/processed_dicom_data/dicom_processed_data_b'


# 获取目录中匹配模式的文件列表，并按文件名中的四位数排序
files = sorted(
    [f for f in os.listdir(directory) if f.startswith('processed_a_') and f.endswith('.dcm')],
    key=lambda x: int(x.split('_')[2].split('.')[0])
)

# 提取文件中的序列号并排序
file_numbers = [int(f.split('_')[2].split('.')[0]) for f in files]

# 找到文件序列中的最小和最大编号
min_number = min(file_numbers)
max_number = max(file_numbers)

# 反转文件列表
files.reverse()

# 重命名每个文件
for i, filename in enumerate(files):
    new_count = min_number + i
    new_filename = f"processed_a_{str(new_count).zfill(4)}.dcm"
    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
    print(f"Renamed {filename} to {new_filename}")

print("All files have been renamed in reverse order.")
