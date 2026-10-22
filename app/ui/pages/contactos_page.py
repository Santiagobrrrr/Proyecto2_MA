from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QFrame, QMessageBox
)
from app.services.exportacion import obtener_contactos
from app.core.agenda import buscar_contacto

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

        busqueda = QHBoxLayout()
        busqueda.setSpacing(10)

        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setObjectName("campo_busqueda")
        self.campo_busqueda.setPlaceholderText("Buscar contacto por ID...")
        self.campo_busqueda.setClearButtonEnabled(True)
        self.campo_busqueda.setMaxLength(7)

        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.setObjectName("boton_buscar")

        self.boton_mostrar = QPushButton("Mostrar todos")
        self.boton_mostrar.setObjectName("boton_secundario")

        busqueda.addWidget(self.campo_busqueda, 1)
        busqueda.addWidget(self.boton_buscar)
        busqueda.addWidget(self.boton_mostrar)

        contenido.addLayout(busqueda)

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

        self.boton_buscar.clicked.connect(self.buscar_por_id)
        self.boton_mostrar.clicked.connect(self.mostrar_todos)
        self.campo_busqueda.returnPressed.connect(self.buscar_por_id)

        self.cargar_contactos()

    def mostrar_contactos(self, contactos):
        campos = ["id", "nombre", "telefono", "correo", "ciudad"]

        self.tabla.setRowCount(len(contactos))

        for fila, contacto in enumerate(contactos):
            for columna, campo in enumerate(campos):
                elemento = QTableWidgetItem(str(contacto[campo]))

                if columna == 0:
                    elemento.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                self.tabla.setItem(fila, columna, elemento)

    def cargar_contactos(self):
        try:
            contactos = obtener_contactos()
            self.mostrar_contactos(contactos)

            cantidad = len(contactos)
            texto = "contacto" if cantidad == 1 else "contactos"

            if cantidad == 0:
                self.contador.setText("Agenda vacía")
            else:
                self.contador.setText(f"{cantidad} {texto}")

        except (OSError, ValueError) as error:
            self.tabla.setRowCount(0)
            self.contador.setText("No disponible")

            QMessageBox.warning(
                self,
                "Error al cargar contactos",
                f"No se pudieron leer los contactos.\n\n{error}"
            )

    def buscar_por_id(self):
        identificador = self.campo_busqueda.text().strip()

        if not identificador:
            QMessageBox.information(
                self,
                "Buscar contacto",
                "Ingresa el ID del contacto que deseas buscar."
            )
            self.campo_busqueda.setFocus()
            return

        try:
            resultado = buscar_contacto(identificador)

            if resultado is None:
                self.mostrar_contactos([])
                self.contador.setText("Sin resultados")

                QMessageBox.information(
                    self,
                    "Contacto no encontrado",
                    f"No existe un contacto con el ID {identificador}."
                )
                return

            contacto, posicion = resultado
            self.mostrar_contactos([contacto])
            self.contador.setText("1 resultado")

        except (OSError, ValueError) as error:
            QMessageBox.warning(
                self,
                "Error de búsqueda",
                str(error)
            )

    def mostrar_todos(self):
        self.campo_busqueda.clear()
        self.cargar_contactos()