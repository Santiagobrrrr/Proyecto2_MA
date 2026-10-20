
import tempfile
from pathlib import Path
from unittest.mock import patch
from app.core import agenda

with tempfile.TemporaryDirectory() as carpeta:
    ruta = Path(carpeta)
    archivo_datos = ruta / "contactos.dat"
    archivo_indice = ruta / "indice.json"

    with patch.object(agenda, "CARPETA", ruta), \
         patch.object(agenda, "ARCHIVO", archivo_datos), \
         patch.object(agenda, "INDICE", archivo_indice):

        contacto = {
            "id": 501,
            "nombre": "Ana Martínez",
            "telefono": "45671234",
            "correo": "ana@correo.com",
            "ciudad": "Quetzaltenango"
        }

        agenda.agregar_contacto(contacto)
        print("Contacto creado:", agenda.buscar_contacto(501))

        # Simular un índice JSON dañado.
        archivo_indice.write_text("{indice dañado", encoding="utf-8")

        try:
            agenda.verificar_archivos()
            print("ERROR: No se detectó la corrupción.")
        except ValueError as error:
            print("CORRECTO:", error)

        # Comprobar que el índice dañado no fue sobrescrito.
        contenido = archivo_indice.read_text(encoding="utf-8")

        if contenido == "{indice dañado":
            print("CORRECTO: El índice no fue sobrescrito.")
        else:
            print("ERROR: El índice fue modificado.")

print("Prueba finalizada. Los archivos originales siguen intactos.")