# Reglas de creación de contenido — Backend desde POO

Material de cátedra para **Programación III** (TUP, UTN FRM). Ocho unidades de
estudio que llevan al alumno desde haber terminado POO en Python hasta poder
encarar el backend del TPI Food Store con agentes de IA.

Se dicta **en paralelo** con el módulo de frontend (`material/frontend/`), dentro
de la misma cursada y con otro docente a cargo. Antes de escribir una sola línea,
leer [`TEMARIO.md`](TEMARIO.md), y en particular su sección de sincronización.

---

## 1. Qué es una unidad de estudio

**Un instructivo enumera pasos. Una unidad de estudio funda cada paso en el
concepto que lo explica, y cada concepto en la decisión de diseño que lo originó.**

El alumno tiene que poder leerla solo, sin haber estado en el aula. Este es el
estándar que fijó la Dirección y no es negociable.

Los **nueve rasgos obligatorios** de cada capítulo:

1. Subtítulo `*Unidad de estudio · Edición ampliada con fundamentos teóricos*`
2. Índice de contenidos numerado (10-13 puntos) en la sección de alcance
3. **Sección N.2 de génesis**: qué problema resolvió la tecnología, qué se usaba
   antes y por qué colapsó, quién la propuso, cuándo y bajo qué norma. Cierra
   enunciando las decisiones de diseño que explican todo lo observable después
4. Formalización del modelo, con vocabulario preciso y los límites del estándar
5. **Anatomía del artefacto** campo por campo (una aplicación ASGI, un modelo
   SQLModel, una transacción, un mensaje de la cola), conectando cada campo con lo
   que la herramienta de diagnóstico muestra en pantalla
6. Sección de **seguridad y evolución**: qué le falta al diseño original y qué
   extensiones lo atacan, aunque el práctico no las configure
7. **Cada afirmación lleva su porqué.** Nunca "no uses carga perezosa"; siempre "la
   razón es concreta: la carga perezosa emite una consulta al acceder al atributo,
   y en contexto asincrónico ese acceso ocurre fuera del `await` que la haría
   válida"
8. Referencias cruzadas explícitas **en las dos direcciones**, hacia adelante y
   hacia atrás
9. **Encuadre metodológico** de los procedimientos: no una lista de
   comprobaciones sino qué valida cada una, y cuando hay diagnóstico se nombra el
   método

**Cierre obligatorio, en este orden:**

Verificación · Errores frecuentes · Actividades (5-7, las últimas de exploración,
pidiendo relacionar lo observado con una sección teórica citada por número) ·
Síntesis (**abre por la decisión de diseño, no por el procedimiento**) ·
Referencias y lecturas complementarias **en prosa, no en lista**.

## 2. Registro: cuerpo impersonal, recuadros en voseo

El cuerpo del capítulo es **académico impersonal**. Los recuadros van en **voseo,
dirigidos al alumno**. El contraste es deliberado y la Dirección lo confirmó.

Los cuatro recuadros y su emoji: ⚠️ advertencia · 💡 tip · 🧪 experimento ·
📌 nota. **Entre 10 y 14 por capítulo.**

## 3. Ortografía

Español rioplatense, con **acentos y ñ correctos, sin excepción**.

## 4. Nada de arte ASCII

Un esquema hecho con caracteres de recuadro se ve bien en el `.md` y **queda
ilegible en Word**: la fuente monoespaciada rompe la alineación. Verificado sobre
el PDF del Capítulo 2 del módulo de deploy.

Si un esquema necesita cajas y flechas —o un árbol de carpetas— va como **figura**
o como **tabla**, nunca como dibujo de caracteres. Su entrada se declara en
[`FIGURAS.md`](FIGURAS.md) y su código Mermaid en [`DIAGRAMAS.md`](DIAGRAMAS.md).

## 5. El puente con POO es obligatorio

Este módulo **no empieza de cero**: empieza donde terminaron las ocho actividades
de POO en Python. Cada capítulo debe señalar explícitamente qué de aquello se
está usando, y la tabla de correspondencias está en `TEMARIO.md`.

Los tres puentes más fuertes, que hay que nombrar cuando corresponda:

- **Actividad 8** (dependencia de uso y de creación) → `Depends()` de FastAPI, y
  la regla del TPI de que el Router **no construye** el Unit of Work.
- **Actividad 4** (`Protocol`, duck typing) → los puertos `CachePort` y
  `EventPort` del TPI, y la implementación alternativa que permite degradar.
- **Actividad 6** (agregación y composición) → el Unit of Work componiendo
  repositorios.

## 6. Trazabilidad con el TPI

Este módulo existe para habilitar el TPI, **pero vive en otro árbol y en otro
repositorio**. El documento del director trozado está en:

```
Deploy a VPS/calculadora/trabajo integrador/docs-tpi/
```

Ese es un repositorio git independiente, con la garantía de que su contenido nunca
difiere del `.docx` original. Este material **no lo modifica nunca**; sólo lo cita.

Cada capítulo cita las secciones por su **número original** (`1.4`, `8.3`, `10.1`),
nombra las reglas que quedan explicadas, y **nunca copia texto del TPI**.

**Antes de afirmar cualquier cosa sobre el TPI, verificarla leyendo la sección.**
Durante la escritura del módulo de frontend hubo que corregir tres afirmaciones
que se habían dado por buenas sin leer la fuente completa.

## 7. Las tres familias de reglas

El backend declara **37 reglas** en tres familias, y no hay que mezclarlas:

- **RN-01 a RN-22** — negocio. Qué puede y qué no puede pasar en el dominio.
- **EA-01 a EA-08** — ejecución asincrónica. **Todas en la sección 1.4.**
- **TB-01 a TB-07** — trabajo diferido. **Todas en la sección 10.1.**

Más los **50 casos TST** de la sección 15.2, que son el garante de buena parte.

Cuando una regla declara su garante, **citarlo**: dice dónde se verifica y a veces
—como en TST-45 del frontend— el diseño de la prueba explica la regla mejor que su
enunciado.

## 8. Ningún concepto se enuncia antes de su problema

Regla de oro pedagógica del módulo, y la que más fácil se rompe al escribir rápido:

- **EA-05 no se enuncia** hasta haber visto explotar una carga perezosa en
  contexto asincrónico.
- **RN-18 no se enuncia** hasta haber provocado un interbloqueo.
- **TB-02 no se enuncia** hasta haber visto una tarea ejecutarse dos veces.
- **El Unit of Work no se presenta** hasta que el alumno se comió una operación a
  medio aplicar.

Si un capítulo enuncia la solución antes que el problema, está mal escrito aunque
todo lo que diga sea cierto.

## 9. Código de ejemplo

- Ejecutable y verificado, no ilustrativo.
- Coherente con el **stack real del TPI**, que son diecinueve tecnologías: Python
  3.12+, FastAPI 0.111+, SQLModel, SQLAlchemy 2.0 asincrónico, psycopg 3,
  Alembic (plantilla asincrónica), PostgreSQL 16+, Redis 7.4+, redis-py
  asincrónico, taskiq y taskiq-redis, taskiq-fastapi, sse-starlette, PyJWT,
  Passlib con bcrypt, pytest, httpx, asgi-lifespan y uvicorn.
- Los ejemplos progresan hacia el dominio del TPI (productos, pedidos, stock).
- **Todos los handlers con `async def`**, sin excepción (EA-01).

## 10. Extensión

Alrededor de **8.500 a 9.500 palabras por capítulo**. La extensión es consecuencia
de fundar cada afirmación, no un objetivo en sí. La primera pasada tiende a quedar
corta: **medir y ampliar** antes de dar un capítulo por terminado.

## 11. Archivos

| Archivo | Contiene |
| --- | --- |
| `TEMARIO.md` | El recorrido de las 8 clases y la sincronización con frontend |
| `CLAUDE.md` | Este archivo |
| `FIGURAS.md` | Catálogo de figuras: número, título, qué muestra, quién la toma |
| `DIAGRAMAS.md` | Código Mermaid de los diagramas |
| `capitulos/` | `01-…` a `08-…` |

## 12. Memoria

Proyecto engram: **`tpi-foodstore`**. Guardar con proyecto explícito:

```bash
engram save "<título>" "<contenido>" --type <tipo> --project tpi-foodstore
```

## 13. Antes de dar un capítulo por terminado

- [ ] Los nueve rasgos presentes, el cierre en el orden obligatorio
- [ ] Entre 8.500 y 9.500 palabras; entre 10 y 14 recuadros
- [ ] Cada afirmación tiene su porqué
- [ ] Ningún concepto enunciado antes de su problema
- [ ] El puente con POO señalado explícitamente donde corresponde
- [ ] Cuerpo impersonal, recuadros en voseo; acentos y ñ correctos
- [ ] Recuadros contados **por su emoji**, no por líneas que empiezan con `> **`:
      `grep -cP '^> \*\*[⚠💡🧪📌]' capitulos/NN-*.md` — entre 10 y 14
- [ ] Cero arte ASCII; los esquemas en `FIGURAS.md` y `DIAGRAMAS.md`
- [ ] Las figuras **citadas** coinciden exactamente con las **declaradas**
- [ ] Toda afirmación sobre el TPI verificada contra la sección original
- [ ] Referencias finales en prosa, no en lista
