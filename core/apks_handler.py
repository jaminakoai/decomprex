import zipfile
import os
import shutil

def extract_apks(apks_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with zipfile.ZipFile(apks_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    split_dir = os.path.join(output_dir, 'split')
    os.makedirs(split_dir, exist_ok=True)
    for file in os.listdir(output_dir):
        if file.endswith('.apk'):
            shutil.copy(os.path.join(output_dir, file), split_dir)
