
from app.core.agenda import (
    agregar_contacto,
    buscar_contacto,
    modificar_contacto
)

contactos = [
   {
        "id": 205,
        "nombre": "María Fernanda Pérez",
        "telefono": "59874123",
        "correo": "maria.perez@correo.com",
        "ciudad": "Guatemala"
    },
    {
        "id": 310,
        "nombre": "Carlos Méndez",
        "telefono": "47895612",
        "correo": "carlos.mendez@correo.com",
        "ciudad": "Retalhuleu"
    }
]

print("\nAGREGAR CONTACTOS")

for contacto in contactos:
    posicion = agregar_contacto(contacto)
    print(contacto["nombre"], "- Byte:", posicion)

print("\nBUSCAR CONTACTO 205")
print(buscar_contacto(205))

print("\nMODIFICAR CONTACTO 205")
posicion = modificar_contacto(
    205,
    {"ciudad": "Coatepeque"}
)
print("Modificado en byte:", posicion)

print("\nVERIFICAR CONTACTOS")

for identificador in [101, 205, 310]:
    print(buscar_contacto(identificador))
