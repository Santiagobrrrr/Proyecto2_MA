from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QHeaderView, QPushButton, QFrame
)

class ContactosPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(20)

        encabezado = QHBoxLayout()

        informacion = QVBoxLayout()
        informacion.setSpacing(5)

        titulo = QLabel("Contactos")
        titulo.setObjectName("pagina_titulo")

        descripcion = QLabel("Consulta y administra tus contactos.")
        descripcion.setObjectName("pagina_descripcion")

        informacion.addWidget(titulo)
        informacion.addWidget(descripcion)

        self.boton_agregar = QPushButton("+ Nuevo contacto")
        self.boton_agregar.setObjectName("boton_primario")
        self.boton_agregar.setEnabled(False)
        self.boton_agregar.setToolTip(
            "Disponible cuando implementemos el formulario de registro."
        )

        encabezado.addLayout(informacion)
        encabezado.addStretch()
        encabezado.addWidget(self.boton_agregar)

        layout.addLayout(encabezado)

        panel = QFrame()
        panel.setObjectName("panel_contactos")

        contenido = QVBoxLayout(panel)
        contenido.setContentsMargins(24, 24, 24, 24)
        contenido.setSpacing(16)

        titulo_tabla = QLabel("Directorio")
        titulo_tabla.setObjectName("panel_titulo")

        self.contador = QLabel("0 contactos")
        self.contador.setObjectName("pagina_descripcion")

        fila_superior = QHBoxLayout()
        fila_superior.addWidget(titulo_tabla)
        fila_superior.addStretch()
        fila_superior.addWidget(self.contador)

        contenido.addLayout(fila_superior)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Teléfono", "Correo", "Ciudad"]
        )

        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.tabla.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setShowGrid(False)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.verticalHeader().setDefaultSectionSize(48)

        cabecera = self.tabla.horizontalHeader()
        cabecera.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        cabecera.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )

        contenido.addWidget(self.tabla)
        layout.addWidget(panel, 1)