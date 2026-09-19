# partición en chunks con overlap
import glob
import os
import io
import pypdf

import tiktoken

# Tokenizador local
ENCODING = tiktoken.get_encoding("cl100k_base")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CORPUS_DIR = os.path.join(BASE_DIR, "data", "rulebook")


def chunk_text(text: str, source: str, chunk_size: int = 300, overlap: int = 50) -> list[dict]:
    if overlap >= chunk_size:
        raise ValueError("overlap debe ser menor que chunk_size")

    tokens = ENCODING.encode(text)
    source = source
    step = chunk_size - overlap

    chunks = []
    chunk_index = 0
    for start in range(0, len(tokens), step):
        window = tokens[start: start + chunk_size]
        if not window:
            break

        chunks.append(
            {
                "id": f"{source}_chunk_{chunk_index}",
                "text": ENCODING.decode(window),
                "source": source,
                "chunk_index": chunk_index,
            }
        )
        chunk_index += 1

        if start + chunk_size >= len(tokens):
            break

    return chunks


def extract_text(filename: str, content: bytes) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".pdf":
        reader = pypdf.PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if ext in (".md", ".txt"):
        return content.decode("utf-8")
    raise ValueError(f"Extensión no soportada: {ext}")


def chunk_file(path: str, chunk_size: int = 300, overlap: int = 50) -> list[dict]:
    """Lee un archivo de texto y lo parte en chunks de `chunk_size` tokens,
    donde cada chunk repite los últimos `overlap` tokens del anterior.

    Devuelve una lista de dicts: {id, text, source, chunk_index}.
    """
    with open(path, "rb") as f:
        content = f.read()

    source = os.path.basename(path)
    text = extract_text(source, content)

    return chunk_text(text, source, chunk_size, overlap)


def chunk_all(directory: str = DEFAULT_CORPUS_DIR, chunk_size: int = 300, overlap: int = 50) -> list[dict]:
    """Recorre todos los archivos del corpus (excluye README.md) y junta sus chunks."""
    all_chunks = []
    for path in sorted(glob.glob(os.path.join(directory, "[0-9]*.md"))):
        all_chunks.extend(chunk_file(path, chunk_size, overlap))
    return all_chunks


if __name__ == "__main__":
    chunks = chunk_all()
    print(f"Total de chunks: {len(chunks)}")
    for c in chunks[:3]:
        n_tokens = len(ENCODING.encode(c["text"]))
        print(f"\n--- {c['id']} ({n_tokens} tokens) ---")
        print(c["text"][:300])
