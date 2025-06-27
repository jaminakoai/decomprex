import zipfile
import os
import shutil

def extract_split_apks(apks_path, split_output_dir):
    """APKS dosyasındaki tüm split APK'leri çıkartır."""
    os.makedirs(split_output_dir, exist_ok=True)
    with zipfile.ZipFile(apks_path, 'r') as z:
        for file in z.namelist():
            if file.endswith('.apk'):
                z.extract(file, split_output_dir)
    # Base ve splitleri ayrı tut
    base_apk = None
    split_apks = []
    for fname in os.listdir(split_output_dir):
        fpath = os.path.join(split_output_dir, fname)
        if fname == "base.apk":
            base_apk = fpath
        elif fname.endswith(".apk"):
            split_apks.append(fpath)
    return base_apk, split_apks
