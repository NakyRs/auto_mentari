from PyQt6.QtCore import QThread, pyqtSignal

class ExecuteWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, driver, matkul, pertemuan, tipe, key):
        super().__init__()

        self.driver = driver
        self.matkul = matkul
        self.pertemuan = pertemuan
        self.tipe = tipe
        self.key = key

    def run(self):
        try:
            self.driver.execute(self.matkul, self.pertemuan, self.tipe, self.key)
            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))
