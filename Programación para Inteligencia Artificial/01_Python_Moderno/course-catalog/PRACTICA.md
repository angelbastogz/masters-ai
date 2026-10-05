# Práctica: un catálogo reproducible con MCP

Resuelve **9 ejercicios** sobre el proyecto construido con [GUIA.md](./GUIA.md):
los cinco siguientes y los cuatro de [CALIDAD.md](./CALIDAD.md).

## Ejercicio 1 · Punto de entrada

Ejecuta `uv run python -c "import main"`. Explica por qué no consulta el catálogo.
Identifica también la condición que impide iniciar el transporte al importar
`server.py`. Distingue registrar una herramienta de iniciar el servidor.

> Al importar main, __name__ vale el nombre del módulo y no "__main__", así que el bloque `if __name__ == "__main__:` no
> se ejecuta.
> Entonces import main no llama a main(). Por esa misma razón importar server.py no ejecuta mcp.run(transport="stdio") y
> el transporte
> no se inicia. Lo que sí ocurre al importar es el registro. el decorador @mcp.tool() agrega find_courses a la instancia
> mcp con su nombre
> y esquema sin abrir ningun transporte. Iniciar el servidor es llamar a mcp.run().

## Ejercicio 2 · Datos y argumentos

Copia `data/courses.json` a `data/extra_courses.json` y agrega un curso cuyo título
incluya Python. Usa `--catalog` para consultar esa copia desde `main.py` y comprueba
que aparecen tres resultados. Prueba una ruta inexistente y registra el código
de salida. La herramienta MCP sigue usando el catálogo predeterminado.

```
uv run python main.py python --catalog data/extra_courses.json
```

> Resultado: aparecen 3 coincidencias con código de salida 0.

```
uv run python main.py python --catalog data/missing_file.json
```

> Resultado: ERROR | __main__ | Catalog search failed
>
> FileNotFoundError: [Errno 2] No such file or directory: 'data/missing_file.json'

## Ejercicio 3 · Niveles y destinos

Compara una misma consulta con DEBUG, INFO y ERROR. Después usa
`--log-level ERROR --log-file logs/app.log`. Explica por qué el archivo conserva
mensajes que no aparecen en consola y por qué stdout debe reservarse al protocolo
en `server.py`.

```
uv run python main.py python --log-level DEBUG
```

> Resultado: DEBUG | catalog.search | Reading catalog: /Users/angelbastogz/Documents/Maestria/masters-ai/Programación
> para Inteligencia Artificial/01_Python_Moderno/course-catalog/data/courses.json
>
> INFO | catalog.search | Search completed: 2 matches

```
uv run python main.py python --log-level INFO
```

> Resultado: INFO | catalog.search | Search completed: 2 matches

```
uv run python main.py python --log-level ERROR
```

> Resultado: Vació, no hay errores

```
uv run python main.py python --log-level ERROR --log-file logs/app.log
```

> Porque en `configure_logging` cada destino tiene su propio nivel. El logger raíz acepta todo desde DEBUG y
> después cada handler filtra por separado. El handler de la consola usa el nivel de --log-level, y el del archivo
> siempre usa DEBUG.
>
> stdout debe reservarse al protocolo en server.py porque con transport="stdio" el cliente lee stdout.
> Un log en stdout se mezclaría con el protocolo y rompería la comunicación.

## Ejercicio 4 · Mejorar el diagnóstico

Añade al mensaje INFO de `catalog/search.py` la cantidad total de cursos leídos,
además de la cantidad de coincidencias. Usa argumentos de logging. Comprueba
que la consulta directa y la llamada MCP siguen devolviendo los mismos cursos.

```
uv run python main.py python
```

> Resultado: INFO | catalog.search | Search completed: 2 matches out of 3 courses

## Ejercicio 5 · Reproducción y llamada MCP

Desde una copia limpia, ejecuta `uv sync --locked` y `client.py` con `python`,
`astronomy` y una cadena de espacios. Identifica la herramienta disponible y
distingue respuesta vacía de error. Explica qué aportan `pyproject.toml`,
`uv.lock` y `.python-version` y por qué no se entrega `.venv`.

> El servidor expone una sola herramienta `find_courses` que el cliente obtiene con list_tools() antes de llamarla.
>
> astronomy es una consulta válida sin coincidencias, devuelve result: [] con is_error: false.
> La cadena de espacios es una consulta inválida, search courses lanza ValueError, el servidor la convierte en ToolError
> y el cliente recibe is_error: true con su respectivo mensaje de error
> "text": "Error executing tool find_courses: Cannot search the catalog. Check the query and server logs."
> 
> pyproject.tml declara el proyecto y sus dependencias con sus versiones permitidas. Igual configura herramientas como pytest y ruff.
> 
> uv.lock fijas las versiones exactas de todas las dependencias, incluyendo las indirectas.
> 
> .python-version indica la versión de python que uv debe usar.

## Entregables

- El proyecto con código, datos pequeños, pruebas, `pyproject.toml`, `uv.lock`,
  `.python-version` y `Makefile`.
- Un README con comandos, resultados de las llamadas y explicaciones de los
  ejercicios, incluida la evidencia de las comprobaciones de calidad.

Comprueba la ejecución desde una copia limpia. Entrega el proyecto sin `.venv`,
cachés ni logs.
