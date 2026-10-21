import os
import hashlib
import zipfile
from datetime import datetime
from pathlib import Path
from app.core.agenda import ARCHIVO, INDICE, verificar_archivos

ARCHIVO_HASH = Path("datos/contactos.sha256")
CARPETA_RESPALDOS = Path("respaldos")

def calcular_hash():
    if not ARCHIVO.exists():
        raise FileNotFoundError("No existe el archivo de contactos.")

    sha256 = hashlib.sha256()

    with open(ARCHIVO, "rb") as archivo:
        while True:
            bloque = archivo.read(4096)

            if not bloque:
                break

            sha256.update(bloque)

    return sha256.hexdigest()

def guardar_hash():
    hash_actual = calcular_hash()
    temporal = ARCHIVO_HASH.with_suffix(".tmp")

    with open(temporal, "w", encoding="utf-8") as archivo:
        archivo.write(hash_actual)

    temporal.replace(ARCHIVO_HASH)
    return hash_actual

def verificar_integridad():
    if not ARCHIVO.exists():
        if ARCHIVO_HASH.exists():
            return False, "Falta el archivo de contactos."
        return True, "No hay contactos registrados."

    if not ARCHIVO_HASH.exists():
        return False, "No existe el archivo de verificación SHA-256."

    with open(ARCHIVO_HASH, "r", encoding="utf-8") as archivo:
        hash_guardado = archivo.read().strip()

    hash_actual = calcular_hash()

    if hash_actual == hash_guardado:
        return True, "La integridad del archivo es correcta."

    return False, "Se detectaron modificaciones en contactos.dat."

def crear_respaldo():
    verificar_archivos()

    if not ARCHIVO.exists() or not INDICE.exists():
        raise FileNotFoundError("Faltan archivos para crear el respaldo.")

    CARPETA_RESPALDOS.mkdir(exist_ok=True)
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_zip = CARPETA_RESPALDOS / f"respaldo_{fecha}.zip"

    with zipfile.ZipFile(ruta_zip, "w", zipfile.ZIP_DEFLATED) as zip_archivo:
        zip_archivo.write(ARCHIVO, arcname=ARCHIVO.name)
        zip_archivo.write(INDICE, arcname=INDICE.name)

    tamanio_original = ARCHIVO.stat().st_size + INDICE.stat().st_size
    tamanio_comprimido = ruta_zip.stat().st_size

    return ruta_zip, tamanio_original, tamanio_comprimido


def obtener_metadatos():
    if not ARCHIVO.exists():
        raise FileNotFoundError("No existe el archivo de contactos.")

    informacion = os.stat(ARCHIVO)

    datos = {
        "nombre": ARCHIVO.name,
        "ruta": str(ARCHIVO.resolve()),
        "tamanio": informacion.st_size,
        "modificacion": datetime.fromtimestamp(informacion.st_mtime).strftime("%d/%m/%Y %H:%M:%S"),
        "lectura": os.access(ARCHIVO, os.R_OK),
        "escritura": os.access(ARCHIVO, os.W_OK)
    }

    return datos
