
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

print("AGREGAR CONTACTO")
posicion = agregar_contacto(contacto)
print("Guardado en byte:", posicion)

print("\nBUSCAR CONTACTO")
resultado = buscar_contacto(101)
print(resultado)

print("\nMODIFICAR CONTACTO")
posicion = modificar_contacto(
    101,
    {"ciudad": "Retalhuleu"}
)
print("Modificado en byte:", posicion)

print("\nVERIFICAR CAMBIO")
print(buscar_contacto(101))
