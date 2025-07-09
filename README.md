# Proyecto de API con FastAPI paraConsulta y Procesamiento de CFDIs

Este proyecto está diseñado para consumir servicios web del SAT (Servicio De Administración Tributaria), descargar masivamente CFDIs, procesarlos y cargarlos en una base de datos.

## Índice

- [Instalación](#instalación)
- [Cómo Empezar](#cómo-empezar)
- [Características Principales](#características-principales)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Referencia de la API](#referencia-de-la-api)

---

## Instalación

Para comenzar con el proyecto, sigue estos pasos:

1. **Crea un entorno virtual (recomendado):**

   ```bash
   python -m venv venv
   ```

2. **Activa el entorno virtual:**
   
   - En Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - En Windows:
     ```cmd
     .\venv\Scripts\activate
     ```

3. **Instala las dependencias:**

   El proyecto utiliza un archivo de dependencias llamado `requeriments` (sin extensión). Instala las dependencias ejecutando:

   ```bash
   pip install -r requeriments
   ```

4. **Clona el repositorio o descarga los archivos necesarios:**
   
   Asegúrate de tener todos los archivos del proyecto en tu máquina.

---

## Cómo Empezar

1. **Configura tus credenciales y parámetros:**

   - Copia tus credenciales del SAT en un archivo `.env` o configúralas como variables de entorno.
   
2. **Inicia la aplicación:**
   
   Ejecuta el siguiente comando para iniciar la aplicación:

   ```bash
   uvicorn main:app --reload
   ```

   Esto iniciará el servidor de FastAPI en tu máquina local.

---

## Características Principales

- **Consumo de Servicios Web SAT:** La API puede consultar y descargar CFDIs desde los servicios web del SAT.
- **Descarga Masiva:** Implementación para descargar múltiples CFDIs de manera eficiente.
- **Procesamiento de Datos:** Capacidad para procesar y analizar CFDIs en busca de información relevante.
- **Carga a Base de Datos:** Integración con una base de datos para almacenar los CFDIs y su información procesada.

---

# Estructura del Proyecto

Tu proyecto está diseñado para manejar servicios relacionados con el CFDI (Comprobante Fiscal Digital por Internet) y la integración con el SAT. La siguiente es una descripción detallada de cada directorio y su contenido:

## Detalles de Cada Directorio

### `app/`

El directorio principal del proyecto. Incluye los siguientes subdirectorios:

- **api**
  - Contiene los servicios web (API) expuestos por el proyecto.
  - Subdirectorios:
    - `v1`: Versión 1 de la API, que incluye las clases y funcionalidades específicas.

- **core**
  - Módulo central del proyecto, contiene configuración, conexiones y clases base.
  - Subdirectorios:
    - `config.py`: Configuración del proyecto.
    - `DBConnect.py`: Clase para manejar la conexión con la base de datos.
    
- **models**
  - Contiene clases que representan los objetos de negocio (modelos) del proyecto.
  - Subdirectorios:
    - `CFDIDocument.py`: Modelo para el procesamiento y almacenamiento de documentos CFDI.
    - `SATBlackList.py`: Modelo para manejar la lista negra del SAT.

- **services**
  - Contiene servicios específicos que implementan la lógica de negocio.
  - Subdirectorios:
    - `Authentication.py`: Servicio de autenticación y manejo de tokens.
    - `CheckRequestDownload.py`: Servicio para verificar solicitudes de descarga.
    - `Fiel.py`: Servicio relacionado con el FIel (Formulario Electrónico del Impuesto al Valor Agregado).
    - `MassiveDownload.py`: Servicio para descargar datos.
    - `ReadCFDI.py`: Servicio para leer y procesar documentos CFDI.
    - `RequestDownload.py`: Servicio para manejar solicitudes de descarga.
    - `Signer.py`: Servicio para firmar documentos electrónicos.
    - `Utils.py`: Utils genericas para el proyecto.
    - `ValidationCFDI.py`: Servicio para validación de documentos CFDI.
    - `WebServiceRequest.py`: Clase base para hacer solicitudes a los servicios web.

- **tmplts_xml**
  - Contiene plantillas XML necesarias para la generación y firma de documentos CFDI.
  - Subdirectorios:
    - `autenticacion.xml`: Plantilla para autenticar en el SAT.
    - `descargamasiva.xml`: Plantilla para descargar de datos.
    - `signer.xml`: Plantilla para firmar documentos.
    - `solicitadescarga.xml`: Plantilla para solicitudes de descarga.
    - `verificasolicituddescarga.xml`: Plantilla para verificar solicitudes de descarga.

- **main.py**
  - Archivo principal que inicia el proyecto y define los puntos de entrada.

---

### **packages_cfdi**

Directorio dedicado a contener paquetes y dependencias específicos del proyecto, como módulos externos o recursos reutilizables.

---

## Diagrama de Estructura

```
app/
├── api/
│   └── v1/
│       ├── __init__.py
│       └── webservices.py
├── core/
│   ├── config.py
│   └── DBConnect.py
├── models/
│   ├── CFDIDocument.py
│   └── SATBlackList.py
├── services/
│   ├── Authentication.py
│   ├── CheckRequestDownload.py
│   ├── Fiel.py
│   ├── MassiveDownload.py
│   ├── ReadCFDI.py
│   ├── RequestDownload.py
│   ├── Signer.py
│   ├── Utils.py
│   ├── ValidationCFDI.py
│   └── WebServiceRequest.py
├── tmplts_xml/
│   ├── autenticacion.xml
│   ├── descargamasiva.xml
│   ├── signer.xml
│   ├── solicitadescarga.xml
│   └── verificasolicituddescarga.xml
└── main.py
```

## Configuración

### Variables de Entorno

Configurar las siguientes variables de entorno antes de ejecutar el servicio:

- `VAULT_ADDR`: Dirección del servidor Vault (ejemplo: `https://127.0.0.1:8200`).
- `VAULT_CACERT`: Ruta al archivo `.pem` que contiene el certificado CA de Vault.
- `VAULT_TOKEN`: Token de autenticación para acceder a Vault.

Puedes definir estas variables en un archivo `.env`, pero no compartas valores reales en entornos públicos.

### Base de Datos

Configura tu motor de bases de datos y asegúrate de que esté disponible. El proyecto actualmente soporta PostgreSQL, pero puede ser adaptado a otros sistemas.

---

## Referencia de la API

A continuación, se encuentran los endpoints disponibles en la API:

| **Endpoint**                  | **Método HTTP** | **Acción**                     |
|-------------------------------|-----------------|----------------------------------|
| `/v1/webservices/savecerts`  | POST            | Guardar certificados de CFDI.   |
| `/v1/webservices/authenticate` | POST           | Autenticación con el SAT.       |
| `/v1/webservices/downloadrequest` | POST         | Realizar una solicitud de descarga masiva de CFDIs. |
| `/v1/webservices/verifydownloadrequest` | POST     | Verificar el estado de una solicitud de descarga. |
| `/v1/webservices/downloadpackage` | POST          | Descargar un paquete de CFDIs.  |
| `/v1/webservices/statuscfdi`   | POST           | Consultar el estatus de un CFDI. |

### Detalles de los endpoints

#### 1. **/v1/webservices/savecerts**
- **Método:** POST
- **Acción:** Guardar certificados de CFDI.
- **Descripción:** Permite guardar los certificados necesarios para autenticarse en los servicios del SAT.

---

#### 2. **/v1/webservices/authenticate**
- **Método:** POST
- **Acción:** Autenticación con el SAT.
- **Descripción:** Realiza la autenticación necesaria para acceder a los servicios del SAT y descargar CFDIs.

---

#### 3. **/v1/webservices/downloadrequest**
- **Método:** POST
- **Acción:** Realizar una solicitud de descarga masiva de CFDIs.
- **Descripción:** Envía una petición para descargar múltiples CFDIs desde el SAT.

---

#### 4. **/v1/webservices/verifydownloadrequest**
- **Método:** POST
- **Acción:** Verificar el estado de una solicitud de descarga.
- **Descripción:** Consulta el estado actual de una solicitud de descarga previamente realizada.

---

#### 5. **/v1/webservices/downloadpackage**
- **Método:** POST
- **Acción:** Descargar un paquete de CFDIs.
- **Descripción:** Permite descargar un grupo específico de CFDIs solicitados anteriormente.

---

#### 6. **/v1/webservices/statuscfdi**
- **Método:** POST
- **Acción:** Consultar el estatus de un CFDI.
- **Descripción:** Verifica el estado de un CFDI específico en el SAT.

---
