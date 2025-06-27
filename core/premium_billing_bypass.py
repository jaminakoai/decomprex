import os
import re

KEYWORDS = [
    "isPremium", "isVip", "checkPurchase", "isSubscribed", "BillingClient", "purchase", "license", "trial", "hasAccess"
]

def bypass_smali_premium(smali_dir):
    """Premium ve Google Billing fonksiyonlarını bulup bypass eder."""
    for root, _, files in os.walk(smali_dir):
        for file in files:
            if file.endswith('.smali'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                modified = False
                for kw in KEYWORDS:
                    # Yöntem adını bulup, return 1 patch uygula (örnek)
                    content_new = re.sub(
                        rf'(\.method[^\n]*{kw}[^\n]*\n)(.*?)(\.end method)',
                        lambda m: m.group(1) + re.sub(r'return [01]', 'return 1', m.group(2)) + m.group(3),
                        content, flags=re.DOTALL)
                    if content_new != content:
                        content = content_new
                        modified = True
                if modified:
                    with open(path, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(content)
