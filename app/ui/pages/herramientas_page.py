from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QScrollArea
)

from app.services.herramientas import (
    verificar_integridad,
    crear_respaldo,
    obtener_metadatos
)


class HerramientasPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(15)

        titulo = QLabel("Herramientas")
        titulo.setObjectName("pagina_titulo")

        descripcion = QLabel(
            "Verifica la integridad, crea respaldos y consulta "
            "información del archivo de contactos."
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

        # Integridad SHA-256
        panel_integridad = QFrame()
        panel_integridad.setObjectName("panel_contactos")

        integridad_layout = QVBoxLayout(panel_integridad)
        integridad_layout.setContentsMargins(28, 25, 28, 25)
        integridad_layout.setSpacing(14)

        titulo_integridad = QLabel("Integridad SHA-256")
        titulo_integridad.setObjectName("panel_titulo")

        descripcion_integridad = QLabel(
            "Comprueba que el archivo contactos.dat no haya sido "
            "modificado fuera de la aplicación."
        )
        descripcion_integridad.setObjectName("pagina_descripcion")
        descripcion_integridad.setWordWrap(True)

        self.estado_integridad = QLabel(
            "Presiona el botón para verificar la integridad."
        )
        self.estado_integridad.setObjectName("pagina_descripcion")
        self.estado_integridad.setWordWrap(True)

        boton_integridad = QPushButton("Verificar integridad")
        boton_integridad.setObjectName("boton_herramienta")
        boton_integridad.setMinimumSize(190, 44)
        boton_integridad.setCursor(Qt.CursorShape.PointingHandCursor)
        boton_integridad.clicked.connect(self.comprobar_hash)

        fila_integridad = QHBoxLayout()
        fila_integridad.addWidget(boton_integridad)
        fila_integridad.addStretch()

        integridad_layout.addWidget(titulo_integridad)
        integridad_layout.addWidget(descripcion_integridad)
        integridad_layout.addWidget(self.estado_integridad)
        integridad_layout.addLayout(fila_integridad)

        contenido.addWidget(panel_integridad)

        # Respaldo ZIP
        panel_respaldo = QFrame()
        panel_respaldo.setObjectName("panel_contactos")

        respaldo_layout = QVBoxLayout(panel_respaldo)
        respaldo_layout.setContentsMargins(28, 25, 28, 25)
        respaldo_layout.setSpacing(14)

        titulo_respaldo = QLabel("Respaldo ZIP")
        titulo_respaldo.setObjectName("panel_titulo")

        descripcion_respaldo = QLabel(
            "Crea un respaldo comprimido del archivo de contactos "
            "y su índice JSON."
        )
        descripcion_respaldo.setObjectName("pagina_descripcion")
        descripcion_respaldo.setWordWrap(True)

        self.estado_respaldo = QLabel(
            "Todavía no se ha creado un respaldo en esta sesión."
        )
        self.estado_respaldo.setObjectName("pagina_descripcion")
        self.estado_respaldo.setWordWrap(True)

        self.detalle_respaldo = QLabel("")
        self.detalle_respaldo.setObjectName("pagina_descripcion")
        self.detalle_respaldo.setWordWrap(True)

        boton_respaldo = QPushButton("Crear respaldo ZIP")
        boton_respaldo.setObjectName("boton_herramienta")
        boton_respaldo.setMinimumSize(190, 44)
        boton_respaldo.setCursor(Qt.CursorShape.PointingHandCursor)
        boton_respaldo.clicked.connect(self.generar_respaldo)

        fila_respaldo = QHBoxLayout()
        fila_respaldo.addWidget(boton_respaldo)
        fila_respaldo.addStretch()

        respaldo_layout.addWidget(titulo_respaldo)
        respaldo_layout.addWidget(descripcion_respaldo)
        respaldo_layout.addWidget(self.estado_respaldo)
        respaldo_layout.addWidget(self.detalle_respaldo)
        respaldo_layout.addLayout(fila_respaldo)

        contenido.addWidget(panel_respaldo)

        # Metadatos
        panel_metadatos = QFrame()
        panel_metadatos.setObjectName("panel_contactos")

        metadatos_layout = QVBoxLayout(panel_metadatos)
        metadatos_layout.setContentsMargins(28, 25, 28, 25)
        metadatos_layout.setSpacing(14)

        titulo_metadatos = QLabel("Metadatos del archivo")
        titulo_metadatos.setObjectName("panel_titulo")

        descripcion_metadatos = QLabel(
            "Consulta las propiedades del archivo de contactos, "
            "incluyendo tamaño, modificación y permisos."
        )
        descripcion_metadatos.setObjectName("pagina_descripcion")
        descripcion_metadatos.setWordWrap(True)

        self.detalle_metadatos = QLabel(
            "Presiona el botón para consultar los metadatos."
        )
        self.detalle_metadatos.setObjectName("pagina_descripcion")
        self.detalle_metadatos.setWordWrap(True)
        self.detalle_metadatos.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        boton_metadatos = QPushButton("Consultar metadatos")
        boton_metadatos.setObjectName("boton_herramienta")
        boton_metadatos.setMinimumSize(190, 44)
        boton_metadatos.setCursor(Qt.CursorShape.PointingHandCursor)
        boton_metadatos.clicked.connect(self.consultar_metadatos)

        fila_metadatos = QHBoxLayout()
        fila_metadatos.addWidget(boton_metadatos)
        fila_metadatos.addStretch()

        metadatos_layout.addWidget(titulo_metadatos)
        metadatos_layout.addWidget(descripcion_metadatos)
        metadatos_layout.addWidget(self.detalle_metadatos)
        metadatos_layout.addLayout(fila_metadatos)

        contenido.addWidget(panel_metadatos)
        contenido.addStretch()

        scroll.setWidget(contenedor)
        layout.addWidget(scroll, 1)

    def comprobar_hash(self):
        try:
            estado, mensaje = verificar_integridad()

            if estado:
                self.estado_integridad.setText(
                    f"✓ Integridad correcta. {mensaje}"
                )
            else:
                self.estado_integridad.setText(
                    f"✕ Advertencia de integridad: {mensaje}"
                )

        except (OSError, ValueError) as error:
            self.estado_integridad.setText(
                f"✕ No se pudo verificar la integridad: {error}"
            )

    def generar_respaldo(self):
        try:
            estado, mensaje = verificar_integridad()

            if not estado:
                self.estado_respaldo.setText(
                    f"✕ No se creó el respaldo: {mensaje}"
                )
                return

            ruta, tamanio_original, tamanio_zip = crear_respaldo()

            diferencia = tamanio_original - tamanio_zip

            porcentaje = (
                (diferencia / tamanio_original) * 100
                if tamanio_original > 0 else 0
            )

            self.estado_respaldo.setText(
                f"✓ Respaldo creado: {ruta}"
            )

            self.detalle_respaldo.setText(
                f"Tamaño original: {tamanio_original:,} bytes\n"
                f"Tamaño comprimido: {tamanio_zip:,} bytes\n"
                f"Diferencia: {diferencia:,} bytes\n"
                f"Reducción: {porcentaje:.2f}%"
            )

        except (OSError, ValueError, RuntimeError) as error:
            self.estado_respaldo.setText(
                f"✕ No se pudo crear el respaldo: {error}"
            )
            self.detalle_respaldo.clear()

    def consultar_metadatos(self):
        try:
            datos = obtener_metadatos()

            modificacion = datos["modificacion"]

            if isinstance(modificacion, (int, float)):
                modificacion = datetime.fromtimestamp(
                    modificacion
                ).strftime("%d/%m/%Y %H:%M:%S")

            self.detalle_metadatos.setText(
                f"Nombre: {datos['nombre']}\n"
                f"Ruta: {datos['ruta']}\n"
                f"Tamaño: {datos['tamanio']:,} bytes\n"
                f"Última modificación: {modificacion}\n"
                f"Permiso de lectura: "
                f"{'Sí' if datos['lectura'] else 'No'}\n"
                f"Permiso de escritura: "
                f"{'Sí' if datos['escritura'] else 'No'}"
            )

        except (OSError, ValueError, KeyError) as error:
            self.detalle_metadatos.setText(
                f"✕ No se pudieron consultar los metadatos: {error}"
            )