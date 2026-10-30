from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QStackedWidget
)
from app.ui.pages.contactos_page import ContactosPage
from app.ui.components.header import Header
from app.ui.components.sidebar import Sidebar
from app.ui.components.page import Page
from app.ui.pages.exportar_page import ExportarPage
from app.ui.pages.ayuda_page import AyudaPage
from app.ui.pages.herramientas_page import HerramientasPage
from app.ui.styles import ESTILOS
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox
from app.services.herramientas import verificar_integridad

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

        self.pagina_exportar = ExportarPage()
        self.paginas.addWidget(self.pagina_exportar)

        self.pagina_herramientas = HerramientasPage()
        self.paginas.addWidget(self.pagina_herramientas)

        self.pagina_ayuda = AyudaPage()
        self.paginas.addWidget(self.pagina_ayuda)

        layout_contenido.addWidget(self.paginas, 1)
        layout_general.addWidget(contenido, 1)

        self.setCentralWidget(contenedor)

        self.sidebar.pagina_seleccionada.connect(
            self.paginas.setCurrentIndex
        )
        
        self.sidebar.pagina_seleccionada.connect(self.actualizar_pagina)
        
        QTimer.singleShot(0, self.verificar_integridad_inicial)

    def actualizar_pagina(self, indice):
        if indice == 1:
            self.pagina_exportar.actualizar_contador()   
    
    def verificar_integridad_inicial(self):
        try:
            estado, mensaje = verificar_integridad()

            if estado:
                self.actualizar_estado_sistema(
                    "● Integridad correcta",
                    "#0F9D92"
                )
            else:
                self.actualizar_estado_sistema(
                    "● Integridad comprometida",
                    "#DC2626"
                )

                QMessageBox.warning(
                    self,
                    "Advertencia de integridad",
                    "Se detectó un problema de integridad en "
                    "el archivo de contactos.\n\n"
                    f"{mensaje}\n\n"
                    "Las operaciones de registro y modificación "
                    "están protegidas para evitar nuevas escrituras.\n\n"
                    "Revisa el archivo o restaura un respaldo válido."
                )

        except (OSError, ValueError) as error:
            self.actualizar_estado_sistema(
                "● Error de verificación",
                "#DC2626"
            )

            QMessageBox.critical(
                self,
                "Error al verificar integridad",
                str(error)
            )

    def actualizar_estado_sistema(self, texto, color):
        self.encabezado.estado.setText(texto)
        self.encabezado.estado.setStyleSheet(
            f"color: {color}; font-weight: 600;"
        )