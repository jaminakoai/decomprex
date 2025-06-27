import zipfile

def detect_engine(apk_path):
    """APK dosyasından uygulama motorunu tespit eder."""
    with zipfile.ZipFile(apk_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        if any("libil2cpp.so" in f for f in file_list) or "assets/bin/Data" in file_list:
            return "Unity"
        if any("libapp.so" in f for f in file_list) or "assets/flutter_assets" in file_list:
            return "Flutter"
        if any("index.android.bundle" in f for f in file_list):
            return "React Native"
        return "Native"
