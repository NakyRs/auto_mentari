from PyQt6.QtWidgets import QWidget,QVBoxLayout,QLabel
from PyQt6.QtCore import Qt

class AboutTab(QWidget):
    def __init__(self):
        super().__init__()

        layout= QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addSpacing(30)

        label_title= QLabel('Auto E-Learning')
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_title.setStyleSheet("font-size: 22px; font-weight: bold;")

        layout.addSpacing(30)

        desc_text=(
            "Aplikasi Dekstop sederhana berbasis python "
            "Untuk otomatisasi E-Learning Unpam"
        )
        label_desc= QLabel(desc_text)
        label_desc.setWordWrap(True)
        label_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_desc.setStyleSheet("font-size: 14px; padding: 0 20px;")

        layout.addSpacing(30)

        # Developer info
        label_author = QLabel("Dikembangkan oleh:")
        label_author.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # GitHub link (blue hardcoded for both themes)
        label_link = QLabel(
            f'<a href="https://github.com/NakyRs" style="color: #0078d7; text-decoration: none; '
            f'font-weight: bold; font-size: 16px;">github.com/NakyRs</a>'
        )
        label_link.setOpenExternalLinks(True)
        label_link.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Copyright
        layout.addSpacing(20)
        label_copy = QLabel(f"\u00a9 2025 NaufalZ")
        label_copy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_copy.setStyleSheet("font-size: 12px; color: #888;")

        layout.addWidget(label_title)
        layout.addWidget(label_desc)
        layout.addWidget(label_author)
        layout.addWidget(label_link)
        layout.addWidget(label_copy)

        layout.addStretch()
        self.setLayout(layout)