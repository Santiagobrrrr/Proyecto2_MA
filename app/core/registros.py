
# Tamaño de cada campo en bytes
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
    datos = texto.encode("utf-8")

    if not texto or len(datos) > tamanio:
        raise ValueError(
            f"Campo vacío o demasiado largo (máximo {tamanio} bytes)."
        )

    return datos.ljust(tamanio, b" ")


def empaquetar_contacto(contacto):
    registro = b""

    for campo, tamanio in CAMPOS.items():
        registro += preparar_campo(contacto[campo], tamanio)

    return registro + b"\n"


def desempaquetar_contacto(registro):
    if len(registro) != TAMANIO_REGISTRO or registro[-1:] != b"\n":
        raise ValueError("El registro tiene un tamaño incorrecto.")

    contacto = {}
    inicio = 0

    for campo, tamanio in CAMPOS.items():
        datos = registro[inicio:inicio + tamanio]
        contacto[campo] = datos.decode("utf-8").strip()
        inicio += tamanio

    contacto["id"] = int(contacto["id"])
    return contacto
