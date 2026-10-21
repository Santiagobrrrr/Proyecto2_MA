
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agenda de Contactos")
        self.resize(1150, 740)
        self.setMinimumSize(900, 600)

        contenedor = QWidget()
        self.layout_principal = QVBoxLayout(contenedor)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        self.setCentralWidget(contenedor)