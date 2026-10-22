from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class Page(QWidget):
    def __init__(self, titulo, descripcion):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(10)

        titulo_pagina = QLabel(titulo)
        titulo_pagina.setObjectName("pagina_titulo")

        descripcion_pagina = QLabel(descripcion)
        descripcion_pagina.setObjectName("pagina_descripcion")
        descripcion_pagina.setWordWrap(True)

        layout.addWidget(titulo_pagina)
        layout.addWidget(descripcion_pagina)
        layout.addStretch()