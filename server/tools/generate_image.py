# server/tools/generate_image.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

def generate_image(prompt: str) -> str:
    url = "https://api.stability.ai/v2beta/stable-image/generate/ultra"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
    }

    files = {
        "prompt": (None, prompt),
        "output_format": (None, "jpeg"),
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        return data["image"]  # base64 string
    else:
        raise Exception(f"Error al generar imagen: {response.status_code} - {response.text}")
