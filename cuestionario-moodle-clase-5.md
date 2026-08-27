# Alta del cuestionario autocorregido — Clase 5 (Red interna y prácticas de desarrollo)

> **Qué es este documento.** Los pasos para dar de alta el **Cuestionario** en el aula, a partir
> del banco `cuestionario-moodle-clase-5.xml`. No es material para el alumno.
> La clave con las respuestas está en `cuestionario-moodle-clase-5-respuestas.md`.

- **Campus:** `https://campustest.frm.utn.edu.ar` · **Curso:** id **14** — DevOps
- **Sección destino:** **30** — «Actividades 🧩» (`sectionid=555`)
- **Banco:** `cuestionario-moodle-clase-5.xml` — 31 preguntas
- **Composición:** 27 opción múltiple · 2 emparejamiento · 1 respuesta corta · 1 verdadero/falso
- **Cobertura:** 25 secciones del capítulo 5

---

## 1. Importar el banco

1. Ir a **https://campustest.frm.utn.edu.ar/question/bank/importquestions/import.php?courseid=14**
2. Formato: **Formato XML de Moodle**.
3. **«Obtener categoría del archivo» = Sí** → crea
   `Clase 5 - Red interna y practicas de desarrollo`.
4. Arrastrar el archivo → **Importar** → deben listarse las 31 preguntas.

## 2. Crear el cuestionario

Sección «Actividades 🧩» → *Añadir actividad* → **Cuestionario**.

- **Nombre:** `Clase 5 – Autoevaluación: red interna, persistencia e integración continua`
- **Descripción:** el bloque HTML de §4.

## 3. Cargar las preguntas

Pestaña **Preguntas** → *Agregar* → *del banco* → categoría
`Clase 5 - Red interna y practicas de desarrollo` → las 31 → **Calificación máxima: 10**.

### 3.1. Paginación — qué va junto y qué va separado

Este banco tiene **la filtración más difícil de ver de las cinco clases**, y conviene dejarla
documentada porque no se detecta buscando texto repetido.

El emparejamiento **C5-02** (las tres decisiones del modelo de red) contiene esta fila:

> *«Publicar un puerto es opcional y ortogonal → La comunicación entre contenedores de una red no
> requiere publicar nada»*

Y el verdadero/falso **C5-31** pregunta si el servicio `db` tiene que publicar el 5432 para que la
API se conecte. **Es la misma afirmación con otras palabras.** No comparten ni una frase, así que
una búsqueda literal no la encuentra: se detecta leyendo.

La misma fila **también** revela a **C5-06** (qué convierte a la red interna en un mecanismo de
seguridad), porque nombra el «límite de alcance».

| Revela | A quién | Qué le regala |
|---|---|---|
| **C5-02** (emparejar las tres decisiones) | **C5-31** (V/F: ¿hay que publicar el 5432?) | *«no requiere publicar nada»*, dicho de otro modo |
| **C5-02** | **C5-06** (qué la vuelve un mecanismo de seguridad) | *«límite de alcance: una frontera de seguridad»* |
| **C5-08** (la cadena de conexión) | **C5-03** (respuesta corta: el nombre interno) | El enunciado muestra `calculadora_db` entero |

**La corrección:** `C5-02` se movió de la página 1 a la **página 4**, después de sus dos víctimas.

**Distribución en 13 páginas:**

| Pág | Bloque | Preguntas | Por qué |
|---|---|---|---|
| 1 | Por qué existe la red interna | 01, **06** | El problema, y qué la vuelve seguridad |
| 2 | Quién ejecuta el código | 04, 05 | La pregunta que ordena todo el capítulo |
| 3 | Publicar y comunicar | **31**, **03** | El V/F y la respuesta corta, **antes** del emparejar |
| 4 | Las decisiones de diseño | **02** | El emparejamiento, solo, ya después |
| 5 | La base de datos | 07, 08 | Configuración del servicio y cadena de conexión |
| 6 | Degradación elegante | 09, 10, 11, 12 | El patrón, el 503, el health check, el criterio |
| 7 | Inyección SQL | 13 | Sola: es el ítem de seguridad del capítulo |
| 8 | La verificación del aislamiento | 14 | Sola: es *la* comprobación de la clase |
| 9 | Estado y persistencia | 15, 16 | Volúmenes y servicios con/sin estado |
| 10 | Prácticas de repositorio | 17, 18, 19 | Secretos, los dos ignore, dependencias |
| 11 | Integración continua | 20, 21, 22, 23 | Por qué, informar vs bloquear, CD, el orden |
| 12 | Lo que falta | 24, 30 | Copias de seguridad y el patrón que se repite |
| 13 | Diagnóstico | 25, 26, 27, 28, 29 | La tabla de errores frecuentes |

Las páginas 7 y 8 tienen **una sola pregunta** cada una, y es deliberado: `C5-13` (consultas
parametrizadas) y `C5-14` (el aislamiento verificado desde afuera) son las dos que el capítulo
señala como centrales, y darles su propia pantalla las separa del ruido.

> ⚠️ **No activar «Reordenar las preguntas al azar»**: mezcla las preguntas entre páginas y tira
> abajo las protecciones de orden. El barajado **dentro** de cada pregunta ya viene en el XML.

---

## 4. Descripción — pegar en «Descripción» (modo HTML)

```html
<div style="font-family: sans-serif; line-height: 1.6; color: #000000;">
  <p style="font-size: 1rem;">Autoevaluación de la teoría de la Clase 5, la que cierra la unidad.
    Son <strong>31 preguntas</strong> que se corrigen solas y que podés repetir las veces que
    quieras: la nota que queda es la más alta.</p>

  <p style="font-size: 1rem;">Varias preguntas cierran círculos abiertos en clases anteriores: el
    firewall de la Clase 2, las capas de la Clase 3, el proxy de la Clase 4. Si una respuesta te
    suena conocida, probablemente lo sea.</p>

  <div style="background-color: #f8edef; padding: 12px; border-radius: 6px; border-left: 4px solid #7B1E2B; margin: 16px 0;">
    <p style="margin: 0; color: #5c0120;">⏱️ <strong>Tiempo estimado:</strong> 25 a 35 minutos ·
      <strong>Intentos:</strong> ilimitados · <strong>Nota:</strong> la más alta</p>
  </div>

  <div style="margin-top: 16px; background-color: #fff4e5; padding: 12px; border-radius: 6px; border-left: 4px solid #d97706;">
    <p style="margin: 0;">⚠️ <strong>Antes de arrancar:</strong> tené abierto el apunte
      <strong>Clase 5.pdf</strong>. Y tené a mano la pregunta que ordena todo el capítulo:
      <strong>¿quién ejecuta este código?</strong></p>
  </div>

  <div style="margin-top: 12px; background-color: #fdecea; padding: 12px; border-radius: 6px; border-left: 4px solid #c0392b;">
    <p style="margin: 0;">🚩 <strong>Lo que más se pierde:</strong> confundir <em>publicar un
      puerto</em> con <em>comunicarse por la red interna</em>. Son dos mecanismos distintos y
      ortogonales, y de esa confusión salen la mitad de las bases de datos expuestas a internet
      del mundo.</p>
  </div>

  <div style="text-align: center; margin-top: 20px;">
    <p style="font-size: 1.05rem; color: #7b1e2b; font-weight: bold;">✨ El puerto más seguro es el
      que nunca se publicó</p>
  </div>
</div>
```

---

## 5. Configuración

| Campo | Valor | Por qué |
|---|---|---|
| Intentos permitidos | **Sin límite** | Es autoevaluación, no examen |
| Método de calificación | **Calificación más alta** | ídem |
| Preguntas por página | **Personalizado: 13 páginas** | Ver §3.1 |
| Barajar dentro de las preguntas | **Sí** | El XML ya lo trae |
| Límite de tiempo | **Sin límite** | Se resuelve con el apunte al lado |
| Calificación máxima | **10** | Consistente con el resto del curso |
| Comportamiento de las preguntas | **Retroalimentación inmediata** | Ver nota |
| Navegación | **Libre** | |
| Calificación para aprobar | **6** | |

> 🔑 **Retroalimentación inmediata, no diferida.** Cada opción incorrecta tiene escrita su propia
> explicación. Con diferida llega cuando el alumno ya se desconectó del razonamiento.

**Disponibilidad:** como es la última clase de la unidad, conviene **no ponerle fecha de cierre**.
Es el repaso natural antes del parcial.

---

## 6. Qué cubre y qué no

Cubre **25 secciones** del capítulo. El detalle sección por sección está en la clave.

Este banco es el más «transversal» de los cinco: `C5-06` remite al firewall de §2.8, `C5-15` al
modelo de capas de §3.3.2, `C5-07` al enrutamiento de §4.8.1 y a la traducción de direcciones de
§2.8.1, y `C5-30` pide reconocer explícitamente el patrón que comparten el DNS de la Clase 1 y el
DNS embebido de Docker.

**El desarrollo sigue en la Tarea entregable.**

---

## 7. Nota de diseño

La estructura de este banco sigue el arco del capítulo, que va de lo técnico a lo profesional:

- **Preguntas 1 a 8** — el modelo de red y por qué el frontend no puede usarla.
- **9 a 13** — decisiones de diseño: degradación elegante, códigos de estado que dicen la verdad,
  health checks útiles, inyección SQL.
- **14 a 16** — la verificación y el estado.
- **17 a 24** — prácticas: secretos, ramas, integración continua, lo que falta.
- **25 a 31** — diagnóstico y síntesis.

Ese último tramo es el que suele quedar afuera de los cuestionarios técnicos, y es justamente el
que separa «hacer andar un despliegue» de «operar un servicio». `C5-21` (informar contra bloquear)
y `C5-23` (integración continua **antes** que despliegue automático) no son preguntas sobre
herramientas: son preguntas sobre criterio.

La única respuesta corta, **C5-03**, pide escribir `calculadora_db`. Parece trivial y no lo es:
mide si entendieron el formato `proyecto_servicio` **y** que ese nombre solo existe dentro de esa
red. Quien contesta `db.tudominio.com` o una IP no entendió el capítulo.

---

## 8. Checklist

- [ ] XML importado con «Obtener categoría del archivo = Sí» → 31 preguntas
- [ ] Cuestionario creado en la sección «Actividades 🧩»
- [ ] Las 31 preguntas agregadas desde el banco
- [ ] Paginación de §3.1 aplicada (13 páginas) y **«Reordenar al azar» desactivado**
- [ ] Verificado que `C5-02` quede en la **página 4**, no antes
- [ ] Verificado que las páginas 7 y 8 tengan **una sola pregunta** cada una
- [ ] Calificación máxima **10**, aprobación **6**
- [ ] Comportamiento: **retroalimentación inmediata**
- [ ] Sin fecha de cierre (sirve de repaso para el parcial)
- [ ] `Clase 5.pdf` visible en la sección
- [ ] **Vista previa con un intento propio**
- [ ] La clave (`cuestionario-moodle-clase-5-respuestas.md`) **no** subida al aula
