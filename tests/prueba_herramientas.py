
from app.core.agenda import verificar_archivos
from app.services.herramientas import (
    guardar_hash,
    verificar_integridad,
    crear_respaldo
)

print("VERIFICAR ARCHIVOS")
print(verificar_archivos())

print("\nGENERAR HASH INICIAL")
print(guardar_hash())

print("\nCOMPROBAR INTEGRIDAD")
estado, mensaje = verificar_integridad()
print("CORRECTO:" if estado else "ERROR:", mensaje)

print("\nCREAR RESPALDO ZIP")
ruta, original, comprimido = crear_respaldo()

print("Archivo:", ruta)
print("Tamaño original:", original, "bytes")
print("Tamaño ZIP:", comprimido, "bytes")

if ruta.exists() and ruta.stat().st_size > 0:
    print("CORRECTO: Respaldo generado.")
