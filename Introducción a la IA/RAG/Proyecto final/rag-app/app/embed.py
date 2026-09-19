# cliente de embeddings de Google AI
import os
from dotenv import load_dotenv, find_dotenv
from google import genai
from chromadb import Documents, EmbeddingFunction, Embeddings

load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment")

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
MODEL="gemini-embedding-001"

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        response = gemini_client.models.embed_content(
            model=MODEL,
            contents=input,
        )
        return [embedding.values for embedding in response.embeddings]


gemini_ef = GeminiEmbeddingFunction()