import os
import sys
import shutil
import zipfile
import subprocess
import click

# Konfigürasyon
BUNDLETOOL_JAR = os.path.abspath("bundletool-all.jar")
APKS_OUT_DIR = os.path.abspath("apks")
SIGNED_DIR = os.path.abspath("signed_apks")
KEYSTORE = os.path.abspath("my-release-key.jks")
KEY_ALIAS = "key0"
KEYSTORE_PASS = "Ali2019..."
KEY_PASS = "Ali2019..."

@click.command()
@click.option('--apk', 'apk_path', type=click.Path(), help='APK veya APKS dosyası yolu')
def main(apk_path):
    if not apk_path or not os.path.exists(apk_path):
        print("Bir APK veya APKS dosyası gereklidir.")
        sys.exit(1)

    if apk_path.endswith('.apks'):
        check_tools()
        extract_apks(apk_path)
        base_apk = find_apk("base.apk", APKS_OUT_DIR)
        if not base_apk:
            print("base.apk bulunamadı, çıkış yapılıyor.")
            sys.exit(1)
        # Patch fonksiyonunu burada çağır
        patch_base_apk(base_apk)
        resign_all_apks()
        print_adb_install_instructions()
        print("[✓] Split APK işlemleri tamamlandı.")
        sys.exit(0)

    print("Sadece .apks dosyaları için geliştirilmiştir.")
    sys.exit(1)

def check_tools():
    if not os.path.exists(BUNDLETOOL_JAR):
        print("bundletool-all.jar bulunamadı!")
        sys.exit(1)
    if not shutil.which("apksigner"):
        print("apksigner aracı bulunamadı! (Android SDK Build Tools içinde gelir)")
        sys.exit(1)
    if not shutil.which("adb"):
        print("adb aracı bulunamadı!")
        sys.exit(1)
    if not shutil.which("jarsigner"):
        print("jarsigner aracı bulunamadı!")
        sys.exit(1)
    if not os.path.exists(KEYSTORE):
        print("İmzalama için my-release-key.jks dosyası ana klasörde olmalı! (keytool ile üretilebilir)")
        sys.exit(1)

def extract_apks(apks_path):
    print(f"[1] .apks dosyasını çıkartıyor: {apks_path}")
    if os.path.exists(APKS_OUT_DIR):
        shutil.rmtree(APKS_OUT_DIR)
    os.makedirs(APKS_OUT_DIR, exist_ok=True)
    with zipfile.ZipFile(apks_path, "r") as z:
        z.extractall(APKS_OUT_DIR)
    print(f"[✓] Tüm split APK'lar '{APKS_OUT_DIR}' klasörüne çıkarıldı.")

def find_apk(name, root):
    for root_dir, _, files in os.walk(root):
        for f in files:
            if f == name:
                return os.path.join(root_dir, f)
    return None

def patch_base_apk(base_apk_path):
    print(f"[2] base.apk üzerinde satın alma patch uygulanıyor: {base_apk_path}")
    # Satın alma bypass için örnek patch fonksiyonu:
    smali_patch_purchase_true(base_apk_path)
    print("[✓] base.apk satın alma patch işlemi tamamlandı.")

def smali_patch_purchase_true(apk_path):
    """
    Örnek: Satın alma kontrolünün geçtiği bir fonksiyonun (isPurchased, hasPremium vs.) her zaman true dönmesini patch'le.
    Burada örnek olarak apktool ile decompile edip smali dosyasında return true (const/4 v0, 0x1; return v0) yapılır.
    """
    # 1. Decompile
    decompiled_dir = apk_path + "_decompiled"
    if os.path.exists(decompiled_dir):
        shutil.rmtree(decompiled_dir)
    print("  [*] Apktool ile decompile ediliyor...")
    subprocess.run([
        "apktool", "d", "-f", apk_path, "-o", decompiled_dir
    ], check=True)

    # 2. Smali dosyasını bul ve patchle (örnek method adı, senin uygulamana göre değiştir)
    # Burada örneği generic bırakıyoruz, gerçek patch için methodu bulmalısın!
    target_smali = None
    method_name = "isPurchased"  # örnek, uygulamanın satın alma methodunu bul!
    for root, _, files in os.walk(decompiled_dir):
        for file in files:
            if file.endswith(".smali"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if f".method public {method_name}()" in content:
                    target_smali = path
                    break
        if target_smali:
            break
    if target_smali:
        print(f"  [+] Patch uygulanıyor: {target_smali}")
        with open(target_smali, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        new_lines = []
        patch_applied = False
        in_method = False
        for line in lines:
            if f".method public {method_name}()" in line:
                in_method = True
                new_lines.append(line)
                continue
            if in_method and ".end method" in line:
                # Methodun başında return true ekle!
                new_lines.append("    const/4 v0, 0x1\n    return v0\n")
                patch_applied = True
                in_method = False
            new_lines.append(line)
        if patch_applied:
            with open(target_smali, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        else:
            print("  [!] Patch uygulanacak method bulunamadı. Kendin kontrol et!")
    else:
        print("  [!] Patch uygulanacak method bulunamadı. Kendin kontrol et!")

    # 3. Rebuild
    print("  [*] Apktool ile tekrar build ediliyor...")
    rebuilt_apk = apk_path.replace(".apk", "_patched.apk")
    subprocess.run([
        "apktool", "b", decompiled_dir, "-o", rebuilt_apk
    ], check=True)
    # 4. Orijinal apk'yı yedekle, patcheden kopyala
    shutil.move(rebuilt_apk, apk_path)
    shutil.rmtree(decompiled_dir)
    print("  [+] Patchlenmiş APK kaydedildi.")

def resign_all_apks():
    print(f"[3] Tüm APK'lar {SIGNED_DIR} klasörüne kopyalanıyor ve tekrar imzalanıyor...")
    if os.path.exists(SIGNED_DIR):
        shutil.rmtree(SIGNED_DIR)
    os.makedirs(SIGNED_DIR, exist_ok=True)
    for root_dir, _, files in os.walk(APKS_OUT_DIR):
        for file in files:
            if file.endswith(".apk"):
                src_apk = os.path.join(root_dir, file)
                dst_apk = os.path.join(SIGNED_DIR, file)
                shutil.copy2(src_apk, dst_apk)
                sign_apk(dst_apk)
    print(f"[✓] Tüm APK'lar tekrar imzalandı ve {SIGNED_DIR} klasörüne kopyalandı.")

def sign_apk(apk_path):
    print(f"    İmzalanıyor: {os.path.basename(apk_path)}")
    unsigned_apk = apk_path.replace(".apk", "_unsigned.apk")
    shutil.move(apk_path, unsigned_apk)
    jarsigner_cmd = [
        "jarsigner",
        "-verbose",
        "-keystore", KEYSTORE,
        "-storepass", KEYSTORE_PASS,
        "-keypass", KEY_PASS,
        unsigned_apk,
        KEY_ALIAS
    ]
    subprocess.run(jarsigner_cmd, check=True)
    apksigner_cmd = [
        "apksigner", "sign",
        "--ks", KEYSTORE,
        "--ks-key-alias", KEY_ALIAS,
        "--ks-pass", f"pass:{KEYSTORE_PASS}",
        "--key-pass", f"pass:{KEY_PASS}",
        "--out", apk_path,
        unsigned_apk
    ]
    subprocess.run(apksigner_cmd, check=True)
    os.remove(unsigned_apk)

def print_adb_install_instructions():
    print("\n[4] Split APK'lar telefona toplu yüklemek için şu komutu kullan:")
    print(f"\ncd {SIGNED_DIR}\nadb install-multiple *.apk\n")

if __name__ == "__main__":
    main()
