
from app.services.exportacion import exportar_json, generar_pdf

ruta_json = exportar_json()
print("JSON generado:", ruta_json)

ruta_pdf = generar_pdf()
print("PDF generado:", ruta_pdf)

if ruta_pdf.exists() and ruta_pdf.stat().st_size > 0:
    print("CORRECTO: El reporte PDF se generó correctamente.")
    print("Tamaño:", ruta_pdf.stat().st_size, "bytes")
else:
    print("ERROR: No se pudo generar el PDF.")
