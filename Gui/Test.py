from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
import sys

class PageA(QWidget):
    show_page_b_signal = Signal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.input_line_edit = QLineEdit(self)
        layout.addWidget(self.input_line_edit)

        button_a = QPushButton("Show Page B", self)
        button_a.clicked.connect(self.show_page_b)
        layout.addWidget(button_a)

    def show_page_b(self):
        input_text = self.input_line_edit.text()
        self.show_page_b_signal.emit(input_text)

class PageB(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.display_label = QLabel(self)
        layout.addWidget(self.display_label)

        button_b = QPushButton("Back to Page A", self)
        button_b.clicked.connect(self.show_page_a)
        layout.addWidget(button_b)

    def show_page_a(self):
        # Perform actions specific to Page B, if needed
        self.display_label.setText("Received from Page A: {}".format(self.sender_data))
        self.show()

    def set_sender_data(self, data):
        self.sender_data = data

class PageManager(QObject):
    def __init__(self):
        super().__init__()

        self.page_a = PageA()
        self.page_b = PageB()

        self.page_a.show_page_b_signal.connect(self.show_page_b)

    def show_page_b(self, data):
        self.page_b.set_sender_data(data)
        self.page_b.show()

def main():
    app = QApplication(sys.argv)

    manager = PageManager()
    manager.page_a.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
