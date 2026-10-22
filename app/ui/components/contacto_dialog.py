from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox
)
from app.core.agenda import agregar_contacto

class ContactoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Nuevo contacto")
        self.setMinimumWidth(460)
        self.setModal(True)
        self.setObjectName("contacto_dialog")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(20)

        titulo = QLabel("Nuevo contacto")
        titulo.setObjectName("dialog_titulo")

        descripcion = QLabel("Completa la información para registrar un contacto.")
        descripcion.setObjectName("dialog_descripcion")
        descripcion.setWordWrap(True)

        layout.addWidget(titulo)
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

        botones = QHBoxLayout()
        botones.addStretch()

        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setObjectName("boton_secundario")
        boton_cancelar.clicked.connect(self.reject)

        boton_guardar = QPushButton("Guardar contacto")
        boton_guardar.setObjectName("boton_primario")
        boton_guardar.clicked.connect(self.guardar_contacto)

        botones.addWidget(boton_cancelar)
        botones.addWidget(boton_guardar)

        layout.addLayout(botones)

    def guardar_contacto(self):
        contacto = {
            "id": self.campo_id.text().strip(),
            "nombre": self.campo_nombre.text().strip(),
            "telefono": self.campo_telefono.text().strip(),
            "correo": self.campo_correo.text().strip(),
            "ciudad": self.campo_ciudad.text().strip()
        }

        try:
            agregar_contacto(contacto)

            QMessageBox.information(
                self,
                "Contacto registrado",
                "El contacto se guardó correctamente."
            )

            self.accept()

        except (OSError, ValueError, RuntimeError) as error:
            QMessageBox.warning(
                self,
                "No se pudo guardar",
                str(error)
            )