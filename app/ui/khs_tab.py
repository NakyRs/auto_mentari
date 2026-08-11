from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel,
    QComboBox,QTextEdit, QTabWidget,
)
from PyQt6.QtCore import Qt
from .utils import CheckableComboBox
from .worker import ExecuteWorker
from app.definitions import readFileJson, writeFileJson

class KHSTab(QWidget):
    def __init__(self, settings, driver, main_window):
        super().__init__()

        self.settings= settings
        self.driver= driver
        self.main_window= main_window

        layout= QVBoxLayout()
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label_title= QLabel('KHS')
        self.btn_start = QPushButton("Start")
        self.btn_login = QPushButton("Login")
        self.answer_option= QComboBox()
        self.answer_option.addItems(["1","2","3","4","random"])
        self.combo_matkul = CheckableComboBox()
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(label_title)
        layout.addWidget(self.btn_login)

        layout.addWidget(QLabel("Matkul"))
        layout.addWidget(self.combo_matkul)

        layout.addWidget(QLabel("Jawaban ke-"))
        layout.addWidget(self.answer_option)

        layout.addWidget(self.btn_start)
        layout.addWidget(self.log)

        self.btn_login.clicked.connect(self.login)
        self.btn_start.clicked.connect(self.start_process)

        self.setLayout(layout)

        self.load_matkul()

    def login(self):
        self.driver.login()
        self.log_print("Login selesai")

    def log_print(self, text):
        self.log.append(text)

    def load_matkul(self):
        try:
            matkul = self.main_window.matkul
            self.matkul_data = matkul

            self.combo_matkul.clear()
            self.combo_matkul.addItems(matkul.keys())
            
        except:
            self.log_print("File tidak ditemukan, membuat file...")
            self.driver.updateDataMatkul()
            self.load_matkul()

    def start_process(self):
        if self.main_window.is_process_running:
            return

        nama_matkul = self.combo_matkul.checked_items()
        pilihan = self.answer_option.currentText()

        if pilihan == "random":
            pilihan = "random"
        else:
            pilihan = int(pilihan)

        if not nama_matkul:
            self.log_print("Isi matkul terlebih dahulu")
            return
        if not self.main_window.settings.get("semester", ""):
            self.log_print("Isi semester di setting terlebih dahulu")
            return
        self.log_print(f"================================")
        self.log_print(f"Matkul: {nama_matkul}")
        self.log_print("Memulai Proses...")
        self.main_window.set_process_running(True)
        try:
            self.worker = ExecuteWorker(driver=self.driver, matkul= nama_matkul, pilihan= pilihan)

            self.worker.finished.connect(self.finish_process)
            self.worker.error.connect(self.error_process)

            self.worker.start()

            self.log_print("Proses dimulai...")
        except Exception as e:
            self.log_print("Proses Gagal")
            self.log_print(f"Error: {e}")
            self.main_window.set_process_running(False)

    def finish_process(self, errors):
        self.log_print("Proses selesai")
        self.bring_main_window_to_front()
        self.main_window.set_process_running(False)
        if errors:
            self.log_print("Gagal:")
            for item in errors:
                self.log_print(
                    f"-{item['matkul']}"
                )
        else:
            self.log_print("Semua matkul berhasil.")

    def error_process(self, text):
        self.log_print("Proses Gagal")
        self.log_print(f"Error: {text}")
        self.bring_main_window_to_front()
        self.main_window.set_process_running(False)

    def bring_main_window_to_front(self):
        self.main_window.showNormal()
        self.main_window.raise_()
        self.main_window.activateWindow()
