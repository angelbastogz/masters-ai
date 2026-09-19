# Corpus: Official Baseball Rules (2026 Edition)

Corpus de texto para el proyecto RAG. 11 documentos Markdown, ~55,000 palabras en total,
partidos por sección del reglamento oficial de MLB.

## Fuente

*Official Baseball Rules*, 2026 Edition — Office of the Commissioner of Baseball (MLB).
Descargado el 2026-09-15 de:
https://mktg.mlbstatic.com/mlb/official-information/2026-official-baseball-rules.pdf

Documento de referencia pública distribuido libremente por MLB. Se incluye aquí con fines
educativos (proyecto final de curso, uso no comercial).

## Documentos

| Archivo | Sección | Palabras (aprox.) |
|---|---|---|
| `01_objectives_of_the_game.md` | 1.00 — Objectives of the Game | 150 |
| `02_the_playing_field.md` | 2.00 — The Playing Field | 1,000 |
| `03_equipment_and_uniforms.md` | 3.00 — Equipment and Uniforms | 2,060 |
| `04_game_preliminaries.md` | 4.00 — Game Preliminaries | 2,360 |
| `05_playing_the_game.md` | 5.00 — Playing the Game | 17,080 |
| `06_improper_play_illegal_action.md` | 6.00 — Improper Play, Illegal Action, and Conduct | 8,490 |
| `07_ending_the_game.md` | 7.00 — Ending the Game | 2,170 |
| `08_the_umpire.md` | 8.00 — The Umpire | 2,290 |
| `09_the_official_scorer.md` | 9.00 — The Official Scorer | 13,650 |
| `10_definitions_of_terms.md` | Definitions of Terms | 4,880 |
| `11_appendices.md` | Appendices (field/mound/glove diagrams, described in text) | 590 |

Se excluyó el índice alfabético final del PDF (solo referencias cruzadas de números de regla,
sin contenido para recuperar).

Nota: el texto viene de extracción automática del PDF (`pdftotext`), así que conserva algo de
ruido propio del layout original (números de página, encabezados de página repetidos). No afecta
el chunking ni la recuperación.

## Pregunta imposible de responder (para probar abstención)

El corpus es un reglamento — no contiene resultados, estadísticas ni noticias. Ejemplos de
preguntas que el sistema debe rechazar por falta de evidencia:

- "¿Quién ganó la Serie Mundial de 2026?"
- "¿Cuál fue el promedio de bateo de Aaron Judge la temporada pasada?"
- "¿Qué equipo tiene el mejor récord esta temporada?"
