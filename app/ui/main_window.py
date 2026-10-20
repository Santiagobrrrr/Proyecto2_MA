from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agenda de Contactos")
        self.resize(1100, 700)
        self.setMinimumSize(850, 550)

        titulo = QLabel("Agenda de Contactos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(titulo)