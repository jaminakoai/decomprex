import zipfile

def detect_sdk_trackers(apk_path):
    """Appsflyer, Firebase, OneSignal gibi popüler takip SDK'larını tespit eder."""
    trackers = []
    known_sdks = {
        "Appsflyer": "com/appsflyer",
        "Firebase": "com/google/firebase",
        "OneSignal": "com/onesignal",
        "Facebook": "com/facebook",
        "Adjust": "com/adjust"
    }
    with zipfile.ZipFile(apk_path, 'r') as zip_ref:
        files = zip_ref.namelist()
        for sdk, pattern in known_sdks.items():
            if any(pattern in f for f in files):
                trackers.append(sdk)
    return trackers
