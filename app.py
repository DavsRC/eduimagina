import streamlit as st
import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

# Configuración general de la página de Streamlit
# Defino el título y el layout 'wide' para aprovechar mejor el espacio en pantalla.
st.set_page_config(page_title="EduImagina AI", layout="wide")

# Bloque de estilos CSS para limpiar la interfaz y dar estilo a los botones.
st.markdown("""
<style>
    .main {background-color: #f0f2f6;}
    h1 {color: #2c3e50;}
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 0.4rem 1rem;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Función de carga del modelo.
# Utilizo @st.cache_resource para que el modelo se cargue solo una vez en memoria
# y no ralentice la aplicación cada vez que interactúo con un botón.
@st.cache_resource
def load_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    
    # Detección automática de hardware. Priorizo CUDA (Nvidia) si está disponible.
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Uso float16 si estoy en GPU para ahorrar memoria VRAM. En CPU es necesario usar float32.
    dtype = torch.float16 if device == "cuda" else torch.float32

    # Carga del pipeline base desde Hugging Face.
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype)
    
    # CORRECCIÓN IMPORTANTE: Cambio el Scheduler a EulerDiscreteScheduler.
    # El planificador por defecto (PNDM) a veces genera errores de índice en ciertos entornos locales.
    # Euler es más robusto y generalmente más rápido para este tipo de generaciones.
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
    
    pipe = pipe.to(device)

    # Optimizaciones de memoria para evitar que la aplicación se cierre inesperadamente.
    pipe.enable_attention_slicing()
    
    # Esta opción es útil si la GPU tiene poca memoria, procesa la imagen por partes.
    # Si causa lentitud excesiva, se puede comentar.
    pipe.enable_vae_tiling()

    return pipe

# Muestro un spinner visual mientras se ejecuta la carga inicial del modelo.
with st.spinner("Inicializando el motor de IA... (Esto puede tardar unos minutos la primera vez)"):
    pipe = load_model()

# --- Interfaz de Usuario ---

st.title("EduImagina: Ilustrador de Conceptos Educativos")
st.markdown(
    "Herramienta de apoyo docente para generar material visual didáctico mediante Inteligencia Artificial."
)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Panel de Control")

    # Entrada del usuario (Prompt principal)
    topic = st.text_input("Concepto a ilustrar", "La fotosíntesis")

    # Selección de estilo (Prompt Engineering implícito)
    style_option = st.selectbox(
        "Estilo gráfico",
        (
            "Libro de texto (Esquemático)",
            "Cartoon 3D (Estilo Pixar)",
            "Fotorealista (Documental)",
            "Arte Pixel (Retro)",
        ),
    )

    # Mapeo de estilos a instrucciones técnicas para el modelo.
    style_prompts = {
        "Libro de texto (Esquemático)": "educational diagram, white background, textbook style, isometric, clear labels, schematic",
        "Cartoon 3D (Estilo Pixar)": "pixar style, 3d render, cute, vibrant colors, soft lighting, 4k, high composition",
        "Fotorealista (Documental)": "national geographic photography, highly detailed, cinematic lighting, 8k, realistic texture",
        "Arte Pixel (Retro)": "pixel art, 16-bit, retro game style, clean lines",
    }

    # Parámetros avanzados visibles
    num_inference_steps = st.slider(
        "Calidad (Pasos)",
        min_value=15,
        max_value=50,
        value=30,
        help="Más pasos aumentan la definición pero tardan más tiempo.",
    )

    st.info(
        "Nota: Verifique siempre la precisión científica de las imágenes generadas antes de usarlas en clase."
    )

    generate_btn = st.button("Generar Imagen")

with col2:
    st.subheader("Visualización")

    if generate_btn and topic:
        # Construcción del prompt positivo
        final_prompt = f"{topic}, {style_prompts[style_option]}"
        
        # Prompt negativo: Lo que NO queremos ver en la imagen.
        # Es fundamental para evitar deformaciones y mantener el estilo 'family friendly'.
        negative_prompt = (
            "distorted, blurry, text, watermark, violent, nudity, deformed hands, "
            "bad anatomy, extra limbs, ugly, messy"
        )

        with st.spinner(f"Dibujando '{topic}'... Por favor espere."):
            try:
                # Ejecución de la inferencia
                image = pipe(
                    prompt=final_prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=7.5, # Valor estándar para adherencia al texto
                    height=512,
                    width=512,
                ).images[0]

                st.image(image, caption=f"Resultado: {topic} ({style_option})", use_column_width=True)
                st.success("Imagen generada con éxito.")
                
            except Exception as e:
                st.error(f"Ocurrió un error durante la generación: {e}")