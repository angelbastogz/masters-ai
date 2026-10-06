# Catálogo de cursos con MCP

Una función consulta `data/courses.json`. `main.py` la usa desde la terminal y
`server.py` la expone como herramienta MCP mediante stdio.

```bash
uv sync --locked
uv run --locked python main.py python
uv run --locked python main.py astronomy
uv run --locked python main.py python --log-level DEBUG --log-file logs/app.log
uv run --locked python client.py python
```

`client.py` inicia y detiene el servidor automáticamente. No arranques otra copia
antes de ejecutar el cliente. Los resultados incluyen dos cursos para `python`
y ninguno para `astronomy`. Una consulta vacía produce un error:

```bash
uv run --locked python main.py " "
uv run --locked python client.py " "
```

Ambos comandos terminan con código 1. `main.py` también permite cambiar el
archivo mediante `--catalog data/another_catalog.json`.

## Archivos

| Archivo | Responsabilidad |
|---|---|
| `catalog/search.py` | Modelo Course, lectura y búsqueda. |
| `catalog/logging_config.py` | Niveles, formato y destinos. |
| `main.py` | Argumentos de terminal y salida JSON. |
| `server.py` | Registro de la herramienta y transporte MCP. |
| `client.py` | Cliente de demostración que inicia el servidor. |
| `tests/` | Casos de búsqueda y comunicación real por stdio. |

La ruta del catálogo se calcula desde el archivo Python y no desde la carpeta
actual. El servidor reserva stdout para MCP y envía los logs a stderr.

## Iniciar solo el servidor

```bash
uv run --locked python server.py
```

Espera mensajes MCP por stdin. No abre una página web ni acepta consultas
escritas como texto libre. Detén esta ejecución con Ctrl+C y usa el cliente
incluido o [MCP Inspector](../GUIA.md#7-inspeccionar-la-herramienta).

## Ejercicios de la práctica

Los ejercicios resueltos, con sus comandos, resultados y explicaciones, están en
[PRACTICA.md](PRACTICA.md).

## Calidad

```bash
make check
```

> Resultado: 
```
uv run --locked ruff check .
All checks passed!
uv run --locked ruff format --check .
11 files already formatted
uv run --locked mypy --strict main.py server.py client.py catalog
Success: no issues found in 6 source files
uv run --locked python -m pytest
........                                                                                                                                                                                                                          [100%]
8 passed in 0.68s
```