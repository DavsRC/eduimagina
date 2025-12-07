# EduImagina: Ilustrador de Conceptos Educativos con IA Generativa

EduImagina es una aplicación de apoyo docente que utiliza modelos generativos avanzados (Stable Diffusion) para crear ilustraciones didácticas a partir de descripciones de texto.  
El objetivo principal es facilitar la visualización de conceptos abstractos en contextos educativos (por ejemplo, “el sistema solar”, “ciclo del agua”, “estructura de un átomo”) mediante imágenes claras, coherentes y libres de derechos de autor.

Este proyecto forma parte de una evidencia de aprendizaje sobre generación de contenido con IA generativa, integrando experimentación, análisis ético y una aplicación funcional accesible para usuarios finales.

---

## 1. Objetivos del proyecto

- Permitir que docentes generen material visual educativo de forma rápida y personalizada.
- Explorar el comportamiento de un modelo de difusión (Stable Diffusion v1.5) bajo diferentes configuraciones:
  - Distintos schedulers de muestreo.
  - Diferente número de pasos de inferencia.
  - Variación del parámetro guidance scale.
- Desarrollar una aplicación web sencilla con Streamlit que exponga los parámetros más relevantes al usuario.
- Reflexionar sobre los riesgos y aspectos éticos del uso de IA generativa en educación.

---

## 2. Arquitectura y tecnologías utilizadas

- **Modelo generativo**: Stable Diffusion v1.5 (Hugging Face Diffusers).
- **Framework de inferencia**: `diffusers`, `torch`, `transformers`, `accelerate`.
- **Aplicación web**: Streamlit.
- **Entorno de experimentación**: Google Colab (notebook con experimentos A, B y C).
- **Control de versiones y documentación**: GitHub.

La aplicación permite seleccionar:

- Concepto a ilustrar (entrada de texto).
- Estilo visual (diagrama de libro de texto, cartoon 3D, realista, arte pixel).
- Número de pasos de inferencia.
- Guidance scale (fidelidad al texto).

---

## 3. Estructura del repositorio

Estructura sugerida del proyecto:

```text
.
├── app.py                                   # Aplicación principal de Streamlit
├── requirements.txt                         # Dependencias del proyecto
├── README.md                                # Este archivo
├── notebooks/
│   └── EA3_Generación_de_contenido_con_IA_generativa.ipynb   # Notebook con experimentación
└── assets/
    ├── expA_pndm_heart.png                  # Ejemplo Experimento A (PNDM)
    ├── expA_euler_heart.png                 # Ejemplo Experimento A (Euler)
    ├── expB_robot_15steps.png               # Ejemplo Experimento B (15 pasos)
    ├── expB_robot_50steps.png               # Ejemplo Experimento B (50 pasos)
    ├── expC_watercycle_guidance_5.0.png     # Ejemplo Experimento C (guidance 5.0)
    ├── expC_watercycle_guidance_7.5.png     # Ejemplo Experimento C (guidance 7.5)
    └── expC_watercycle_guidance_10.0.png    # Ejemplo Experimento C (guidance 10.0)
```
