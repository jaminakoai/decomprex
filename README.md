# DecompreX

**Profesyonel, modüler, izinli APK/APKS analiz ve bypass aracı**

## Özellikler
- Oto decompile (APK/APKS)
- App engine tespiti (Unity/Flutter/ReactNative/Native)
- Premium/satın alma bypass
- Frida engeli kaldırma ve agent injection
- Split APK desteği ve multi yükleme için hazır çıktı
- Terminal ve (isteğe bağlı) GUI desteği

## Kurulum
```bash
sudo apt update
sudo apt install python3 python3-pip apksigner apktool jadx zipalign -y
pip3 install -r requirements.txt
```

## Kullanım
```bash
python3 cli.py --apk /path/to/app.apk
python3 cli.py --apks /path/to/app.apks
```

Çıktıdan sonra çoklu yükleme için:
```bash
adb install-multiple -r ./output/split/base.apk ./output/split/split_config.arm64_v8a.apk ./output/split/split_config.tr.apk
```
