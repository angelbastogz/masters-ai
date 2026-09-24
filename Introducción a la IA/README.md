# Introducción a la IA

Primera asignatura de la maestría. Cubre los fundamentos de la Inteligencia Artificial: agentes, algoritmos de búsqueda, redes neuronales, visión computacional, aprendizaje no supervisado y, como proyecto final, un sistema RAG.

[← Volver al índice de la maestría](../README.md)

## Temas

| # | Tema | Ejercicios | Notebooks |
|---|---|---|---|
| 01 | [Conceptos básicos de Inteligencia Artificial](./01_Conceptos_b%C3%A1sicos_de_Inteligencia_Artificial) | [Ejercicio 01 — Aplicaciones de IA que uso o he usado](./01_Conceptos_b%C3%A1sicos_de_Inteligencia_Artificial/Ejercicios/ejercicio-01.md) | — |
| 02 | [Agentes](./02_Agentes) | [Ejercicio 01 — Cambiar la ubicación del Wumpus y los pits](./02_Agentes/Ejercicios/ejercicio-01.md)<br>[Ejercicio 02 — Descripción PEAS de agentes inteligentes](./02_Agentes/Ejercicios/ejercicio-02.md) | — |
| 03 | [Búsqueda no informada](./03_B%C3%BAsqueda_no_informada) | [Ejercicio 01 — Comparar BFS, UCS, DFS, DLS e IDS en el mapa de Rumania](./03_B%C3%BAsqueda_no_informada/Ejercicios/ejercicio-01.md) | — |
| 04 | [Búsqueda informada](./04_B%C3%BAsqueda_informada) | [Ejercicio 01 — Comparar Greedy y A* en el mapa de Rumania](./04_B%C3%BAsqueda_informada/Ejercicios/ejercicio-01.md) | — |
| 05 | [Perceptrón multicapa](./05_Perceptr%C3%B3n_multicapa) | [Ejercicio 01 — Más capas en el perceptrón multicapa (Iris)](./05_Perceptr%C3%B3n_multicapa/Ejercicios/ejercicio-01.md) | [Notebooks](./05_Perceptr%C3%B3n_multicapa/Notebooks) |
| 06 | [Visión computacional](./06_Visi%C3%B3n_computacional) | [Ejercicio 01 — Cambiar la imagen de predicción en YOLO](./06_Visi%C3%B3n_computacional/Ejercicios/ejercicio-01.md) | [Notebooks](./06_Visi%C3%B3n_computacional/Notebooks) |
| 07 | [Clustering K-medias](./07_Clustering_K-medias) | [Ejercicio 01 — Separar los blobs y volver a elegir k](./07_Clustering_K-medias/Ejercicios/ejercicio-01.md) | [Notebooks](./07_Clustering_K-medias/Notebooks) |

## Proyecto final

**[RAG sobre el reglamento oficial de béisbol](./RAG/Proyecto%20final)** — sistema de preguntas y respuestas sobre el *Official Baseball Rules* de MLB, con API en FastAPI, UI en Streamlit, ChromaDB y Gemini.

- [Reporte del proyecto](./RAG/Proyecto%20final/README.md)
- [Código e instrucciones para correrlo](./RAG/Proyecto%20final/rag-app/README.md)

## Estructura de cada tema

```
NN_Nombre_del_tema/
├── Ejercicios/   # Enunciado y resolución de cada ejercicio (ejercicio-NN.md)
├── Notebooks/    # Notebooks de la clase usados en los ejercicios (cuando aplica)
├── evidencia/    # Capturas y gráficas referenciadas desde los ejercicios
└── config/       # Archivos de configuración propios (cuando aplica)
```
