import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel,
    QComboBox,QTextEdit, QTabWidget,
)
from PyQt6.QtCore import Qt
from .worker import ExecuteWorker
from .about_tab import AboutTab
from .khs_tab import KHSTab
from .setting_dialog import Setting
from app.definitions import readFileJson, writeFileJson
from app.driver_executor import DriverExecutor

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Auto E-Learning")
        self.setFixedSize(400,600)

        self.settings= self.load_settings()
        self.driver= DriverExecutor(self.settings)
        self.matkul= {}
        self.is_process_running = False
        
        layout = QVBoxLayout()

        self.info = QLabel("Auto E-Learning")

        self.btn_update = QPushButton("Update Data")
        self.btn_login = QPushButton("Login")
        self.btn_start = QPushButton("Start")
        self.btn_setting = QPushButton("Setting")

        self.combo_matkul = QComboBox()
        self.combo_pertemuan = QComboBox()
        self.combo_tipe = QComboBox()

        self.combo_tipe.addItems(["Pretest", "Posttest", "Kuesioner"])

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.info)
        layout.addWidget(self.btn_update)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_setting)

        layout.addWidget(QLabel("Matkul"))
        layout.addWidget(self.combo_matkul)

        layout.addWidget(QLabel("Pertemuan"))
        layout.addWidget(self.combo_pertemuan)

        layout.addWidget(QLabel("Tipe"))
        layout.addWidget(self.combo_tipe)

        layout.addWidget(self.btn_start)
        layout.addWidget(self.log)

        self.load_matkul()

        container_ele = QWidget()
        container_ele.setLayout(layout)

        self.container_about= AboutTab()
        self.container_khs= KHSTab(settings= self.settings, driver= self.driver, main_window=self)

        tabs= QTabWidget()
        tabs.addTab(container_ele,'E-Learning')
        tabs.addTab(self.container_khs, 'KHS')
        tabs.addTab(self.container_about, 'About')
        self.setCentralWidget(tabs)

        # CONNECT EVENT
        self.btn_update.clicked.connect(self.update_data)
        self.btn_login.clicked.connect(self.login)
        self.btn_start.clicked.connect(self.start_process)
        self.btn_setting.clicked.connect(self.setting_window)
        self.combo_matkul.currentTextChanged.connect(self.update_pertemuan)
        # load pertama
        # self.update_pertemuan(self.combo_matkul.currentText())

    def update_pertemuan(self, matkul):
        self.combo_pertemuan.clear()
        self.combo_pertemuan.addItems(self.matkul_data.get(matkul, []))

    def update_data(self):
        try:
            self.driver.updateDataMatkul()

            self.log_print("Data berhasil diupdate")
            self.load_matkul()
            self.container_khs.load_matkul()

        except Exception as e:
            self.log_print("Update data gagal")
            self.log_print(f"Error: {e}")

    def log_print(self, text):
        self.log.append(text)

    def load_matkul(self):
        try:
            self.matkul = readFileJson("matkul.json")
            self.matkul_data = self.matkul

            self.combo_matkul.clear()
            self.combo_matkul.addItems(self.matkul.keys())

            if self.combo_matkul.count() > 0:
                self.update_pertemuan(self.combo_matkul.currentText())
            
        except:
            self.log_print("File tidak ditemukan, membuat file...")
            self.driver.updateDataMatkul()
            self.load_matkul()

    def login(self):
        self.driver.login()
        self.log_print("Login selesai")

    def start_process(self):
        if self.is_process_running:
            return

        nama_matkul = self.combo_matkul.currentText()
        nama_pert = self.combo_pertemuan.currentText()
        tipe = self.combo_tipe.currentText()
        key= self.settings.get('key','')
        random= self.settings.get(tipe, True)

        self.log_print(f"================================")
        self.log_print(f"Matkul: {nama_matkul}")
        self.log_print(f"Pertemuan: {nama_pert}")
        self.log_print(f"Tipe: {tipe}")
        self.log_print(f"Random: {random}\n")

        if not random and key== '':
            self.log_print("Proses Gagal harap masukkan Api-Key untuk menggunakan opsi yang bukan random")
            return
        
        self.log_print("Memulai Proses...")
        self.set_process_running(True)
        try:
            self.worker = ExecuteWorker(self.driver, nama_matkul, nama_pert, tipe, key)
            
            self.worker.finished.connect(self.finish_process)
            self.worker.error.connect(self.error_process)
            self.worker.start()

            self.log_print("Proses dimulai...")
        except Exception as e:
            self.log_print("Proses Gagal")
            self.log_print(f"Error: {e}")
            self.set_process_running(False)

    def setting_window(self):
        dialog= Setting(self, self.settings)
        if dialog.exec():
            new_settings= dialog.get_settings()

            self.settings= new_settings
            self.driver.update_settings(new_settings)
            writeFileJson(self.settings, 'settings.json')

            self.log_print('Setting Updated')
            print('Updated')
        else:    
            print('cancel')

    def load_settings(self):
        try:
            settings = readFileJson('settings.json')
            return settings

        except FileNotFoundError:
            print("File tidak ditemukan, membuat file...")
            settings = {}
            writeFileJson(settings, 'settings.json')
            return settings
        
    def finish_process(self, worker):
        self.log_print("Proses selesai")
        self.bring_main_window_to_front()
        self.set_process_running(False)

    def error_process(self, text):
        self.log_print("Proses Gagal")
        self.log_print(f"Error: {text}")
        self.bring_main_window_to_front()
        self.set_process_running(False)

    def bring_main_window_to_front(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def set_process_running(self, running):
        self.is_process_running = running

        self.btn_update.setDisabled(running)
        self.btn_login.setDisabled(running)
        self.btn_start.setDisabled(running)
        
        self.container_khs.btn_login.setDisabled(running)
        self.container_khs.btn_start.setDisabled(running)

    def closeEvent(self, event):
        self.driver.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


# def start_process(self):

#     nama_matkul = self.combo_matkul.currentText()

#     nama_pert = self.combo_pertemuan.currentText()

#     tipe = self.combo_tipe.currentText()

#     key = self.settings.get("key", "")

#     self.worker = ExecuteWorker(
#         self.driver,
#         nama_matkul,
#         nama_pert,
#         tipe,
#         key
#     )

#     self.worker.finished.connect(self.finish_process)

#     self.worker.error.connect(self.error_process)

#     self.worker.start()

#     self.log_print("Proses dimulai...")

# def finish_process(self):

#     self.log_print("Proses selesai")
#     self.showNormal()
#     self.activateWindow()
#     self.raise_()

# def error_process(self, text):

#     self.log_print(text)

