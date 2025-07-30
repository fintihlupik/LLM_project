import gradio as gr
import requests
from PIL import Image
import io
import base64
import os

BASE_URL = os.getenv("BACKEND_URL", "http://backend:8000")


API_ENDPOINTS = {
    "Horus - Faster post generation": f"{BASE_URL}/generate/basic",
    "Isis - Advanced reasoning":      f"{BASE_URL}/agent/finance_complete",
    "Thoth - Academic RAG":           f"{BASE_URL}/query/rag",
    "Anubis - Ticker Analysis with Yahoo": f"{BASE_URL}/yahoo/financial-story",
}

# Funcion que envuelve la llamada a la API
def chat_wrapper(message, history, model, audience, platform, region, llm_model_choice):
    payload = {
        "prompt": message,
        "audience": audience,
        "platform": platform,
        "region": region
    }

    # Solo Isis necesita el modelo LLM
    if model == "Isis - Advanced reasoning":
        payload["model"] = llm_model_choice

    # Anubis también puede requerir un nivel de detalle
    if model == "Anubis - Ticker Analysis with Yahoo":
        payload["detail_level"] = "simple"  # Puedes cambiar a "advanced" si lo prefieres

    try:
        response = requests.post(API_ENDPOINTS[model], json=payload)
        response.raise_for_status()
        json_response = response.json()

        # Manejo especial para Anubis
        if model == "Anubis - Ticker Analysis with Yahoo":
            story = json_response.get("story", "No story received.")
            link = json_response.get("yahoo_link", "")
            output = f"{story}\n\n🔗 [Ver en Yahoo]({link})"
        else:
            output = json_response.get("output", json_response.get("response", "No response received."))

    except Exception as e:
        output = f"❌ Error: {str(e)}"

    return [{"role": "assistant", "content": output}], output

# Interfaz Gradio
with gr.Blocks(
    theme=gr.themes.Base(
        primary_hue="blue",
        neutral_hue="slate",
        radius_size="md",
        font="sans"
    ),
    css="""
:root, html, body, .gradio-container {
    background-color: #e6f0fa !important;
    color-scheme: light !important;
    font-family: 'Segoe UI', sans-serif;
    color: #1e40af !important;
}

/* Estructura general */
.gr-block.gr-box {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin: 2rem auto;
    max-width: 900px;
}

/* Título */
#header {
    text-align: center;
    color: #1e40af;
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 2rem;
}

/* Campos de entrada */
input, textarea, select {
    background-color: #ffffff !important;
    color: #1e40af !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 6px !important;
    padding: 10px !important;
    font-size: 1rem;
}

/* Botones */
button:not(.copy-btn):not(.copy-button) {
    background-color: #1e40af !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 6px !important;
    padding: 10px 20px !important;
    border: none !important;
}
button:hover:not(.copy-btn):not(.copy-button) {
    background-color: #4a66bf !important;
}

/* Títulos, labels */
.gr-markdown h2, .gr-markdown h3, label {
    color: #1e40af !important;
    font-weight: bold;
}
.gr-textbox label, .gr-dropdown label {
    color: #1e40af !important;
}

/* Chat principal */
.gr-chatbot {
    background-color: #ffffff !important;
    color: #1e40af !important;
    max-height: 600px !important;
    min-height: 400px !important;
    overflow-y: auto !important;
    font-size: 1.05rem !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    border: 1px solid #ccc !important;
}

/* Mensajes */
.gr-chatbot .message.user {
    background-color: #629bf7 !important;
    color: white !important;
    font-weight: 500;
}
.gr-chatbot .message.assistant {
    background-color: #bdc0c4 !important;
    color: #1e40af !important;
    font-weight: 400;
}

/* Resultado de texto (copia) */
textarea[readonly], .gr-textbox[readonly] {
    background-color: white !important;
    color: #1e40af !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 6px !important;
}

/* Imágenes */
img {
    border-radius: 8px;
    border: 1px solid #ccc;
    max-width: 100%;
    margin-top: 1rem;
    animation: fadein 0.6s ease-in;
}

@keyframes fadein {
    from { opacity: 0; transform: scale(0.97); }
    to { opacity: 1; transform: scale(1); }
}

#segmentation-btn {
    margin-top: 30px;
}

#generate-image-btn {
    margin-top: 30px;
}


"""
) as demo:
    # Logo de FinancIA
    gr.HTML("""
        <div style="display: flex; justify-content: center; padding: 1rem 0;">
        <img src="https://raw.githubusercontent.com/Bootcamp-IA-P4/Datathon-santuario-animal/main/img/Financia-ia-logo.png" alt="FinancIA Logo" style="height: 120px;" />
        </div>
        """)


    # Título
    gr.Markdown("<div id='header'> Financial Content Assistant</div>")
    show_settings = gr.State(value=False)

    with gr.Row():
        model_selector = gr.Dropdown(
            choices=[
                "Horus - Faster post generation",
                "Isis - Advanced reasoning",
                "Thoth - Academic RAG",
                "Anubis - Ticker Analysis with Yahoo"
            ],
            value="Horus - Faster post generation",
            label="Choose your agent",
            scale=7
        )

        toggle_btn = gr.Button("Segmentation", scale=3, elem_id="segmentation-btn")


    with gr.Column(visible=False) as config_panel:
        audience = gr.Dropdown(
            label="Age group",
            choices=["08-11", "12-15", "16-19", "20-25", "26-85"],
            value="20-25"
        )
        platform = gr.Dropdown(
            label="Plataform",
            choices=["instagram", "twitter", "linkedin"],
            value="instagram"
        )
        region = gr.Dropdown(
                label="Region",
                choices=[
                    # English
                    "English (Australia)",
                    "English (Canada)",
                    "English (Ireland)",
                    "English (India)",
                    "English (Kenya)",
                    "English (Nigeria)",
                    "English (New Zealand)",
                    "English (Pakistani)",
                    "English (United Kingdom)",
                    "English (United States)",
                    "English (South Africa)",

                    # Spanish
                    "Spanish (Argentina)",
                    "Spanish (Bolivia)",
                    "Spanish (Chile)",
                    "Spanish (Colombia)",
                    "Spanish (Cuba)",
                    "Spanish (Ecuador)",
                    "Spanish (Spain)",
                    "Spanish (Mexico)",
                    "Spanish (Peru)",
                    "Spanish (Uruguay)",
                    "Spanish (Venezuela)",

                    # French
                    "French (Belgium)",
                    "French (Canada)",
                    "French (Switzerland)",
                    "French (Ivory Coast)",
                    "French (Cameroon)",
                    "French (Algeria)",
                    "French (France)",
                    "French (Morocco)",
                    "French (Senegal)",
                    "French (Tunisia)",

                    # Fallback
                    "Other"
             ],
        value="Spanish (Mexico)"
        )
        
        # Modelo LLM solo para Isis
        llm_model = gr.Dropdown(
            label="LLM model (Isis only)",
            choices=["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "gemma2-9b-it"],
            value="llama-3.1-8b-instant",
            visible=False
        )
        
        llm_info = gr.Markdown(
            """
            Choose the LLM engine for advanced reasoning:

            - **LLaMA 3 8B Instant** → Faster, lightweight  
            - **LLaMA 3 70B Versatile** → Best quality, slower  
            - **Gemma 9B IT** → Balanced and efficient
            """,
            visible=False
        )

            
   # Estado para guardar respuesta
    last_response = gr.State()

    # Chat principal
    chatbot = gr.ChatInterface(
        fn=chat_wrapper,
        chatbot=gr.Chatbot(elem_id="chatbox", type="messages"),
        type="messages",
        textbox=gr.Textbox(placeholder="What content do you need today?", scale=9),
        additional_inputs=[model_selector, audience, platform, region, llm_model],
        additional_outputs=[last_response],
        title="",
    )

    # Caja de texto para copiar (al final del chat)
    output_text = gr.Textbox(
        label="If you liked it, click to copy the answer.",
        visible=False,
        interactive=False,
        lines=6,
        show_copy_button=True
    )
    # --- Generador de imágenes con Stability AI ---
    gr.Markdown("### Image generator")

    with gr.Row():
        image_prompt = gr.Textbox(
            label="Describe the image you want to generate",
            placeholder="Example: A financial robot on the stock market",
            lines=1,
            scale=7
        )
        generate_image_btn = gr.Button("Generate image", scale=3, elem_id="generate-image-btn")


    def generate_image_ui(prompt):
        print(f"[DEBUG] Prompt received: {prompt}")
        try:
            response = requests.post(f"{BASE_URL}/images/generate", json={"prompt": prompt})
            response.raise_for_status()


            # Convertir bytes directamente a imagen PIL
            image = Image.open(io.BytesIO(response.content))
            print("[DEBUG] Image generated and converted successfully")
            return image

        except Exception as e:
            print(f"[ERROR] Error generating image: {e}")
            return None

    # Conectar el botón de generación de imagen con la función
    image_output = gr.Image(label="Generated image", type="pil")
    generate_image_btn.click(fn=generate_image_ui, inputs=image_prompt, outputs=image_output)


    # Siempre que cambie last_response, se actualiza la caja
    def show_response(text):
        return gr.update(value=text, visible=True)

    last_response.change(fn=show_response, inputs=last_response, outputs=output_text)

    def toggle_settings(current):
        return not current, gr.update(visible=not current)

    toggle_btn.click(toggle_settings, show_settings, [show_settings, config_panel])
    
    def toggle_llm_model_visibility(selected_model):
        is_isis = selected_model == "Isis - Advanced reasoning"
        return gr.update(visible=is_isis), gr.update(visible=is_isis)

    model_selector.change(
        fn=toggle_llm_model_visibility,
        inputs=model_selector,
        outputs=[llm_model, llm_info]
    )
  



if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)