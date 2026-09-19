# Gemini: respuesta anclada + abstenerse
import time
from google.genai.errors import ServerError, ClientError

from app.store import query
from app.embed import gemini_client

MAX_RETRIES = 3


def answer(question: str, chunks: list[dict], threshold: float = 0.65) -> dict:
    if not chunks or chunks[0]["distance"] > threshold:
        return {"text": "No tengo información suficiente en el contexto para responder eso.", "abstained": True}

    context = "\n\n---\n\n".join(
        f"[Fuente: {c['source']}]\n{c['text']}" for c in chunks
    )

    contents = f"""
    Usa solo el siguiente contexto para responder la pregunta.
    Si un documento del contexto no es relevante, ignóralo.
    Si el contexto no contiene la respuesta, di que no lo sabes.

    Contexto:
    {context}

    Pregunta: {question}
    """

    for attempt in range(MAX_RETRIES):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-3.6-flash",
                contents=contents,
            )
            # Prefer text parts only (avoids thought_signature warning on thinking models)
            text = "".join(
                part.text
                for part in response.candidates[0].content.parts
                if getattr(part, "text", None)
            )
            return {"text": text, "abstained": False}
        except ServerError as e:
            if attempt < MAX_RETRIES - 1:
                wait = 5 * (2 ** attempt)
                print(f"Modelo no disponible, reintentando en {wait} segundos.")
                print(f"Error: {e}")
                time.sleep(wait)
        except ClientError as e:
            print(f"Cuota excedida en generate_content: {e}")
            return {
                "text": "Se alcanzó el límite diario de uso del modelo de IA. Intenta más tarde o revisa tu cuota en Google AI Studio.",
                "abstained": True}

        return {"text": "El modelo no está disponible por el momento. Intenta de nuevo en unos minutos.",
                "abstained": True}


if __name__ == "__main__":
    prompt = "¿Cuántos jugadores tiene un equipo de béisbol?"
    # prompt = "¿Quién ganó la Serie Mundial de 2026?"
    print(answer(question=prompt, chunks=query(prompt=prompt, top_k=5), threshold=0.65))
