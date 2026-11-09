<div align="center">

# Agenda de Contactos

**Proyecto No. 2 · Manejo e Implementación de Archivos**  
Universidad Rafael Landívar · Ingeniería en Informática y Sistemas

`Python` · `PySide6` · `JSON` · `SHA-256` · `ZIP`

</div>

---

## Descripción

**Agenda de Contactos** es una aplicación de escritorio que permite guardar, buscar y modificar contactos de manera sencilla. Cada registro incluye un ID, nombre, teléfono, correo electrónico y ciudad.

El proyecto se desarrolló para practicar el manejo de archivos. Utiliza registros de tamaño fijo y un índice en JSON que ayuda a encontrar un contacto por su ID sin recorrer todo el archivo de datos.

## ¿Qué permite hacer?

| Sección | Funciones |
| --- | --- |
| **Contactos** | Agregar contactos, buscarlos por ID y modificar su información. |
| **Exportar** | Guardar los contactos en JSON y generar un reporte PDF. |
| **Herramientas** | Verificar la integridad con SHA-256, crear respaldos ZIP y consultar información del archivo. |
| **Ayuda** | Consultar indicaciones básicas para utilizar la aplicación. |

## ¿Cómo funciona el almacenamiento?

Los contactos se guardan en `datos/contactos.dat`. Cada registro ocupa **168 bytes** y sus campos se completan con espacios hasta alcanzar el tamaño definido.

| Campo | Tamaño |
| --- | ---: |
| ID | 7 bytes |
| Nombre | 48 bytes |
| Teléfono | 16 bytes |
| Correo | 64 bytes |
| Ciudad | 32 bytes |
| Salto de línea | 1 byte |
| **Total por registro** | **168 bytes** |

Para buscar un contacto, el programa consulta `indice.json`, obtiene el número de registro y calcula su ubicación dentro de `contactos.dat`. Con `seek()` llega directamente a esa posición y con `tell()` puede consultar dónde se encuentra el cursor del archivo. Al editar, se sobrescribe solamente el registro seleccionado.

Después de agregar o modificar un contacto, se actualiza su hash SHA-256. Al iniciar la aplicación, el sistema comprueba ese valor y avisa si encuentra una diferencia.

## Organización del proyecto

```text
Proyecto2_MA/
├── app/
│   ├── core/           # Registros, búsquedas e índice
│   ├── services/       # Exportaciones, integridad y respaldos
│   └── ui/             # Interfaz y ventanas
├── datos/              # Contactos, índice y hash
├── exportaciones/      # Archivos JSON y PDF generados
├── respaldos/          # Copias de seguridad ZIP
├── docs/capturas/      # Espacio para evidencias
├── tests/              # Scripts de prueba
├── main.py             # Inicio del programa
└── requirements.txt    # Librerías necesarias
```

## Instalación y ejecución

Se necesita **Python 3**. Estos pasos están pensados para una terminal **PowerShell en Windows**.

1. Descargar el proyecto:

   ```powershell
   git clone https://github.com/Santiagobrrrr/Proyecto2_MA.git
   cd Proyecto2_MA
   ```

2. Crear el entorno virtual e instalar las librerías:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Abrir la aplicación:

   ```powershell
   .\.venv\Scripts\python.exe main.py
   ```

Si es la primera vez que se ejecuta, la agenda estará vacía. Los archivos de datos se irán creando al registrar contactos.

## Archivos generados

La aplicación trabaja con los siguientes archivos:

| Ubicación | Contenido |
| --- | --- |
| `datos/` | `contactos.dat`, `indice.json` y `contactos.sha256`. |
| `exportaciones/` | `contactos.json` y `reporte_contactos.pdf`. |
| `respaldos/` | Copias ZIP del archivo de contactos y su índice. |

Estos archivos se mantienen en la computadora y están excluidos del repositorio mediante `.gitignore`. Para la entrega del laboratorio, se reúnen por separado.

## Documentación

- **[Manual técnico del proyecto](https://github.com/Santiagobrrrr/Proyecto2_MA/blob/main/Informe_T%C3%A9cnico_MA.pdf)** — explica la estructura de los registros, el acceso aleatorio, el índice y las demás funciones.
- **Pruebas:** la carpeta `tests/` contiene scripts para comprobar las operaciones principales. Algunos trabajan con los datos locales, por lo que se recomienda hacer un respaldo antes de ejecutarlos.

---

**Proyecto 2 de Manejo e Implementación de Archivos**. Los avances pueden consultarse en el [historial de commits](https://github.com/Santiagobrrrr/Proyecto2_MA/commits/main).