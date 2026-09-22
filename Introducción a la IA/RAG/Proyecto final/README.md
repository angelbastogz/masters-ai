# Reporte del proyecto final
> Esté es el reporte del proyecto final, instrucciones sobre como correr el proyecto y sobre la estructura puedes encontrarlo en [./rag-app/README.md](./rag-app/README.md).

## Descripción del proyecto

Sistema RAG que responde preguntas sobre el
*Official Baseball Rules* (edición 2026 de MLB). Cuenta con:

- una **API en FastAPI** (`/health`, `/ingest`, `/query`) que parte los documentos en chunks,
  los embebe con Google AI, los guarda en ChromaDB y responde con Gemini
  citando las fuentes;
- una **UI en Streamlit** que consume esa API, muestra las citas de cada respuesta
  y permite subir documentos nuevos para indexarlos.

Si el corpus no contiene evidencia suficiente, el sistema **se abstiene** en vez de inventar
una respuesta.

## Corpus
Esté sistema RAG se conforma de un corpus de 11 archivos md ubicados en [./rag-app/data/rulebook](./rag-app/data/rulebook).
Los 11 archivos conforman el reglamento oficial de la Major League Baseball. 
Las instrucciones para indexar el corpus puedes encontrarlo en [./rag-app/README.md](./rag-app/README.md#uso)

## Evidencias

> Cuantos jugadores conforman un equipo de beisbol?

### Streamlit
COLOCAR VIDEO `jugadores-equipo.mov`

### cURL
```curl
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Cuantos jugadores conforman un equipo de beisbol?"}'
```

COLOCAR VIDEO `curl-jugadores-equipo.mov`

### docs

COLOCAR VIDEO `docs-jugadores-equipo.mov`

> Quien gano la serie mundial en 2026 ?

### Streamlit

### cURL
```curl
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Quien gano la serie mundial en 2026 ?"}'
```

### docs