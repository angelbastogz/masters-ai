# RAG — Reglamento oficial de béisbol

Sistema RAG que responde preguntas sobre el
*Official Baseball Rules* (edición 2026 de MLB). Cuenta con:

- una **API en FastAPI** (`/health`, `/ingest`, `/query`) que parte los documentos en chunks,
  los embebe con Google AI, los guarda en ChromaDB y responde con Gemini
  citando las fuentes;
- una **UI en Streamlit** que consume esa API, muestra las citas de cada respuesta
  y permite subir documentos nuevos para indexarlos.

Si el corpus no contiene evidencia suficiente, el sistema **se abstiene** en vez de inventar
una respuesta.

## Arquitectura

```
documento (.md/.txt/.pdf)
   │  extract_text + chunk_text        app/chunk.py    (tiktoken, 300 tokens, overlap 50)
   ▼
chunks ──► embeddings (gemini-embedding-001)   app/embed.py
   │
   ▼
ChromaDB persistente (./chroma)                app/store.py

pregunta ──► top-k chunks (store.query) ──► ¿distancia > 0.65? ── sí ──► abstiene (sin llamar al LLM)
                                                   │ no
                                                   ▼
                                    Gemini (gemini-3.6-flash), solo con el contexto   app/generate.py
                                                   │
                                                   ▼
                              { answer, citations, abstained }   app/main.py ──► ui/streamlit_app.py
```

| Módulo | Responsabilidad |
|---|---|
| [app/chunk.py](app/chunk.py) | Extrae texto (`.md`, `.txt`, `.pdf` con `pypdf`) y lo parte en ventanas de 300 tokens con 50 de overlap (`tiktoken`, codificación `cl100k_base`, una aproximación local del tokenizador de Gemini). |
| [app/embed.py](app/embed.py) | Cliente de Gemini y `GeminiEmbeddingFunction` (`gemini-embedding-001`). Falla al importarse si falta `GEMINI_API_KEY`. |
| [app/store.py](app/store.py) | ChromaDB: `ingest()` (en lotes de 50) y `query()` (top-k, devuelve `id`, `text`, `source`, `distance`). |
| [app/generate.py](app/generate.py) | Prompt anclado al contexto, abstención por umbral de distancia y manejo de errores de Gemini. |
| [app/main.py](app/main.py) | Endpoints de FastAPI. |
| [ui/streamlit_app.py](ui/streamlit_app.py) | Chat en Streamlit, citas, subida de archivos y estado de la API. |
| [data/rulebook/](data/rulebook/) | Corpus: 11 documentos Markdown (~55,000 palabras). Ver su [README](data/rulebook/README.md) para fuente y atribución. |

## Estructura

```
rag-app/
├── app/
│   ├── chunk.py
│   ├── embed.py
│   ├── generate.py
│   ├── main.py
│   └── store.py
├── data/rulebook/        # corpus (11 .md + README con la fuente)
├── ui/streamlit_app.py
├── chroma/               # base vectorial (se genera sola, ignorada por git)
├── requirements.txt
├── .env.example
└── README.md
```

## Instalación

Requiere Python 3.10 o superior. Desde la raíz del repositorio:

```bash
cd "Introducción a la IA/RAG/Proyecto final/rag-app"
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows (PowerShell):

```powershell
cd "Introducción a la IA\RAG\Proyecto final\rag-app"
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Configuración

Copia `.env.example` a `.env` y completa las claves:

```
GEMINI_API_KEY=tu_clave_de_gemini
OPENAI_API_KEY=tu_clave_de_openai
```

- `GEMINI_API_KEY` es **obligatoria**: la usan los embeddings, la generación y el
  chat directo con Gemini. Se crea en [Google AI Studio](https://aistudio.google.com/apikey).
- `OPENAI_API_KEY` solo hace falta si vas a usar el proveedor "OpenAI" del chat
  ([OpenAI API keys](https://platform.openai.com/api-keys)).

No subas `.env` al repositorio. Si Gemini responde **403 / leaked**, esa clave ya es pública:
crea una nueva, revoca la anterior y pon solo la nueva en `.env`.

La UI apunta a la API en `http://localhost:8000` (constante `FASTAPI_URL` en
`ui/streamlit_app.py`).

## Uso

Todos los comandos se ejecutan desde la raíz de `rag-app/` con el venv activado.

### 1. Levantar la API

```bash
uvicorn app.main:app --reload
```

Documentación interactiva (Swagger) en `http://localhost:8000/docs`.

> La API se arranca como módulo (`app.main:app`); no funciona con `python app/main.py`
> porque los módulos se importan como `app.*`. Lo mismo aplica para probar `store.py` o
> `generate.py` sueltos: `python -m app.store`, `python -m app.generate`.

### 2. Indexar el corpus

La base vectorial (`chroma/`) empieza vacía. Para cargar el reglamento completo:

```bash
curl -X POST http://localhost:8000/ingest \
  $(for f in data/rulebook/[0-9]*.md; do echo -F "files=@$f"; done)
```

Alternativamente, desde Swagger (`/docs` → `POST /ingest` → *Try it out*) selecciona los
archivos `data/rulebook/01_…md` a `11_…md` (no incluyas el `README.md`).

> **El ingest completo tarda varios minutos**: son ~331 chunks en lotes de 50 y hay una pausa
> de 60 s entre lotes para respetar el límite de tokens por minuto del tier gratuito de
> embeddings. Por eso conviene usar `curl` o Swagger para el corpus completo; la subida desde
> la UI tiene un timeout de 120 s y es mejor para pocos archivos pequeños.

Puedes confirmar cuántos chunks hay indexados con `GET /health` (campo `documents`).

### 3. Levantar la UI

En otra terminal:

```bash
streamlit run ui/streamlit_app.py
```

Se abre en `http://localhost:8501`. En la barra lateral:

- **Proveedor / Modelo**: "Fast API" es el chat RAG (usa tu API). "Gemini" y "OpenAI" son un
  chatbot directo, sin recuperación ni citas.
- **Nuevo chat**: reinicia la conversación (cambiar de proveedor también la reinicia).
- Con "Fast API" seleccionado aparecen además **Agregar documentos** (sube `.md`, `.txt` o
  `.pdf` y los indexa vía `POST /ingest`) y un indicador del estado de la API con el número de
  chunks indexados.

Cada respuesta del RAG trae un desplegable **Fuentes** con los chunks usados (archivo, distancia
y un fragmento del texto).

## API

### `GET /health`

```json
{ "status": "ok", "chroma_status": "ok", "documents": 331 }
```

`chroma_status` es `"error"` (y `documents` `null`) si no se puede leer la colección.

### `POST /ingest`

`multipart/form-data` con uno o más archivos en el campo `files` (`.md`, `.txt` o `.pdf`).
Extrae el texto, lo parte en chunks, lo embebe y lo guarda en Chroma.

```json
{ "documents": 11, "chunks": 331 }
```

Errores: `400` si un archivo no tiene nombre o su extensión no está soportada; `500` si falla
el embedding o el guardado. Los PDF escaneados (imágenes sin texto) no se soportan: no hay OCR.

### `POST /query`

```json
{ "query": "¿Cuántos jugadores tiene un equipo de béisbol?", "top_k": 5 }
```

`top_k` es opcional (por defecto 5).

```json
{
  "answer": "Un equipo tiene nueve jugadores (Regla 1.01)…",
  "citations": [
    { "id": "01_objectives_of_the_game.md_chunk_0", "source": "01_objectives_of_the_game.md",
      "text": "…", "score": 0.558 }
  ],
  "abstained": false
}
```

- `score` es la **distancia** de Chroma (menor = más parecido).
- `citations` lista los chunks que se le dieron a Gemini como contexto; queda vacío si
  `abstained` es `true`.
- Error `500` con el detalle en `detail` si falla la recuperación o la generación (el traceback
  queda en la consola de `uvicorn`).

## Abstención (no inventar)

1. **Filtro por distancia.** Si el chunk más cercano tiene distancia mayor a `0.65`, se responde
   "No tengo información suficiente…" sin llamar al LLM (`abstained: true`).
2. **Instrucción en el prompt.** Aun si pasa el filtro, Gemini debe responder solo con el
   contexto y decir que no lo sabe si la respuesta no está ahí.

El umbral se calibró con tres preguntas de prueba (mejor distancia): `0.558` para una pregunta
respondible ("¿Cuántos jugadores tiene un equipo de béisbol?"), `0.712` para una de béisbol que
el reglamento no cubre ("¿Quién ganó la Serie Mundial de 2026?") y `0.986` para una ajena
("¿Cuándo es la independencia de México?"). El corpus está en inglés y las preguntas pueden
hacerse en español (los embeddings de Gemini son multilingües).

## Límites conocidos

- **Cuotas del tier gratuito de Gemini.** Embeddings: ~30K tokens por minuto (de ahí los lotes
  de 50 y la pausa de 60 s). Generación con `gemini-3.6-flash`: 20 solicitudes por día; al
  agotarse, `/query` responde con un mensaje de límite diario y `abstained: true`. Puedes ver
  tus límites en [AI Studio](https://aistudio.google.com/rate-limit) y cambiar el modelo en
  `app/generate.py`.
- Las citas son todos los chunks recuperados, no solo los que el modelo usó realmente.
- El texto de los PDF y del reglamento viene de extracción automática y conserva algo de ruido
  (números de página, encabezados repetidos).
