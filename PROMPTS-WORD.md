# Prompts para armar los documentos en Word

Instrucciones listas para copiar y pegar en el panel de **Claude for Word**, con la
versión final del Capítulo 1 (`Clase_1_DNS_unidad_ampliada.docx`) como patrón de formato.

## Plan de armado

**Seis documentos separados, no uno solo.** Un documento de 20 horas de contenido en un
único archivo es inmanejable en Word: se vuelve lento, la numeración se desincroniza y
cualquier error obliga a rehacer mucho.

| # | Documento | Archivo fuente |
|---|---|---|
| 0 | Tarea previa — GitHub Student Pack | `00-tarea-previa-student-pack.md` |
| 1 | Clase 1 — DNS y dominio | `01-dns-y-dominio.md` |
| 2 | Clase 2 — VPS, puertos y seguridad | `02-vps-puertos-y-seguridad.md` |
| 3 | Clase 3 — Docker | `03-docker.md` |
| 4 | Clase 4 — El despliegue | `04-deploy-easypanel.md` |
| 5 | Clase 5 — Red interna y DevOps | `05-red-interna-y-devops.md` |

Para cada uno: **abrir `Clase_1_DNS_unidad_ampliada.docx`**, Guardar como con el nombre del
documento nuevo, **borrarle el cuerpo sin tocar el encabezado ni el pie**, correr el
PROMPT 1 una vez y después el PROMPT 2 con el `.md` correspondiente.

> **⚠️ OJO ACÁ**
> El documento 1 ya está terminado y es el patrón: **no lo regeneres.** Duplicalo. Los otros
> cinco salen de esa copia, y así el formato es idéntico por construcción en vez de por
> descripción.

---

# El estándar: qué es una "unidad de estudio"

La Dirección revisó la Clase 1 y devolvió una versión ampliada que fijó el estándar del
material. **No es un apunte de clase: es una unidad de estudio.** El alumno tiene que
poder leerla sola, sin haber estado en el aula, y salir entendiendo *por qué* el sistema
funciona como funciona —no solo qué botón apretar.

El cambio de fondo es de género. Un instructivo enumera pasos. Una unidad de estudio
**funda cada paso en el concepto que lo explica**, y cada concepto en la decisión de
diseño que lo originó. El resultado es aproximadamente el doble de extensión, y esa
extensión no es relleno: es la capa de fundamento que antes faltaba.

## Los nueve rasgos del patrón

Estos son los rasgos que la Dirección incorporó. Todo capítulo del material tiene que
tenerlos.

**1. Subtítulo de unidad.** Debajo del título del capítulo, en cursiva:
*Unidad de estudio · Edición ampliada con fundamentos teóricos*.

**2. Índice de contenidos al inicio.** Una lista numerada, dentro de la sección de
alcance, enumerando los temas del capítulo. Entre 10 y 13 puntos.

**3. Una sección de génesis, antes de todo procedimiento.** La sección `N.2` explica
**por qué existe** la tecnología: qué problema concreto vino a resolver, qué se usaba
antes y por qué colapsó, quién la propuso, en qué año y bajo qué norma. Cierra
enunciando las **decisiones de diseño** que explican todo el comportamiento observable
en el resto del capítulo.

**4. Formalización del modelo.** Antes de operar, se define el modelo formal con su
vocabulario preciso y sus límites: qué es un árbol de nombres, qué es una zona frente a
un dominio, qué límites impone el estándar. Los términos técnicos se nombran en su forma
original entre paréntesis.

**5. Anatomía del artefacto.** Una sección que abre la caja negra —el mensaje del
protocolo, el archivo de construcción, la tabla de reglas— campo por campo, y **conecta
explícitamente cada campo con lo que la herramienta de diagnóstico muestra en pantalla**.
Es lo que convierte una salida críptica en un informe legible.

**6. Sección de seguridad y evolución.** Qué le falta al diseño original, qué extensiones
lo atacan y qué protegen exactamente cada una. Se estudia aunque el práctico no la
configure: completa el mapa conceptual y suele explicar comportamientos divergentes entre
alumnos.

**7. Cada afirmación lleva su porqué.** Nunca "el CNAME no puede coexistir con otros
registros". Siempre: *"La razón es lógica, no caprichosa: el CNAME afirma «este nombre es,
a todos los efectos, aquel otro»; admitir simultáneamente otros datos propios contradiría
esa afirmación."* Si una regla se enuncia sin fundamento, falta trabajo.

**8. Referencias cruzadas explícitas, en las dos direcciones.** Hacia adelante ("es la
clave de la sección 1.8") y hacia atrás ("otro de los significados posibles de ese código
que la sección 1.5 dejó anotado"). Son las que convierten un capítulo en un cuerpo y no en
una pila de secciones.

**9. Encuadre metodológico de los procedimientos.** No se enuncia una lista de
comprobaciones: se explica qué valida cada una. *"Obsérvese que no son cuatro variantes de
la misma prueba: cada una valida una pieza distinta del modelo teórico."* Y cuando hay un
diagnóstico, se nombra el método: *"El método es el experimental clásico: antes de medir el
fenómeno hay que verificar el instrumento."*

## Dos secciones nuevas al cierre

**Actividades escalonadas.** Entre 5 y 7, no 3. Las últimas son de exploración y pueden
exceder el entorno mínimo; en ese caso se marcan con *(requiere entorno Unix)* o el
requisito que corresponda. Cada actividad avanzada pide **relacionar lo observado con una
sección teórica concreta**, citada por número.

**Referencias y lecturas complementarias.** Sección final, **en prosa, no en lista**. Dos
párrafos: el primero recorre las fuentes normativas citándolas por número (RFC, estándares
OCI, documentación oficial); el segundo, la bibliografía académica con edición, editorial y
año. Cada obra viene con una línea de para qué sirve.

> **📌 DATO**
> La síntesis final también cambia. Antes abría con el procedimiento ("la resolución es
> previa e independiente"). Ahora abre con **la decisión de diseño** ("el DNS reemplazó a
> un archivo centralizado que no escalaba; sus tres decisiones de diseño explican todo el
> comportamiento observable"). El procedimiento pasa a ser el punto 2. Es un detalle chico
> que ordena la jerarquía de lo importante.

> **⚠️ OJO ACÁ**
> Lo que el patrón **no** cambia son los recuadros. Siguen en voseo, siguen dirigidos al
> alumno, y el contraste entre el cuerpo impersonal y el recuadro en segunda persona es
> deliberado. La Dirección los dejó intactos y sumó los suyos con la misma voz. Si en algún
> momento alguien te sugiere "unificar el registro", la respuesta es no.

---

# La plantilla: el documento del director es el patrón

**La versión final de la Clase 1 es `Clase_1_DNS_unidad_ampliada.docx`, y los cinco
capítulos tienen que salir idénticos a ese archivo en formato.** No se parte de
`Plantilla - TUPaD.docx`: se parte del documento del director, o se reproduce su formato
exactamente.

La forma más segura de lograrlo, y la que evita depender de que el modelo interprete bien
una descripción, es **partir del propio archivo del director**:

1. Abrir `Clase_1_DNS_unidad_ampliada.docx`.
2. **Guardar como** con el nombre del capítulo nuevo.
3. Borrar todo el cuerpo, **sin tocar el encabezado ni el pie**.
4. Correr el PROMPT 1 sobre ese archivo, que ahora solo tiene que ajustar el titulillo del
   encabezado y verificar que los estilos estén.

Si por lo que sea hay que reconstruir el formato desde cero, el PROMPT 1 trae la
especificación completa medida sobre el archivo original.

> **⚠️ OJO ACÁ**
> El documento del director **no lleva los logos institucionales** que traía
> `Plantilla - TUPaD.docx`: su encabezado y su pie son solo texto. Está verificado sobre el
> archivo, y es una diferencia deliberada de esta versión respecto de los documentos que
> venías generando.
>
> Lo digo una vez y no vuelvo sobre el tema: **si en algún momento la Dirección pide los
> logos de vuelta, hay que reponerlos en los cinco documentos**, no en uno. Conviene
> preguntarlo ahora y no después de armar los cinco.

---

## Especificación del formato, medida sobre el archivo

Todos los valores de esta sección salieron de descomprimir
`Clase_1_DNS_unidad_ampliada.docx` y leer su XML. No son estimaciones.

### Página

| Parámetro | Valor |
|---|---|
| Tamaño | A4 vertical |
| Margen superior | 2,65 cm |
| Margen inferior | 2,1 cm |
| Márgenes laterales | 2,54 cm |
| Encabezado y pie | a 1,25 cm del borde |

### Encabezado y pie

| Elemento | Contenido y formato |
|---|---|
| Encabezado, renglón 1 | `TECNICATURA UNIVERSITARIA EN PROGRAMACIÓN` a la izquierda y `UTN FRM` a la derecha · Calibri 8 · con línea inferior fina gris |
| Encabezado, renglón 2 | `Programación 3 · Unidad N — <título del capítulo>` · Calibri 7,5 · color `#595959` |
| Pie | `PROGRAMACIÓN 3` a la izquierda y `Página N` a la derecha |
| Logos | **Ninguno**, ni en el encabezado ni en el pie |

### Texto

| Elemento | Fuente | Tamaño | Color | Espaciado |
|---|---|---|---|---|
| Cuerpo | Calibri | 11 | automático | interlineado 1,15 · 8 pt después |
| Título del capítulo | **Cambria** | 20 | `#1F4E79` | negrita · 10 pt antes · 4 pt después |
| Subtítulo de unidad | Calibri | 11 | `#595959` | sin negrita ni cursiva · 12 pt después |
| Título 2 (`## N.N.`) | **Cambria** | 13 | `#2E74B5` | negrita · 14 pt antes · 7 pt después |
| Título 3 (`### N.N.N.`) | Calibri | 11,5 | `#404040` | negrita · 12 pt antes · 6 pt después |
| Epígrafe de figura | Calibri | 9 | `#595959` | centrado · sin cursiva |

### Recuadros

Son **tablas de una fila por una columna, sin bordes**, de 15,9 cm de ancho. El título va
en el primer párrafo de la celda, en Calibri 10 negrita del color indicado; el cuerpo, en
Calibri 11. Ambos con 5 pt de espacio después.

| Recuadro | Fondo de la celda | Color del título |
|---|---|---|
| `⚠️ OJO ACÁ` | `#FDECEA` | `#C00000` |
| `💡 PARA ENTENDER` | `#DEEBF7` | `#2E74B5` |
| `🧪 EXPERIMENTO` | `#E2F0DC` | `#538135` |
| `📌 DATO` | `#EFEFEF` | `#595959` |

### Código

| Elemento | Formato |
|---|---|
| Bloque de código | Consolas 9,5 · fondo `#F2F2F2` · sangría izquierda y derecha 0,42 cm · **sin bordes** |
| Código en línea | Consolas 10 · fondo `#EEEEEE` |

### Tablas de datos

| Parámetro | Valor |
|---|---|
| Bordes | todos los lados y los interiores · línea simple 0,5 pt · color `#999999` |
| Fila de encabezado | fondo `#D9E2F3` · negrita · 11 pt · **se repite en cada página** |
| Listas | numeración y viñetas reales de Word · sangría izquierda 1,27 cm con francesa de 0,63 cm |

> **📌 DATO**
> Dos detalles del original que se apartan de lo que uno esperaría, y que hay que respetar
> igual porque el criterio es "idéntico al capítulo 1": los **recuadros son tablas**, no
> párrafos con sombreado, y los **bloques de código no llevan borde izquierdo**, solo fondo
> y sangría. Si más adelante alguien retoca esos dos criterios, se retocan en los cinco
> capítulos a la vez.

---

# PROMPT 1 — Preparación del documento

Se corre **una vez por documento**. La versión corta asume que partiste del archivo del
director guardado con otro nombre y con el cuerpo borrado; la versión larga reconstruye el
formato desde cero.

## Versión corta — partiendo del archivo del director

```
Este documento salió de duplicar la versión final del Capítulo 1 y borrarle el
cuerpo. Voy a volcarle otro capítulo, así que necesito dos cosas antes.

1. TITULILLO DEL ENCABEZADO
   El encabezado tiene dos renglones. El segundo dice:

      Programación 3 · Unidad 1 — Del navegador al servidor

   Cambialo por:

      Programación 3 · Unidad N — <TÍTULO DEL CAPÍTULO NUEVO>

   Respetá el formato actual de ese renglón: Calibri 7,5, color #595959. No
   toques el primer renglón ni el pie de página.

2. INVENTARIO DE ESTILOS
   Decime qué estilos de párrafo y de carácter tiene el documento, y
   confirmame que están los que voy a necesitar:
   Título del capítulo, Título 2, Título 3, cuerpo, epígrafe de figura,
   bloque de código y código en línea.

   Si alguno de esos NO existe como estilo con nombre —es probable, porque el
   documento original trae mucho formato aplicado directamente— avisame cuál
   falta y creámelo con estos valores:

   · Bloque de código  → PÁRRAFO: Consolas 9,5 · fondo #F2F2F2 · sangría
     izquierda y derecha 0,42 cm · SIN bordes · interlineado sencillo · sin
     espacio entre párrafos del mismo estilo · "Conservar líneas juntas".
   · Código en línea   → CARÁCTER: Consolas 10 · fondo #EEEEEE.
   · Epígrafe          → PÁRRAFO: Calibri 9 · color #595959 · centrado · sin
     cursiva · 6 pt antes y 14 pt después.

3. VERIFICACIÓN
   Confirmame que el cuerpo del documento está vacío y que el encabezado y el
   pie siguen intactos, con el titulillo ya corregido.

No agregues todavía ningún texto del cuerpo.
```

## Versión larga — reconstruyendo el formato desde cero

Se usa solo si no se pudo partir del archivo del director.

```
Necesito preparar un documento para que quede IDÉNTICO en formato a la versión
final del Capítulo 1 de este material. Te paso la especificación exacta. No
agregues todavía ningún texto del cuerpo.

1. PÁGINA
   A4 vertical. Márgenes: superior 2,65 cm · inferior 2,1 cm · izquierdo y
   derecho 2,54 cm. Encabezado y pie a 1,25 cm del borde.

2. ENCABEZADO — dos renglones, SIN logos ni imágenes
   a) Primer renglón: "TECNICATURA UNIVERSITARIA EN PROGRAMACIÓN" alineado a
      la izquierda y "UTN FRM" alineado a la derecha, en el mismo renglón.
      Calibri 8. Con una línea inferior fina gris que lo separe del siguiente.
   b) Segundo renglón: "Programación 3 · Unidad N — <título del capítulo>".
      Calibri 7,5, color #595959.

3. PIE — SIN logos ni imágenes
   "PROGRAMACIÓN 3" a la izquierda y "Página N" a la derecha, con el número
   como campo automático.

4. ESTILOS DE TEXTO
   Cuerpo: Calibri 11, interlineado 1,15, 8 pt de espacio después.

   | Estilo               | Fuente  | Tam. | Color   | Espaciado                    |
   |----------------------|---------|------|---------|------------------------------|
   | Título del capítulo  | Cambria | 20   | #1F4E79 | negrita · 10 pt antes · 4 después |
   | Subtítulo de unidad  | Calibri | 11   | #595959 | sin negrita ni cursiva · 12 pt después |
   | Título 2             | Cambria | 13   | #2E74B5 | negrita · 14 pt antes · 7 después |
   | Título 3             | Calibri | 11,5 | #404040 | negrita · 12 pt antes · 6 después |
   | Epígrafe             | Calibri | 9    | #595959 | centrado · sin cursiva       |

5. CÓDIGO — dos estilos, y prestá atención al tipo de cada uno
   a) "Bloque de código" — estilo de PÁRRAFO: Consolas 9,5 · fondo #F2F2F2 ·
      sangría izquierda y derecha 0,42 cm · SIN bordes de ningún lado ·
      interlineado sencillo · SIN espacio entre párrafos del mismo estilo ·
      "Conservar líneas juntas" activado.
   b) "Código en línea" — estilo de CARÁCTER: Consolas 10 · fondo #EEEEEE.

   Si el documento trae un estilo llamado "Código HTML", NO lo uses ni lo
   modifiques: es de carácter y no admite sangría, fondo ni espaciado.

6. RECUADROS — se hacen con TABLAS, no con estilos de párrafo
   Cada recuadro es una tabla de 1 fila por 1 columna, de 15,9 cm de ancho,
   SIN bordes, con la celda rellena del color que corresponda. Adentro: el
   título en Calibri 10 negrita del color indicado, y el cuerpo en Calibri 11.
   Ambos con 5 pt de espacio después.

   | Recuadro           | Fondo de la celda | Color del título |
   |--------------------|-------------------|------------------|
   | ⚠️ OJO ACÁ         | #FDECEA           | #C00000          |
   | 💡 PARA ENTENDER   | #DEEBF7           | #2E74B5          |
   | 🧪 EXPERIMENTO     | #E2F0DC           | #538135          |
   | 📌 DATO            | #EFEFEF           | #595959          |

7. TABLAS DE DATOS
   Bordes en todos los lados y en los interiores, línea simple de 0,5 pt,
   color #999999. Fila de encabezado con fondo #D9E2F3, en negrita, 11 pt, y
   marcada para repetirse en cada página.

8. IDIOMA
   Español de Argentina (es-AR) en el documento y en todos los estilos.

Cuando termines, listame qué creaste y qué modificaste, y confirmame:
  a) Que "Bloque de código" quedó como estilo de PÁRRAFO.
  b) Que el encabezado y el pie NO tienen imágenes.
  c) Que el titulillo del encabezado dice el número y el título de ESTE
     capítulo.
```

---

# PROMPT 2 — Volcado del contenido

Se corre **una vez por documento**, adjuntando **dos archivos**:

1. El `.md` del capítulo que corresponda.
2. **`FIGURAS.md`**, siempre. Es el que le permite escribir dentro de cada marco qué
   hay que capturar y qué resaltar, en vez de dejar un rectángulo mudo.

> **⚠️ OJO ACÁ**
> Con el patrón de unidad de estudio, cada capítulo ronda las **9.000 a 11.000 palabras**:
> son entre 8 y 10 veces la tarea previa, y ya con la tarea previa apareció presión de
> contexto en la conversación. Si le pedís un capítulo entero de una, no es que *haya
> riesgo* de que se quede sin margen: se va a quedar sin margen, y va a empezar a resumir
> sin avisar.
>
> **Volcá por tramos, sin excepción.** El prompt de abajo ya lo contempla: le pide que
> trabaje por secciones y que pare al final de cada una. Vos le decís "seguí" y continúa.
> Con capítulos de este tamaño contá con **dos conversaciones separadas** por documento, y
> tenelo previsto de antemano en vez de descubrirlo a mitad de camino.

```
Adjunto el manuscrito fuente de un capítulo en Markdown. Volcalo al documento
actual, que ya tiene la plantilla y los estilos preparados.

═══ REGLA PRINCIPAL ═══
TRANSCRIBÍ, NO REESCRIBAS. El texto ya está editado y revisado. No resumas, no
reformules, no "mejores" la redacción, no agregues introducciones ni
conclusiones propias, no cambies el orden de nada. Si algo te parece mejorable
o encontrás un error, dejalo tal cual y anotámelo al final en una lista aparte.

═══ MAPEO DE ESTILOS ═══
El mapeo va por NIVEL de encabezado, no por el texto: algunos capítulos usan
numeración "N.N." y otros títulos como "Paso 3 — ...". Da igual, mapeá por la
cantidad de almohadillas.

| En el Markdown                  | Cómo va en Word                                |
|---------------------------------|------------------------------------------------|
| #                               | Título del capítulo: Cambria 20 negrita #1F4E79 |
| Línea en *cursiva* justo debajo del # | Subtítulo de unidad: Calibri 11 #595959, sin negrita ni cursiva |
| ##                              | Título 2: Cambria 13 negrita #2E74B5            |
| ###                             | Título 3: Calibri 11,5 negrita #404040          |
| Párrafo común                   | Cuerpo: Calibri 11, interlineado 1,15           |
| **negrita**                     | negrita                                        |
| Listas con - o numeradas        | Lista real de Word, sangría 1,27 cm con francesa de 0,63 |
| Bloques delimitados por ```     | Bloque de código                               |
| `código en línea`               | Código en línea                                |
| Tablas                          | Tabla, con el formato de abajo                 |
| - [ ] casilla de verificación   | Lista con casillas reales de Word (símbolo ☐)  |
| --- (regla horizontal)          | Se omite                                       |

Bloques de código: Consolas 9,5 · fondo #F2F2F2 · sangría izquierda y derecha
0,42 cm · SIN bordes. Un bloque de varias líneas es un solo bloque visual, no
líneas sueltas separadas. No agregues numeración de línea ni coloreado de
sintaxis. Si el documento trae un estilo "Código HTML", no lo uses: es de
carácter y no admite fondo ni sangría.

Código en línea: Consolas 10 · fondo #EEEEEE.

Tablas de datos: bordes en todos los lados y en los interiores, línea simple de
0,5 pt color #999999. Primera fila como encabezado, con fondo #D9E2F3, en
negrita, y marcada para repetirse en cada página.

URLs: convertí toda dirección web en hipervínculo real y funcional, con el
texto visible tal como está en el manuscrito. El documento se va a leer en
pantalla y en PDF.

═══ RECUADROS — SE HACEN CON TABLAS ═══
En el Markdown vienen como citas que empiezan con un emoji y un título en
negrita. Cada uno va en el documento como una TABLA DE 1 FILA POR 1 COLUMNA,
de 15,9 cm de ancho, SIN bordes, con la celda rellena del color que
corresponda. No uses estilos de párrafo con sombreado: tienen que ser tablas,
para que queden idénticos al Capítulo 1.

  | Recuadro           | Fondo de la celda | Color del título |
  |--------------------|-------------------|------------------|
  | ⚠️ OJO ACÁ         | #FDECEA           | #C00000          |
  | 💡 PARA ENTENDER   | #DEEBF7           | #2E74B5          |
  | 🧪 EXPERIMENTO     | #E2F0DC           | #538135          |
  | 📌 DATO            | #EFEFEF           | #595959          |

Adentro de la celda: el emoji y el título como PRIMER PÁRRAFO, en Calibri 10
negrita, del color indicado en la tabla. El cuerpo del recuadro debajo, en
Calibri 11. Ambos con 5 pt de espacio después.

Quitá el símbolo ">" de cada línea. Si un recuadro tiene varios párrafos, una
lista o un bloque de código adentro, todo eso va dentro de la MISMA celda.

═══ FIGURAS ═══
Adjunto también FIGURAS.md, que es el catálogo con la especificación completa
de las 26 figuras del material. Usalo para llenar cada marco de posición.

Cuando encuentres en el capítulo una línea con este formato:

  [FIGURA 1.3: descripción — ver FIGURAS.md]

reemplazala por estos tres elementos:

  a) UN MARCO DE POSICIÓN
     Una tabla de 1 fila por 1 columna, del ancho del texto y 7 cm de alto,
     con borde punteado gris de 1 pt y relleno #FAFAFA.

  b) DENTRO DEL MARCO, centrado, en Calibri 9, cursiva, color #909497.
     Buscá esa figura en FIGURAS.md y escribí:
       · Primera línea, en negrita y sin cursiva: "FIGURA 1.3"
       · Segunda línea: el campo "Tipo" de esa figura
         (diagrama / captura de pantalla / composición)
       · Tercera línea: qué debe mostrar, resumido en una o dos oraciones
       · Cuarta línea, solo si esa figura tiene indicación de "Resaltar" o
         "Difuminar": esa indicación, precedida por "Resaltar:" o "Difuminar:"

  c) DEBAJO DEL MARCO
     Un párrafo con estilo "Epígrafe" que diga "Figura 1.3. " seguido del texto
     exacto del campo "Epígrafe" de esa figura en FIGURAS.md.

IMPORTANTE sobre FIGURAS.md:
  · Los bloques de diagrama en arte ASCII que trae ese archivo son
    instrucciones para dibujar la figura. NO los copies al documento.
  · Si alguna figura del capítulo no aparece en FIGURAS.md, usá la descripción
    del propio marcador y avisame al final cuáles fueron.

No generes ni insertes ninguna imagen. Yo las inserto después, reemplazando el
contenido de cada marco.

═══ IDIOMA ═══
Español rioplatense, es-AR. Respetá todos los acentos y la ñ tal como vienen.
NO cambies el voseo de los recuadros por tuteo ni por "usted": el contraste
entre el cuerpo impersonal y los recuadros en segunda persona es intencional.

═══ RITMO DE TRABAJO ═══
Este capítulo es largo. NO intentes volcarlo entero de una sola vez.

Trabajá por tramos: volcá una sección de nivel ## completa (con todas sus
subsecciones, tablas, recuadros y figuras), pará, y decime en una línea qué
sección terminaste y cuál sigue. Yo te contesto "seguí" y continuás.

Si en algún momento sentís que te estás quedando sin margen de contexto,
decímelo ANTES de seguir. Prefiero mil veces retomar en otra conversación que
descubrir después que resumiste una sección sin avisar.

Nunca abrevies, condenses ni saltees contenido por razones de espacio. Si no
entra, se corta y se sigue después.

═══ AL TERMINAR ═══
Decime:
1. Cuántos recuadros aplicaste, discriminados por tipo.
2. Cuántos bloques de código, y confirmame que todos quedaron con el estilo de
   párrafo "Bloque de código".
3. Cuántas tablas.
4. Cuántos marcos de figura dejaste y con qué números.
5. Cualquier cosa que te haya parecido un error del manuscrito: contradicción,
   dato inconsistente, término usado de dos formas distintas. Esto es útil de
   verdad, no lo omitas por cortesía.
```

---

## Tabla de control: qué tiene que reportar cada capítulo

Contrastá contra esto lo que te reporte al terminar. Si un número no coincide, se comió
algo y hay que revisar antes de seguir.

| Documento | Recuadros | Bloques de código | Tablas | Figuras | Palabras |
|---|---|---|---|---|---|
| Tarea previa | 4 | 0 | 4 | 0 | 1.150 |
| Clase 1 — DNS y dominio | 20 | 8 | 17 | 6 | 10.660 |
| Clase 2 — VPS y seguridad | 18 | 19 | 17 | **6** | 8.740 |
| Clase 3 — Docker | 17 | 20 | 15 | 1 | 7.400 |
| Clase 4 — Despliegue | 18 | 6 | 16 | 9 | 6.370 |
| Clase 5 — Red interna y DevOps | 17 | 8 | 15 | 4 | 6.390 |

La columna de palabras no se la vas a pedir a Word: está para que dimensiones el trabajo
antes de arrancar. Un capítulo de 10.000 palabras son unas 25 a 30 páginas armadas.

> **📌 DATO**
> La Clase 2 y la Clase 3 son las que más bloques de código tienen: 20 cada una. Son
> justamente las que ponen a prueba el estilo "Bloque de código" que la tarea previa nunca
> ejercitó, porque no tenía ni uno. Mirá con atención el resultado de esas dos.

> **⚠️ OJO ACÁ**
> Los recuadros son los que más se pierden en el camino. Son **94 en total** y están
> repartidos por todo el cuerpo, así que si un capítulo te reporta cuatro menos de los que
> dice esta tabla, hay cuatro párrafos que quedaron en Normal y visualmente no se
> distinguen de la prosa. Contá antes de seguir con el capítulo siguiente.

---

# PROMPT 3 — Índice y control final

Se corre al final de cada documento.

```
Terminá el documento:

1. Insertá una tabla de contenidos al principio, después del título, con tres
   niveles de encabezado.
2. Verificá que la numeración de secciones del manuscrito (1.1, 1.2, 1.2.1)
   coincida con la jerarquía de estilos aplicada, y avisame si hay saltos.
3. Revisá que ningún bloque de código haya quedado con el formato del cuerpo:
   todos tienen que estar en Consolas 9,5 con fondo #F2F2F2.
4. Revisá que ninguna tabla de datos se corte entre páginas sin repetir el
   encabezado.
5. Contame cuántos recuadros hay, discriminados por tipo, y confirmame que
   TODOS son tablas de 1x1 sin bordes con la celda rellena. Si alguno quedó
   como párrafo con sombreado, decime cuál.
6. Confirmame que el renglón del titulillo ("Programación 3 · Unidad N — ...")
   figura en el encabezado con el número y el título correctos de ESTE
   capítulo, no los del anterior.
7. Confirmame que el pie dice "PROGRAMACIÓN 3" y que el número de página es un
   campo automático, no un número escrito a mano.

No cambies ni una palabra del contenido.
```

> **⚠️ OJO ACÁ**
> El punto 6 es el que se va a olvidar sí o sí cuando armes el capítulo siguiente copiando
> el anterior: el titulillo queda diciendo "Unidad 1" en el documento de la Unidad 2, y no
> lo vas a notar hasta que tengas los cinco PDF uno al lado del otro.
>
> El punto 5 importa por lo mismo: un recuadro que quedó como párrafo con sombreado se ve
> **casi** igual que los demás. Casi. Y "casi idéntico al Capítulo 1" no es lo que pidió la
> Dirección.

---

# PROMPT 4 — Inserción de figuras

Sirve para **una o para todas juntas**. No hay que editar el prompt: lo que le dice a
qué marco va cada imagen es **el nombre del archivo**.

## Antes: renombrar los archivos

Esto es lo único que hay que hacer a mano, y es lo que hace que el prompt funcione sin
modificarlo:

```
figura-1-1.svg      ← el diagrama del recorrido de la petición
figura-1-2.svg      ← el diagrama de resolución recursiva
figura-1-3.png      ← la captura del nslookup
figura-1-4.png      ← dnschecker.org
figura-1-5.png      ← el Student Pack
figura-1-6.png      ← los registros en Namecheap
```

> **⚠️ OJO ACÁ**
> mermaid.live te descarga los archivos con nombres tipo
> `mermaid-diagram-2026-07-27-143052.svg`. **Renombralos antes de adjuntar.** Si le pasás
> tres archivos con nombres crípticos, tiene que adivinar cuál va en cada marco, y va a
> adivinar mal en alguno.

## El prompt

```
Adjunto una o más imágenes. El nombre de cada archivo indica a qué figura
corresponde: "figura-1-3" va al marco de la FIGURA 1.3, y así con todas.

En el documento, cada figura tiene un marco de posición: una tabla de 1x1 con
borde punteado gris, que adentro dice "FIGURA N.N" y describe qué había que
capturar ahí.

Para cada imagen adjunta, en orden numérico:

1. Ubicá el marco cuyo texto empieza con el número de figura correspondiente.
2. Decime las primeras palabras del texto que hay adentro de ese marco, ANTES
   de borrarlo.
3. Borrá todo el texto de adentro del marco.
4. Insertá la imagen, centrada, ajustada al ancho del texto y manteniendo la
   proporción original.
5. Sacale al marco el borde punteado y el relleno gris, para que quede
   solamente la imagen.
6. NO toques el párrafo de epígrafe que está debajo del marco. Ese queda tal
   cual está.

Si el nombre de algún archivo no se corresponde con ningún marco del
documento, o si encontrás dos marcos con el mismo número, PARÁ y avisame en
vez de adivinar.

Al terminar, listame en una tabla: número de figura, primeras palabras del
texto que borraste, y nombre del archivo que insertaste ahí.
```

> **💡 PARA ENTENDER**
> El paso 2 y la tabla final no son burocracia. Si por cualquier motivo agarra el marco
> equivocado, te enterás en ese momento y no cuando abrís el PDF terminado y ves el
> diagrama de DNS donde iba el recorrido de la petición HTTPS. Son dos segundos de
> lectura contra rehacer medio documento.

> **📌 DATO**
> Podés insertar las figuras **a medida que las vayas consiguiendo**. No hace falta
> esperar a tenerlas las seis: el documento ya está armado y los marcos te esperan. Corré
> el prompt hoy con las que tengas y volvé a correrlo la semana que viene con el resto.

---

# PROMPT 5 — Actualizar el texto de un documento que ya tiene figuras

Para cuando el manuscrito cambió **después** de generar el documento y las imágenes ya
están insertadas. Regenerar costaría volver a insertarlas todas, así que se parchea.

> **⚠️ OJO ACÁ — cuándo NO usar este prompt**
> Parchear solo conviene si los cambios son **locales**: párrafos reescritos, un recuadro
> nuevo, una tabla corregida, con la numeración de secciones intacta.
>
> Si el capítulo **cambió de estructura** —secciones nuevas intercaladas, secciones
> renumeradas, el orden alterado—, parchear es peor que regenerar. El modelo tiene que
> alinear dos documentos que ya no se corresponden sección por sección, y ahí es cuando se
> equivoca de marco y te pisa una figura.
>
> **La regla:** si la numeración de secciones cambió, regenerá el documento desde cero con
> los PROMPT 1 y 2, y volvé a insertar las figuras con el PROMPT 4. Las imágenes ya las
> tenés en el disco: reinsertarlas son cinco minutos. Reparar un documento desalineado son
> dos horas.

Se adjunta **el `.md` actualizado del capítulo**.

```
Este documento se generó a partir de una versión anterior del manuscrito, y
las figuras ya están insertadas. Adjunto el manuscrito ACTUALIZADO. Necesito
que traslades al documento únicamente los cambios de texto.

═══ REGLA INVIOLABLE ═══
NO TOQUES NINGUNA IMAGEN.

Cada imagen del documento está seguida de un párrafo con estilo "Epígrafe". Ni
las imágenes ni sus epígrafes se borran, se mueven, se redimensionan ni se
reemplazan. Si para actualizar una sección tenés que reescribir el texto que
rodea a una figura, reescribí SOLO el texto: la imagen y su epígrafe se quedan
exactamente donde están.

PRIMER PASO, antes de modificar nada: recorré el documento y listame cada
imagen con el número de figura de su epígrafe y la sección en la que está.
Esa lista es la que vamos a verificar al final.

═══ QUÉ COMPARAR ═══
Recorré el manuscrito adjunto y el documento sección por sección, y aplicá al
documento toda diferencia de texto que encuentres.

Si encontrás que la numeración de secciones del manuscrito NO se corresponde
con la del documento —secciones nuevas, renumeradas o reordenadas— PARÁ y
avisame antes de tocar nada. En ese caso conviene regenerar, no parchear.

═══ CÓMO APLICARLO ═══
· Copiá el formato de lo que ya está en el documento. Para cada elemento nuevo,
  buscá uno del mismo tipo que ya exista y replicalo exactamente: mismo tipo de
  letra, mismo cuerpo, mismo color, mismo espaciado.
· Los recuadros nuevos van como TABLA de 1x1 sin bordes, con la celda rellena,
  igual que los que ya están. El fondo depende del emoji:
  ⚠️ #FDECEA · 💡 #DEEBF7 · 🧪 #E2F0DC · 📌 #EFEFEF.
· Las tablas nuevas: bordes 0,5 pt color #999999, encabezado con fondo #D9E2F3
  en negrita, repetición en cada página.
· Los bloques de código nuevos: Consolas 9,5, fondo #F2F2F2, sangría izquierda
  y derecha 0,42 cm, sin bordes.
· TRANSCRIBÍ, NO REESCRIBAS. El manuscrito adjunto es la versión final.
· Al terminar, actualizá la tabla de contenidos.

═══ AL TERMINAR ═══
Decime:
1. Qué secciones modificaste y en una línea qué cambió en cada una.
2. La misma lista de imágenes del primer paso, ahora al final: número de
   figura, epígrafe y sección. Tiene que ser idéntica a la inicial.
3. Cualquier término del manuscrito viejo que haya quedado suelto en el
   documento.
```

> **⚠️ OJO ACÁ**
> El punto 2 del cierre es el que importa, y por eso el prompt pide la misma lista dos
> veces: una antes de tocar nada y otra al final. Un parche que arregla el texto y en el
> camino se lleva puesta una figura es peor que no parchear —el texto lo revisás leyendo,
> pero una imagen que desapareció tres páginas más abajo te la comés hasta que exportás el
> PDF—. Con las dos listas, la comparás de un vistazo.
>
> **Guardá una copia del `.docx` antes de correr este prompt.** Son dos segundos y es la
> única red de seguridad real.

---

# Imágenes: qué se genera y qué no

Esta es la parte donde conviene ser claro, porque la respuesta no es la misma para los
tres tipos de imagen del material.

| Tipo | Cantidad | Cómo se produce |
|---|---|---|
| **Capturas de pantalla** | 18 | Las sacás vos. **No se generan.** |
| **Diagramas técnicos** | 8 | Herramienta de diagramación, **no IA generativa** |
| **Portada y separadores** | 6 | **Higgsfield** |

## Las 18 capturas: no se generan, y el motivo importa

Panel de Easypanel, hPanel, Namecheap, GitHub, terminales. Una imagen generada por IA de
"el panel de Easypanel" sería **documentación fabricada**: no se correspondería con
ninguna pantalla real. El alumno abre el panel, no coincide con el apunte, y a partir de
ahí no le cree nada más al material.

La especificación de cada una está en `FIGURAS.md`.

## Los 8 diagramas: tampoco con IA generativa

Los generadores de imágenes **no escriben texto legible**. Etiquetas como
`calculadora_db`, `Host: api.tudominio.com` o `ORIGENES_PERMITIDOS` salen deformadas o
directamente inventadas. Un diagrama técnico con las etiquetas mal es peor que no tener
diagrama, porque el alumno se lo cree.

`FIGURAS.md` trae el esquema de los ocho, y `DIAGRAMAS.md` el código Mermaid de los que ya están escritos. Opciones, de mejor a peor:

| Herramienta | Ventaja |
|---|---|
| **draw.io / diagrams.net** | Gratis, exporta PNG y SVG, editable para siempre |
| **Mermaid** | Se escribe como texto, versionable junto al material |
| **PowerPoint** | Ya lo tenés, y es coherente con la estética de la plantilla |

## Portada y separadores: acá sí, Higgsfield

Seis imágenes decorativas, sin una sola letra adentro. Ahí la IA generativa está en su
mejor uso.

**Dónde correrlo:** el conector de Higgsfield está disponible en claude.ai. Generás ahí,
descargás el PNG y lo insertás en Word con *Insertar → Imágenes*. No dependas de que el
conector esté disponible dentro del complemento de Word.

### Prompt para la portada

```
Generá una ilustración conceptual editorial en estilo isométrico minimalista,
sobre fondo blanco.

Escena: un servidor físico del que salen dos rutas de luz hacia dos pantallas
flotantes. Una pantalla muestra la silueta de una interfaz de calculadora; la
otra muestra bloques abstractos que sugieren datos estructurados. Entre el
servidor y las pantallas, un nodo circular que reparte las dos rutas.

Paleta: azul cobalto, gris grafito y un único acento naranja.
Composición horizontal, mucho espacio negativo, líneas limpias.

IMPORTANTE: sin texto, sin letras, sin números, sin logos, sin marcas de
ningún tipo. Ninguna palabra en la imagen.

Aspecto: profesional, sobrio, apto para material académico universitario.
```

### Prompts para los cinco separadores

Misma base, cambiando solo la escena. Mantené **siempre** la paleta, el estilo isométrico
minimalista y la instrucción de que no haya texto, para que los seis se vean como una
familia.

| Clase | Escena a describir |
|---|---|
| 1 — DNS | Una red de nodos conectados que converge desde muchos puntos hacia uno solo, sugiriendo una jerarquía de consultas |
| 2 — VPS y seguridad | Un servidor rodeado de un perímetro de escudos hexagonales, con una sola puerta abierta y el resto selladas |
| 3 — Docker | Contenedores de carga apilados en capas, uno abierto mostrando engranajes en su interior |
| 4 — Despliegue | Un flujo ascendente desde una caja en el suelo hacia una nube, con un nodo que distribuye hacia dos destinos |
| 5 — Red interna | Dos cajas dentro de un recinto cerrado, unidas por un canal luminoso interno, con el recinto sin aberturas hacia afuera |

> **⚠️ OJO ACÁ**
> La instrucción "sin texto, sin letras, sin números" no es opcional ni es un exceso de
> cautela. Los generadores de imágenes meten texto inventado por defecto, y te vas a
> encontrar con la portada de tu apunte diciendo "SERVR DEPLOI" en un cartelito. Repetila
> en todos los prompts.

> **📌 DATO**
> Si querés que los seis se vean realmente como un conjunto, generá primero la portada y
> después, para los separadores, pasale esa imagen como referencia de estilo. Sale mucho
> más coherente que describir la paleta seis veces.
