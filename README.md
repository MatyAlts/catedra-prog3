# Material de cátedra — Programación III

**Tecnicatura Universitaria en Programación · UTN Facultad Regional Mendoza**
Docente: Matías Santiago Torres

Este repositorio contiene el **manuscrito fuente** del material de cátedra de
Programación III: tres módulos, veintiuna unidades de estudio, y las herramientas que
generan los entregables a partir de ellas.

---

## Qué hay acá

| Módulo | Unidades | Ubicación | Estado |
| --- | --- | --- | --- |
| **Despliegue en un VPS** | 5 | Raíz del repositorio (`01-…` a `05-…`) | Dictado |
| **Frontend, de HTML a TypeScript** | 8 | [`frontend/`](frontend/) | Escrito |
| **Backend, de POO a un servicio** | 8 | [`backend/`](backend/) | Escrito |

Los dos últimos se dictan **en paralelo dentro de la misma cursada**, con otro docente
a cargo del backend: los alumnos pasan media jornada con cada uno. Esa simultaneidad no
es un detalle organizativo — es lo que permite que la misma petición se estudie desde
sus dos extremos en la misma semana. La sincronización semana a semana está declarada
en los dos temarios.

Los tres módulos habilitan el **trabajo integrador Food Store**, cuyo documento fuente
vive en un repositorio aparte:
[`TPI-Metodologia1-trozado`](https://github.com/MatyAlts/TPI-Metodologia1-trozado).
El material lo **cita por número de sección y nunca lo copia**.

---

## Qué es una unidad de estudio

**Un instructivo enumera pasos. Una unidad de estudio funda cada paso en el concepto que
lo explica, y cada concepto en la decisión de diseño que lo originó.**

El alumno tiene que poder leerla solo, sin haber estado en el aula. Es el estándar que
fijó la Dirección al revisar la primera clase del módulo de despliegue, y rige para todo
lo que se escriba después. Sus nueve rasgos obligatorios —génesis histórica, anatomía
del artefacto, seguridad y evolución, referencias en prosa, entre otros— están
enunciados en los archivos `CLAUDE.md` de cada módulo, que son las reglas de escritura
además de las instrucciones para trabajar con agentes.

Dos convenciones que se notan al leer:

- **El cuerpo es académico impersonal; los recuadros van en voseo**, dirigidos al
  alumno. El contraste es deliberado.
- **Ningún concepto se enuncia antes de su problema.** El patrón Unit of Work no aparece
  hasta que el alumno se comió una operación aplicada a medias; la regla de orden de
  bloqueo no aparece hasta haber provocado un interbloqueo.

---

## Estructura de un módulo

```
frontend/  ·  backend/
├── CLAUDE.md      reglas de escritura del módulo
├── TEMARIO.md     el recorrido de las 8 clases y su sincronización
├── FIGURAS.md     catálogo de figuras: número, título, qué muestra, quién la toma
├── DIAGRAMAS.md   código Mermaid de los diagramas
└── capitulos/     01-… a 08-…
```

El módulo de despliegue precede a esa organización y vive en la raíz, con la misma
lógica: `FIGURAS.md`, `DIAGRAMAS.md` y `PROMPTS-WORD.md` acompañan a los cinco
capítulos. Su README propio quedó en
[`README-modulo-deploy.md`](README-modulo-deploy.md).

---

## Los `.md` son la fuente; los `.docx` y `.pdf` son derivados

Los entregables que reciben los alumnos —los `.docx` para revisión y los `.pdf`
publicados en el aula virtual— **se generan desde los `.md`** con los scripts de este
repositorio. Están versionados junto al manuscrito para que la versión entregada quede
registrada, pero **la fuente es siempre el `.md`**: una corrección se hace ahí y se
regenera.

También se versionan las miniaturas de los videos ([`miniaturas/`](miniaturas/)), que se
generan por script y no se editan a mano, y los guiones de los videos de cátedra.

---

## Verificaciones antes de dar un capítulo por terminado

El estándar es medible, y conviene medirlo en lugar de confiar:

```bash
# Extensión: entre 8.500 y 9.500 palabras
wc -w capitulos/07-*.md

# Recuadros: entre 10 y 14, contados POR SU EMOJI
grep -cP '^> \*\*[⚠💡🧪📌]' capitulos/07-*.md

# Arte ASCII: tiene que dar cero (queda ilegible al exportar a Word)
grep -c '[┌─┐│└┘├┤┬┴┼]' capitulos/07-*.md
```

Ese tercer chequeo existe porque el problema se detectó en un PDF ya generado. Y el
segundo tiene su historia: una versión anterior contaba las líneas que empiezan con
`> **`, lo que incluía las líneas internas de cada recuadro e inflaba el número. Al
corregirlo aparecieron cuatro capítulos por debajo del mínimo. **Un chequeo mal escrito
es peor que no tenerlo**, porque da tranquilidad sin dar garantía.

La última verificación es de coherencia: las figuras **citadas** en un capítulo tienen
que coincidir exactamente con las **declaradas** en `FIGURAS.md`.

---

## Lo que falta

Las **capturas de pantalla** declaradas en los `FIGURAS.md` de los dos módulos nuevos.
Están especificadas una por una —qué tiene que verse en cada una— pero todavía no
tomadas. Los diagramas, en cambio, están completos: su código Mermaid está en los
`DIAGRAMAS.md`.

---

## Licencia y uso

Material docente de cátedra. Si te sirve para tus clases, usalo y citá la fuente.
