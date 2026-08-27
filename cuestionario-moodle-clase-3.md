# Alta del cuestionario autocorregido — Clase 3 (Docker: la receta reproducible)

> **Qué es este documento.** Los pasos para dar de alta el **Cuestionario** en el aula, a partir
> del banco `cuestionario-moodle-clase-3.xml`. No es material para el alumno.
> La clave con las respuestas está en `cuestionario-moodle-clase-3-respuestas.md`.

- **Campus:** `https://campustest.frm.utn.edu.ar` · **Curso:** id **14** — DevOps
- **Sección destino:** **30** — «Actividades 🧩» (`sectionid=555`)
- **Banco:** `cuestionario-moodle-clase-3.xml` — 31 preguntas
- **Composición:** 24 opción múltiple · 3 emparejamiento · 2 respuesta corta · 2 verdadero/falso
- **Cobertura:** 22 secciones del capítulo 3

---

## 1. Importar el banco

1. Ir a **https://campustest.frm.utn.edu.ar/question/bank/importquestions/import.php?courseid=14**
2. Formato: **Formato XML de Moodle**.
3. **«Obtener categoría del archivo» = Sí**. El XML crea sola la categoría
   `Clase 3 - Docker: la receta reproducible`.
4. Arrastrar el archivo → **Importar** → deben listarse las 31 preguntas.

> Si aparece «Archivo XML inválido - se esperaba una cadena (usar CDATA?)», mirá la sección
> equivalente de `cuestionario-moodle-clase-2.md`, que explica el diagnóstico y trae el script de
> verificación. **Este archivo ya está validado.**

## 2. Crear el cuestionario

Sección «Actividades 🧩» → *Añadir actividad* → **Cuestionario**.

- **Nombre:** `Clase 3 – Autoevaluación: Docker, imágenes y capas`
- **Descripción:** el bloque HTML de §4.

## 3. Cargar las preguntas

Pestaña **Preguntas** → *Agregar* → *del banco* → categoría
`Clase 3 - Docker: la receta reproducible` → las 31 → **Calificación máxima: 10**.

### 3.1. Paginación — qué va junto y qué va separado

En este banco **no hay filtraciones literales**: ninguna pregunta contiene, en su enunciado ni en
sus opciones, la respuesta de otra. Lo que sí hay son **cadenas conceptuales**, donde una pregunta
apoya a la siguiente, y ahí lo que importa es el **orden**:

| Va primero | Después | Por qué |
|---|---|---|
| **C3-04** (qué es un contenedor) | **C3-03** (emparejar espacios de nombres) | Primero el concepto, después el detalle de cada namespace |
| **C3-14** (la regla de invalidación) | **C3-15** (el orden de copiado) | La segunda es la aplicación de la primera |
| **C3-12** (V/F: EXPOSE abre el puerto) | **C3-13** (emparejar instrucción/capa) | El emparejamiento clasifica EXPOSE como metadato |
| **C3-17** (respuesta corta: `0.0.0.0`) | **C3-18** (por qué falla `127.0.0.1`) | La corta no debe poder deducirse por descarte |
| **C3-24** (respuesta corta: imagen base) | **C3-25** (por qué importa la imagen base) | ídem |

**Distribución en 12 páginas:**

| Pág | Bloque | Preguntas |
|---|---|---|
| 1 | Por qué existen los contenedores | 01, 02 |
| 2 | El modelo formal | **04, 05**, 03 |
| 3 | Imágenes y capas | 06, 07 |
| 4 | Contenedor y máquina virtual | 08, 09 |
| 5 | El contexto de construcción | 10, 11 |
| 6 | Capas y metadatos | **12**, 13 |
| 7 | El caché de capas | **14**, 15, 16 |
| 8 | La interfaz de escucha | **17**, 18 |
| 9 | Señales y secretos | 19, 20 |
| 10 | El Dockerfile del frontend | 21, 22, 23 |
| 11 | Imagen base e inspección | **24**, 25, 26 |
| 12 | Ecosistema y buenas prácticas | 27, 28, 29, 30, 31 |

> ⚠️ **No activar «Reordenar las preguntas al azar»**: mezcla las preguntas entre páginas y rompe
> el orden de las cadenas de arriba. El barajado **dentro** de cada pregunta ya viene en el XML.

---

## 4. Descripción — pegar en «Descripción» (modo HTML)

```html
<div style="font-family: sans-serif; line-height: 1.6; color: #000000;">
  <p style="font-size: 1rem;">Autoevaluación de la teoría de la Clase 3. Son
    <strong>31 preguntas</strong> que se corrigen solas y que podés repetir las veces que
    quieras: la nota que queda es la más alta.</p>

  <p style="font-size: 1rem;">No es una prueba de memoria. Cada pregunta te dice
    <strong>por qué</strong> la opción que elegiste está bien o mal, y te remite a la sección
    exacta del apunte.</p>

  <div style="background-color: #f8edef; padding: 12px; border-radius: 6px; border-left: 4px solid #7B1E2B; margin: 16px 0;">
    <p style="margin: 0; color: #5c0120;">⏱️ <strong>Tiempo estimado:</strong> 25 a 35 minutos ·
      <strong>Intentos:</strong> ilimitados · <strong>Nota:</strong> la más alta</p>
  </div>

  <div style="margin-top: 16px; background-color: #fff4e5; padding: 12px; border-radius: 6px; border-left: 4px solid #d97706;">
    <p style="margin: 0;">⚠️ <strong>Antes de arrancar:</strong> tené abierto el apunte
      <strong>Clase 3.pdf</strong>. Si podés, tené también una terminal con Docker: varias
      preguntas se contestan mejor después de haber corrido el comando.</p>
  </div>

  <div style="margin-top: 12px; background-color: #fdecea; padding: 12px; border-radius: 6px; border-left: 4px solid #c0392b;">
    <p style="margin: 0;">🚩 <strong>Lo que más se pierde:</strong> las preguntas sobre qué
      instrucciones <em>crean capa</em> y cuáles son solo metadato. <code>EXPOSE</code> no abre
      ningún puerto, y de ahí sale la mitad de la confusión de esta clase.</p>
  </div>

  <div style="text-align: center; margin-top: 20px;">
    <p style="font-size: 1.05rem; color: #7b1e2b; font-weight: bold;">✨ La máquina pasó a ser
      parte del código</p>
  </div>
</div>
```

---

## 5. Configuración

| Campo | Valor | Por qué |
|---|---|---|
| Intentos permitidos | **Sin límite** | Es autoevaluación, no examen |
| Método de calificación | **Calificación más alta** | ídem |
| Preguntas por página | **Personalizado: 12 páginas** | Ver §3.1 |
| Barajar dentro de las preguntas | **Sí** | El XML ya lo trae |
| Límite de tiempo | **Sin límite** | Se resuelve con el apunte al lado |
| Calificación máxima | **10** | Consistente con el resto del curso |
| Comportamiento de las preguntas | **Retroalimentación inmediata** | Ver nota |
| Navegación | **Libre** | |
| Calificación para aprobar | **6** | |

> 🔑 **Retroalimentación inmediata, no diferida.** Cada opción incorrecta de este banco tiene
> escrita su propia explicación. Con diferida, esa explicación llega cuando el alumno ya se
> desconectó del razonamiento; con inmediata la lee en el momento exacto en que se equivocó.

---

## 6. Qué cubre y qué no

| Parte del cuadernillo | ¿Va al cuestionario? |
|---|---|
| Verdadero/falso con justificación | **Sí**, transformada en opción múltiple sobre el *porqué* |
| Opción múltiple | **Sí** |
| Desarrollo conceptual | No: exige redacción |
| Casos de diagnóstico | **Parcialmente**, los que admiten opción múltiple |
| Lectura de salidas | **Parcialmente** |

**El desarrollo sigue en la Tarea entregable.** El cuestionario corrige solo las 31 conceptuales.

---

## 7. Nota de diseño

Las preguntas de **respuesta corta** de este banco son las que más discriminan: piden escribir
`0.0.0.0` (la interfaz de escucha dentro del contenedor) y `python:3.12-slim` (la imagen base).
Ninguna se adivina.

El **emparejamiento de espacios de nombres** (C3-03) es el que más valor tiene por pregunta:
cubre de una sola vez `mnt`, `pid`, `net`, `uts` y `user`, y su retroalimentación conecta el
espacio de nombres de red con el problema de Docker y el firewall de la Clase 2.

Quedaron **dos verdadero/falso**, y los dos apuntan a intuiciones falsas muy resistentes: que
borrar un secreto en una capa posterior lo elimina (`C3-06`) y que `EXPOSE` abre el puerto
(`C3-12`).

---

## 8. Checklist

- [ ] XML importado con «Obtener categoría del archivo = Sí» → 31 preguntas
- [ ] Cuestionario creado en la sección «Actividades 🧩»
- [ ] Las 31 preguntas agregadas desde el banco
- [ ] Paginación de §3.1 aplicada (12 páginas) y **«Reordenar al azar» desactivado**
- [ ] Calificación máxima **10**, aprobación **6**
- [ ] Comportamiento: **retroalimentación inmediata**
- [ ] `Clase 3.pdf` visible en la sección
- [ ] **Vista previa con un intento propio**
- [ ] La clave (`cuestionario-moodle-clase-3-respuestas.md`) **no** subida al aula
