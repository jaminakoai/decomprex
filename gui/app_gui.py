import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DecompreX - APK/APKS Analyzer")
        self.setGeometry(100, 100, 700, 400)
        layout = QVBoxLayout()
        self.label = QLabel("APK/APKS dosyanızı seçin ve işlemi başlatın.")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        btn_select = QPushButton("Dosya Seç")
        btn_select.clicked.connect(self.select_file)
        btn_run = QPushButton("Analiz Et")
        btn_run.clicked.connect(self.analyze)
        layout.addWidget(self.label)
        layout.addWidget(btn_select)
        layout.addWidget(btn_run)
        layout.addWidget(self.output)
        self.setLayout(layout)
        self.apk_path = None

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "APK/APKS Seç", "", "APK Files (*.apk *.apks)")
        if file:
            self.apk_path = file
            self.label.setText(f"Seçilen dosya: {file}")

    def analyze(self):
        if not self.apk_path:
            self.output.append("Önce bir dosya seçin.")
            return
        # Burada CLI fonksiyonlarını çağırabilir veya subprocess ile terminalde çalıştırabilirsin
        self.output.append(f"Analiz başlatıldı: {self.apk_path}")
        # ... (detayları ekleyebilirsin)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
