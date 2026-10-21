from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout

class Header(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("encabezado")
        self.setFixedHeight(110)

        principal = QHBoxLayout(self)
        principal.setContentsMargins(35, 20, 35, 20)

        informacion = QVBoxLayout()
        informacion.setSpacing(5)

        titulo = QLabel("Agenda de Contactos")
        titulo.setObjectName("titulo")

        descripcion = QLabel("Gestiona tus contactos de manera sencilla.")
        descripcion.setObjectName("descripcion")

        informacion.addWidget(titulo)
        informacion.addWidget(descripcion)

        estado = QLabel("●  Sistema local")
        estado.setObjectName("estado")

        principal.addLayout(informacion)
        principal.addStretch()
        principal.addWidget(estado)