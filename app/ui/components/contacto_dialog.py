from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox
)
from app.core.agenda import agregar_contacto, modificar_contacto

class ContactoDialog(QDialog):
    def __init__(self, parent=None, contacto=None):
        super().__init__(parent)

        self.contacto = contacto
        self.editando = contacto is not None

        titulo = "Editar contacto" if self.editando else "Nuevo contacto"

        self.setWindowTitle(titulo)
        self.setMinimumWidth(460)
        self.setModal(True)
        self.setObjectName("contacto_dialog")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(20)

        etiqueta_titulo = QLabel(titulo)
        etiqueta_titulo.setObjectName("dialog_titulo")

        descripcion = QLabel(
            "Actualiza la información del contacto."
            if self.editando
            else "Completa la información para registrar un contacto."
        )
        descripcion.setObjectName("dialog_descripcion")
        descripcion.setWordWrap(True)

        layout.addWidget(etiqueta_titulo)
        layout.addWidget(descripcion)

        formulario = QFormLayout()
        formulario.setSpacing(14)

        self.campo_id = QLineEdit()
        self.campo_id.setPlaceholderText("Ej. 405")
        self.campo_id.setMaxLength(7)

        self.campo_nombre = QLineEdit()
        self.campo_nombre.setPlaceholderText("Nombre completo")
        self.campo_nombre.setMaxLength(48)

        self.campo_telefono = QLineEdit()
        self.campo_telefono.setPlaceholderText("Número de teléfono")
        self.campo_telefono.setMaxLength(16)

        self.campo_correo = QLineEdit()
        self.campo_correo.setPlaceholderText("correo@ejemplo.com")
        self.campo_correo.setMaxLength(64)

        self.campo_ciudad = QLineEdit()
        self.campo_ciudad.setPlaceholderText("Ciudad")
        self.campo_ciudad.setMaxLength(32)

        formulario.addRow("ID:", self.campo_id)
        formulario.addRow("Nombre:", self.campo_nombre)
        formulario.addRow("Teléfono:", self.campo_telefono)
        formulario.addRow("Correo:", self.campo_correo)
        formulario.addRow("Ciudad:", self.campo_ciudad)

        layout.addLayout(formulario)

        if self.editando:
            self.cargar_datos()

        botones = QHBoxLayout()
        botones.addStretch()

        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setObjectName("boton_secundario")
        boton_cancelar.clicked.connect(self.reject)

        boton_guardar = QPushButton(
            "Guardar cambios" if self.editando else "Guardar contacto"
        )
        boton_guardar.setObjectName("boton_primario")
        boton_guardar.clicked.connect(self.guardar_contacto)

        botones.addWidget(boton_cancelar)
        botones.addWidget(boton_guardar)

        layout.addLayout(botones)

    def cargar_datos(self):
        self.campo_id.setText(str(self.contacto["id"]))
        self.campo_nombre.setText(self.contacto["nombre"])
        self.campo_telefono.setText(self.contacto["telefono"])
        self.campo_correo.setText(self.contacto["correo"])
        self.campo_ciudad.setText(self.contacto["ciudad"])

        self.campo_id.setReadOnly(True)
        self.campo_id.setToolTip(
            "El ID no puede modificarse porque identifica el registro."
        )

    def obtener_datos(self):
        return {
            "id": self.campo_id.text().strip(),
            "nombre": self.campo_nombre.text().strip(),
            "telefono": self.campo_telefono.text().strip(),
            "correo": self.campo_correo.text().strip(),
            "ciudad": self.campo_ciudad.text().strip()
        }

    def guardar_contacto(self):
        datos = self.obtener_datos()

        try:
            if self.editando:
                nuevos_datos = {
                    "nombre": datos["nombre"],
                    "telefono": datos["telefono"],
                    "correo": datos["correo"],
                    "ciudad": datos["ciudad"]
                }

                modificar_contacto(
                    self.contacto["id"],
                    nuevos_datos
                )

                mensaje = "Los cambios se guardaron correctamente."

            else:
                agregar_contacto(datos)
                mensaje = "El contacto se registró correctamente."

            QMessageBox.information(
                self,
                "Operación completada",
                mensaje
            )

            self.accept()

        except (OSError, ValueError, RuntimeError) as error:
            QMessageBox.warning(
                self,
                "No se pudo guardar",
                str(error)
            )