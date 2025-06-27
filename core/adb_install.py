import os

def generate_adb_install_script(split_dir, output_script):
    """Split APK'ler için çoklu yükleme komutunu otomatik üretir."""
    apks = [os.path.join(split_dir, f) for f in os.listdir(split_dir) if f.endswith('.apk')]
    apks_str = " ".join(sorted(apks))
    with open(output_script, "w") as script:
        script.write(f'#!/bin/bash\nadb install-multiple -r {apks_str}\n')
    os.chmod(output_script, 0o755)
    return output_script
