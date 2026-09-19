# ChromaDB: alta, consulta top-k
import os
import chromadb
import time

from app.embed import gemini_ef
from app.chunk import chunk_all

CHROMA_DB_NAME = "chroma"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DB_PATH = os.path.join(BASE_DIR, CHROMA_DB_NAME)

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(
    name=CHROMA_DB_NAME,
    embedding_function=gemini_ef,
)

BATCH_SIZE = 50 # to avoid restriction limits of gemini embedding

def ingest(chunks: list[dict]) -> None:
    ids = [c["id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]

    for start in range(0, len(chunks), BATCH_SIZE):
        end = start + BATCH_SIZE
        collection.add(
            documents=documents[start:end],
            ids=ids[start:end],
            metadatas=metadatas[start:end],
        )
        time.sleep(60)

def query(prompt: str, top_k: int = 5) -> list[dict]:
    results = collection.query(
        query_texts=[prompt],
        n_results=top_k,
    )
    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    return [
        {
            "id": ids[i],
            "text": documents[i],
            "source": metadatas[i]["source"],
            "distance": distances[i]
        }
        for i in range(len(ids))
    ]

if __name__ == "__main__":
    #chunks = chunk_all()
    #ingest(chunks)
    print("¿Cuántos jugadores tiene un equipo de béisbol?")
    print(query(prompt="¿Cuántos jugadores tiene un equipo de béisbol?", top_k=5))
    print("¿Quién ganó la Serie Mundial de 2026?")
    print(query(prompt="¿Quién ganó la Serie Mundial de 2026?", top_k=5))
    print("¿Cuando es la independencia de mexico?")
    print(query(prompt="¿Cuando es la independencia de mexico?", top_k=5))