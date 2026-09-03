# Manual de estilo criollo — módulo de frontend

Este archivo describe **cómo se traduce un capítulo académico al registro criollo**
que la Dirección aprobó el 2026-09-02. No es una guía de gusto: es la
formalización del método que el director aplicó sobre el Capítulo 1, extraído
sección por sección de `capitulo1frontendencriollo.docx`.

El capítulo 1 (`capitulos/01-la-web-como-plataforma.md`) es el **ejemplo
canónico**. Ante cualquier duda, se mira cómo quedó ahí.

Los capítulos académicos originales están respaldados en `capitulos/_academico/`.

---

## 1. Qué es y qué no es esta traducción

**No es un resumen.** El capítulo criollo tiene aproximadamente la misma extensión
que el académico: el Capítulo 1 pasó de 8.976 a ~9.000 palabras. Lo que cambia es
el idioma, no la densidad.

**No se pierde ni un concepto.** Si el original dice *idempotencia*, el criollo
dice *idempotencia* — y además explica qué es y por qué importa. Si el original
cita la RFC 9110, el criollo la cita. Si el original nombra RN-F07, el criollo la
nombra.

**Lo que cambia:** la sintaxis, la persona gramatical, la forma de presentar las
enumeraciones y el andamiaje de lectura.

> Regla de contraste: el original está escrito en el idioma de los papers —denso,
> comprimido, cada frase cargada—. El criollo lo desarma y lo cuenta como se lo
> contarías a alguien en un café. Sin perder una sola precisión técnica.

---

## 2. Encabezado del capítulo

```markdown
# Capítulo N — GUÍA DE LECTURA

## <Título corto del capítulo>

### <Subtítulo temático>, explicado en criollo

*Traducción didáctica del texto académico, sección por sección. Mismos conceptos,
otro idioma.*
```

Reemplaza al `*Unidad de estudio · Edición ampliada con fundamentos teóricos*` del
académico.

## 3. El preámbulo obligatorio

Todo capítulo abre con una sección **«Antes de empezar: cómo usar esta guía»** que
explica el contrato de lectura y anuncia las tres partes (`Qué dice`, `En
criollo`, `Para el pizarrón`).

Cierra con el recuadro **LA IDEA MADRE DE TODO EL CAPÍTULO**: una sola frase que
resume el capítulo entero, más dos o tres oraciones que expliquen por qué esa
frase gobierna todo lo que sigue. Sale, casi siempre, del párrafo de encuadre que
el académico tenía en su sección N.1.

**El índice numerado de contenidos del académico se elimina.** El documento se
navega por sus títulos.

## 4. La estructura tripartita

En las secciones **conceptuales** (típicamente N.1 a N.4, las que fundan el
modelo) el contenido se organiza así:

| Parte | Encabezado | Registro | Función |
| --- | --- | --- | --- |
| Qué dice | `### Qué dice` | Impersonal, condensado | La idea del original en dos o tres oraciones densas |
| En criollo | `### En criollo` | **Voseo**, expandido | La explicación larga, con la analogía que la hace pegar |
| Para el pizarrón | recuadro `💡 PARA EL PIZARRÓN` | Voseo | La frase que el alumno se tiene que llevar |

En las secciones **operativas** (anatomías, herramientas, estudios de caso,
seguridad) no se usa `Qué dice` / `En criollo`: se va directo, y los subtítulos de
tercer nivel pasan a ser **títulos temáticos en criollo** que anuncian qué viene:

- `### Los tres detalles que más se pasan por alto`
- `### Tres pares que no hay que confundir`
- `### Acá se ve la tercera decisión de diseño en acción, y es contraintuitiva`
- `### Precisión de vocabulario, porque acá se confunden dos cosas`
- `### Las tres versiones del protocolo, y lo que no cambió`

## 5. Los títulos de sección se reescriben

Se conserva **la numeración exacta** y se cambia el separador de `.` a ` — `.
El título deja de nombrar la categoría académica y pasa a nombrar la pregunta:

| Académico | Criollo |
| --- | --- |
| `## 1.1. Alcance de la clase` | `# 1.1 — De qué se trata esta clase` |
| `## 1.2. Por qué existe la web: origen y objetivos de diseño` | `# 1.2 — Por qué existe la web: el problema que vino a resolver` |
| `## 1.4. Arquitectura del protocolo HTTP` | `# 1.4 — Cómo está armado HTTP` |
| `### 1.4.1. El modelo petición-respuesta y la ausencia de estado` | `## 1.4.1 — Petición y respuesta, y el servidor que no se acuerda de nada` |
| `### 1.4.2. Semántica de los métodos` | `## 1.4.2 — Los métodos: seguridad e idempotencia` |
| `## 1.6. Anatomía del identificador uniforme de recurso` | `# 1.6 — Anatomía de la URL` |
| `## 1.13. Verificación` | `# 1.13 — Verificación: el checklist honesto` |
| `## 1.14. Errores frecuentes` | `# 1.14 — Los ocho errores frecuentes` |
| `## 1.15. Actividades` | `# 1.15 — Las actividades, y qué busca cada una` |
| `## 1.16. Síntesis` | `# 1.16 — Síntesis: las diez frases` |
| `## 1.17. Referencias y lecturas complementarias` | `# 1.17 — Qué leer, y en qué orden` |

**Nivel de encabezado:** las secciones `N.x` van con `#`, las `N.x.y` con `##`, y
los títulos temáticos internos con `###`.

## 6. La prosa densa se convierte en tabla

Ésta es la transformación más característica del método y la que más rinde. Cuando
el académico enumera **tres o más elementos comparables en párrafos seguidos**, el
criollo los pone en una tabla de dos o tres columnas.

Ejemplo del Capítulo 1: los tres párrafos de FTP / Gopher / hipertexto se
convirtieron en

```markdown
| Herramienta | Qué hacía bien | Por qué no alcanzaba |
```

y las cuatro decisiones de diseño en

```markdown
| Decisión | Qué gana | Qué cuesta |
```

Otros encabezados de tabla que el director usó, y que conviene reutilizar:

- `| Si no sabés esto… | …no vas a entender esto otro |`
- `| Propiedad | Qué significa | Quiénes la cumplen |`
- `| Familia | Significado | Qué informa realmente |`
- `| Par | La diferencia, en una frase | El error típico |`
- `| La línea | Qué hace de verdad | Si falta |`
- `| La celda | Qué sabés de ella, y desde dónde |`
- `| Pestaña | Qué muestra | Cuándo la usás |`
- `| Encabezado | Qué ordena | Contra qué protege |`
- `| El error | Por qué duele | Sección |`

**Lo que NO se convierte en tabla:** las listas de pasos secuenciales (el recorrido
de una petición, un procedimiento), los bloques de código y las listas de la
sección de verificación. Ésas quedan como listas.

## 7. Los recuadros

Se conserva el emoji al inicio —**el generador lo usa para elegir el color y no lo
imprime en el Word**— y se le agrega **una etiqueta en mayúscula** que anuncia de
qué tipo es y, con frecuencia, dos puntos y un título concreto.

| Emoji | Etiquetas del director | Color en el Word |
| --- | --- | --- |
| `💡` | `LA IDEA MADRE DE TODO EL CAPÍTULO`, `PARA EL PIZARRÓN`, `PARA ENTENDER`, `LAS SEIS` | azul |
| `⚠️` | `OJO ACÁ`, y títulos de advertencia sin etiqueta (`El malentendido más caro sobre HTTPS`) | rojo |
| `🧪` | `EXPERIMENTO — hacelo hoy, en cualquier sitio` | verde |
| `📌` | notas al margen con título propio (`Guardá esta conexión: es el modelo de todo el módulo`, `Y una noticia buena para vos`) | gris |

Forma en el markdown:

```markdown
> **💡 PARA ENTENDER: la lista de invitados y la pulsera**
> Esto explica algo que molesta y parece redundante: **¿por qué tengo que mandar el
> token en cada llamada?**
>
> Pensalo como la entrada a un evento…
```

**Cantidad:** entre 14 y 18 por capítulo — **más que en el académico**, que pedía
entre 10 y 14. El Capítulo 1 tiene 17.

### El blockquote sin emoji no es un recuadro

Un blockquote que **no** abre con emoji es una **cita**, y el generador lo marca
distinto a propósito: barra gris a la izquierda, sin fondo de color. El material
académico ya lo usaba para dos cosas, y el criollo **las conserva tal cual**:

- el enunciado textual de una regla `RN-F` (`> **RN-F03.** El estado del servidor
  vive únicamente en…`), con su garante;
- la formulación de un criterio que después se desarma en el cuerpo.

Fuera de esos dos casos, **no se usa**. Si algo merece destacarse, es recuadro y
lleva emoji. El Capítulo 1 no tiene ninguna cita; el Capítulo 8 tiene siete,
porque es el que repasa las once reglas.

**Los recuadros del criollo son más largos que los del académico.** Ahí es donde
vive la analogía, y la analogía es el corazón del método. Un recuadro de cinco o
seis renglones con una comparación bien elegida vale más que dos párrafos de
prosa.

## 8. El registro

**Todo el capítulo está en voseo.** Ésta es la ruptura con el estándar anterior,
que pedía cuerpo impersonal y recuadros en voseo. La Dirección lo cambió: ahora el
contraste ya no existe.

La única excepción son los bloques `### Qué dice`, que se mantienen impersonales
**a propósito**: representan la voz del texto académico que después se traduce.

Marcas de registro que el director usa y conviene sostener:

- Voseo pleno: *fijate*, *mirá*, *pensalo*, *acordate*, *guardá esta conexión*,
  *abrí el panel*, *contá cuántas*, *pará: acabás de abrir un agujero*.
- Apelación directa al lector: *«Vos ya sabés programar»*, *«Vos ya no»*,
  *«Y una noticia buena para vos»*.
- Frases cortas de remate en negrita: *«Una se abre.»*, *«El código funcionó: está
  mirando el lugar equivocado.»*, *«El agente escribe rápido. Vos tenés que saber
  qué mirar.»*
- Anticipación de la objeción: *«Esto explica algo que molesta y parece
  redundante: ¿por qué tengo que…?»*
- Numeración hablada dentro del párrafo: *«La primera. …»* / *«La segunda. …»*

**Lo que no se hace:** ni sarcasmo, ni chiste a costa del alumno, ni informalidad
que le baje el precio al contenido. El registro es cálido y directo porque el
material es serio, no a pesar de eso.

## 9. La analogía es obligatoria

Cada concepto abstracto del capítulo lleva **una** analogía concreta. Del Capítulo 1:

| Concepto | Analogía |
| --- | --- |
| Token en cada petición vs. sesión en el servidor | La lista de invitados y la pulsera |
| Idempotencia | El botón del ascensor contra el botón de comprar |
| HTML vs. DOM | El plano en papel y la casa construida |
| El fragmento `#` no viaja al servidor | La anotación en el margen de tu ejemplar del libro |
| `<div>` estilizado como botón | Una puerta pintada en la pared |
| Qué garantiza HTTPS | El sobre lacrado con el sello del remitente |
| Tolerancia del parser al marcado inválido | El amigo que te entiende igual aunque hables mal y nunca te corrige |

Una analogía por concepto, y que se pueda dibujar. Si no se puede dibujar, no
sirve.

## 10. El cierre, sección por sección

**Verificación** → `N.13 — Verificación: el checklist honesto`. Lista de
comprobaciones, cada una cerrando con la sección de referencia entre paréntesis y
en cursiva: `*(1.4.3)*`. Abre con «No son ejercicios: son el criterio para saber
si el capítulo se entendió».

**Errores frecuentes** → `N.14 — Los <N> errores frecuentes`, en tabla de tres
columnas `El error | Por qué duele | Sección`. Abre con «Todos tienen algo en
común: en el momento, no parecen errores. Por eso son frecuentes».

**Actividades** → `N.15 — Las actividades, y qué busca cada una`. Cada actividad
con su `### N. Título` y, debajo del enunciado, una línea en cursiva:
`**Qué busca:** *…*` que revela la intención pedagógica.

**Síntesis** → `N.16 — Síntesis: las diez frases`. Lista, no prosa. Cada punto
abre por la decisión de diseño, nunca por el procedimiento.

**Referencias** → `N.17 — Qué leer, y en qué orden`, con tres bloques:

```markdown
### Si leés una sola cosa
### Si leés tres
### Las fuentes normativas (para consultar, no para leer de corrido)
```

Éste es el **segundo cambio al estándar anterior**: el académico las pedía en
prosa, el criollo las pide priorizadas y en lista. Cada obra conserva edición,
editorial y año, y su línea de para qué sirve.

**Cierre nuevo** → `Cierre: las <N> cosas que hay que recordar`. Un recuadro `💡`
con las frases numeradas y en negrita, y después un párrafo final con «una más,
que no está escrita en el capítulo pero está en todas sus páginas».

## 11. Lo que no cambia

Todo esto se hereda del estándar académico y sigue vigente:

- **Cada afirmación lleva su porqué.**
- **Ningún concepto se enuncia antes de su problema** (`CLAUDE.md` §6).
- Las secciones del TPI se citan por su número original y **nunca se copian**.
- Las reglas `RN-F01` a `RN-F11` se nombran cuando quedan explicadas.
- Referencias cruzadas en las dos direcciones, hacia adelante y hacia atrás.
- **Cero arte ASCII.** Los esquemas van como figura.
- Las figuras conservan su número, su pie y su entrada en `FIGURAS.md`.
- Los bloques de código son ejecutables y coherentes con el stack real del TPI.
- Español rioplatense con acentos y ñ correctos, sin excepción.

## 12. Antes de dar por terminado un capítulo criollo

- [ ] Extensión comparable a la del académico (±10 %)
- [ ] Ningún concepto, norma, RFC, regla RN-F o referencia al TPI perdido en la traducción
- [ ] Preámbulo «Antes de empezar» y recuadro `LA IDEA MADRE` presentes
- [ ] Índice numerado de contenidos eliminado
- [ ] Estructura `Qué dice` / `En criollo` en las secciones conceptuales
- [ ] Al menos tres enumeraciones en prosa convertidas en tablas comparativas
- [ ] Una analogía concreta por concepto abstracto
- [ ] Entre 14 y 18 recuadros, contados por emoji:
      `grep -c '^> \*\*[⚠💡🧪📌]' capitulos/NN-*.md`
- [ ] Cierre en el orden obligatorio, con las cinco secciones reescritas
- [ ] Sección `Cierre: las N cosas que hay que recordar` presente
- [ ] Todos los bloques de código y todas las listas de pasos del académico conservados
- [ ] Cero arte ASCII
