# Alta del cuestionario autocorregido — Clase 2 (VPS, puertos y firewall)

> **Qué es este documento.** Los pasos para dar de alta el **Cuestionario** en el aula, a partir
> del banco de preguntas `cuestionario-moodle-clase-2.xml` que acompaña este archivo.
> No es material para el alumno.

- **Campus:** `https://campustest.frm.utn.edu.ar`
- **Curso:** id **14** — DevOps
- **Sección destino:** **30** — «Actividades 🧩» (`sectionid=555`), la misma donde ya vive
  la Tarea de la Clase 1 (`cmid=1450`)
- **Banco a importar:** `cuestionario-moodle-clase-2.xml` — 31 preguntas, 67 KB
- **Verificado en vivo:** Moodle **4.5.12+** (build 20260722), token de webservices válido

---

## 0. Por qué esto no se creó por API

Se consultaron las **437 funciones** habilitadas para el token. Las 18 de `mod_quiz` son
**todas de lectura o de intentos de alumno** (`get_quizzes_by_courses`, `start_attempt`,
`process_attempt`, `get_attempt_review`…). No existe —ni en Moodle core ni como plugin
instalado en este campus— ninguna función que permita:

- crear una instancia de cuestionario en un curso,
- crear preguntas en el banco,
- asociar preguntas a un cuestionario.

La única función de preguntas disponible es `core_question_update_flag`, que marca una
pregunta como destacada durante un intento.

**Conclusión:** el contenido —que es el trabajo real— va en el XML. La creación del
cuestionario son tres clics manuales, una sola vez.

---

## 1. Importar el banco de preguntas

1. Ir a **https://campustest.frm.utn.edu.ar/question/bank/importquestions/import.php?courseid=14**
   (o: curso → *Más* → *Banco de preguntas* → desplegable → **Importar**).
2. Formato de archivo: **Formato XML de Moodle**.
3. En *General*, dejar **«Obtener categoría del archivo» = Sí**. El XML trae su propia
   categoría y la crea sola: `Clase 2 - VPS, puertos y firewall`.
4. Arrastrar `cuestionario-moodle-clase-2.xml` y pulsar **Importar**.
5. Moodle lista las 31 preguntas importadas. **Continuar**.

> Si el import falla, casi siempre es porque se eligió otro formato (GIFT, Aiken). El archivo
> es XML de Moodle; ningún otro formato lo va a leer.

### Si aparece «Archivo XML inválido - se esperaba una cadena (usar CDATA?)»

Es el error más común al generar XML de Moodle a mano, y **no es un problema del archivo que
subiste sino de cómo se generó**. Moodle parsea con `xmlize` y luego espera que todo elemento
`<text>` contenga una **cadena**, no elementos. Si un `<text>` lleva HTML crudo —por ejemplo
`<code>ufw default deny incoming</code>`— el parser ve un nodo hijo donde esperaba texto y
aborta.

La regla: **todo `<text>` que contenga HTML tiene que ir envuelto en `<![CDATA[ ... ]]>`.**
Es fácil olvidarlo en los `<answer>` de las preguntas de emparejamiento, porque el lado
izquierdo (`<subquestion><text>`) y el derecho (`<answer><text>`) se escriben en líneas
distintas.

Detalle importante: como «Detenerse en error» viene en **Sí** por defecto, **una sola**
pregunta mal formada aborta la importación completa. El mensaje dice «Importando 31 preguntas»
y acto seguido «No se han importado las preguntas»: las contó, pero no guardó ninguna.

Antes de subir, el archivo se puede verificar así — si imprime algo, hay `<text>` con HTML sin
CDATA:

```python
# verificar_xml.py  -- si imprime algo, esa pregunta rompe el import
import xml.etree.ElementTree as ET
raiz = ET.parse("cuestionario-moodle-clase-2.xml").getroot()
for q in raiz.findall("question"):
    if any(list(txt) for txt in q.iter("text")):
        print("HTML sin CDATA en:", q.find("name/text").text)
```

*(Corregido el 17/08/2026: la pregunta `C2-30` tenía `<code>` sin CDATA en un emparejamiento.
El archivo actual ya está validado.)*

---

## 2. Crear el cuestionario

1. Activar **Modo de edición** en el curso.
2. En la sección **«Actividades 🧩»** → *Añadir una actividad o un recurso* → **Cuestionario**.
3. **Nombre:** `Clase 2 – Autoevaluación: la VPS, puertos y firewall`
4. **Descripción:** el bloque HTML de §4.
5. Guardar y regresar al curso.

## 3. Cargar las preguntas en el cuestionario

1. Entrar al cuestionario → pestaña **Preguntas**.
2. **Agregar** → *del banco de preguntas* → categoría `Clase 2 - VPS, puertos y firewall`.
3. Seleccionar las 31 y **Añadir preguntas seleccionadas**.
4. **Calificación máxima: 10** (arriba a la derecha) y **Guardar**. Moodle escala los 31
   puntos brutos a 10 automáticamente.

> Orden: el XML las nombra `C2-01` … `C2-31` para que queden en orden temático al ordenar por
> nombre. Ese **no** es el orden final: ver §3.1.

### 3.1. Paginación — qué va junto y qué va separado

La paginación decide qué preguntas se ven **en la misma pantalla**. En este banco hay tres
pares donde una revela la respuesta de otra, y hay que separarlos:

| Revela | A quién | Qué le regala |
|---|---|---|
| **C2-14** (emparejar rangos IANA) | **C2-13** (¿puerto más alto?) | La fila «49152 – **65535**» está a la vista |
| **C2-20** (por qué Docker esquiva ufw) | **C2-18** y **C2-19** (respuesta corta: ¿qué cadena?) | Su opción correcta dice literalmente *FORWARD* e *INPUT* |
| **C2-30** (emparejar principios) | **C2-31** (¿qué violaban Redis y MongoDB?) | Una fila es «Valores predeterminados seguros» |

En los tres casos la que revela es de **emparejar u opción múltiple** —con las respuestas
escritas en pantalla— y la víctima es de **respuesta corta o conceptual**.

**Distribución en 10 páginas:**

| Pág | Bloque | Preguntas | Por qué |
|---|---|---|---|
| 1 | Virtualización y el VPS | 01, 02, 03, 04 | Independientes entre sí |
| 2 | SSH: el protocolo | 05, 06, 08 | Capas, TOFU y directiva |
| 3 | SSH: las claves | 07, 09, 10 | Mecanismo → consecuencia → algoritmo |
| 4 | Puertos y sockets | **13**, 11, 12, 15 | El 65535 **antes** del emparejar |
| 5 | Rangos y herramientas | **14**, 16 | Acá recién el emparejar de rangos |
| 6 | El recorrido del paquete | **18, 19** | Las dos de respuesta corta, **solas** |
| 7 | netfilter y Docker | **17, 20**, 21, 22 | El emparejar y la explicación, después |
| 8 | Firewall y exposición | 23, 24, 25, 26 | Se refuerzan sin filtrarse |
| 9 | Riesgos y endurecimiento | 27, 28, 29, **31** | 31 antes del emparejar de principios |
| 10 | Síntesis: los principios | **30** | Sola: es el cierre que integra todo |

**Por qué agrupar y no dejar 1 por página.** Con *retroalimentación inmediata* cada pregunta
tiene su propio botón «Comprobar»: el feedback llega igual esté sola o acompañada. No se pierde
nada y se pasa de 31 cargas de página a 10, con los bloques leyéndose como una unidad.

**Qué NO se blindó, y a propósito.** La retroalimentación de C2-07 menciona
`authorized_keys` y adelanta parte de C2-09. Se dejó así: esto es una autoevaluación con
intentos ilimitados, no un parcial. Que el feedback de una pregunta ilumine la siguiente es
**andamiaje**, no fuga. Solo se separaron los tres casos donde la respuesta aparece literal en
pantalla sin haber entendido nada. *Si alguna vez se usa este banco como parcial, hay que
separar más agresivo y sacar los emparejamientos, que son los que más revelan.*

> ⚠️ **No activar «Reordenar las preguntas al azar»** (`shufflequestions`): mezcla las preguntas
> entre páginas y tira abajo las tres protecciones de orden. El barajado **dentro** de cada
> pregunta ya viene en el XML y ese sí conviene dejarlo.

**Cómo aplicarlo:** pestaña *Preguntas* → *Seleccionar todo* → **Repaginar** con «1 pregunta por
página» → reordenar arrastrando según la tabla → eliminar los saltos de página sobrantes con el
icono de salto → **Vista previa** y verificar que la página 6 muestre solo las dos de respuesta
corta.

---

## 4. Descripción — pegar en el campo «Descripción» (modo HTML)

```html
<div style="font-family: sans-serif; line-height: 1.6; color: #000000;">
  <p style="font-size: 1rem;">Autoevaluación de la teoría de la Clase 2. Son
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
      <strong>Clase 2.pdf</strong>. Cuando dudes, buscá la sección — encontrarla también es
      parte del ejercicio.</p>
  </div>

  <div style="margin-top: 12px; background-color: #fdecea; padding: 12px; border-radius: 6px; border-left: 4px solid #c0392b;">
    <p style="margin: 0;">🚩 <strong>Ojo con las de emparejar y las de respuesta corta:</strong>
      no se adivinan. Si te trabás en el recorrido del paquete por netfilter, volvé a la
      sección 2.7.1 y mirá el esquema antes de seguir.</p>
  </div>

  <div style="text-align: center; margin-top: 20px;">
    <p style="font-size: 1.05rem; color: #7b1e2b; font-weight: bold;">✨ El puerto más seguro
      es el que nunca se publicó</p>
  </div>
</div>
```

---

## 5. Configuración del cuestionario

La columna «Convención del curso» es lo que ya usa la *Autoevaluación de POO* (`cmid=1447`),
relevada del campus.

| Campo | Convención del curso | Recomendado acá | Por qué |
|---|---|---|---|
| Intentos permitidos | Sin límite | **Sin límite** | Es autoevaluación, no examen |
| Método de calificación | Calificación más alta | **Calificación más alta** | ídem |
| Preguntas por página | 1 | **Personalizado: 10 páginas** | Ver §3.1 |
| Barajar dentro de las preguntas | Sí | **Sí** | El XML ya trae `shuffleanswers` |
| Límite de tiempo | Sin límite | **Sin límite** | Se resuelve con el apunte al lado |
| Calificación máxima | 10 | **10** | Consistente con el resto del curso |
| **Comportamiento de las preguntas** | Retroalimentación diferida | **Retroalimentación inmediata** | Ver abajo |
| Navegación | Libre | **Libre** | |
| Calificación para aprobar | — | **6** | |

> 🔑 **El único cambio que te propongo respecto de la convención.** El curso usa
> *retroalimentación diferida*: el alumno responde las 31 y recién al final ve algo.
> Poné **retroalimentación inmediata**.
>
> El motivo es concreto: cada opción incorrecta de este banco tiene escrita **su propia
> explicación** de por qué está mal. Con retroalimentación diferida esa explicación llega
> cuando el alumno ya se desconectó del razonamiento; con retroalimentación inmediata la lee
> en el momento exacto en que acaba de equivocarse, que es cuando sirve. Es la diferencia
> entre un examen y una herramienta de estudio.
>
> Si preferís mantener la convención del curso, no rompe nada — solo desperdicia la mitad
> del trabajo que hay adentro del XML.

**Disponibilidad:** abrir al inicio de la clase. No conviene ponerle fecha de cierre: sirve
para repasar antes del parcial.

---

## 6. Qué cubre y qué no

| Parte del cuadernillo | ¿Va al cuestionario? |
|---|---|
| A — Verdadero/falso con justificación | **Sí**, transformada (ver §7) |
| B — Opción múltiple | **Sí** |
| C — Desarrollo conceptual | No: exige redacción |
| D — Casos de diagnóstico | **Parcialmente**: D1, D5 y D6 se convirtieron en opción múltiple |
| E — Lectura de salidas | **Parcialmente**: los rangos IANA y el contraste ufw/nmap |

**Las partes C, D y E completas siguen viviendo en la Tarea entregable.** El cuestionario no
las reemplaza: se corrigen solas las 31 preguntas conceptuales, y a mano queda únicamente el
desarrollo — que es lo único que realmente necesita ojo humano.

Composición del banco: 20 de opción múltiple · 5 de verdadero/falso · 3 de emparejamiento ·
3 de respuesta corta.

---

## 7. Nota de diseño: por qué casi no hay verdadero/falso

En el cuadernillo impreso, la Parte A son 10 verdadero/falso **con justificación obligatoria**.
Esa justificación es lo que hace valiosa la pregunta, y es exactamente lo que una máquina no
puede corregir.

Pasarlas a V/F puro habría sido lo fácil, y habría sido un error: regala **50 % de acierto por
azar** y mide memoria en vez de comprensión.

Lo que se hizo en cambio: **convertirlas en opción múltiple donde las opciones son las
justificaciones**. En vez de preguntar «¿verdadero o falso?», el ítem pregunta *por qué*, y los
tres distractores son razonamientos equivocados pero plausibles — de los que efectivamente
aparecen en clase.

Ejemplo, `C2-20`: en vez de «¿Docker se saltea ufw? V/F», la pregunta describe el síntoma real
(ufw dice cerrado, nmap dice abierto) y pide elegir la explicación. Uno de los distractores es
«la regla quedó mal escrita y hay que recargarla», que es la primera reacción de cualquiera.
Quien la elige recibe: *«La regla está perfectamente escrita: `ufw status` la muestra. El
problema es que esa regla no se evalúa nunca para ese tráfico.»*

Quedaron **5 verdadero/falso**, solo donde la afirmación es tajante y no admite matiz. En esos
casos la retroalimentación general desarrolla el porqué completo, así que el 50 % de azar se
paga con una explicación que el alumno igual tiene que leer.

**Los 3 de respuesta corta no se adivinan:** piden escribir el nombre de la cadena de netfilter
(`FORWARD`, `INPUT`) y el puerto máximo. O sabés el recorrido del paquete o no contestás.

---

## 8. Checklist

- [ ] XML importado con «Obtener categoría del archivo = Sí» → 31 preguntas en el banco
- [ ] Cuestionario creado en la sección «Actividades 🧩»
- [ ] Las 31 preguntas agregadas desde el banco
- [ ] Paginación de §3.1 aplicada (10 páginas) y **«Reordenar al azar» desactivado**
- [ ] Calificación máxima **10**, aprobación **6**
- [ ] Comportamiento: **retroalimentación inmediata**
- [ ] Intentos: sin límite · Método: calificación más alta
- [ ] `Clase 2.pdf` visible en la sección (el cuestionario remite a sus secciones)
- [ ] **Vista previa con un intento propio**: verificar que se vea la retroalimentación por
      opción y que las de emparejamiento barajen bien
- [ ] La Tarea entregable de la Clase 2 (partes C, D y E) dada de alta por separado
