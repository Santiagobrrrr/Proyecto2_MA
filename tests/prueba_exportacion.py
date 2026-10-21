
import json
from app.services.exportacion import exportar_json

ruta = exportar_json()

with open(ruta, "r", encoding="utf-8") as archivo:
    contactos = json.load(archivo)

print("Archivo generado:", ruta)
print("Total de contactos:", len(contactos))

for contacto in contactos:
    print(contacto["id"], "-", contacto["nombre"])

if len(contactos) == 3:
    print("CORRECTO: Se exportaron los tres contactos.")
else:
    print("REVISAR: La cantidad de contactos es diferente.")
