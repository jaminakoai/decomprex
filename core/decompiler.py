import os
import subprocess

def decompile_apk(apk_path, decompile_dir):
    jadx_out = os.path.abspath(os.path.join(decompile_dir, "jadx"))
    os.makedirs(jadx_out, exist_ok=True)
    apk_path_abs = os.path.abspath(apk_path)  # Mutlak yol kullan!
    if not apk_path_abs.endswith(".apk"):
        raise Exception("Yalnızca .apk dosyası decompile edilebilir.")
    if not os.path.exists(apk_path_abs):
        raise Exception(f"APK dosyası bulunamadı: {apk_path_abs}")
    try:
        subprocess.run(['jadx', '-d', jadx_out, apk_path_abs], check=True)
    except subprocess.CalledProcessError as e:
        print("JADX hatası:", e)
        raise
