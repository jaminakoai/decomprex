import os
import re

def patch_manifest_permissions(manifest_path):
    """AndroidManifest.xml üzerinde dangerous permission veya debug flag düzenler."""
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # örnek: android:debuggable="true" → "false"
    content = re.sub(r'android:debuggable="true"', 'android:debuggable="false"', content)
    # örnek: Gereksiz farazi izinleri kaldır
    content = re.sub(r'<uses-permission android:name="android\.permission\.SYSTEM_ALERT_WINDOW"\s*/>', '', content)
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)
