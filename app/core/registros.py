
CAMPOS = {
    "id": 7,
    "nombre": 48,
    "telefono": 16,
    "correo": 64,
    "ciudad": 32
}

TAMANIO_REGISTRO = sum(CAMPOS.values()) + 1

def preparar_campo(valor, tamanio):
    texto = str(valor).strip()

    if not texto:
        raise ValueError("Los campos no pueden estar vacíos.")

    if "\n" in texto or "\r" in texto or "\x00" in texto:
        raise ValueError("El campo contiene caracteres no permitidos.")

    datos = texto.encode("utf-8")

    if len(datos) > tamanio:
        raise ValueError(f"El campo supera los {tamanio} bytes.")

    return datos.ljust(tamanio, b" ")

def empaquetar_contacto(contacto):
    try:
        identificador = int(contacto["id"])
    except (KeyError, ValueError, TypeError, OverflowError):
        raise ValueError("El ID debe ser un número entero válido.")

    if isinstance(contacto["id"], bool) or str(contacto["id"]).strip() != str(identificador):
        raise ValueError("El ID debe ser un número entero válido.")

    if identificador < 1 or identificador > 9999999:
        raise ValueError("El ID debe tener entre 1 y 7 dígitos.")

    registro = preparar_campo(identificador, CAMPOS["id"])

    for campo in ("nombre", "telefono", "correo", "ciudad"):
        if campo not in contacto or contacto[campo] is None:
            raise ValueError(f"Falta el campo: {campo}")

        registro += preparar_campo(contacto[campo], CAMPOS[campo])

    return registro + b"\n"

def desempaquetar_contacto(registro):
    if len(registro) != TAMANIO_REGISTRO:
        raise ValueError("El registro tiene un tamaño incorrecto.")

    if registro[-1:] != b"\n":
        raise ValueError("El registro no tiene el separador correcto.")

    contacto = {}
    inicio = 0

    try:
        for campo, tamanio in CAMPOS.items():
            datos = registro[inicio:inicio + tamanio]
            contacto[campo] = datos.decode("utf-8").strip()
            inicio += tamanio
    except UnicodeDecodeError:
        raise ValueError("El registro contiene texto UTF-8 inválido.")

    identificador = contacto["id"]

    if not identificador.isascii() or not identificador.isdecimal():
        raise ValueError("El registro contiene un ID inválido.")

    contacto["id"] = int(identificador)

    if contacto["id"] < 1 or contacto["id"] > 9999999:
        raise ValueError("El ID está fuera de rango.")

    for campo in ("nombre", "telefono", "correo", "ciudad"):
        if not contacto[campo]:
            raise ValueError(f"El campo {campo} está vacío.")

    return contacto