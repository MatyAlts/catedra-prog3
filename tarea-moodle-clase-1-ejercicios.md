# Alta de tarea entregable — Clase 1: Ejercicios de teoría (DNS)

> **Qué es este documento.** La receta para dar de alta la actividad **Tarea** en el aula virtual.
> Todo lo que está en bloques de código se copia y se pega tal cual en el campo que indica el título.
> No es material para el alumno: es la hoja de ruta del docente.

- **Curso:** Programación 3 — Tecnicatura Universitaria en Programación (UTN FRM)
- **Unidad:** 1 — Del navegador al servidor
- **Sección del curso:** la misma donde vive el bloque `actividad-moodle-clase-1-dns.html`
- **Tipo de actividad Moodle:** Tarea (`assign`)
- **Archivos que acompañan:** `Clase 1 - Ejercicios de teoria.pdf` (se publica) y
  `Clase 1 - Ejercicios de teoria - Respuestas.pdf` (**NO se publica todavía**, ver §6)

---

## 0. Antes de tocar Moodle

1. Subir al repositorio de archivos del curso **solo** `Clase 1 - Ejercicios de teoria.pdf`.
2. Verificar que el apunte `Clase 1.pdf` ya esté publicado en la sección: la tarea lo referencia
   por sección (§1.7, §1.9.2…) y sin el apunte a mano el ejercicio no se puede resolver.
3. Tener decidido si la entrega es individual o grupal. **Leé §4 antes de decidir** — hay una
   trampa de Moodle que arruina la calificación y no avisa.

> ⚠️ **La clave de corrección no se sube ahora.** Si el PDF de respuestas queda visible en la
> sección desde el minuto cero, la entrega deja de medir absolutamente nada. Se publica recién
> después de que cierre la fecha límite (§6).

---

## 1. Configuración de la actividad, campo por campo

Los nombres de campo son los del formulario de Moodle en español.

### General

| Campo | Valor |
|---|---|
| Nombre de la tarea | `Clase 1 – Ejercicios de teoría: DNS y dominio propio` |
| Descripción | El bloque HTML de §2 |
| Muestra la descripción en la página del curso | **No** (la sección ya tiene el bloque de la clase; duplicarlo la satura) |
| Instrucciones de la entrega | El bloque HTML de §3 |
| Archivos adicionales | `Clase 1 - Ejercicios de teoria.pdf` |

### Disponibilidad

| Campo | Valor sugerido | Por qué |
|---|---|---|
| Permitir entregas desde | **vie 14/08/2026, 14:00** | Arranque de la clase. Que puedan subir apenas terminan. |
| Fecha de entrega | **lun 17/08/2026, 23:59** | El fin de semana cubre a quien no llegó a cerrarlo en la mesa. |
| Fecha límite | **mié 19/08/2026, 23:59** | Después de esta fecha Moodle no acepta nada más. |
| Recordar calificar el | **vie 21/08/2026** | |

> Ajustá las fechas a tu comisión. Lo que **no** conviene mover es el orden: la clave se publica
> después de la *fecha límite*, no después de la *fecha de entrega*.

### Tipos de entrega

| Campo | Valor |
|---|---|
| Tipos de entrega | ☑ **Archivos enviados** — ☐ Texto en línea |
| Número máximo de archivos subidos | **5** |
| Tamaño máximo de la entrega | **20 MB** |
| Tipos de archivo aceptados | `.pdf .jpg .jpeg .png` |

Los cinco archivos y los formatos de imagen son a propósito: si el grupo imprime el PDF y lo
resuelve a mano, va a subir fotos de las hojas. Pedir un único PDF prolijo garantiza que la mitad
del curso pelee con un conversor en vez de con el DNS.

> 🤖 **Si pensás corregir con Active-IA**, esto cambia: exigí **un solo PDF con texto
> seleccionable** y sacá los formatos de imagen. Las fotos rompen el flujo de corrección
> automática, y una consigna que mezcla imagen y texto obliga a corregir a mano igual.

### Tipos de retroalimentación

| Campo | Valor |
|---|---|
| Comentarios de retroalimentación | **Sí** |
| Comentario en línea | No |
| Hoja de calificaciones externa | Sí (cómodo para cargar las notas de toda la comisión de una) |

### Configuración de la entrega

| Campo | Valor |
|---|---|
| Requerir que los alumnos pulsen el botón de envío | **Sí** |
| Requerir que los estudiantes acepten las condiciones de entrega | No |
| Permitir reapertura | **Manualmente** |
| Número máximo de intentos | 2 |

«Requerir que pulsen enviar» evita el caso clásico del borrador que quedó cargado y nunca
enviado, que después es una discusión de la que no se sale.

### Configuración de entrega por grupo

| Campo | Valor |
|---|---|
| Entrega por grupos | **No** |

**Leé §4 antes de cambiar esto a Sí.**

### Calificación

| Campo | Valor |
|---|---|
| Tipo | Puntuación |
| Puntuación máxima | **100** |
| Método de calificación | Calificación simple directa (o Rúbrica, con los criterios de §5) |
| Categoría de calificación | La de la Unidad 1 |
| Calificación para aprobar | **60** |
| Ocultar identidad | No |
| Ocultar la calificación a los estudiantes hasta… | **Sí**, hasta publicar todas |

### Finalización de actividad

| Campo | Valor |
|---|---|
| Rastreo de finalización | Mostrar la actividad como completada cuando se cumplan las condiciones |
| Condición | ☑ El estudiante debe entregar para completar esta actividad |

---

## 2. Descripción — pegar en el campo «Descripción»

Pegar con el editor en modo **HTML** (`</>` en la barra de TinyMCE / Atto).

```html
<div style="font-family: sans-serif; line-height: 1.6; color: #000000;">
  <p style="font-size: 1rem;">Esta actividad cierra la teoría de la Clase 1. No es una prueba de
    memoria: es una prueba de <strong>lectura con criterio</strong>. Todo lo que se pregunta está
    en el capítulo 1 del apunte, y cada respuesta de la clave remite a la sección que la justifica.</p>

  <p style="font-size: 1rem;">Se resuelve <strong>en grupos de dos o tres, durante la clase</strong>,
    con el apunte a mano. Lo que se evalúa no es que recuerden comandos: es que puedan
    <strong>nombrar el concepto que explica cada síntoma</strong>.</p>

  <div style="background-color: #f8edef; padding: 12px; border-radius: 6px; border-left: 4px solid #7B1E2B; margin: 16px 0;">
    <p style="margin: 0; color: #5c0120;">⏱️ <strong>Tiempo estimado:</strong> 50 a 60 minutos ·
      <strong>Puntaje:</strong> 100 puntos · <strong>Se aprueba con 60</strong></p>
  </div>

  <p style="font-size: 1rem; color: #7b1e2b;"><strong>📌 Qué contiene el cuadernillo</strong></p>
  <ul style="padding-left: 20px; font-size: 1rem;">
    <li><strong>Parte A</strong> — 10 verdadero/falso <em>con justificación obligatoria</em> (20 pts)</li>
    <li><strong>Parte B</strong> — 10 de opción múltiple (10 pts)</li>
    <li><strong>Parte C</strong> — 10 de desarrollo conceptual (30 pts)</li>
    <li><strong>Parte D</strong> — 6 casos de diagnóstico: qué pasa, cómo lo confirmás, cómo lo arreglás (30 pts)</li>
    <li><strong>Parte E</strong> — 3 lecturas de salidas reales de <code>dig</code> y <code>nslookup</code> (10 pts)</li>
  </ul>

  <div style="margin-top: 16px; background-color: #fff4e5; padding: 12px; border-radius: 6px; border-left: 4px solid #d97706;">
    <p style="margin: 0;">⚠️ <strong>Antes de arrancar:</strong> tené abierto el apunte
      <strong>Clase 1.pdf</strong>. Cuando dudes, buscá la sección — encontrarla también es parte
      del ejercicio.</p>
  </div>

  <div style="margin-top: 12px; background-color: #fdecea; padding: 12px; border-radius: 6px; border-left: 4px solid #c0392b;">
    <p style="margin: 0;">🚩 <strong>Lo que más se pierde:</strong> las justificaciones de la
      Parte A. Un «Falso» sin justificar <strong>no suma puntaje</strong>. Una línea alcanza, pero
      tiene que estar.</p>
  </div>

  <div style="text-align: center; margin-top: 20px;">
    <p style="font-size: 1.05rem; color: #7b1e2b; font-weight: bold;">✨ Si podés explicar por qué
      falla, ya sabés arreglarlo</p>
  </div>
</div>
```

---

## 3. Instrucciones de la entrega — pegar en «Instrucciones de la entrega»

```html
<div style="font-family: sans-serif; line-height: 1.6; color: #000000;">
  <p><strong>Entrega individual, resolución grupal.</strong> Trabajan de a dos o tres, pero
    <strong>cada integrante sube el archivo</strong> desde su propio usuario. Puede ser
    exactamente el mismo archivo: no es copia, es el trabajo del grupo.</p>
  <p><strong>En la primera hoja tienen que figurar los nombres completos de todos los
    integrantes.</strong> Una entrega sin integrantes identificados se califica como individual.</p>
  <p>Formato aceptado: un PDF, o hasta 5 fotos legibles de las hojas (<code>.jpg</code> /
    <code>.png</code>). Si sacás fotos, revisá que se lea antes de subir.</p>
  <p>No hace falta transcribir los enunciados: alcanza con el número de ítem
    (<code>A1</code>, <code>B4</code>, <code>D2</code>…) y la respuesta.</p>
</div>
```

---

## 4. La trampa de «Entrega por grupos» — leer antes de activarla

Moodle ofrece **Entrega por grupos**, y para una actividad que se resuelve en grupo parece la
opción obvia. No lo es, y el motivo es específico:

Los grupos de esta actividad se arman **en la mesa, en el momento**. No existen como grupos
del curso en Moodle. Si activás «Entrega por grupos» sin haber creado esos grupos y sin asignar
un **agrupamiento**, Moodle mete a todos los estudiantes sin grupo en el **«Grupo por defecto»**
— y entonces:

- una sola entrega de un solo estudiante cuenta como la entrega de **todo el curso**;
- la calificación que le pongas a esa entrega se propaga a **todos**;
- y el panel de entregas te muestra todo en verde, así que no hay síntoma que te avise.

**Recomendación: dejar «Entrega por grupos» en No**, y resolverlo con la carátula de integrantes
(§3). Es menos elegante y es infinitamente más seguro.

<details>
<summary>Si igual querés la entrega grupal de verdad</summary>

Entonces el orden es este, y no se puede saltear ningún paso:

1. **Participantes → Grupos**: crear los grupos reales de la clase con sus integrantes.
2. **Agrupamientos**: crear un agrupamiento (p. ej. `Clase 1 – Ejercicios`) y meter adentro esos grupos.
3. En la tarea: `Entrega por grupos = Sí`, `Se requiere que todos los miembros del grupo entreguen = No`,
   y `Agrupamiento para los grupos = Clase 1 – Ejercicios`.
4. Verificar en **Ver todas las entregas** que la columna *Grupo* no diga «Grupo por defecto» para nadie.

El paso 4 no es opcional. Es el único que detecta el problema antes de que califiques.
</details>

---

## 5. Rúbrica de corrección (100 puntos)

Si usás **Calificación simple directa**, esta tabla es la guía; si usás **Rúbrica**, cargá un
criterio por fila.

| # | Criterio | Qué se mira | Puntos |
|---|---|---|---|
| 1 | **Parte A — V/F con justificación** | 2 puntos por ítem. El V/F solo, sin justificación, vale **0**. La justificación tiene que nombrar el mecanismo, no repetir la afirmación. | 20 |
| 2 | **Parte B — Opción múltiple** | 1 punto por ítem, respuesta correcta. Sin puntaje parcial. | 10 |
| 3 | **Parte C — Desarrollo conceptual** | 3 puntos por ítem: 3 si aparecen los conceptos clave con vocabulario técnico correcto; 1,5 si la idea está pero el vocabulario es impreciso; 0 si falta el concepto central. | 30 |
| 4 | **Parte D — Casos de diagnóstico** | 5 puntos por caso: 2 por el diagnóstico, 1 por la evidencia/comando, 1 por la corrección, 1 por **nombrar el concepto** del apunte que lo explica. | 30 |
| 5 | **Parte E — Lectura de salidas** | 4 + 3 + 3. Se corrige por sub-ítem: leer el `status`, las flags, quién respondió, el TTL remanente. | 10 |

**Criterios transversales** (no suman, pero orientan la devolución):

- Confundir **NXDOMAIN con timeout** en cualquier parte del trabajo es el error conceptual más
  caro del capítulo: marcalo aunque el ítem esté bien puntuado.
- Decir «hay que esperar a que propague» sin corregir la idea de que la propagación no existe
  como proceso: señalarlo siempre.
- El ítem **E1(iv)** (por qué el TTL dice `287` y no `300`) no está explícito en el apunte. No es
  para descontar: es para premiar al grupo que lo dedujo.

---

## 6. Después del cierre — publicar la clave

Una vez pasada la **fecha límite** (mié 19/08, 23:59) y no antes:

1. Subir `Clase 1 - Ejercicios de teoria - Respuestas.pdf` a la sección de la unidad, como
   recurso **Archivo**, con el nombre `Clase 1 – Ejercicios de teoría: clave de corrección`.
2. Agregarle esta descripción:

```html
<p style="font-family: sans-serif;">Clave de corrección con las respuestas desarrolladas. Cada
  una cierra con la sección del apunte donde se justifica, así que también funciona como índice
  de repaso: si un ítem te salió mal, tenés ahí exactamente qué releer.</p>
```

3. Calificar y **liberar las calificaciones todas juntas** (recordá que en §1 quedaron ocultas
   hasta publicarlas).

---

## 7. Checklist de alta

- [ ] `Clase 1 - Ejercicios de teoria.pdf` subido y adjunto en **Archivos adicionales**
- [ ] `Clase 1.pdf` (el apunte) visible en la sección
- [ ] Clave de corrección **NO** publicada
- [ ] Descripción e Instrucciones de la entrega pegadas **en modo HTML** (si se pegan en modo
      visual, el editor se come los estilos)
- [ ] Fechas cargadas y coherentes con el calendario de la comisión
- [ ] Puntuación máxima **100**, calificación para aprobar **60**
- [ ] `Entrega por grupos = No` (o los cuatro pasos de §4 hechos y verificados)
- [ ] Tipos de archivo restringidos
- [ ] Calificaciones ocultas hasta publicarlas
- [ ] Finalización de actividad: «debe entregar»
- [ ] Vista previa con un usuario de prueba: se ve el PDF adjunto y el botón de entrega

---

## Nota al margen: esto podría ser un Cuestionario

Las **Partes A y B** (V/F y opción múltiple, 30 de los 100 puntos) son autocorregibles. En un
**Cuestionario** de Moodle se corrigen solas, con retroalimentación automática por opción, y no
tocás una sola entrega.

Las partes C, D y E no: exigen desarrollo y no hay forma honesta de automatizarlas.

Si en algún momento querés partir la actividad en dos —un Cuestionario autocorregido para A y B,
y esta Tarea reducida a C, D y E—, se puede armar sin rehacer nada: el banco de preguntas ya está
escrito. Para esta clase, con una sola Tarea alcanza.
