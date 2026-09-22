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

https://github.com/user-attachments/assets/bb4c545a-5ec3-40fc-95ef-1807fdee746b

### cURL
```curl
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Cuantos jugadores conforman un equipo de beisbol?"}'
```

https://github.com/user-attachments/assets/ecc9424c-276f-469e-8240-b4ea64255070

### docs

https://github.com/user-attachments/assets/ebc929ff-5eac-4a52-b1dd-15a180eabe17

> Quien gano la serie mundial en 2026 ?

### Streamlit

https://github.com/user-attachments/assets/faa6b3e9-435c-4473-96f3-889d51342356

### cURL
```curl
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Quien gano la serie mundial en 2026 ?"}'
```

https://github.com/user-attachments/assets/254c0e9b-d75a-4e56-af20-b196bf7338b5

### docs

https://github.com/user-attachments/assets/ea65afc6-64f4-4168-9d47-9b7e2a86248d

