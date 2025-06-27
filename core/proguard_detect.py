import os
import re

def detect_proguard(smali_dir):
    """ProGuard veya obfuscation tespitini gerçekleştirir, mapping çözümü önerir."""
    proguarded_classes = []
    for root, _, files in os.walk(smali_dir):
        for file in files:
            if file.startswith("a") and file.endswith('.smali'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                # Basit proguard pattern: class isimleri kısa ve anlamsız
                if re.match(r'\.class public L[a-zA-Z];', content):
                    proguarded_classes.append(path)
    return proguarded_classes

def suggest_mapping_solution():
    """Mapping dosyasının bulunması ve çözüm yolları hakkında bilgi verir."""
    return (
        "ProGuard tespit edildi. Mapping dosyasına ulaşabiliyorsanız "
        "('mapping.txt'), apktool veya jadx ile class isimlerini çözebilirsiniz. "
        "Aksi halde, kodun işlevini davranışsal analiz ile çıkarmanız önerilir."
    )
