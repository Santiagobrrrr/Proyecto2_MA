from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout

class Sidebar(QFrame):
    pagina_seleccionada = Signal(int)

    def __init__(self):
        super().__init__()

        self.setObjectName("sidebar")
        self.setFixedWidth(235)
        self.botones = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 30, 18, 25)
        layout.setSpacing(9)

        titulo = QLabel("MENÚ PRINCIPAL")
        titulo.setObjectName("sidebar_seccion")

        layout.addWidget(titulo)
        layout.addSpacing(18)

        opciones = [
            "Contactos",
            "Exportar",
            "Herramientas",
            "Ayuda"
        ]

        for indice, nombre in enumerate(opciones):
            boton = QPushButton(nombre)
            boton.setObjectName("sidebar_boton")
            boton.setCheckable(True)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)

            boton.clicked.connect(
                lambda marcado=False, i=indice: self.seleccionar_pagina(i)
            )

            layout.addWidget(boton)
            self.botones.append(boton)

        layout.addStretch()

        version = QLabel("Proyecto 2  ·  Versión 1.0")
        version.setObjectName("sidebar_version")

        layout.addWidget(version)

        self.seleccionar_pagina(0)

    def seleccionar_pagina(self, indice):
        for numero, boton in enumerate(self.botones):
            boton.setChecked(numero == indice)

        self.pagina_seleccionada.emit(indice)