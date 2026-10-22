# Programación para Inteligencia Artificial

Segunda asignatura de la maestría. Cubre Python moderno aplicado a la IA: tipado y validación con Pydantic, iteración y concurrencia con `asyncio`, organización de proyectos reproducibles con uv, procesamiento de datos con NumPy, pandas y PyTorch, visualización con Matplotlib, Python como cliente SQL/NoSQL, workflows con LangGraph, agentes con LangChain y la exposición de herramientas mediante servidores MCP.

[← Volver al índice de la maestría](../README.md)

## Unidades

| # | Unidad | Estado |
|---|---|---|
| 01 | [Python moderno](./01_Python_Moderno) | Completada |
| 02 | [Datos y representaciones](./02_Datos_y_representaciones) | Completada |
| 03 | [Integración de componentes](./03_Integraci%C3%B3n_de_components) | Completada |
| 04 | [Proyecto final](./proyecto-final) | Completada |

## Unidad 1 — Python moderno

> Fecha límite de entrega de las prácticas de la Unidad 1: **7 de octubre de 2026**.

| # | Sesión | Ejercicios | Notebooks |
|---|---|---|---|
| 01 | [Curso acelerado de Python](./01_Python_Moderno/sesion-01-curso-acelerado-python) | [Práctica](./01_Python_Moderno/sesion-01-curso-acelerado-python/PRACTICA.md) | [U1 N1 — Curso acelerado de Python](./01_Python_Moderno/sesion-01-curso-acelerado-python/u1_n1_curso_acelerado_python.ipynb)<br>[U1 N2 — El Zen de Python](./01_Python_Moderno/sesion-01-curso-acelerado-python/u1_n2_zen_de_python.ipynb) |
| 02 | [Tipado, Pydantic y modelos de datos](./01_Python_Moderno/sesion-02-tipado-pydantic) | [Práctica](./01_Python_Moderno/sesion-02-tipado-pydantic/PRACTICA.md) | [U1 N3 — Tipado y Pydantic](./01_Python_Moderno/sesion-02-tipado-pydantic/u1_n3_tipado_pydantic.ipynb) |
| 03 | [Iteración, recursos y concurrencia](./01_Python_Moderno/sesion-03-iteracion-recursos-concurrencia) | [Práctica](./01_Python_Moderno/sesion-03-iteracion-recursos-concurrencia/PRACTICA.md) | [U1 N4 — Iteración, recursos y concurrencia](./01_Python_Moderno/sesion-03-iteracion-recursos-concurrencia/u1_n4_iteracion_recursos_concurrencia.ipynb) |
| 04 | [Organización y reproducibilidad con uv y MCP](./01_Python_Moderno/sesion-04-reproducibilidad) | [Práctica](./01_Python_Moderno/sesion-04-reproducibilidad/PRACTICA.md) | — |

La sesión 4 se resuelve como un proyecto en lugar de una notebook: **[course-catalog](./01_Python_Moderno/sesion-04-reproducibilidad/course-catalog)**, un catálogo de cursos consultable como CLI y como herramienta MCP, con logging, pruebas (`pytest`) y entorno reproducible con uv.

## Unidad 2 — Datos y representaciones

| # | Sesión | Ejercicios | Notebooks |
|---|---|---|---|
| 01 | [NumPy y vectorización](./02_Datos_y_representaciones/sesion-01-numpy) | [Práctica](./02_Datos_y_representaciones/sesion-01-numpy/PRACTICA.md) | [U2 N1 — Arreglos NumPy](./02_Datos_y_representaciones/sesion-01-numpy/01-exploracion/u2_n1_arreglos_numpy.ipynb)<br>[U2 N2 — Reporte de mediciones](./02_Datos_y_representaciones/sesion-01-numpy/02-reporte-mediciones/u2_n2_reporte_mediciones.ipynb) |
| 02 | [Tablas con pandas y paso a NumPy](./02_Datos_y_representaciones/sesion-02-pandas) | [Práctica](./02_Datos_y_representaciones/sesion-02-pandas/PRACTICA.md) | [U2 N3 — pandas con Titanic](./02_Datos_y_representaciones/sesion-02-pandas/u2_n3_pandas_titanic.ipynb) |
| 03 | [Tensores y datasets con PyTorch](./02_Datos_y_representaciones/sesion-03-pytorch) | [Práctica](./02_Datos_y_representaciones/sesion-03-pytorch/PRACTICA.md) | [U2 N4 — Tensores y datasets](./02_Datos_y_representaciones/sesion-03-pytorch/u2_n4_tensores_datasets.ipynb) |
| 04 | [Visualización de datos](./02_Datos_y_representaciones/sesion-04-visualizacion) | [Práctica](./02_Datos_y_representaciones/sesion-04-visualizacion/PRACTICA.md) | [U2 N5 — Visualización](./02_Datos_y_representaciones/sesion-04-visualizacion/u2_n5_visualizacion.ipynb) |

Cada sesión es un proyecto `uv` con su `main.py` para repetir el procesamiento desde la terminal. Las sesiones 1 a 3 empaquetan la lógica en módulos con pruebas (`measurements/`, `titanic/`, `data_lab/`). El conjunto de Titanic usado en la sesión 2 vive en [datasets](./datasets).

## Unidad 3 — Integración de componentes

| # | Sesión | Ejercicios | Notebooks |
|---|---|---|---|
| 01 | [Python como cliente SQL y NoSQL](./03_Integraci%C3%B3n_de_components/sesion-01-sql-nosql) | [Práctica](./03_Integraci%C3%B3n_de_components/sesion-01-sql-nosql/PRACTICA.md) | [U3 N1 — SQLite y pandas](./03_Integraci%C3%B3n_de_components/sesion-01-sql-nosql/u3_n1_sqlite_pandas.ipynb)<br>[U3 N2 — Neo4j](./03_Integraci%C3%B3n_de_components/sesion-01-sql-nosql/u3_n2_neo4j.ipynb) |
| 02 | [Workflows de datos con LangGraph](./03_Integraci%C3%B3n_de_components/sesion-02-langgraph) | [Práctica](./03_Integraci%C3%B3n_de_components/sesion-02-langgraph/PRACTICA.md) | [U3 N3 — Workflows con LangGraph](./03_Integraci%C3%B3n_de_components/sesion-02-langgraph/u3_n3_langgraph_workflows.ipynb) |
| 03 | [Agentes con LangChain](./03_Integraci%C3%B3n_de_components/sesion-03-langchain) (opcional) | [Práctica](./03_Integraci%C3%B3n_de_components/sesion-03-langchain/PRACTICA.md) | [U3 N4 — Agentes con LangChain](./03_Integraci%C3%B3n_de_components/sesion-03-langchain/u3_n4_langchain_agents.ipynb) |

Las sesiones 2 y 3 trabajan sobre el mismo catálogo de documentos (`sample_data.py`). La sesión 3 separa el agente en módulos (`catalog_tools.py`, `agent_app.py`, `agent_hooks.py`, `input_guardrails.py`, `mcp_client.py`) y requiere una API key propia en `.env` (ver `.env.example`) para ejecutar el modelo.

## Proyecto final

**[Búsqueda y análisis de productos de Amazon con MCP](./proyecto-final)** — servidor MCP por HTTP local sobre una muestra de *Amazon Reviews 2023 · Electronics* (600 productos y 6 992 reseñas), con búsqueda semántica por embeddings (`all-MiniLM-L6-v2`) y análisis de calificaciones.

- [Enunciado del proyecto](./proyecto-final/README.md)
- [Código, herramientas e instrucciones para correrlo (`amazon-products`)](./proyecto-final/amazon-products/README.md)

## Estructura de la asignatura

```
Programación para Inteligencia Artificial/
├── README.md                          # Este archivo
├── 01_Python_Moderno/
│   ├── sesion-01-curso-acelerado-python/
│   ├── sesion-02-tipado-pydantic/
│   ├── sesion-03-iteracion-recursos-concurrencia/
│   └── sesion-04-reproducibilidad/
│       └── course-catalog/            # Proyecto uv: CLI + servidor MCP
├── 02_Datos_y_representaciones/
│   ├── README.md                      # Temario y entrega de la unidad
│   ├── sesion-01-numpy/
│   │   ├── datos/                     # CSV de mediciones
│   │   ├── 01-exploracion/            # Proyecto uv + notebook U2 N1
│   │   └── 02-reporte-mediciones/     # Proyecto uv + notebook U2 N2
│   ├── sesion-02-pandas/              # Proyecto uv: módulo titanic/
│   ├── sesion-03-pytorch/             # Proyecto uv: módulo data_lab/
│   └── sesion-04-visualizacion/       # Proyecto uv: gráficos con Matplotlib
├── 03_Integración_de_components/
│   ├── sesion-01-sql-nosql/           # SQLite, pandas y Neo4j
│   ├── sesion-02-langgraph/           # Workflows con estado, nodos y subgraphs
│   └── sesion-03-langchain/           # Agente con tools, guardrails y cliente MCP
├── datasets/                          # Titanic-Dataset.csv
└── proyecto-final/
    ├── README.md, GUIA.md, ...        # Enunciado y material proporcionado
    ├── datasets/                      # products.jsonl.gz y reviews.jsonl.gz
    └── amazon-products/               # Mi solución: servidor MCP (uv)
        ├── server.py, main.py, client.py
        └── support/                   # data, settings, encoder, search, analysis
```

## Estructura de cada sesión

```
NN_Nombre_de_la_unidad/
└── sesion-NN-tema/
    ├── README.md       # Material de la sesión: presentación, recorrido y enlaces
    ├── PRACTICA.md     # Entregables de la práctica
    ├── FUENTES.md      # Documentación oficial consultada (cuando aplica)
    ├── pyproject.toml  # Proyecto uv reproducible (cuando aplica)
    ├── main.py         # Ejecución desde la terminal (cuando aplica)
    └── *.ipynb         # Notebooks de la clase con los ejercicios resueltos
```
