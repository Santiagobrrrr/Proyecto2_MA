from datetime import datetime
from fpdf import FPDF
import json
from pathlib import Path
from app.core.agenda import ARCHIVO, verificar_archivos
from app.core.registros import TAMANIO_REGISTRO, desempaquetar_contacto

CARPETA_EXPORTACION = Path("exportaciones")
ARCHIVO_JSON = CARPETA_EXPORTACION / "contactos.json"

def obtener_contactos():
    verificar_archivos()
    contactos = []

    if not ARCHIVO.exists():
        return contactos

    with open(ARCHIVO, "rb") as archivo:
        while True:
            registro = archivo.read(TAMANIO_REGISTRO)

            if not registro:
                break

            contacto = desempaquetar_contacto(registro)
            contactos.append(contacto)

    return contactos

def exportar_json():
    contactos = obtener_contactos()
    CARPETA_EXPORTACION.mkdir(exist_ok=True)

    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(contactos, archivo, indent=4, ensure_ascii=False)

    return ARCHIVO_JSON


def generar_pdf():
    if not ARCHIVO_JSON.exists():
        raise FileNotFoundError("Primero debe exportar los contactos a JSON.")

    with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
        contactos = json.load(archivo)

    if not isinstance(contactos, list):
        raise ValueError("El archivo JSON no tiene el formato esperado.")

    CARPETA_EXPORTACION.mkdir(exist_ok=True)
    ruta_pdf = CARPETA_EXPORTACION / "reporte_contactos.pdf"

    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(12, 15, 12)
    pdf.add_page()

    pdf.set_fill_color(23, 50, 77)
    pdf.rect(0, 0, 297, 35, "F")

    pdf.set_font("Helvetica", "B", 19)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(14, 10)
    pdf.cell(0, 10, "AGENDA DE CONTACTOS")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(14, 22)
    pdf.cell(0, 7, "Reporte general de contactos")

    pdf.set_text_color(60, 70, 80)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_y(43)

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.cell(135, 8, f"Fecha de generacion: {fecha}")
    pdf.cell(135, 8, f"Total de contactos: {len(contactos)}", align="R")
    pdf.ln(13)

    columnas = [
        ("ID", 20),
        ("Nombre", 65),
        ("Telefono", 32),
        ("Correo electronico", 98),
        ("Ciudad", 58)
    ]

    def escribir_encabezado():
        pdf.set_fill_color(23, 50, 77)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 10)

        for titulo, ancho in columnas:
            pdf.cell(ancho, 10, titulo, border=0, fill=True)

        pdf.ln()
        pdf.set_text_color(40, 50, 60)

    escribir_encabezado()

    for numero, contacto in enumerate(contactos):
        if pdf.get_y() + 10 > pdf.h - 18:
            pdf.add_page()
            escribir_encabezado()

        if numero % 2 == 0:
            pdf.set_fill_color(240, 245, 249)
        else:
            pdf.set_fill_color(255, 255, 255)

        pdf.set_font("Helvetica", "", 9)

        valores = [
            str(contacto["id"]),
            contacto["nombre"],
            contacto["telefono"],
            contacto["correo"],
            contacto["ciudad"]
        ]

        for valor, (_, ancho) in zip(valores, columnas):
            # Helvetica no admite todos los caracteres Unicode.
            texto = str(valor).encode("latin-1", errors="replace").decode("latin-1")
            pdf.cell(ancho, 10, texto[:55], fill=True)

        pdf.ln()

    pdf.output(str(ruta_pdf))
    return ruta_pdf