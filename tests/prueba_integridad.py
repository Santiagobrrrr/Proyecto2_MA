
import tempfile
from pathlib import Path
from unittest.mock import patch
from app.core import agenda
from app.services import herramientas

with tempfile.TemporaryDirectory() as carpeta:
    ruta = Path(carpeta)
    datos = ruta / "contactos.dat"
    indice = ruta / "indice.json"
    archivo_hash = ruta / "contactos.sha256"

    with patch.object(agenda, "CARPETA", ruta), \
         patch.object(agenda, "ARCHIVO", datos), \
         patch.object(agenda, "INDICE", indice), \
         patch.object(herramientas, "ARCHIVO", datos), \
         patch.object(herramientas, "ARCHIVO_HASH", archivo_hash):

        contacto = {
            "id": 501,
            "nombre": "Ana Martínez",
            "telefono": "45671234",
            "correo": "ana@correo.com",
            "ciudad": "Quetzaltenango"
        }

        # Crear archivos iniciales para la prueba.
        datos.touch()
        herramientas.guardar_hash()
        agenda.agregar_contacto(contacto)

        estado, mensaje = herramientas.verificar_integridad()
        print("Integridad inicial:", estado, mensaje)

        # Alterar un byte sin actualizar el hash.
        with open(datos, "r+b") as archivo:
            archivo.seek(10)
            archivo.write(b"X")

        estado, mensaje = herramientas.verificar_integridad()
        print("Integridad despues de alterar:", estado, mensaje)

        try:
            agenda.modificar_contacto(501, {"ciudad": "Guatemala"})
            print("ERROR: Se permitio modificar un archivo alterado.")
        except ValueError as error:
            print("CORRECTO: Modificacion bloqueada:", error)

print("CORRECTO: Los archivos originales no fueron modificados.")
