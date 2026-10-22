# Maestría en IA

Repositorio donde recopilo los trabajos, ejercicios y proyectos que voy realizando durante mi maestría en Inteligencia Artificial.

Cada asignatura vive en su propia carpeta en la raíz del repositorio y tiene su propio `README.md` con el detalle de temas, ejercicios y proyectos.

## Asignaturas

| # | Asignatura | Estado | Proyecto final |
|---|---|---|---|
| 1 | [Introducción a la IA](./Introducci%C3%B3n%20a%20la%20IA) | ✅ Completada | [RAG sobre el reglamento oficial de béisbol](./Introducci%C3%B3n%20a%20la%20IA/RAG/Proyecto%20final) |
| 2 | [Programación para Inteligencia Artificial](./Programaci%C3%B3n%20para%20Inteligencia%20Artificial) | ✅ Completada | [Búsqueda y análisis de productos de Amazon con MCP](./Programaci%C3%B3n%20para%20Inteligencia%20Artificial/proyecto-final) |

## Estructura del repositorio

```
masters-ai/
├── README.md                                  # Este índice
├── LICENSE
├── Introducción a la IA/
│   ├── README.md                              # Temas, ejercicios y proyecto final
│   ├── 01_Conceptos_básicos_de_Inteligencia_Artificial/
│   ├── 02_Agentes/
│   ├── 03_Búsqueda_no_informada/
│   ├── 04_Búsqueda_informada/
│   ├── 05_Perceptrón_multicapa/
│   ├── 06_Visión_computacional/
│   ├── 07_Clustering_K-medias/
│   └── RAG/Proyecto final/
│       ├── README.md                          # Reporte del proyecto
│       └── rag-app/                           # API FastAPI + UI Streamlit
└── Programación para Inteligencia Artificial/
    ├── README.md                              # Unidades, sesiones y proyecto final
    ├── 01_Python_Moderno/                     # Sesiones 01–04 (incluye course-catalog)
    ├── 02_Datos_y_representaciones/           # NumPy, pandas, PyTorch y visualización
    ├── 03_Integración_de_components/          # SQL/NoSQL, LangGraph y LangChain
    ├── datasets/                              # Titanic-Dataset.csv
    └── proyecto-final/
        └── amazon-products/                   # Servidor MCP de productos de Amazon
```

Cada asignatura organiza su contenido a su manera:

- **Introducción a la IA**: temas `NN_Nombre_del_tema/` con subcarpetas `Ejercicios/`, `Notebooks/` y `evidencia/` según aplique.
- **Programación para Inteligencia Artificial**: unidades `NN_Nombre_de_la_unidad/` con sesiones `sesion-NN-tema/`, cada una con `README.md`, `PRACTICA.md`, notebooks y, cuando aplica, un proyecto `uv` reproducible.

### Agregar una nueva asignatura

1. Crear la carpeta en la raíz con el nombre de la asignatura.
2. Agregar un `README.md` dentro de ella con la tabla de temas (puedes copiar el de una asignatura existente).
3. Añadir una fila a la tabla de [Asignaturas](#asignaturas) de este README.

## Licencia

Este proyecto está bajo la licencia [MIT](./LICENSE).
