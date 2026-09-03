# Reglas de creación de contenido — Frontend desde cero

Material de cátedra para **Programación III** (TUP, UTN FRM). Ocho unidades de
estudio que llevan al alumno de cero web hasta poder encarar el frontend del TPI
Food Store con agentes de IA.

Antes de escribir una sola línea, leer [`TEMARIO.md`](TEMARIO.md).

> **El 2026-09-02 la Dirección cambió el registro de todo el módulo al criollo.**
> Los ocho capítulos de `capitulos/` están escritos en ese registro; los originales
> académicos quedaron respaldados en `capitulos/_academico/`. El método de
> traducción está formalizado en [`CRIOLLO.md`](CRIOLLO.md), y el Capítulo 1 es su
> ejemplo canónico. Este archivo sigue siendo la fuente de los **nueve rasgos** y
> de las reglas de contenido; `CRIOLLO.md` gobierna la **forma**. Donde los dos
> difieren —el registro de §2 y las referencias en prosa de §1— manda `CRIOLLO.md`.

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
5. **Anatomía del artefacto** campo por campo (una petición HTTP, una regla CSS,
   un nodo del DOM, una definición de tipo), conectando cada campo con lo que la
   herramienta de diagnóstico muestra en pantalla
6. Sección de **seguridad y evolución**: qué le falta al diseño original y qué
   extensiones lo atacan, aunque el práctico no las configure
7. **Cada afirmación lleva su porqué.** Nunca "no uses `innerHTML`"; siempre "la
   razón es concreta: `innerHTML` parsea el texto como marcado, así que un dato
   con `<script>` deja de ser dato y pasa a ser código"
8. Referencias cruzadas explícitas **en las dos direcciones**, hacia adelante y
   hacia atrás
9. **Encuadre metodológico** de los procedimientos: no una lista de
   comprobaciones sino qué valida cada una, y cuando hay diagnóstico se nombra el
   método

**Cierre obligatorio, en este orden:**

Verificación · Errores frecuentes · Actividades (5-7, las últimas de exploración,
pidiendo relacionar lo observado con una sección teórica citada por número) ·
Síntesis (**abre por la decisión de diseño, no por el procedimiento**) ·
Referencias y lecturas complementarias.

**Cambio del 2026-09-02:** el estándar académico las pedía **en prosa, no en
lista**. El registro criollo las pide **priorizadas y en lista**, bajo los tres
encabezados `Si leés una sola cosa` / `Si leés tres` / `Las fuentes normativas`
(ver [`CRIOLLO.md`](CRIOLLO.md) §10). Cada obra conserva edición, editorial, año
y su línea de para qué sirve.

## 2. Registro: todo en criollo

**Desde el 2026-09-02, todo el capítulo va en voseo.** La Dirección revisó el
Capítulo 1, lo reescribió entero en registro criollo y pidió que el resto del
módulo lo siguiera. El contraste anterior —cuerpo impersonal, recuadros en
voseo— **quedó sin efecto**.

La única excepción son los bloques `### Qué dice`, que se mantienen impersonales
**a propósito**: representan la voz del texto académico que después se traduce.

Los cuatro recuadros y su emoji siguen siendo los mismos: ⚠️ advertencia ·
💡 tip · 🧪 experimento · 📌 nota. Lo que cambia es que **el emoji ya no se
imprime en el Word** —sólo elige el color— y que el título del recuadro lleva su
etiqueta en mayúscula (`OJO ACÁ`, `PARA EL PIZARRÓN`, `PARA ENTENDER`,
`EXPERIMENTO`, `LA IDEA MADRE`). El generador se invoca con `--sin-emoji`.

El detalle completo, en [`CRIOLLO.md`](CRIOLLO.md).

## 3. Ortografía

Español rioplatense, con **acentos y ñ correctos, sin excepción**. Nunca
reemplazar un carácter acentuado por su equivalente ASCII.

## 4. Nada de arte ASCII

Un esquema hecho con caracteres de recuadro (`┌─┐│└┘▶▼`) se ve bien en el `.md` y
**queda ilegible en Word**: la fuente monoespaciada rompe la alineación y el
corrector le mete subrayados encima. Verificado sobre el PDF del Capítulo 2 del
módulo de deploy.

Si un esquema necesita cajas y flechas, va como **figura**, con su entrada en
[`FIGURAS.md`](FIGURAS.md) y su código Mermaid en [`DIAGRAMAS.md`](DIAGRAMAS.md).

Se toleran sólo las anotaciones de una línea (una llave señalando parte de una
URL), porque no dependen de que dos renglones queden alineados.

## 5. Trazabilidad con el TPI

Este módulo existe para habilitar el TPI, **pero vive en otro árbol y en otro
repositorio**. El documento del director trozado está en:

```
Deploy a VPS/calculadora/trabajo integrador/docs-tpi/
```

Ese es un repositorio git independiente, con sus propias reglas —incluida la
garantía de que su contenido nunca difiere del `.docx` original—. Este material
**no lo modifica nunca**; sólo lo cita.

Cada capítulo:

- cita las secciones que habilita **por su número original** (`2.5`, `13.2`,
  `14.1`), que es el del documento del director y sirve para ir y volver;
- nombra las reglas `RN-F01` a `RN-F11` que quedan explicadas;
- **nunca copia texto del TPI.**

Copiar el TPI acá crearía una segunda versión que algún día va a diferir. Como
los dos árboles están separados, nadie se daría cuenta hasta que sea tarde: por
eso se cita por número y no se transcribe.

## 6. Ningún concepto se enuncia antes de su problema

Regla de oro pedagógica del módulo, y la que más fácil se rompe al escribir rápido:

- **RN-F02 no se enuncia** hasta haber mostrado un XSS funcionando.
- **RN-F01 no se enuncia** hasta haber mostrado una fuga de memoria real.
- **Vite no se presenta** hasta que el alumno sintió el dolor de no tener bundler.
- **TypeScript no se presenta** hasta que el alumno se comió un error que el
  compilador habría atrapado.

Si un capítulo enuncia la solución antes que el problema, está mal escrito aunque
todo lo que diga sea cierto.

## 7. Código de ejemplo

- Ejecutable y verificado, no ilustrativo.
- Coherente con el **stack real del TPI**, que son doce tecnologias y no cuatro:
  TypeScript 5 estricto, Vite 5 (plantilla `vanilla-ts`), DOM API + Web Components,
  History API, EventSource, Tailwind 3, `@tanstack/query-core` 5,
  `@tanstack/form-core`, `zustand/vanilla` 4, Axios 1, Chart.js 4 y DOMPurify 3.
  **Sin framework de interfaz** — lo prohibido es lo que se haria cargo del ciclo
  de vida, no las bibliotecas.
- Los ejemplos progresan hacia el dominio del TPI (productos, pedidos, stock), no
  hacia `foo`/`bar`.

## 8. Extensión

Alrededor de **10.000 palabras por capítulo**, en línea con el módulo de deploy a
VPS. La extensión es consecuencia de fundar cada afirmación, no un objetivo en sí.

## 9. Archivos

Este módulo vive en `material/frontend/`, junto al resto del material de cátedra
de Programación III (el módulo de deploy a VPS está en `material/`, un nivel
arriba, y comparte estándar y formato).

| Archivo | Contiene |
| --- | --- |
| `TEMARIO.md` | El recorrido de las 8 clases y su trazabilidad con el TPI |
| `CLAUDE.md` | Este archivo: los nueve rasgos y las reglas de contenido |
| `CRIOLLO.md` | El manual de estilo del registro criollo: gobierna la forma |
| `FIGURAS.md` | Catálogo de figuras: número, título, qué muestra, quién la toma |
| `DIAGRAMAS.md` | Código Mermaid de los diagramas |
| `capitulos/` | `01-…` a `08-…`, en registro criollo |
| `capitulos/_academico/` | Respaldo de los ocho capítulos en el registro académico anterior |

## 10. Memoria

Proyecto engram: **`tpi-foodstore`**. Guardar con proyecto explícito:

```bash
engram save "<título>" "<contenido>" --type <tipo> --project tpi-foodstore
```

## 11. Antes de dar un capítulo por terminado

- [ ] Los nueve rasgos presentes, el cierre en el orden obligatorio
- [ ] Cada afirmación tiene su porqué
- [ ] Ningún concepto enunciado antes de su problema
- [ ] Todo el capítulo en voseo, salvo los bloques `### Qué dice`
- [ ] Acentos y ñ correctos
- [ ] Recuadros contados **por su emoji**, no por líneas que empiezan con `> **`:
      `grep -c '^> \*\*[⚠💡🧪📌]' capitulos/NN-*.md` — entre 14 y 18
- [ ] Cero arte ASCII; los esquemas están en `FIGURAS.md` y `DIAGRAMAS.md`
- [ ] Referencias cruzadas en las dos direcciones, sin enlaces rotos
- [ ] Las secciones del TPI se citan y se enlazan, no se copian
- [ ] Referencias finales priorizadas en lista (`CRIOLLO.md` §10)
- [ ] El checklist propio del registro criollo (`CRIOLLO.md` §12) también pasa
