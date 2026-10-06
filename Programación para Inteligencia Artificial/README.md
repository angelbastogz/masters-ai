# Programación para Inteligencia Artificial

Segunda asignatura de la maestría. Cubre Python moderno aplicado a la IA: tipado y validación con Pydantic, iteración y concurrencia con `asyncio`, organización de proyectos reproducibles con uv y la exposición de herramientas mediante un servidor MCP local.

[← Volver al índice de la maestría](../README.md)

## Unidades

| # | Unidad | Estado |
|---|---|---|
| 01 | [Python moderno](./01_Python_Moderno) | Completada |
| 02 | Datos y representaciones | Pendiente |
| 03 | Integración de componentes | Pendiente |
| 04 | Proyecto integrador | Pendiente |

## Unidad 1 — Python moderno

> Fecha límite de entrega de las prácticas de la Unidad 1: **7 de octubre de 2026**.

| # | Sesión | Ejercicios | Notebooks |
|---|---|---|---|
| 01 | [Curso acelerado de Python](./01_Python_Moderno/sesion-01-curso-acelerado-python) | [Práctica](./01_Python_Moderno/sesion-01-curso-acelerado-python/PRACTICA.md) | [U1 N1 — Curso acelerado de Python](./01_Python_Moderno/sesion-01-curso-acelerado-python/u1_n1_curso_acelerado_python.ipynb)<br>[U1 N2 — El Zen de Python](./01_Python_Moderno/sesion-01-curso-acelerado-python/u1_n2_zen_de_python.ipynb) |
| 02 | [Tipado, Pydantic y modelos de datos](./01_Python_Moderno/sesion-02-tipado-pydantic) | [Práctica](./01_Python_Moderno/sesion-02-tipado-pydantic/PRACTICA.md) | [U1 N3 — Tipado y Pydantic](./01_Python_Moderno/sesion-02-tipado-pydantic/u1_n3_tipado_pydantic.ipynb) |
| 03 | [Iteración, recursos y concurrencia](./01_Python_Moderno/sesion-03-iteracion-recursos-concurrencia) | [Práctica](./01_Python_Moderno/sesion-03-iteracion-recursos-concurrencia/PRACTICA.md) | [U1 N4 — Iteración, recursos y concurrencia](./01_Python_Moderno/sesion-03-iteracion-recursos-concurrencia/u1_n4_iteracion_recursos_concurrencia.ipynb) |
| 04 | [Organización y reproducibilidad con uv y MCP](./01_Python_Moderno/sesion-04-reproducibilidad) | [Práctica](./01_Python_Moderno/sesion-04-reproducibilidad/PRACTICA.md) | — |

La sesión 4 se resuelve como un proyecto en lugar de una notebook: **[course-catalog](./01_Python_Moderno/sesion-04-reproducibilidad/course-catalog)**, un catálogo de cursos consultable como CLI y como herramienta MCP, con logging, pruebas (`pytest`) y entorno reproducible con uv.

## Estructura de cada sesión

```
NN_Nombre_de_la_unidad/
└── sesion-NN-tema/
    ├── README.md     # Material de la sesión: presentación, recorrido y enlaces
    ├── PRACTICA.md   # Entregables de la práctica
    └── *.ipynb       # Notebooks de la clase con los ejercicios resueltos
```
