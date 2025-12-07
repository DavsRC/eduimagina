# Manual de instalación y guía de usuario de EduImagina

## 1. Descripción general

EduImagina es una aplicación que genera ilustraciones didácticas a partir de descripciones de texto.
Está pensada como herramienta de apoyo para docentes de primaria y secundaria, utilizando modelos de difusión (Stable Diffusion) para crear imágenes en distintos estilos visuales.

Este manual explica:

- Cómo instalar y ejecutar el proyecto en un entorno local.
- Cómo usar la aplicación paso a paso.
- Consideraciones básicas de uso responsable.

## 2. Requisitos previos

Antes de instalar el proyecto de forma local, se recomienda contar con:

- Sistema operativo: Windows, Linux o macOS.
- Python 3.9 o superior.
- Git instalado (para clonar el repositorio).
- Cuenta en Hugging Face (si se requiere autenticación para el modelo).
- GPU con soporte CUDA (opcional, pero recomendable para acelerar la generación).

Nota: La aplicación también está disponible mediante un despliegue público; la instalación local es necesaria solo si se desea ejecutar todo en la propia máquina.

## 3. Instalación local

### 3.1. Clonar el repositorio

En una terminal, ir a la carpeta donde se desea guardar el proyecto y ejecutar:

```bash
git clone https://github.com/DavsRC/eduimagina.git
cd eduimagina
```

### 3.2. Crear y activar un entorno virtual

Se recomienda aislar las dependencias en un entorno virtual de Python:

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux / macOS
source venv/bin/activate
```

Verificar que el entorno está activo (el prefijo `(venv)` suele aparecer en la consola).

### 3.3. Instalar dependencias

Con el entorno virtual activo, instalar las dependencias definidas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

Este archivo incluye las librerías necesarias para ejecutar el modelo y la aplicación web (por ejemplo `torch`, `diffusers`, `streamlit`, `gradio`, entre otras).

### 3.4. Autenticación en Hugging Face (si aplica)

Si el modelo utilizado requiere autenticación, iniciar sesión en Hugging Face con un token de acceso:

```bash
python
>>> from huggingface_hub import login
>>> login("TU_HF_TOKEN_AQUI")
>>> exit()
```

Otra opción es definir la variable de entorno `HUGGINGFACE_HUB_TOKEN` con el token correspondiente.

## 4. Ejecución de la aplicación

El repositorio puede incluir dos formas principales de ejecutar la aplicación: una versión con Streamlit y otra con Gradio.

### 4.1. Versión Streamlit (desarrollo local)

Con el entorno virtual activo y estando en la carpeta raíz del proyecto:

```bash
streamlit run app.py
```

Streamlit iniciará un servidor local y mostrará una URL similar a:

```text
http://localhost:8501
```

Abrir esa dirección en el navegador para acceder a la interfaz de EduImagina.

### 4.2. Versión Gradio (para despliegue o pruebas)

La version de Gradio con ajustes es (el archivo `app_gradio.py` usado en Hugging Face Spaces, cuando lo subas a Hugging por favor cambia el nombre a `app.py`), también se puede ejecutar localmente con:

```bash
python app.py
```

Gradio mostrará en consola una URL local y, en algunos casos, un enlace público temporal para pruebas.

## 5. Guía de uso de la aplicación

### 5.1. Flujo básico

1. Abrir la aplicación en el navegador (ya sea local o mediante el enlace público del despliegue).
2. En el campo de texto principal, escribir el concepto o tema que se desea ilustrar.  
   Ejemplos:
   - "La fotosíntesis"
   - "El sistema solar"
   - "Estructura de una célula animal"
3. Seleccionar el estilo gráfico deseado (libro de texto esquemático, cartoon 3D, fotorealista, arte pixel, etcétera).
4. Ajustar los parámetros técnicos que la interfaz expone, como:
   - Pasos de inferencia (quality/steps).
   - Guidance scale (si está disponible).
5. Hacer clic en el botón de generación.
6. Esperar a que el modelo genere la imagen.
7. Revisar la ilustración resultante y, si es útil, descargarla o incorporarla en presentaciones o materiales de clase.

### 5.2. Recomendaciones prácticas

- Escribir prompts claros y específicos. Por ejemplo:  
  "Diagrama simple de la fotosíntesis para niños de primaria" suele producir mejores resultados que un prompt muy genérico.
- Probar diferentes estilos para encontrar el que mejor se adapte al nivel educativo y al tipo de explicación.
- Comenzar con un número de pasos de inferencia intermedio (por ejemplo 25 o 30) y ajustarlo según calidad y tiempo de respuesta.

## 6. Uso responsable y consideraciones básicas

- Verificar siempre la precisión científica y conceptual de las imágenes generadas antes de utilizarlas en clase.
- Recordar que las imágenes se generan a partir de un modelo entrenado con grandes cantidades de datos y pueden reflejar sesgos presentes en esos datos.
- Usar las ilustraciones como apoyo visual complementario, no como única fuente de información.
- Informar a estudiantes, cuando sea pertinente, que las imágenes han sido generadas por un sistema de inteligencia artificial.

## 7. Soporte y contacto

En caso de errores o dudas sobre la instalación o el uso:

- Revisar el archivo `README.md` del repositorio para obtener una visión general del proyecto.
- Consultar el notebook de Google Colab incluido en la carpeta `notebooks`, donde se documentan los experimentos y la configuración del modelo.
- Crear un issue en el repositorio de GitHub describiendo el problema, el sistema operativo y los pasos que llevaron al error.
