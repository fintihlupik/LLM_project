import gradio as gr
import requests

API_ENDPOINTS = {
    "Horus": "http://127.0.0.1:8000/generate",
    "Isis": "http://127.0.0.1:8000/agent/finance"
}

# Se guarda el último mensaje generado
def chat_wrapper(message, history, model, audience, platform, region):
    payload = {
        "prompt": message,
        "audience": audience,
        "platform": platform,
        "region": region
    }
    try:
        response = requests.post(API_ENDPOINTS[model], json=payload)
        response.raise_for_status()
        output = response.json().get("output", "No response received.")
    except Exception as e:
        output = f"❌ Error: {str(e)}"

    # Devolvemos el mensaje para el chat y lo guardamos como estado
    return [{"role": "assistant", "content": output}], output

with gr.Blocks(css="""
#header {
    text-align: center;
    color: #1e40af;
    font-size: 2rem;
    font-weight: bold;
    margin: 1rem;
}
#chatbox .message.user {
    background-color: #e0f2fe;
    color: #1e40af;
}
#chatbox .message.bot {
    background-color: #F2F2F2;
    color: #1e40af;
}

""") as demo:

    # Título
    gr.Markdown("<div id='header'>🤖 FinancIA — Financial Content Assistant</div>")

    # Selector de modelo
    model_selector = gr.Dropdown(
        choices=["Horus", "Isis"],
        value="Horus",
        label="Modelo"
    )

    # Ajustes toggle
    show_settings = gr.State(value=False)
    toggle_btn = gr.Button("⚙️ Segmentation")

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

   # Estado para guardar respuesta
    last_response = gr.State()

    # Chat principal
    chatbot = gr.ChatInterface(
        fn=chat_wrapper,
        chatbot=gr.Chatbot(elem_id="chatbox", type="messages"),
        type="messages",
        textbox=gr.Textbox(placeholder="What content do you need today?", scale=9),
        additional_inputs=[model_selector, audience, platform, region],
        additional_outputs=[last_response],
        title="",
    )

    # Caja de texto para copiar (al final del chat)
    output_text = gr.Textbox(
        label="If you liked it, click to copy the answer. ✂️",
        visible=False,
        interactive=False,
        lines=6,
        show_copy_button=True
    )

    # Siempre que cambie last_response, se actualiza la caja
    def show_response(text):
        return gr.update(value=text, visible=True)

    last_response.change(fn=show_response, inputs=last_response, outputs=output_text)

    def toggle_settings(current):
        return not current, gr.update(visible=not current)

    toggle_btn.click(toggle_settings, show_settings, [show_settings, config_panel])

demo.launch()