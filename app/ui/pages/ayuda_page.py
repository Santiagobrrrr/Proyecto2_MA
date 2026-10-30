from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFrame, QScrollArea
)


class AyudaPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(20)

        titulo = QLabel("Ayuda")
        titulo.setObjectName("pagina_titulo")

        descripcion = QLabel(
            "Guía de uso e información técnica de la Agenda de Contactos."
        )
        descripcion.setObjectName("pagina_descripcion")
        descripcion.setWordWrap(True)

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("herramientas_scroll")

        contenedor = QWidget()
        contenido = QVBoxLayout(contenedor)
        contenido.setContentsMargins(0, 5, 8, 5)
        contenido.setSpacing(20)

        secciones = [
            (
                "Gestión de contactos",
                "Para registrar un contacto, ingresa a Contactos y "
                "selecciona «+ Nuevo contacto». Completa los campos "
                "solicitados y guarda la información.\n\n"
                "Para buscar un contacto, escribe su ID en el buscador. "
                "También puedes seleccionar una fila y presionar "
                "«Editar contacto» para actualizar sus datos."
            ),
            (
                "Exportaciones",
                "En la sección Exportar puedes generar un archivo JSON "
                "con los contactos registrados y crear un reporte PDF.\n\n"
                "El reporte PDF utiliza los datos del JSON exportado. "
                "Los archivos se guardan en la carpeta exportaciones."
            ),
            (
                "Herramientas del sistema",
                "Verificar integridad: comprueba mediante SHA-256 si "
                "el archivo de contactos fue modificado externamente.\n\n"
                "Crear respaldo ZIP: genera una copia comprimida del "
                "archivo de contactos y su índice JSON.\n\n"
                "Consultar metadatos: muestra tamaño, fecha de "
                "modificación y permisos de lectura y escritura."
            ),
            (
                "Información técnica",
                "Almacenamiento: archivo binario contactos.dat.\n"
                "Longitud de registro: 168 bytes.\n"
                "Índice primario: indice.json.\n"
                "Acceso aleatorio: seek() y tell().\n"
                "Integridad: algoritmo SHA-256.\n"
                "Respaldo: formato ZIP.\n"
                "Exportaciones: JSON y PDF."
            )
        ]

        for nombre, texto in secciones:
            panel = QFrame()
            panel.setObjectName("panel_contactos")

            panel_layout = QVBoxLayout(panel)
            panel_layout.setContentsMargins(28, 25, 28, 25)
            panel_layout.setSpacing(12)

            titulo_panel = QLabel(nombre)
            titulo_panel.setObjectName("panel_titulo")

            descripcion_panel = QLabel(texto)
            descripcion_panel.setObjectName("pagina_descripcion")
            descripcion_panel.setWordWrap(True)

            panel_layout.addWidget(titulo_panel)
            panel_layout.addWidget(descripcion_panel)

            contenido.addWidget(panel)

        contenido.addStretch()

        scroll.setWidget(contenedor)
        layout.addWidget(scroll, 1)