import json
from openai import AsyncOpenAI
import os

class LLMService:
    def __init__(self, base_url="http://localhost:11434/v1", model="gemma2"):
        # Utilizamos la API compatible con OpenAI de Ollama por defecto
        # Asume que Ollama está corriendo en local en el puerto 11434
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key="ollama" # Requerido por la librería, pero ignorado por Ollama local
        )
        self.model = model

    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3
        )
        return response.choices[0].message.content

    async def extract_json(self, prompt: str, system_prompt: str = None) -> dict:
        """
        Obliga al modelo a devolver un objeto JSON estructurado.
        Muy útil para extraer el grafo de conocimiento.
        """
        messages = []
        if system_prompt:
            # Añadimos instrucciones estrictas de JSON
            sys_prompt = system_prompt + "\nIMPORTANT: You must respond ONLY with a valid JSON object. No markdown formatting, no explanations."
            messages.append({"role": "system", "content": sys_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback por si el modelo devolvió markdown (ej. ```json ... ```)
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
