# gemini_service.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=(
        "Eres un experto en seguridad de software. Analiza el código que te "
        "entreguen en busca de vulnerabilidades. Para cada una: explica por qué "
        "representa un riesgo, y sugiere cómo corregirla. Si el código no tiene "
        "vulnerabilidades evidentes, dilo claramente."
    )
)


async def analizar_codigo(codigo: str) -> str:
    respuesta = await model.generate_content_async(codigo)
    return respuesta.text
