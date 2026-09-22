# FastAPI: /health, /ingest, /query
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import logging

from app.store import collection, ingest, query, list_sources
from app.generate import answer
from app.chunk import chunk_text, extract_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/health")
def get_health() -> dict:
    try:
        count = collection.count()
        chroma_status = "ok"
    except Exception:
        count = None
        chroma_status = "error"

    return {
        "status": "ok",
        "chroma_status": chroma_status,
        "documents": count
    }


@app.post("/ingest")
async def post_ingest(files: list[UploadFile] = File(...)) -> dict:
    all_chunks = []
    for file in files:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Todos los archivos deben tener nombre")

        raw = await file.read()
        try:
            text = extract_text(file.filename, raw)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        all_chunks.extend(chunk_text(text, source=file.filename))

    try:
        ingest(all_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {e}")

    return {
        "documents": len({c["source"] for c in all_chunks}),
        "chunks": len(all_chunks)
    }


@app.get("/sources")
def get_sources() -> dict:
    return {"sources": list_sources()}


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    source: str | None = None


@app.post("/query")
def post_query(request: QueryRequest) -> dict:
    try:
        chunks = query(request.query, top_k=request.top_k, source=request.source)
        result = answer(question=request.query, chunks=chunks)
    except Exception as e:
        logger.exception(f"Error procesando la pregunta: {e}")
        raise HTTPException(status_code=500, detail=f"Error procesando la pregunta: {e}")

    citations = [] if result["abstained"] else [
        {"id": c["id"], "source": c["source"], "text": c["text"], "score": c["distance"]}
        for c in chunks
    ]
    return {
        "answer": result["text"],
        "citations": citations,
        "abstained": result["abstained"]
    }
