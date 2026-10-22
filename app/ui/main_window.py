from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
)
from app.ui.components.header import Header
from app.ui.components.sidebar import Sidebar
from app.ui.styles import ESTILOS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agenda de Contactos")
        self.resize(1150, 740)
        self.setMinimumSize(900, 600)
        self.setStyleSheet(ESTILOS)

        contenedor = QWidget()
        layout_general = QHBoxLayout(contenedor)
        layout_general.setContentsMargins(0, 0, 0, 0)
        layout_general.setSpacing(0)

        self.sidebar = Sidebar()
        layout_general.addWidget(self.sidebar)

        contenido = QWidget()
        layout_contenido = QVBoxLayout(contenido)
        layout_contenido.setContentsMargins(0, 0, 0, 0)
        layout_contenido.setSpacing(0)

        self.encabezado = Header()
        layout_contenido.addWidget(self.encabezado)
        layout_contenido.addStretch()

        layout_general.addWidget(contenido, 1)

        self.setCentralWidget(contenedor)