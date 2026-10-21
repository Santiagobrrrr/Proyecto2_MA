
from app.services.herramientas import obtener_metadatos

print("INFORMACION DEL ARCHIVO")

datos = obtener_metadatos()

for campo, valor in datos.items():
    print(f"{campo}: {valor}")

if datos["tamanio"] == 504:
    print("CORRECTO: El tamaño coincide con los tres registros.")
else:
    print("REVISAR: El tamaño del archivo es diferente.")
