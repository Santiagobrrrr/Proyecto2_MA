from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame
)

from app.services.exportacion import (
    obtener_contactos,
    exportar_json,
    generar_pdf
)


class ExportarPage(QWidget):
    def __init__(self):
        super().__init__()

        self.ruta_json = None
        self.ruta_pdf = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(20)

        titulo = QLabel("Exportaciones")
        titulo.setObjectName("pagina_titulo")

        descripcion = QLabel(
            "Genera archivos JSON y reportes PDF de tus contactos."
        )
        descripcion.setObjectName("pagina_descripcion")

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        self.contador = QLabel("Contactos disponibles: —")
        self.contador.setObjectName("pagina_descripcion")
        layout.addWidget(self.contador)

        # Panel JSON
        panel_json = QFrame()
        panel_json.setObjectName("panel_contactos")

        contenido_json = QVBoxLayout(panel_json)
        contenido_json.setContentsMargins(28, 28, 28, 28)
        contenido_json.setSpacing(15)

        titulo_json = QLabel("Exportación JSON")
        titulo_json.setObjectName("panel_titulo")

        descripcion_json = QLabel(
            "Exporta los contactos registrados a un archivo JSON "
            "con codificación UTF-8."
        )
        descripcion_json.setObjectName("pagina_descripcion")
        descripcion_json.setWordWrap(True)

        self.estado_json = QLabel("Todavía no se ha generado un archivo.")
        self.estado_json.setObjectName("pagina_descripcion")
        self.estado_json.setWordWrap(True)

        self.boton_json = QPushButton("Generar JSON")
        self.boton_json.setObjectName("boton_exportar")
        self.boton_json.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_json.setMinimumSize(160, 44)

        self.boton_ver_json = QPushButton("Ver JSON")
        self.boton_ver_json.setObjectName("boton_ver_archivo")
        self.boton_ver_json.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_ver_json.setMinimumSize(110, 44)
        self.boton_ver_json.setEnabled(False)

        botones_json = QHBoxLayout()
        botones_json.setSpacing(10)
        botones_json.addWidget(self.boton_json)
        botones_json.addWidget(self.boton_ver_json)
        botones_json.addStretch()

        contenido_json.addWidget(titulo_json)
        contenido_json.addWidget(descripcion_json)
        contenido_json.addWidget(self.estado_json)
        contenido_json.addLayout(botones_json)

        layout.addWidget(panel_json)

        # Panel PDF
        panel_pdf = QFrame()
        panel_pdf.setObjectName("panel_contactos")

        contenido_pdf = QVBoxLayout(panel_pdf)
        contenido_pdf.setContentsMargins(28, 28, 28, 28)
        contenido_pdf.setSpacing(15)

        titulo_pdf = QLabel("Reporte PDF")
        titulo_pdf.setObjectName("panel_titulo")

        descripcion_pdf = QLabel(
            "Genera un reporte PDF utilizando los datos "
            "del archivo JSON exportado."
        )
        descripcion_pdf.setObjectName("pagina_descripcion")
        descripcion_pdf.setWordWrap(True)

        self.estado_pdf = QLabel("Todavía no se ha generado un reporte.")
        self.estado_pdf.setObjectName("pagina_descripcion")
        self.estado_pdf.setWordWrap(True)

        self.boton_pdf = QPushButton("Generar PDF")
        self.boton_pdf.setObjectName("boton_exportar")
        self.boton_pdf.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_pdf.setMinimumSize(160, 44)

        self.boton_ver_pdf = QPushButton("Ver PDF")
        self.boton_ver_pdf.setObjectName("boton_ver_archivo")
        self.boton_ver_pdf.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_ver_pdf.setMinimumSize(110, 44)
        self.boton_ver_pdf.setEnabled(False)

        botones_pdf = QHBoxLayout()
        botones_pdf.setSpacing(10)
        botones_pdf.addWidget(self.boton_pdf)
        botones_pdf.addWidget(self.boton_ver_pdf)
        botones_pdf.addStretch()

        contenido_pdf.addWidget(titulo_pdf)
        contenido_pdf.addWidget(descripcion_pdf)
        contenido_pdf.addWidget(self.estado_pdf)
        contenido_pdf.addLayout(botones_pdf)

        layout.addWidget(panel_pdf)
        layout.addStretch()

        # Eventos
        self.boton_json.clicked.connect(self.generar_json)
        self.boton_pdf.clicked.connect(self.generar_reporte)

        self.boton_ver_json.clicked.connect(
            lambda: self.abrir_archivo(self.ruta_json, self.estado_json)
        )

        self.boton_ver_pdf.clicked.connect(
            lambda: self.abrir_archivo(self.ruta_pdf, self.estado_pdf)
        )

        self.actualizar_archivos()

    def actualizar_contador(self):
        try:
            contactos = obtener_contactos()
            self.contador.setText(
                f"Contactos disponibles: {len(contactos)}"
            )

        except (OSError, ValueError) as error:
            self.contador.setText("Contactos disponibles: No disponible")
            self.estado_json.setText(f"Error al consultar contactos: {error}")

    def actualizar_archivos(self):
        carpeta = Path("exportaciones")

        ruta_json = carpeta / "contactos.json"

        if ruta_json.is_file():
            self.ruta_json = ruta_json
            self.boton_ver_json.setEnabled(True)
            self.estado_json.setText(
                f"Archivo disponible: {ruta_json}"
            )
        else:
            self.ruta_json = None
            self.boton_ver_json.setEnabled(False)

        # Detectamos el PDF generado por el servicio.
        # Si el servicio usa otro nombre, ajustamos esta ruta.
        ruta_pdf = carpeta / "contactos.pdf"

        if ruta_pdf.is_file():
            self.ruta_pdf = ruta_pdf
            self.boton_ver_pdf.setEnabled(True)
            self.estado_pdf.setText(
                f"Reporte disponible: {ruta_pdf}"
            )
        else:
            self.ruta_pdf = None
            self.boton_ver_pdf.setEnabled(False)

    def generar_json(self):
        try:
            ruta = Path(exportar_json())

            self.ruta_json = ruta
            self.boton_ver_json.setEnabled(True)

            self.estado_json.setText(
                f"✓ Archivo generado correctamente: {ruta}"
            )

            self.actualizar_contador()

        except (OSError, ValueError, RuntimeError) as error:
            self.estado_json.setText(
                f"✕ No se pudo generar el archivo: {error}"
            )

    def generar_reporte(self):
        try:
            ruta_json = Path(exportar_json())
            ruta_pdf = Path(generar_pdf())

            self.ruta_json = ruta_json
            self.ruta_pdf = ruta_pdf

            self.boton_ver_json.setEnabled(True)
            self.boton_ver_pdf.setEnabled(True)

            self.estado_json.setText(
                f"✓ JSON actualizado: {ruta_json}"
            )

            self.estado_pdf.setText(
                f"✓ Reporte generado correctamente: {ruta_pdf}"
            )

            self.actualizar_contador()

        except (OSError, ValueError, RuntimeError) as error:
            self.estado_pdf.setText(
                f"✕ No se pudo generar el reporte: {error}"
            )

    def abrir_archivo(self, ruta, etiqueta_estado):
        if ruta is None:
            etiqueta_estado.setText("No hay un archivo disponible.")
            return

        archivo = Path(ruta).resolve()

        if not archivo.is_file():
            etiqueta_estado.setText(
                "No se encontró el archivo solicitado."
            )
            return

        if not QDesktopServices.openUrl(
            QUrl.fromLocalFile(str(archivo))
        ):
            etiqueta_estado.setText(
                "No se pudo abrir el archivo."
            )