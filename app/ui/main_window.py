from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QStackedWidget
)
from app.ui.pages.contactos_page import ContactosPage
from app.ui.components.header import Header
from app.ui.components.sidebar import Sidebar
from app.ui.components.page import Page
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

        self.paginas = QStackedWidget()

        secciones = [
            ("Contactos", "Consulta y administra tus contactos."),
            ("Exportar", "Genera archivos JSON y reportes PDF."),
            ("Herramientas", "Verifica la integridad y crea respaldos."),
            ("Ayuda", "Información sobre el funcionamiento de la aplicación.")
        ]

        self.paginas.addWidget(ContactosPage())

        for titulo, descripcion in secciones[1:]:
            self.paginas.addWidget(Page(titulo, descripcion))

        layout_contenido.addWidget(self.paginas, 1)
        layout_general.addWidget(contenido, 1)

        self.setCentralWidget(contenedor)

        self.sidebar.pagina_seleccionada.connect(
            self.paginas.setCurrentIndex
        )