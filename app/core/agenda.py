
import json
import os
from pathlib import Path
from app.core.registros import TAMANIO_REGISTRO, empaquetar_contacto, desempaquetar_contacto

CARPETA = Path("datos")
ARCHIVO = CARPETA / "contactos.dat"
INDICE = CARPETA / "indice.json"

def validar_id(identificador):
    if isinstance(identificador, bool):
        raise ValueError("El ID debe ser un número entero.")

    try:
        numero = int(identificador)
    except (ValueError, TypeError, OverflowError):
        raise ValueError("El ID debe ser un número entero.")

    if str(identificador).strip() != str(numero):
        raise ValueError("El ID debe ser un número entero.")

    if numero < 1 or numero > 9999999:
        raise ValueError("El ID debe tener entre 1 y 7 dígitos.")

    return numero

def cargar_indice():
    CARPETA.mkdir(exist_ok=True)

    if not INDICE.exists():
        if ARCHIVO.exists() and ARCHIVO.stat().st_size > 0:
            raise ValueError("Falta el índice de contactos.")
        return {}

    try:
        with open(INDICE, "r", encoding="utf-8") as archivo:
            indice = json.load(archivo)
    except (json.JSONDecodeError, UnicodeError):
        raise ValueError("El índice JSON está corrupto.")

    if not isinstance(indice, dict):
        raise ValueError("El índice debe contener un objeto JSON.")

    for clave, numero in indice.items():
        try:
            validar_id(clave)
        except ValueError:
            raise ValueError("El índice contiene un ID inválido.")

        if type(numero) is not int or numero < 0:
            raise ValueError("El índice contiene posiciones inválidas.")

    return indice

def guardar_indice(indice):
    CARPETA.mkdir(exist_ok=True)
    temporal = INDICE.with_suffix(".tmp")

    with open(temporal, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, indent=4, ensure_ascii=False)

    os.replace(temporal, INDICE)

def verificar_archivos():
    indice = cargar_indice()

    if not ARCHIVO.exists():
        if indice:
            raise ValueError("Falta el archivo de contactos.")
        return indice

    tamanio = ARCHIVO.stat().st_size

    if tamanio % TAMANIO_REGISTRO != 0:
        raise ValueError("El archivo contiene registros incompletos.")

    cantidad = tamanio // TAMANIO_REGISTRO

    if len(indice) != cantidad:
        raise ValueError("La cantidad de registros no coincide con el índice.")

    if set(indice.values()) != set(range(cantidad)):
        raise ValueError("El índice contiene posiciones incorrectas.")

    with open(ARCHIVO, "rb") as archivo:
        for clave, numero in indice.items():
            archivo.seek(numero * TAMANIO_REGISTRO)
            registro = archivo.read(TAMANIO_REGISTRO)
            contacto = desempaquetar_contacto(registro)

            if contacto["id"] != int(clave):
                raise ValueError("El índice no coincide con los contactos.")

    return indice

def agregar_contacto(contacto):
    identificador = validar_id(contacto["id"])
    contacto = {**contacto, "id": identificador}
    registro = empaquetar_contacto(contacto)
    indice = verificar_archivos()

    if str(identificador) in indice:
        raise ValueError("Ya existe un contacto con ese ID.")

    CARPETA.mkdir(exist_ok=True)

    with open(ARCHIVO, "ab") as archivo:
        posicion = archivo.tell()
        archivo.write(registro)
        archivo.flush()
        os.fsync(archivo.fileno())

    indice[str(identificador)] = posicion // TAMANIO_REGISTRO

    try:
        guardar_indice(indice)
    except OSError:
        try:
            with open(ARCHIVO, "r+b") as archivo:
                archivo.truncate(posicion)
        except OSError:
            raise RuntimeError("No se pudo actualizar el índice ni revertir el archivo.")
        raise

    return posicion

def buscar_contacto(identificador):
    identificador = validar_id(identificador)
    indice = cargar_indice()
    clave = str(identificador)

    if clave not in indice:
        return None

    if not ARCHIVO.exists():
        raise ValueError("No existe el archivo de contactos.")

    tamanio = ARCHIVO.stat().st_size

    if tamanio % TAMANIO_REGISTRO != 0:
        raise ValueError("El archivo contiene registros incompletos.")

    posicion = indice[clave] * TAMANIO_REGISTRO

    if posicion + TAMANIO_REGISTRO > tamanio:
        raise ValueError("La posición del índice está fuera del archivo.")

    with open(ARCHIVO, "rb") as archivo:
        archivo.seek(posicion)
        posicion_actual = archivo.tell()
        registro = archivo.read(TAMANIO_REGISTRO)

    contacto = desempaquetar_contacto(registro)

    if contacto["id"] != identificador:
        raise ValueError("El índice no coincide con el contacto.")

    return contacto, posicion_actual

def modificar_contacto(identificador, nuevos_datos):
    identificador = validar_id(identificador)
    permitidos = {"nombre", "telefono", "correo", "ciudad"}

    if not nuevos_datos or not set(nuevos_datos).issubset(permitidos):
        raise ValueError("Los campos que desea modificar no son válidos.")

    resultado = buscar_contacto(identificador)

    if resultado is None:
        raise ValueError("El contacto no existe.")

    contacto, posicion = resultado
    contacto.update(nuevos_datos)
    registro = empaquetar_contacto(contacto)

    with open(ARCHIVO, "r+b") as archivo:
        archivo.seek(posicion)
        archivo.write(registro)

    return posicion