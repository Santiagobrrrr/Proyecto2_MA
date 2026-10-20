# Agenda de Contactos con Acceso Aleatorio

## Descripción

Aplicación de escritorio desarrollada en Python para administrar contactos mediante archivos de registros de longitud fija, acceso aleatorio e indexación primaria.

El proyecto corresponde al Laboratorio 2 del curso Manejo e Implementación de Archivos de la Universidad Rafael Landívar.

## Objetivo

Implementar una agenda de contactos que permita almacenar, buscar y modificar información sin necesidad de recorrer todo el archivo, utilizando técnicas de acceso aleatorio.

## Tecnologías

- Python
- PySide6
- fpdf2
- JSON
- SHA-256
- ZIP

## Funcionalidades previstas

- Agregar, buscar y modificar contactos.
- Almacenar registros de tamaño fijo.
- Realizar búsquedas mediante un índice primario.
- Exportar contactos a JSON y PDF.
- Verificar la integridad mediante SHA-256.
- Generar respaldos comprimidos.
- Consultar metadatos y permisos del archivo.

## Estructura

- `app/core/`: manejo de registros e índices.
- `app/services/`: exportación, integridad y respaldos.
- `app/ui/`: interfaz gráfica.
- `datos/`: archivos de almacenamiento.
- `exportaciones/`: reportes generados.
- `respaldos/`: copias de seguridad.
- `docs/`: documentación y evidencias.
- `tests/`: pruebas.

## Instalación y ejecución

Crear un entorno virtual e instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Iniciar la aplicación:

```bash
python main.py
```

## Estado del proyecto

En desarrollo. La primera etapa corresponde a la preparación de la estructura y el entorno de ejecución.