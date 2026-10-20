
from app.core.agenda import (
    agregar_contacto,
    buscar_contacto,
    modificar_contacto
)

contacto = {
    "id": 101,
    "nombre": "José Alejandro López",
    "telefono": "45678912",
    "correo": "jose.lopez@correo.com",
    "ciudad": "Quetzaltenango"
}

pruebas = [
    ("ID duplicado", lambda: agregar_contacto(contacto)),
    ("ID negativo", lambda: buscar_contacto(-5)),
    ("ID inexistente", lambda: modificar_contacto(
        999, {"ciudad": "Guatemala"}
    )),
    ("Modificar ID", lambda: modificar_contacto(
        101, {"id": 205}
    )),
    ("Campo vacío", lambda: modificar_contacto(
        101, {"nombre": ""}
    )),
    ("Campo demasiado largo", lambda: modificar_contacto(
        101, {"ciudad": "A" * 50}
    ))
]

for nombre, prueba in pruebas:
    try:
        prueba()
        print(nombre, "- ERROR: no fue rechazado")
    except ValueError as error:
        print(nombre, "- CORRECTO:", error)
