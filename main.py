if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    from app.ui.main_window import MainWindow
    
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()