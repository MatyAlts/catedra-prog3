# Alta del cuestionario autocorregido — Clase 1 (DNS y dominio propio)

> **Qué es este documento.** Los pasos para dar de alta el **Cuestionario** en el aula, a partir
> del banco `cuestionario-moodle-clase-1.xml`. No es material para el alumno.
> La clave con las respuestas está en `cuestionario-moodle-clase-1-respuestas.md`.

- **Campus:** `https://campustest.frm.utn.edu.ar`
- **Curso:** id **14** — DevOps
- **Sección destino:** **30** — «Actividades 🧩» (`sectionid=555`), junto a la Tarea de la
  Clase 1 (`cmid=1450`)
- **Banco a importar:** `cuestionario-moodle-clase-1.xml` — 31 preguntas
- **Composición:** 24 opción múltiple · 4 emparejamiento · 2 respuesta corta · 1 verdadero/falso

---

## 0. Por qué esto no se creó por API

Ya verificado para este campus: de las **437 funciones** de webservice habilitadas, las 18 de
`mod_quiz` son todas de lectura o de intentos de alumno, y la única de preguntas es
`core_question_update_flag`. **No hay forma de crear un cuestionario ni preguntas por API.**
El contenido —que es el trabajo real— va en el XML; la creación son tres clics.

---

## 1. Importar el banco

1. Ir a **https://campustest.frm.utn.edu.ar/question/bank/importquestions/import.php?courseid=14**
2. Formato: **Formato XML de Moodle**.
3. **«Obtener categoría del archivo» = Sí**. El XML crea sola la categoría
   `Clase 1 - DNS y dominio propio`.
4. Arrastrar el archivo → **Importar** → deben listarse las 31 preguntas.

> Si aparece «Archivo XML inválido - se esperaba una cadena (usar CDATA?)», el archivo tiene HTML
> crudo dentro de un `<text>`. Ver la sección equivalente en `cuestionario-moodle-clase-2.md`,
> que explica el diagnóstico y trae el script de verificación. **Este archivo ya está validado.**

## 2. Crear el cuestionario

Sección «Actividades 🧩» → *Añadir actividad* → **Cuestionario**.

- **Nombre:** `Clase 1 – Autoevaluación: DNS y dominio propio`
- **Descripción:** el bloque HTML de §4.

## 3. Cargar las preguntas

Pestaña **Preguntas** → *Agregar* → *del banco* → categoría `Clase 1 - DNS y dominio propio` →
las 31 → **Calificación máxima: 10**.

### 3.1. Paginación — qué va junto y qué va separado

Hay **tres pares** donde una pregunta contiene la respuesta de otra. En los tres casos la que
revela es de **emparejar u opción múltiple** —con las respuestas escritas en pantalla— y la
víctima es de **respuesta corta o conceptual**:

| Revela | A quién | Qué le regala |
|---|---|---|
| **C1-11** (emparejar niveles de autoridad) | **C1-10** (autoritativo vs. recursivo) | Su fila dice literalmente *«ningún dato propio: sabe recorrer la jerarquía»* |
| **C1-24** (bajar el TTL antes del cambio) | **C1-22** (respuesta corta: ¿qué TTL?) | El enunciado menciona **300 segundos** |
| **C1-18** (los dos registros del práctico) | **C1-28** (¿el comodín cubre el raíz?) | Una opción correcta dice *«el comodín no cubre el dominio raíz»* |

Un cuarto par se dejó sin blindar a propósito: **C1-13** (emparejar RCODEs) refuerza a **C1-12** y
**C1-14**, pero se resolvió con el **orden** —las dos víctimas van en la página anterior— en vez
de con distancia.

**Distribución en 11 páginas:**

| Pág | Bloque | Preguntas | Por qué |
|---|---|---|---|
| 1 | El origen del DNS | 01, 02, 03, 04 | HOSTS.TXT y las tres decisiones de 1983 |
| 2 | Del navegador al servidor | 05, 06, 07 | Log vacío, `Host`, SNI |
| 3 | La jerarquía de nombres | 08, 09, 10 | Zona, raíz, **autoritativo vs. recursivo** |
| 4 | Autoridad y respuestas | **11**, 12, 14 | El emparejar de niveles, ya después de C1-10 |
| 5 | Códigos e indicadores | **13**, 15 | El emparejar de RCODEs, después de sus víctimas |
| 6 | Tipos de registro | 16, 17 | CNAME en el vértice y CAA |
| 7 | Delegación | 19, 20, 21 | Dónde se cargan los registros |
| 8 | TTL y propagación | **22**, 23 | La respuesta corta del TTL **antes** de C1-24 |
| 9 | Caché | **24**, 25 | Bajar el TTL y la caché negativa |
| 10 | Filtrado y comodín | 26, 27, **28**, 29 | El alcance del comodín **antes** de C1-18 |
| 11 | Cierre: registros y verificación | **18**, 30, 31 | Qué cargar, «a mí me anda», DNSSEC/DoH |

**Por qué agrupar y no dejar 1 por página.** Con *retroalimentación inmediata* cada pregunta tiene
su propio botón «Comprobar»: el feedback llega igual esté sola o acompañada. Se pasa de 31 cargas
de página a 11 y los bloques se leen como una unidad.

> ⚠️ **No activar «Reordenar las preguntas al azar»** (`shufflequestions`): mezcla las preguntas
> entre páginas y tira abajo las tres protecciones de orden. El barajado **dentro** de cada
> pregunta ya viene en el XML y ese sí conviene dejarlo.

---

## 4. Descripción — pegar en «Descripción» (modo HTML)

```html
<div style="font-family: sans-serif; line-height: 1.6; color: #000000;">
  <p style="font-size: 1rem;">Autoevaluación de la teoría de la Clase 1. Son
    <strong>31 preguntas</strong> que se corrigen solas y que podés repetir las veces que
    quieras: la nota que queda es la más alta.</p>

  <p style="font-size: 1rem;">No es una prueba de memoria. Cada pregunta te dice
    <strong>por qué</strong> la opción que elegiste está bien o mal, y te remite a la sección
    exacta del apunte. Usalo como material de estudio, no solo como examen.</p>

  <div style="background-color: #f8edef; padding: 12px; border-radius: 6px; border-left: 4px solid #7B1E2B; margin: 16px 0;">
    <p style="margin: 0; color: #5c0120;">⏱️ <strong>Tiempo estimado:</strong> 25 a 35 minutos ·
      <strong>Intentos:</strong> ilimitados · <strong>Nota:</strong> la más alta</p>
  </div>

  <div style="margin-top: 16px; background-color: #fff4e5; padding: 12px; border-radius: 6px; border-left: 4px solid #d97706;">
    <p style="margin: 0;">⚠️ <strong>Antes de arrancar:</strong> tené abierto el apunte
      <strong>Clase 1.pdf</strong>. Cuando dudes, buscá la sección — encontrarla también es
      parte del ejercicio.</p>
  </div>

  <div style="margin-top: 12px; background-color: #fdecea; padding: 12px; border-radius: 6px; border-left: 4px solid #c0392b;">
    <p style="margin: 0;">🚩 <strong>Ojo con los códigos de respuesta.</strong> NXDOMAIN,
      NOERROR y un timeout <em>no</em> dicen lo mismo, y varias preguntas se apoyan justo en esa
      diferencia. Si te trabás, volvé a la sección 1.5.</p>
  </div>

  <div style="text-align: center; margin-top: 20px;">
    <p style="font-size: 1.05rem; color: #7b1e2b; font-weight: bold;">✨ El DNS no es una verdad
      universal: es lo que te dice el que te atiende</p>
  </div>
</div>
```

---

## 5. Configuración

| Campo | Valor | Por qué |
|---|---|---|
| Intentos permitidos | **Sin límite** | Es autoevaluación, no examen |
| Método de calificación | **Calificación más alta** | ídem |
| Preguntas por página | **Personalizado: 11 páginas** | Ver §3.1 |
| Barajar dentro de las preguntas | **Sí** | El XML ya lo trae |
| Límite de tiempo | **Sin límite** | Se resuelve con el apunte al lado |
| Calificación máxima | **10** | Consistente con el resto del curso |
| Comportamiento de las preguntas | **Retroalimentación inmediata** | Ver nota |
| Navegación | **Libre** | |
| Calificación para aprobar | **6** | |

> 🔑 **Retroalimentación inmediata, no diferida.** El curso usa diferida por convención, pero cada
> opción incorrecta de este banco tiene escrita **su propia explicación**. Con diferida, esa
> explicación llega cuando el alumno ya se desconectó del razonamiento; con inmediata la lee en el
> momento exacto en que se equivocó. Es la diferencia entre un examen y una herramienta de estudio.

---

## 6. Qué cubre y qué no

| Parte del cuadernillo | ¿Va al cuestionario? |
|---|---|
| A — Verdadero/falso con justificación | **Sí**, transformada (ver §7) |
| B — Opción múltiple | **Sí** |
| C — Desarrollo conceptual | No: exige redacción |
| D — Casos de diagnóstico | **Parcialmente**: D1, D2, D4, D5 y D6 se convirtieron en opción múltiple |
| E — Lectura de salidas | **Parcialmente**: los RCODE, el indicador `aa` y los NS por proveedor |

Cubre **20 secciones** del capítulo. El detalle sección por sección está en la clave.

**Las partes C, D y E completas siguen en la Tarea entregable.** El cuestionario no las
reemplaza: se corrigen solas las 31 conceptuales y a mano queda únicamente el desarrollo.

---

## 7. Nota de diseño: casi no hay verdadero/falso

En el cuadernillo impreso la Parte A son 10 verdadero/falso **con justificación obligatoria**. Esa
justificación es lo valioso, y es exactamente lo que una máquina no puede corregir.

Pasarlas a V/F puro regala **50 % de acierto por azar**. Lo que se hizo en cambio: **convertirlas
en opción múltiple donde las opciones son las justificaciones**. En vez de «¿verdadero o falso?»,
el ítem pregunta *por qué*, y los distractores son razonamientos equivocados pero plausibles.

Ejemplo, `C1-16`: en vez de «¿se puede usar CNAME en el vértice? V/F», el enunciado plantea a un
grupo que promete no cargar ningún otro registro. Un distractor es *«sí, mientras efectivamente no
cargue otros»* — que es lo que contesta quien memorizó la regla sin entenderla. Recibe: *«No
depende de su voluntad: NS y SOA existen en el vértice por definición de zona, no porque alguien
los cargue.»*

Quedó **un solo verdadero/falso** (`C1-28`, el alcance del comodín), donde la afirmación es tajante
y no admite matiz.

**Las 2 de respuesta corta no se adivinan:** piden escribir la ruta de `/etc/hosts` y el valor del
TTL en segundos. **Los 4 emparejamientos** cubren lo que en el cuadernillo eran enumeraciones: las
tres decisiones de 1983, los niveles de autoridad, los RCODE y los NS por proveedor.

---

## 8. Checklist

- [ ] XML importado con «Obtener categoría del archivo = Sí» → 31 preguntas en el banco
- [ ] Cuestionario creado en la sección «Actividades 🧩»
- [ ] Las 31 preguntas agregadas desde el banco
- [ ] Paginación de §3.1 aplicada (11 páginas) y **«Reordenar al azar» desactivado**
- [ ] Calificación máxima **10**, aprobación **6**
- [ ] Comportamiento: **retroalimentación inmediata**
- [ ] `Clase 1.pdf` visible en la sección (el cuestionario remite a sus secciones)
- [ ] **Vista previa con un intento propio**: verificar la retroalimentación por opción y que los
      emparejamientos barajen bien
- [ ] La clave (`cuestionario-moodle-clase-1-respuestas.md`) **no** subida al aula
