
import json
from pathlib import Path

from app.core.registros import (
    TAMANIO_REGISTRO,
    empaquetar_contacto,
    desempaquetar_contacto
)

CARPETA = Path("datos")
ARCHIVO = CARPETA / "contactos.dat"
INDICE = CARPETA / "indice.json"


def cargar_indice():
    CARPETA.mkdir(exist_ok=True)

    if not INDICE.exists():
        if ARCHIVO.exists() and ARCHIVO.stat().st_size > 0:
            raise ValueError("Falta el índice de contactos.")
        return {}

    with open(INDICE, "r", encoding="utf-8") as archivo:
        indice = json.load(archivo)

    if not isinstance(indice, dict):
        raise ValueError("El índice tiene un formato incorrecto.")

    return indice


def guardar_indice(indice):
    temporal = INDICE.with_suffix(".tmp")

    with open(temporal, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, indent=4, ensure_ascii=False)

    temporal.replace(INDICE)


def agregar_contacto(contacto):
    identificador = int(contacto["id"])

    if identificador <= 0:
        raise ValueError("El ID debe ser positivo.")

    contacto["id"] = identificador
    indice = cargar_indice()

    if str(identificador) in indice:
        raise ValueError("Ya existe un contacto con ese ID.")

    registro = empaquetar_contacto(contacto)

    if ARCHIVO.exists():
        tamanio = ARCHIVO.stat().st_size
        if tamanio % TAMANIO_REGISTRO != 0:
            raise ValueError("El archivo contiene registros incompletos.")

    with open(ARCHIVO, "ab") as archivo:
        posicion = archivo.tell()
        archivo.write(registro)

    numero_registro = posicion // TAMANIO_REGISTRO
    indice[str(identificador)] = numero_registro
    guardar_indice(indice)

    return posicion


def buscar_contacto(identificador):
    indice = cargar_indice()
    clave = str(int(identificador))

    if clave not in indice:
        return None

    numero_registro = indice[clave]
    posicion = numero_registro * TAMANIO_REGISTRO

    with open(ARCHIVO, "rb") as archivo:
        archivo.seek(posicion)
        posicion_actual = archivo.tell()
        registro = archivo.read(TAMANIO_REGISTRO)

    contacto = desempaquetar_contacto(registro)

    if contacto["id"] != int(identificador):
        raise ValueError("El índice no coincide con el archivo.")

    return contacto, posicion_actual


def modificar_contacto(identificador, nuevos_datos):
    resultado = buscar_contacto(identificador)

    if resultado is None:
        raise ValueError("El contacto no existe.")

    contacto, posicion = resultado
    contacto.update(nuevos_datos)
    contacto["id"] = int(identificador)

    registro = empaquetar_contacto(contacto)

    with open(ARCHIVO, "r+b") as archivo:
        archivo.seek(posicion)
        archivo.write(registro)

    return posicion
