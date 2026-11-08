# Agenda de Contactos con Acceso Aleatorio

**Laboratorio No. 2 · Manejo e Implementación de Archivos**  
**Universidad Rafael Landívar · Ingeniería en Informática y Sistemas**  
**Lenguaje:** Python · **Interfaz:** PySide6

## Descripción

**Agenda de Contactos** es una aplicación de escritorio que permite guardar, buscar y modificar contactos de forma sencilla. Cada contacto tiene un ID, nombre, teléfono, correo y ciudad.

El proyecto se realizó para poner en práctica el manejo de archivos con **registros de tamaño fijo**. También utiliza un **índice en JSON** para localizar contactos directamente en el archivo, sin tener que revisarlo completo cada vez que se hace una búsqueda.

## ¿Qué permite hacer?

- **Contactos:** agregar nuevos contactos, buscarlos por ID y modificar su información.
- **Exportar:** generar un archivo JSON con los contactos y crear un reporte PDF a partir de esos datos.
- **Herramientas:** comprobar la integridad del archivo con SHA-256, crear respaldos ZIP y consultar su tamaño, fecha de modificación y permisos.
- **Ayuda:** consultar una guía básica para utilizar la aplicación.

## ¿Cómo se guardan los contactos?

La información se almacena en `datos/contactos.dat`. Todos los registros ocupan **168 bytes**, distribuidos de esta manera:

| Campo | Tamaño |
| --- | ---: |
| ID | 7 bytes |
| Nombre | 48 bytes |
| Teléfono | 16 bytes |
| Correo | 64 bytes |
| Ciudad | 32 bytes |
| Salto de línea | 1 byte |
| **Total** | **168 bytes** |

Los campos se guardan en UTF-8 y se completan con espacios hasta alcanzar el tamaño establecido.

El archivo `datos/indice.json` relaciona cada **ID** con su **número de registro**. Con ese dato, el programa calcula la posición correspondiente y utiliza `seek()` para ir directamente al contacto; `tell()` permite conocer la posición actual dentro del archivo. Al modificar un contacto, se sobrescribe únicamente su registro.

Después de guardar cambios, se actualiza el hash SHA-256. Al iniciar la aplicación, este valor se comprueba para detectar posibles modificaciones externas del archivo.

## Organización del proyecto

```text
Proyecto2_MA/
├── app/
│   ├── core/              # Registros, índice y acceso aleatorio
│   ├── services/          # Exportaciones, integridad y respaldos
│   └── ui/                # Ventanas y componentes de la interfaz
├── datos/                 # Archivo de contactos, índice y hash
├── exportaciones/         # JSON y reporte PDF generados
├── respaldos/             # Copias comprimidas en ZIP
├── docs/capturas/         # Evidencias para la documentación
├── tests/                 # Scripts de prueba
├── main.py                # Inicio de la aplicación
└── requirements.txt       # Dependencias
```

## Requisitos y ejecución

Se necesita **Python 3** y las dependencias incluidas en `requirements.txt` (`PySide6` y `fpdf2`). Los siguientes comandos están pensados para **PowerShell en Windows**.

1. Clonar el repositorio y entrar a la carpeta del proyecto:

   ```powershell
   git clone https://github.com/Santiagobrrrr/Proyecto2_MA.git
   cd Proyecto2_MA
   ```

2. Crear el entorno virtual:

   ```powershell
   python -m venv .venv
   ```

3. Instalar las dependencias:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. Iniciar la aplicación:

   ```powershell
   .\.venv\Scripts\python.exe main.py
   ```

> **Nota:** ejecuta los comandos desde la carpeta principal del proyecto. Si la agenda está vacía, puedes empezar agregando un contacto desde la interfaz.

## Archivos generados y pruebas

La aplicación crea los archivos `contactos.dat`, `indice.json` y `contactos.sha256` dentro de `datos/`. Desde la sección **Exportar** se generan `contactos.json` y `reporte_contactos.pdf`; desde **Herramientas** se pueden crear los respaldos ZIP.

Estos archivos se mantienen **localmente** y no se suben automáticamente a GitHub, ya que están excluidos mediante `.gitignore`. Para la entrega del laboratorio se preparan por separado junto con el manual técnico y las capturas.

La carpeta `tests/` incluye pruebas de las operaciones principales. **Antes de ejecutar scripts de prueba, se recomienda respaldar los datos**, porque algunos trabajan sobre los archivos de la agenda.

---

Proyecto desarrollado como parte del **Laboratorio No. 2 de Manejo e Implementación de Archivos**. El avance del trabajo puede consultarse en el [historial de commits](https://github.com/Santiagobrrrr/Proyecto2_MA/commits/main).