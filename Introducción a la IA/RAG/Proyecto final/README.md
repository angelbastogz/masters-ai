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

## Dominio y tamaño del corpus
El dominio está conformado por el reglamento oficial de la MLB edición 2026, dividido en 11 archivos md para facilitar
la indexación. 

|            |                                                    |
|------------|----------------------------------------------------|
| Documentos | 11 archivos `.md`, aproximadamente 55,000 palabras |
| Chunks     | 331 chunks totales                                 |
| Embedding  | gemini-embedding-001 (Google AI)                   |

## Particiones - Tamaño y overlap

Se particionó en `331` chunks de `300` tokens con overlap de `50` tokens usando el tokenizador `cl100k_base` de OpenAI.
Gemini no provee un tokenizador que pueda utilizar facilmente como el de OpenAI es por eso que utilicé el `cl100k_base`. 

Los embeddings se generaron con el modelo `gemini-embedding-001` de Google AI. 

Utilice 300 tokens para particionar los textos ya que es un punto medio típico y suficiente para cubrir una regla completa con
su explicación.

El overlap de 50 tokens nos permité que si una de las reglas queda dividida en dos chunks no se pierda por completo ya que overlap
asegura que la frontera quede representada en ambos chunks. 


## Abstenciones

Para las abstenciones tenemos dos capas:
* Umbral de distancia

Antes de llamar al LLM, el sistema mirá la distancia del hunk más cercado que devolvió Chroma. Si esa distancia es mayor a `0.65`,
o si no hubo chunks en absoluto, se abstiene inmediatamente. 

```python
def answer(question: str, chunks: list[dict], threshold: float = 0.65) -> dict:
    if not chunks or chunks[0]["distance"] > threshold:
        return {"text": "No tengo información suficiente en el contexto para responder eso.", "abstained": True}
```
[Ver en Github](https://github.com/angelbastogz/masters-ai/blob/a57b9a7d1bc644f4eee7fe06aa0377b2770f604f/Introducci%C3%B3n%20a%20la%20IA/RAG/Proyecto%20final/rag-app/app/generate.py#L11-L13)

Chrome usa distancia euclidiana entre los vectores, por lo que, cuanto más lejos está el embedding de la pregunta del embedding 
del chunk más parecido, más distancia hay.

Elegí un threshold de 0.65 ya que al realizar algunas pruebas noté que ese threshold era suficiente para identificar si alguna pregunta
pertenece al dominio del corpus. 

* Instrucción en el prompt

Si pasa la primera capa, lo siguiente se encuentrá en el prompt que enviamos a Gemini. 
Em el prompt se indicamos a Gemini que utilice unicamente el contexto proporcionado para responder la pregunta y en caso de no contener
la respuesta, diga que no lo sabe.

```python
contents = f"""
    Usa solo el siguiente contexto para responder la pregunta.
    Si un documento del contexto no es relevante, ignóralo.
    Si el contexto no contiene la respuesta, di que no lo sabes.

    Contexto:
    {context}

    Pregunta: {question}
    """
```
[Ver en Github](https://github.com/angelbastogz/masters-ai/blob/a57b9a7d1bc644f4eee7fe06aa0377b2770f604f/Introducci%C3%B3n%20a%20la%20IA/RAG/Proyecto%20final/rag-app/app/generate.py#L19-L28

## Google AI / Chroma

### Google IA

En esté proyecto se utiliza Google AI para dos tareas distintas:

* Embeddings: Usamos el modelo `gemini-embedding-001` en [embed.py](https://github.com/angelbastogz/masters-ai/blob/a57b9a7d1bc644f4eee7fe06aa0377b2770f604f/Introducci%C3%B3n%20a%20la%20IA/RAG/Proyecto%20final/rag-app/app/embed.py#L13-25)
para convertir el texto en vectores numéricos que posteriormente almacenaremos en la base de datos.
* Generación: `gemini-3.6-flash` en [generate.py](https://github.com/angelbastogz/masters-ai/blob/a57b9a7d1bc644f4eee7fe06aa0377b2770f604f/Introducci%C3%B3n%20a%20la%20IA/RAG/Proyecto%20final/rag-app/app/generate.py#L32-35)
para generar la respuesta a la pregunta del usuario utilizando el contexto propocionado. 

### Chroma

En esté proyecto se utiliza Chroma como base de datos vectorial. En ella se almacenan los chunks y el vector de embedding generado con gemini. 

Chroma indexa esos vectors para búsqueda eficiente por similitud.

Chroma no calcula embeddings por si mismo, utiliza GeminiEmbeddingFunction como embedding_function al crear la colección e internamente delega la conversión
de texto a vector a Gemini. 

## Retos opcionales

### Filtro por `source`

EL UI de streamlit muestra una sección "Buscar en un documento" con nu dropdown se los documentos existentes, al seleccionar una de las opciones la pregunta del usuario
consultará únicamente en el source seleccionado.

### Borrar o reindexar un documento sin reconstruir toda la colección

Se agregó el endpoint `DELETE /sources/{source}`, que elimina de Chroma todos los chunks
cuyo `source` coincide con el nombre de archivo indicado. El resto de la colección no se toca.
Si el documento no está indexado responde `404`.

```bash
curl -X DELETE http://localhost:8000/sources/04_game_preliminaries.md
# {"deleted": "04_game_preliminaries.md"}
```

Para reindexar un documento modificado se borra primero su `source` y después se vuelve a
enviar el archivo a `POST /ingest` con el mismo nombre. Solo se recalculan los embeddings de
ese documento, no los de los otros 10.

### Histórico de preguntas en la sesión de Streamlit

Las preguntas que realiza el usuario en la misma sesión se van almacenando y se muestran siguiendo el flujo normal de un chat. 
El historial está limitado a la sesión actual de streamlit, es decir, si se recarga la página o cambia de modelo, la sesión se reinicía y el historial desaparecería. 
