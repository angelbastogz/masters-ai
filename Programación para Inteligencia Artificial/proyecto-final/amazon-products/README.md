# Amazon Reviews MCP

Servidor MCP local (Streamable HTTP) sobre una muestra de Amazon Reviews 2023,
categoría Electronics: 600 productos y 6,992 reseñas. Ofrece tres herramientas:

| Herramienta                       | Qué hace                                                                                              |
|-----------------------------------|-------------------------------------------------------------------------------------------------------|
| `search_products(query, top_k=5)` | Busca productos por similitud semántica entre la consulta y un vector que combina catálogo y reseñas. |
| `analyze_product(product_id)`     | Conteos y proporciones por estrellas (1–5), media y mediana de las calificaciones.                    |
| `compare_products(product_ids)`   | Analiza dos o más productos y calcula la diferencia de medias respecto al primero.                    |

## Requisitos

- [uv](https://docs.astral.sh/uv/) (Python 3.13 se instala según `.python-version`).
- La carpeta `datasets/` con `products.jsonl.gz` y `reviews.jsonl.gz`.

## Instalación

Desde la carpeta `amazon-products/`:

```bash
uv sync --locked
```

## Iniciar el servidor

En una primera terminal:

```bash
uv run --locked python server.py
```

Al iniciar, el servidor carga los datos y calcula los embeddings con
`sentence-transformers/all-MiniLM-L6-v2` (configurado en `config.json`).
La primera vez descarga el modelo, por lo que tarda más. Los vectores no se
guardan en disco: se regeneran en cada arranque, sin ejecutar la notebook.

El servidor queda disponible en `http://127.0.0.1:8000/mcp`.

## Ejecutar el cliente

Con el servidor ya corriendo, en una segunda terminal:

```bash
uv run --locked python main.py
```

El cliente descubre las herramientas y ejecuta seis llamadas de demostración,
incluida una con `top_k=0` que debe devolver un error claro sin detener el servidor.

## Comprobar tipos y estilo

```bash
uv run --locked mypy --strict server.py client.py main.py support
uv run --locked ruff check .
uv run --locked ruff format --check .
```

## Ejemplos de consultas

La diferencia de medias se calcula respecto al primer producto de cada comparación.
Los dos ejemplos siguientes se encuentran comentados en `client.py`, para probarlos, descomente las líneas de la 20 a la 35.

### 1. "4K HDMI cable for gaming console" con top_k = 3

| # | ID         | Producto                         | Similitud | Reseñas | Media | Mediana | Diferencia de medias |
|---|------------|----------------------------------|-----------|---------|-------|---------|----------------------|
| 1 | B09YJXSPPW | HDMI Cable 10 ft 4K              | 0.668     | 11      | 4.45  | 5.0     | 0.00                 |
| 2 | B08CZ4KZHN | Atevon 4K HDMI Cable 6 ft 2-Pack | 0.646     | 16      | 4.50  | 5.0     | +0.05                |
| 3 | B06ZZD1WGJ | BlueRigger Mini HDMI to HDMI     | 0.628     | 13      | 4.62  | 5.0     | +0.16                |

> En los tres resultados obtenidos podemos ver que la búsqueda encontró coincidencias con el texto "4K HDMI cable" y no
> tanto con "for gaming console", aun así, los resultados son buenos, pero sí notamos que el 3 podría no ser relevante
> ya que es un Mini HDMI y la consulta busca un 4K HDMI para gaming.
> El algoritmo ordena los resultados con base en la similitud de un producto con la consulta dada por lo que el producto
> más relevante sería el primero y luego iría disminuyendo posiblemente la relevancia.
> Igual podemos notar que los 3 productos tienen una calificación con mediana 5 y diferencia de medias de 0.05 y 0.16,
> por lo que no se puede afirmar que un cable sea mejor que otro y las calificaciones no influyen en el orden de la
> búsqueda.

### 2. "Fitness tracker with long battery life" con top_k = 3

| # | ID         | Producto             | Similitud | Reseñas | Media | Mediana | Diferencia de medias |
|---|------------|----------------------|-----------|---------|-------|---------|----------------------|
| 1 | B08L4V3PNJ | Garmin Vivoactive 4S | 0.688     | 9       | 4.22  | 5.0     | 0.00                 |
| 2 | B0BTV39NV3 | Garmin Venu Sq Music | 0.674     | 6       | 4.33  | 4.5     | +0.11                |
| 3 | B0BJW6R4YX | Amazfit Bip U Pro    | 0.628     | 9       | 2.78  | 3.0     | −1.44                |

> En los tres resultados obtenidos podemos ver que la búsqueda encontró resultados con títulos diferentes a la query,
> sin embargo, como el algoritmo utiliza 50% catálogo y 50% reseñas se pueden dar casos como estos, en donde las reseñas
> sí mencionan partes del texto que contiene la query y por eso tienen mayor relevancia en la búsqueda.
> De nuevo, las calificaciones no influyen en el orden, pero la reseña (no importa si positiva o negativa) puede
> aumentar la similitud en la búsqueda. Por ejemplo, el primer resultado, 5 de 9 reseñas mencionan la batería y una se
> queja, eso contribuye a que aparezca como primer resultado sin importar la reseña que se queja.
> Por otro lado, podemos ver que el tercer resultado tiene una calificación media de 2.78. Como la query tiene una alta
> similitud con el catálogo y reseñas de ese producto, la búsqueda la posiciona en tercer resultado a pesar de tener una
> baja calificación. En este caso, serviría utilizar las otras tools `analyze_product` y `compare_products` para saber
> qué tan satisfechos quedaron los compradores.

## Limitaciones

1. La búsqueda convierte la query a un solo vector y una parte puede pesar más que otra ocasionando que los resultados
   puedan satisfacer solo una parte de la consulta. Como en el ejemplo 1, la búsqueda encontró resultados con "4K HDMI
   cable" pero no con "gaming console".
2. La búsqueda no diferencia entre reseñas positivas o negativas. Una reseña negativa que incluya palabras de la query
   contribuye a darle una mejor posición en el resultado tanto como una reseña positiva.
3. Dado que los productos tienen pocas reseñas, entre 5 y 30, la media y diferencia de medias pueden no ser muy
   confiables realmente.
4. El modelo utilizado está entrenado en inglés, consultas en otro idioma darán resultados menos relevantes. Además,
   trunca textos de más de 256 tokens, por lo que ignora el final de las reseñas largas.
