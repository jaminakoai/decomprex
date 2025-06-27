import os

def analyze_sqlite_and_prefs(decompile_dir):
    """SQLite veri tabanları ve SharedPreferences dosyalarını listeler."""
    dbs, prefs = [], []
    for root, _, files in os.walk(decompile_dir):
        for file in files:
            if file.endswith('.db'):
                dbs.append(os.path.join(root, file))
            if file.endswith('.xml') and "shared_prefs" in root:
                prefs.append(os.path.join(root, file))
    return dbs, prefs
