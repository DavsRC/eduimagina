import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import gradio as gr

# Carga y configuración del modelo de Stable Diffusion.
# Esta parte es equivalente a la función load_model() que utilizo en la versión con Streamlit.
model_id = "runwayml/stable-diffusion-v1-5"

# Detección automática del dispositivo disponible (GPU si existe, de lo contrario CPU).
device = "cuda" if torch.cuda.is_available() else "cpu"

# Uso float16 en GPU para optimizar memoria, y float32 en CPU para evitar errores.
dtype = torch.float16 if device == "cuda" else torch.float32

# Carga del pipeline base desde Hugging Face.
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype)

# Cambio explícito del scheduler a EulerDiscreteScheduler, tal como hago en la app de Streamlit.
# Este planificador suele ser más robusto y rápido que el PNDM por defecto.
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)

# Envío del pipeline al dispositivo seleccionado.
pipe = pipe.to(device)

# Optimizaciones de memoria para reducir el riesgo de cierres inesperados.
pipe.enable_attention_slicing()
pipe.enable_vae_tiling()

# Defino los estilos disponibles, manteniendo la misma lógica que en la app de Streamlit.
style_prompts = {
    "Libro de texto (Esquemático)": "educational diagram, white background, textbook style, isometric, clear labels, schematic",
    "Cartoon 3D (Estilo Pixar)": "pixar style, 3d render, cute, vibrant colors, soft lighting, 4k, high composition",
    "Fotorealista (Documental)": "national geographic photography, highly detailed, cinematic lighting, 8k, realistic texture",
    "Arte Pixel (Retro)": "pixel art, 16-bit, retro game style, clean lines",
}

# Función principal que usará Gradio para generar la imagen.
# Recibe el concepto, el estilo y el número de pasos de inferencia.
def generate_image(topic, style_option, num_inference_steps):
    # Valido que el tema no venga vacío.
    if not topic or topic.strip() == "":
        return None

    # Construyo el prompt positivo combinando el concepto y el estilo seleccionado.
    final_prompt = f"{topic}, {style_prompts[style_option]}"

    # Prompt negativo para controlar qué tipo de contenido no quiero que aparezca.
    negative_prompt = (
        "distorted, blurry, text, watermark, violent, nudity, deformed hands, "
        "bad anatomy, extra limbs, ugly, messy"
    )

    # Ejecuto la inferencia con el pipeline configurado.
    image = pipe(
        prompt=final_prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=int(num_inference_steps),
        guidance_scale=7.5,  # Mantengo el mismo valor estándar que en la app de Streamlit.
        height=512,
        width=512,
    ).images[0]

    return image

# Defino la interfaz de Gradio, replicando los controles de la app de Streamlit.
demo = gr.Interface(
    fn=generate_image,
    inputs=[
        gr.Textbox(
            label="Concepto a ilustrar",
            value="La fotosíntesis",
            lines=1,
        ),
        gr.Dropdown(
            label="Estilo gráfico",
            choices=list(style_prompts.keys()),
            value="Libro de texto (Esquemático)",
        ),
        gr.Slider(
            label="Calidad (Pasos de inferencia)",
            minimum=15,
            maximum=50,
            value=30,
            step=5,
        ),
    ],
    outputs=gr.Image(label="Resultado"),
    title="EduImagina: Ilustrador de Conceptos Educativos",
    description=(
        "Herramienta de apoyo docente para generar material visual didáctico a partir de texto. "
        "Permite elegir el estilo gráfico y ajustar la calidad de la generación."
    ),
)

if __name__ == "__main__":
    # En local, esta línea lanza la app de Gradio.
    # En Hugging Face Spaces, la plataforma se encarga de llamar a demo.launch().
    demo.launch()
