# Alta del cuestionario autocorregido — Clase 4 (El despliegue)

> **Qué es este documento.** Los pasos para dar de alta el **Cuestionario** en el aula, a partir
> del banco `cuestionario-moodle-clase-4.xml`. No es material para el alumno.
> La clave con las respuestas está en `cuestionario-moodle-clase-4-respuestas.md`.

- **Campus:** `https://campustest.frm.utn.edu.ar` · **Curso:** id **14** — DevOps
- **Sección destino:** **30** — «Actividades 🧩» (`sectionid=555`)
- **Banco:** `cuestionario-moodle-clase-4.xml` — 31 preguntas
- **Composición:** 26 opción múltiple · 3 emparejamiento · 1 respuesta corta · 1 verdadero/falso
- **Cobertura:** 29 secciones del capítulo 4 — la más alta de las cinco clases

---

## 1. Importar el banco

1. Ir a **https://campustest.frm.utn.edu.ar/question/bank/importquestions/import.php?courseid=14**
2. Formato: **Formato XML de Moodle**.
3. **«Obtener categoría del archivo» = Sí** → crea `Clase 4 - El despliegue`.
4. Arrastrar el archivo → **Importar** → deben listarse las 31 preguntas.

## 2. Crear el cuestionario

Sección «Actividades 🧩» → *Añadir actividad* → **Cuestionario**.

- **Nombre:** `Clase 4 – Autoevaluación: proxy inverso, certificados y CORS`
- **Descripción:** el bloque HTML de §4.

## 3. Cargar las preguntas

Pestaña **Preguntas** → *Agregar* → *del banco* → categoría `Clase 4 - El despliegue` → las 31 →
**Calificación máxima: 10**.

### 3.1. Paginación — qué va junto y qué va separado

Este banco tiene **dos emparejamientos que revelan** preguntas conceptuales, y en los dos casos la
solución fue poner la víctima **antes**:

| Revela | A quién | Qué le regala |
|---|---|---|
| **C4-11** (emparejar desafíos ACME) | **C4-12** (los dos requisitos del certificado) | Su fila dice *«HTTP-01: servir un archivo por el puerto 80»* |
| **C4-08** (emparejar el modelo de Traefik) | **C4-09** (404 contra 502) y **C4-10** (el puerto interno) | Nombra enrutador, servicio y *«el contenedor api, puerto 8000»* |

También se adelantó **C4-07** (la respuesta corta del Build path) al inicio de su página, para que
no se deduzca del contraste con la pregunta de polirepositorio.

**Distribución en 12 páginas:**

| Pág | Bloque | Preguntas | Por qué |
|---|---|---|---|
| 1 | Por qué existe el proxy inverso | 01, 02, 03, 04 | HTTP/1.0, SNI, proxy inverso, Traefik |
| 2 | Qué hace Easypanel | 05, 06 | Los tres componentes y el repositorio como fuente |
| 3 | Repositorios y construcción | **07**, 28, 29 | La respuesta corta **primero** |
| 4 | Cómo decide Traefik | **09, 10** | 404/502 y el puerto interno, **antes** del emparejar |
| 5 | El modelo de enrutamiento | **08** | El emparejamiento, solo, ya después |
| 6 | Certificados: el protocolo ACME | **12**, 26 | Los dos requisitos, **antes** del emparejar |
| 7 | Los desafíos de ACME | **11**, 31 | El emparejamiento de desafíos |
| 8 | El frontend y su variable | 13, 25 | `API_URL` y el error hacia 127.0.0.1 |
| 9 | Orígenes | 14, 15, 16 | Qué es un origen, por qué la política, quién autoriza |
| 10 | La verificación previa | 17, 18 | El preflight y qué cuenta como origen distinto |
| 11 | Qué protege CORS y qué no | 19, 20, 21, 30 | El bloque central del capítulo |
| 12 | Evolución y diagnóstico | 22, 23, 24, 27 | HSTS, HTTP/3, Mixed Content, cómo diagnosticar |

Las páginas 4 y 5 parecen desbalanceadas —dos preguntas y después una sola— y es a propósito:
`C4-08` es el emparejamiento que nombra las cuatro piezas del modelo, y ponerlo junto a `C4-09`
convertiría «404 contra 502» en un ejercicio de lectura.

> ⚠️ **No activar «Reordenar las preguntas al azar»**: mezcla las preguntas entre páginas y tira
> abajo las protecciones de orden. El barajado **dentro** de cada pregunta ya viene en el XML.

---

## 4. Descripción — pegar en «Descripción» (modo HTML)

```html
<div style="font-family: sans-serif; line-height: 1.6; color: #000000;">
  <p style="font-size: 1rem;">Autoevaluación de la teoría de la Clase 4. Son
    <strong>31 preguntas</strong> que se corrigen solas y que podés repetir las veces que
    quieras: la nota que queda es la más alta.</p>

  <p style="font-size: 1rem;">Esta clase reúne todo lo anterior: el dominio de la Clase 1, el
    servidor de la Clase 2 y las imágenes de la Clase 3. Varias preguntas se apoyan en esas
    clases, así que si algo no te cierra, la respuesta puede estar más atrás.</p>

  <div style="background-color: #f8edef; padding: 12px; border-radius: 6px; border-left: 4px solid #7B1E2B; margin: 16px 0;">
    <p style="margin: 0; color: #5c0120;">⏱️ <strong>Tiempo estimado:</strong> 25 a 35 minutos ·
      <strong>Intentos:</strong> ilimitados · <strong>Nota:</strong> la más alta</p>
  </div>

  <div style="margin-top: 16px; background-color: #fff4e5; padding: 12px; border-radius: 6px; border-left: 4px solid #d97706;">
    <p style="margin: 0;">⚠️ <strong>Antes de arrancar:</strong> tené abierto el apunte
      <strong>Clase 4.pdf</strong> y el <strong>README.md</strong> del proyecto, en particular la
      sección sobre CORS.</p>
  </div>

  <div style="margin-top: 12px; background-color: #fdecea; padding: 12px; border-radius: 6px; border-left: 4px solid #c0392b;">
    <p style="margin: 0;">🚩 <strong>Lo que más se pierde:</strong> creer que CORS protege la API.
      No la protege: es una política que aplica <em>el navegador</em> a favor del usuario. Un
      <code>curl</code> la ignora por completo, y varias preguntas se apoyan en esa diferencia.</p>
  </div>

  <div style="text-align: center; margin-top: 20px;">
    <p style="font-size: 1.05rem; color: #7b1e2b; font-weight: bold;">✨ Un 502 parece un problema
      del servidor y es un número mal puesto en un formulario</p>
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

> 🔑 **Retroalimentación inmediata, no diferida.** Cada opción incorrecta tiene escrita su propia
> explicación. Con diferida llega cuando el alumno ya se desconectó del razonamiento.

---

## 6. Qué cubre y qué no

Cubre **29 secciones** del capítulo, la cobertura más alta de las cinco clases — porque el capítulo
es también el más largo y el que más piezas reúne. El detalle sección por sección está en la clave.

El bloque de **CORS** concentra siete preguntas (14 a 21, más la 30), y es a propósito: es donde el
capítulo dice que están casi todos los fallos, y donde el malentendido —«CORS protege la API»—
sobrevive con más facilidad a una lectura rápida.

**El desarrollo sigue en la Tarea entregable.**

---

## 7. Nota de diseño

Este banco tiene **una sola respuesta corta** y **un solo verdadero/falso**, muchos menos que los
demás. La razón es el material: el capítulo 4 casi no tiene datos memorizables —no hay puertos
que recordar ni comandos exactos— y en cambio está lleno de **distinciones finas** que se evalúan
mejor eligiendo entre razonamientos.

Los casos más claros:

- **C4-09** (404 contra 502) tiene como distractor el significado *genérico* de esos códigos en
  HTTP. Es correcto en general y equivocado acá: los emite Traefik y señalan etapas de su cadena.
- **C4-19** (V/F: «CORS protege la API») es el único verdadero/falso, y está ahí porque la
  afirmación es tajante y el capítulo la enuncia «sin rodeos».
- **C4-20** describe la escena donde el log dice 200 y el frontend dice que falló, y la respuesta
  correcta es que **los dos tienen razón**. Ese ítem mide comprensión, no memoria.

La única respuesta corta, **C4-07**, pide escribir el Build path. Vale la pena que sea corta y no
múltiple: el error real en clase es escribir `/backend`, y el mensaje que devuelve Docker no
menciona el Build path por ningún lado.

---

## 8. Checklist

- [ ] XML importado con «Obtener categoría del archivo = Sí» → 31 preguntas
- [ ] Cuestionario creado en la sección «Actividades 🧩»
- [ ] Las 31 preguntas agregadas desde el banco
- [ ] Paginación de §3.1 aplicada (12 páginas) y **«Reordenar al azar» desactivado**
- [ ] Verificado que la página 5 tenga **solo** `C4-08`
- [ ] Calificación máxima **10**, aprobación **6**
- [ ] Comportamiento: **retroalimentación inmediata**
- [ ] `Clase 4.pdf` visible en la sección
- [ ] **Vista previa con un intento propio**
- [ ] La clave (`cuestionario-moodle-clase-4-respuestas.md`) **no** subida al aula
