import os
import re

def bypass_premium(smali_dir):
    for root, _, files in os.walk(smali_dir):
        for file in files:
            if file.endswith('.smali'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                # isPremium fonksiyonunu true döndür
                content = re.sub(
                    r'\.method[^\n]*isPremium[^\n]*\n(.*?)\.end method',
                    lambda m: re.sub(r'return [01]', 'return 1', m.group(0)), 
                    content, flags=re.DOTALL)
                # BillingClient, purchase gibi anahtar kelime içeren kodları patchle (örnek)
                if "BillingClient" in content or "purchase" in content:
                    content = content.replace('return 0', 'return 1')
                with open(path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(content)
