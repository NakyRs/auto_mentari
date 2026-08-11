import sys

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QListWidget,
    QListWidgetItem,
)

class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.list_widget = QListWidget()

        self.setModel(self.list_widget.model())
        self.setView(self.list_widget)

        # Tangkap event mouse sebelum diproses QComboBox
        self.view().viewport().installEventFilter(self)

        # Jangan gunakan selection
        self.view().setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )

        self.setPlaceholderText("Pilih matkul...")

    def add_item(self, text):
        item = QListWidgetItem(text)

        item.setFlags(
            item.flags()
            | Qt.ItemFlag.ItemIsUserCheckable
        )

        item.setCheckState(Qt.CheckState.Unchecked)

        self.list_widget.addItem(item)
        
    def addItems(self, items):
        for text in items:
            self.add_item(text)

    def eventFilter(self, obj, event):
        if (
            obj == self.view().viewport()
            and event.type() == QEvent.Type.MouseButtonRelease
        ):
            item = self.view().itemAt(
                event.position().toPoint()
            )

            if item:
                # Toggle checkbox
                if item.checkState() == Qt.CheckState.Checked:
                    item.setCheckState(Qt.CheckState.Unchecked)
                else:
                    item.setCheckState(Qt.CheckState.Checked)

                self.update_text()

                # PENTING:
                # event tidak diteruskan ke QComboBox
                # sehingga popup tetap terbuka
                return True

        return super().eventFilter(obj, event)

    def update_text(self):
        checked = self.checked_items()

        if checked:
            self.setCurrentText(", ".join(checked))
        else:
            self.setCurrentText("Pilih matkul...")

    def checked_items(self):
        result = []

        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)

            if item.checkState() == Qt.CheckState.Checked:
                result.append(item.text())

        return result

if __name__ == "__main__":
    app = QApplication(sys.argv)

    combo = CheckableComboBox()

    combo.add_item("Apple")
    combo.add_item("Banana")
    combo.add_item("Orange")
    combo.add_item("Mango")

    combo.setMinimumWidth(250)

    combo.show()

    sys.exit(app.exec())