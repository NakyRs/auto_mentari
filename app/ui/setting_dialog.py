from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QDialog, QCheckBox, QComboBox, QPushButton
from PyQt6.QtCore import Qt


class Setting(QDialog):
    def __init__(self, parent= None, settings= None):
        super().__init__(parent)

        self.setWindowTitle("Setting")
        self.setFixedSize(400, 250)

        self.settings= settings

        main_layout = QVBoxLayout()

        form = QFormLayout()

        self.input_api_key = QLineEdit()
        self.input_api_key.setText(self.settings.get('key',''))
        form.addRow("Api-Key:", self.input_api_key)

        # self.combo_theme = QComboBox()
        # self.combo_theme.addItems(["Light", "Dark"])
        # form.addRow("Theme:", self.combo_theme)

        label_rand= QLabel('Random Test')
        form.addRow(label_rand)
        self.check_rand_pre = QCheckBox("Pre-Test")
        self.check_rand_post = QCheckBox("Post-Test")
        self.check_rand_pre.setChecked(self.settings.get('Pretest', False))
        self.check_rand_post.setChecked(self.settings.get('Posttest', False))
        form.addRow(self.check_rand_pre)
        form.addRow(self.check_rand_post)

        self.kuisioner_option= QComboBox()
        self.kuisioner_option.addItems(['Ya', 'Random'])
        self.kuisioner_option.setCurrentText("Random" if self.settings.get('Kuesioner', False)else "Ya")
        form.addRow("Kuesioner Option",self.kuisioner_option)

        main_layout.addLayout(form)

        # tombol
        btn_layout = QHBoxLayout()

        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Cancel")

        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)

        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        
    def get_settings(self):
        return {
            "key": self.input_api_key.text(),
            "Pretest": self.check_rand_pre.isChecked(),
            "Posttest": self.check_rand_post.isChecked(),
            "Kuesioner": self.kuisioner_option.currentText()=='Random',
        }