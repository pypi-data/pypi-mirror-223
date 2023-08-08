from PySide6.QtWidgets import QWidget, QBoxLayout, QLineEdit, QPushButton, QHBoxLayout


class CreateFileDialog(QWidget):

    def __init__(self):
        super().__init__()
        self.box_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.file_name_input = QLineEdit()
        self.create_file_button = QPushButton()
        self.create_file_button.setText("Create File")
        self.create_file_button.clicked.connect(self.create_file)
        self.box_h_layout = QHBoxLayout()
        self.box_h_layout.addWidget(self.create_file_button)
        self.box_layout.addWidget(self.file_name_input)
        self.box_layout.addLayout(self.box_h_layout)
        self.setWindowTitle("Create File")
        self.setLayout(self.box_layout)

    def create_file(self):
        file_name = self.file_name_input.text()
        if not file_name.isspace():
            with open(file_name, "w+") as file:
                file.write("")
