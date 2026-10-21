from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from app.ui.components.header import Header
from app.ui.styles import ESTILOS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agenda de Contactos")
        self.resize(1150, 740)
        self.setMinimumSize(900, 600)
        self.setStyleSheet(ESTILOS)

        contenedor = QWidget()
        self.layout_principal = QVBoxLayout(contenedor)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        self.encabezado = Header()
        self.layout_principal.addWidget(self.encabezado)
        self.layout_principal.addStretch()

        self.setCentralWidget(contenedor)