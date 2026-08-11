from PyQt6.QtCore import QThread, pyqtSignal

class ExecuteWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, driver, matkul: str|list[str], pertemuan:str|None= None, tipe: str|None= None, key: str|None= None, pilihan: int|str|None= None):
        super().__init__()

        self.driver = driver
        self.matkul = matkul
        self.pertemuan = pertemuan
        self.tipe = tipe
        self.key = key
        self.pilihan= pilihan

    def run(self):
        try:
            if not self.pertemuan:
                result= self.driver.execute_khs(self.matkul, self.pilihan)
            else:
                result= self.driver.execute(self.matkul, self.pertemuan, self.tipe, self.key)
            self.finished.emit(result if result else [])

        except Exception as e:
            self.error.emit(str(e))
