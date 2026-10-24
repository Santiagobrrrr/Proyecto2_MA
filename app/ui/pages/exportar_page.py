import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QMessageBox
)
from app.services.exportacion import obtener_contactos, exportar_json

class ExportarPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(20)

        titulo = QLabel("Exportar")
        titulo.setObjectName("pagina_titulo")

        descripcion = QLabel(
            "Genera archivos para consultar y compartir tus contactos."
        )
        descripcion.setObjectName("pagina_descripcion")

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        panel = QFrame()
        panel.setObjectName("panel_contactos")

        contenido = QVBoxLayout(panel)
        contenido.setContentsMargins(28, 28, 28, 28)
        contenido.setSpacing(16)

        titulo_panel = QLabel("Exportación JSON")
        titulo_panel.setObjectName("panel_titulo")

        informacion = QLabel(
            "Exporta todos los contactos registrados a un archivo JSON "
            "con codificación UTF-8."
        )
        informacion.setObjectName("pagina_descripcion")
        informacion.setWordWrap(True)

        self.contador = QLabel("Contactos disponibles: —")
        self.contador.setObjectName("pagina_descripcion")

        self.boton_exportar = QPushButton("Generar archivo JSON")
        self.boton_exportar.setObjectName("boton_primario")
        self.boton_exportar.setCursor(Qt.CursorShape.PointingHandCursor)

        self.boton_carpeta = QPushButton("Abrir carpeta")
        self.boton_carpeta.setObjectName("boton_secundario")
        self.boton_carpeta.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_carpeta.setEnabled(False)

        botones = QHBoxLayout()
        botones.addWidget(self.boton_exportar)
        botones.addWidget(self.boton_carpeta)
        botones.addStretch()

        contenido.addWidget(titulo_panel)
        contenido.addWidget(informacion)
        contenido.addSpacing(12)
        contenido.addWidget(self.contador)
        contenido.addLayout(botones)

        layout.addWidget(panel)
        layout.addStretch()

        self.boton_exportar.clicked.connect(self.generar_json)
        self.boton_carpeta.clicked.connect(self.abrir_carpeta)

        self.ruta_exportacion = None

    def actualizar_contador(self):
        try:
            contactos = obtener_contactos()
            self.contador.setText(
                f"Contactos disponibles: {len(contactos)}"
            )

        except (OSError, ValueError) as error:
            self.contador.setText("Contactos disponibles: No disponible")

            QMessageBox.warning(
                self,
                "Error al consultar contactos",
                str(error)
            )

    def generar_json(self):
        try:
            ruta = exportar_json()
            self.ruta_exportacion = ruta

            self.boton_carpeta.setEnabled(True)

            QMessageBox.information(
                self,
                "Exportación completada",
                f"El archivo JSON se generó correctamente.\n\n{ruta}"
            )

            self.actualizar_contador()

        except (OSError, ValueError) as error:
            QMessageBox.warning(
                self,
                "Error de exportación",
                str(error)
            )

    def abrir_carpeta(self):
        if self.ruta_exportacion is None:
            return

        carpeta = self.ruta_exportacion.parent.resolve()

        if os.name == "nt":
            os.startfile(str(carpeta))