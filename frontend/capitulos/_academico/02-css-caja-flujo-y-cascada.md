# Capítulo 2 — CSS: el modelo de caja, el flujo y la cascada

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 2.1. Alcance de la clase

El capítulo anterior terminó con el navegador construyendo un árbol de nodos y
combinándolo con un conjunto de reglas de estilo para producir el árbol de render.
Este capítulo estudia esas reglas: qué son, cómo se resuelven cuando entran en
conflicto y cómo determinan la geometría de cada caja de la pantalla.

Conviene desactivar de entrada una idea equivocada que hace mucho daño: **CSS no
es la capa decorativa del sistema.** Es la capa que decide si un formulario se
puede usar con teclado, si un texto se lee con baja visión, si una tabla de
pedidos entra en un teléfono. La sección 2.5 del TPI —las once reglas obligatorias
del frontend— no habla de colores, pero la regla RN-F06 exige mostrar un estado de
carga mientras la sesión se rehidrata, y la RN-F11 exige que la interfaz siga
siendo utilizable cuando el canal de eventos se cae. **Los dos son problemas de
presentación**, y los dos se resuelven acá.

Hay además una característica de CSS que lo distingue de todo lo demás que este
módulo va a estudiar, y que conviene enunciar desde el principio porque gobierna
la forma de trabajar con él: **CSS nunca falla ruidosamente.** Una propiedad mal
escrita no produce error; se descarta en silencio. Un selector que no coincide con
nada no avisa. Un valor inválido se ignora y la declaración anterior queda en pie.
En JavaScript un error tira una excepción que se ve en la consola; en TypeScript
el compilador se niega a compilar. En CSS no pasa nada de eso: simplemente la
pantalla se ve distinta de lo esperado, sin ninguna explicación.

Esa tolerancia es deliberada —es la misma decisión de diseño de la sección 1.2 del
capítulo anterior, aplicada a los estilos— y tiene una consecuencia metodológica
directa: **en CSS, saber diagnosticar importa más que saber escribir.** Por eso
este capítulo dedica una sección entera a las herramientas de inspección y vuelve
sobre ellas en cada tema.

Al finalizar la clase, el alumno debe poder tomar una interfaz que no se ve como
esperaba, abrir el inspector, **identificar qué regla ganó y por qué**, y corregirla
sin recurrir a `!important`.

**Contenidos**

1. Origen y objetivos de diseño de las hojas de estilo en cascada.
2. Anatomía de una regla y de una declaración.
3. La cascada: origen, importancia, especificidad y orden.
4. Herencia y valores iniciales.
5. El modelo de caja y el problema de `box-sizing`.
6. Colapso de márgenes.
7. El flujo normal: bloque, línea y contextos de formato.
8. Posicionamiento y contextos de apilamiento.
9. Flexbox: distribución en un eje.
10. Grid: distribución en dos ejes.
11. Unidades y diseño adaptable.
12. Tailwind: qué problema resuelve el enfoque *utility-first*.
13. Herramientas de diagnóstico.
14. Evolución: variables, capas, consultas de contenedor.

---

## 2.2. Por qué existe una capa de presentación separada

El HTML original no tenía forma de expresar apariencia, y no por olvido. La
propuesta del CERN describía un formato para **documentos estructurados**: un
título era un título, un párrafo era un párrafo, y cómo se veían era problema del
programa que los mostrara. Cada navegador aplicaba sus propios criterios, y un
mismo documento se veía distinto en cada uno. Eso se consideraba correcto.

Duró poco. A mediados de los noventa la web dejó de usarse sólo para publicar
artículos académicos, y quienes la usaban querían control sobre la apariencia. La
respuesta de los navegadores fue agregar etiquetas de presentación al propio HTML:
`<font>` para tipografía y color, `<center>` para alineación, atributos como
`bgcolor` y `border` desperdigados por todas partes. Netscape e Internet Explorer
competían agregando las suyas, incompatibles entre sí.

El resultado fue un desastre que conviene entender en detalle, porque de sus tres
fallas salieron las tres decisiones de diseño del CSS.

**Primera falla: el documento dejó de ser estructura.** Un título de sección ya no
era un `<h2>`: era un `<font size="5" color="#000080"><b>` dentro de una celda de
tabla. Para el navegador eso es texto en negrita, no un título. Todo lo que el
capítulo anterior explicó sobre el árbol de accesibilidad se perdía: un lector de
pantalla no podía anunciar la estructura porque ya no había estructura que
anunciar.

**Segunda falla: la maquetación con tablas.** Como el HTML no ofrecía forma de
disponer elementos, se usó lo único que colocaba cosas en una grilla: las tablas.
Páginas enteras se construían con tablas anidadas tres y cuatro niveles, rellenas
de imágenes transparentes de un píxel estiradas para forzar separaciones —el
célebre *spacer gif*—. Cambiar el ancho de una columna podía significar reescribir
el documento entero.

**Tercera falla: la duplicación sin límite.** Cada aparición de un título repetía
sus atributos de presentación. Un sitio de doscientas páginas tenía la definición
de su tipografía repetida miles de veces. Cambiar el color corporativo era un
trabajo de días, y siempre quedaban páginas sin actualizar.

Håkon Wium Lie, entonces en el CERN, publicó en octubre de 1994 la propuesta de
*Cascading HTML Style Sheets*. La idea de separar presentación de contenido no era
nueva —existía desde los sistemas de composición tipográfica de los setenta—, y de
hecho había competencia. **DSSSL**, el lenguaje de hojas de estilo para SGML, era
mucho más potente y también mucho más complejo: un lenguaje de programación
completo basado en Scheme. **JSSS**, la propuesta de Netscape, consistía en definir
los estilos con JavaScript.

Ganó CSS, y las razones importan porque explican su forma:

- Era **declarativo**, no un lenguaje de programación. Se podía aprender sin saber
  programar, y en 1996 la mayoría de los autores de páginas web no sabía programar.
- **Degradaba con elegancia**: un navegador que no entendía una propiedad la
  ignoraba y seguía. Eso permitía usar novedades sin romper los navegadores viejos,
  algo que JSSS —al ser código— no podía prometer.
- **No requería que nadie migrara**: se agregaba encima del HTML existente.

CSS1 fue recomendación del W3C en diciembre de 1996; CSS2 en 1998; CSS2.1, que
corrigió y precisó lo anterior, recién en 2011. Desde entonces el estándar dejó de
versionarse como un todo y se desarrolla en **módulos independientes**, cada uno
con su propio nivel. Por eso no existe "CSS3" como especificación: existen decenas
de módulos, algunos en nivel 3, otros en nivel 4 o 5.

De ese origen salen las cuatro decisiones de diseño que este capítulo desarrolla.

**Primera: la cascada.** Varias fuentes de estilo coexisten sobre el mismo
documento y sus conflictos se resuelven por un algoritmo declarado, no por el orden
en que llegaron. La sección 2.5 lo estudia entero.

**Segunda: el control repartido entre tres partes.** Esta es la decisión menos
conocida y la más importante, y merece su propio párrafo más abajo.

**Tercera: la herencia.** Las propiedades tipográficas se heredan de padre a hijo,
de modo que declarar la tipografía una vez en la raíz alcanza para todo el
documento. Es la respuesta directa a la tercera falla.

**Cuarta: la tolerancia al error.** Lo que no se entiende se descarta en silencio,
a nivel de declaración individual. Es lo que permitió que el lenguaje creciera
durante treinta años sin romper nada.

Sobre la segunda decisión conviene detenerse. CSS **no fue diseñado para que el
autor tuviera el control total**. Fue diseñado para repartirlo entre tres partes:
el **navegador**, que aporta sus estilos por defecto; el **usuario**, que puede
imponer los suyos; y el **autor** de la página. Y la prueba de que el reparto va en
serio está en un detalle del algoritmo de la cascada que casi nadie conoce:
**cuando el usuario marca una declaración como `!important`, esa declaración le
gana a la del autor**, incluso si el autor también puso `!important`.

Esto no es una curiosidad. Significa que una persona con baja visión que configura
un tamaño mínimo de letra tiene derecho a que su preferencia se respete por encima
de lo que decidió el diseñador. La consecuencia práctica aparece en la sección 2.11
y es concreta: fijar tamaños de fuente en píxeles rompe ese mecanismo.

> **💡 PARA ENTENDER**
> Fijate en la diferencia con el Capítulo 1. La web resignó garantías **a cambio de
> escalar**. CSS resignó el control del autor **a cambio de que el usuario final
> pueda adaptar la página a sus necesidades**.
>
> Son dos formas distintas de la misma pregunta, y es la que te tenés que hacer
> siempre: *¿qué resignó esto para funcionar, y a favor de quién?*
>
> Acá la respuesta es fuerte: **el que tiene la última palabra sobre cómo se ve una
> página no sos vos, es quien la está leyendo.** Cada vez que escribas CSS que
> impide esa adaptación —y es facilísimo hacerlo sin querer— estás peleándote con
> una decisión de diseño de 1996, y vas a perder de la peor manera: excluyendo
> gente.

---

## 2.3. Cómo el navegador decide el aspecto de un nodo

Antes de escribir reglas conviene recordar dónde encajan. La sección 1.7 describió
el recorrido: el navegador construye el DOM a partir del HTML y el CSSOM a partir
de las hojas de estilo, y de la combinación de ambos sale el árbol de render.

Ese "combinar" es un proceso con nombre propio: **cálculo del valor de cada
propiedad para cada elemento**. Para cada nodo del documento y cada una de las
cientos de propiedades que CSS define, el navegador debe llegar a un único valor
final. El procedimiento tiene cuatro etapas:

1. **Recolección.** Se juntan todas las declaraciones que aplican a ese elemento
   para esa propiedad, vengan de donde vengan.
2. **Cascada.** Si hay más de una, se resuelve el conflicto con el algoritmo de la
   sección 2.5. Queda una sola declaración ganadora.
3. **Herencia o valor inicial.** Si no hubo ninguna declaración, la propiedad toma
   el valor del padre —si es heredable— o su valor inicial.
4. **Cálculo.** El valor se convierte a algo absoluto: `2em` se transforma en
   píxeles, `50%` se resuelve contra el contenedor.

**Todo elemento tiene un valor para toda propiedad, siempre.** No existe la
propiedad "sin definir". Cuando el inspector muestra un valor que nadie escribió,
sale de la etapa 3: o lo heredó, o es el inicial, o es el que el navegador aplica
por defecto.

Esta es la razón por la que un `<h1>` aparece grande y en negrita sin que nadie lo
pida. Existe una hoja de estilos del navegador —la *user-agent stylesheet*— que
declara ese aspecto. No es magia del elemento: es CSS, escrito por el navegador, y
se puede ver en el inspector como cualquier otra regla.

---

## 2.4. Anatomía de una regla

Una hoja de estilos es una secuencia de reglas. Cada regla tiene esta forma:

```css
.tarjeta-producto:hover {
  border-color: #2E74B5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}
```

Las partes, con su nombre normativo:

| Parte | En el ejemplo | Qué hace |
| --- | --- | --- |
| Selector | `.tarjeta-producto:hover` | Determina a qué elementos aplica la regla |
| Bloque de declaraciones | `{ ... }` | Delimita el conjunto de declaraciones |
| Declaración | `border-color: #2E74B5;` | Una asignación de valor a una propiedad |
| Propiedad | `border-color` | Qué aspecto se está definiendo |
| Valor | `#2E74B5` | Qué valor toma |

El selector, a su vez, se compone de **selectores simples** encadenados. En el
ejemplo hay dos: un selector de clase (`.tarjeta-producto`) y una pseudoclase
(`:hover`). Los tipos que más se usan son:

| Tipo | Sintaxis | Coincide con |
| --- | --- | --- |
| Universal | `*` | Cualquier elemento |
| De tipo | `button` | Todos los elementos de esa etiqueta |
| De clase | `.destacado` | Los que llevan esa clase |
| De identificador | `#carrito` | El que lleva ese `id` |
| De atributo | `[type="email"]` | Los que tienen ese atributo con ese valor |
| Pseudoclase | `:focus-visible` | Los que están en ese estado |
| Pseudoelemento | `::before` | Una parte generada del elemento |

Y se relacionan mediante **combinadores**, que expresan la posición relativa en el
árbol del DOM:

| Combinador | Sintaxis | Significa |
| --- | --- | --- |
| Descendiente | `nav a` | Un `a` en cualquier nivel dentro de un `nav` |
| Hijo | `ul > li` | Un `li` que es hijo directo de un `ul` |
| Hermano adyacente | `label + input` | El `input` inmediatamente después de un `label` |
| Hermano general | `h2 ~ p` | Cualquier `p` hermano posterior a un `h2` |

Ahora, el punto que hace a la sección 2.1. **Una declaración con un valor inválido
se descarta individualmente**, sin afectar a las demás:

```css
.precio {
  color: #333333;
  font-size: 18pixeles;   /* inválido: se descarta esta línea sola */
  font-weight: 600;       /* esta se aplica igual */
}
```

Ese comportamiento es la cuarta decisión de diseño de la sección 2.2 en acción, y
tiene dos caras. Permite escribir una propiedad nueva sin miedo a romper
navegadores viejos. Y hace que un error de tipeo sea completamente invisible: nada
falla, nada se registra, la línea simplemente no existe.

> **⚠️ OJO ACÁ**
> **En CSS no hay mensajes de error. Nunca.** Si algo no se ve como esperabas, no
> busques en la consola: no hay nada ahí.
>
> El reflejo correcto es otro: **abrí el inspector y buscá la propiedad en el panel
> de estilos.** Ahí vas a ver una de tres cosas, y cada una te dice algo distinto:
>
> - **No aparece en ningún lado.** Tu selector no coincidió con ese elemento, o
>   escribiste mal el nombre de la propiedad.
> - **Aparece tachada.** Otra regla le ganó en la cascada. Andá a la sección 2.5.
> - **Aparece aplicada pero con otro valor.** El valor que escribiste era inválido y
>   se descartó.
>
> Tres síntomas, tres causas distintas, tres arreglos distintos. **Eso es diagnóstico
> y es la mitad del trabajo con CSS.**

---

## 2.5. La cascada

Cuando varias declaraciones compiten por la misma propiedad del mismo elemento, el
navegador aplica un algoritmo de desempate. Se evalúa en orden, y en cuanto un
criterio decide, los siguientes no se consultan.

*(Ver Figura 2.3: el orden de la cascada.)*

### 2.5.1. Origen e importancia

El primer criterio no es la especificidad, aunque casi todo el mundo lo crea.
Es **de dónde viene la declaración y si está marcada como importante**. El orden,
de menor a mayor prioridad:

| Prioridad | Origen | Importancia |
| --- | --- | --- |
| 1 (más débil) | Navegador | normal |
| 2 | Usuario | normal |
| 3 | Autor | normal |
| 4 | Autor | `!important` |
| 5 | Usuario | `!important` |
| 6 (más fuerte) | Navegador | `!important` |

Fijarse en lo que pasa entre los niveles 3 y 5: **con `!important` el orden se
invierte**. En condiciones normales el autor le gana al usuario, pero cuando ambos
marcan como importante, gana el usuario.

Esa inversión es la decisión de diseño de la sección 2.2 escrita en el algoritmo.
Su propósito es que las preferencias de accesibilidad de una persona no puedan ser
anuladas por el diseñador de un sitio.

### 2.5.2. Especificidad

Si el criterio anterior no alcanzó, se compara la **especificidad** del selector: un
vector de tres números que se compara de izquierda a derecha.

| Componente | Qué cuenta |
| --- | --- |
| A | Selectores de identificador (`#carrito`) |
| B | Clases, atributos y pseudoclases (`.activo`, `[type]`, `:hover`) |
| C | Tipos y pseudoelementos (`div`, `::before`) |

La comparación es **lexicográfica, no numérica**: un solo identificador le gana a
cualquier cantidad de clases. No hay acumulación posible.

| Selector | A | B | C | Comentario |
| --- | --- | --- | --- | --- |
| `p` | 0 | 0 | 1 | |
| `.destacado` | 0 | 1 | 0 | Le gana a cualquier cantidad de tipos |
| `nav ul li a` | 0 | 0 | 4 | Cuatro tipos siguen perdiendo con una clase |
| `.menu .item.activo` | 0 | 3 | 0 | |
| `#carrito` | 1 | 0 | 0 | Le gana a las tres clases anteriores |
| `style="..."` | — | — | — | Los estilos en línea ganan a todo lo anterior |

Tres precisiones que se preguntan siempre:

- El selector universal `*` y los combinadores **no aportan especificidad**.
- La pseudoclase `:not()` no aporta por sí misma, pero **sí aporta su argumento**.
- Las funciones `:is()` y `:where()` difieren justamente en esto: `:is()` toma la
  especificidad de su argumento más específico, mientras que **`:where()` siempre
  vale cero**. Esa es su razón de existir: escribir reglas fáciles de sobrescribir.

> **⚠️ OJO ACÁ**
> **La especificidad no se suma. Se compara de a columnas, y la primera que difiere
> decide.**
>
> Esto choca de frente con la intuición. Mirá:
>
> - `body div.contenedor ul li a.enlace.activo` → `(0, 3, 4)`
> - `#menu` → `(1, 0, 0)`
>
> El primero tiene siete selectores. El segundo tiene uno. **Gana el segundo**, y no
> por poco: gana antes de que la comparación llegue siquiera a mirar las clases.
>
> Es como comparar 0,34 con 1,00. Por más decimales que agregues, nunca vas a
> pasar el 1. Por eso pelearle a un `#identificador` agregando clases es perder el
> tiempo, y por eso conviene no usar identificadores para estilar: **te dejan sin
> margen de maniobra hacia arriba.**

### 2.5.3. Orden de aparición

Si dos declaraciones empatan en origen, importancia y especificidad, **gana la
última que aparece**. De acá sale que el orden de los archivos importe, y que la
regla práctica sea cargar lo general antes que lo particular.

### 2.5.4. Herencia y valores iniciales

Cuando ninguna declaración aplica a un elemento, la propiedad toma su valor por
uno de dos caminos.

Si la propiedad es **heredable**, toma el valor del padre. Lo son casi todas las
tipográficas: `color`, `font-family`, `font-size`, `line-height`, `text-align`,
`visibility`. Declararlas una vez en `html` o `body` alcanza para todo el
documento.

Si **no** es heredable, toma su **valor inicial**, definido por la especificación.
No lo son las de caja y disposición: `margin`, `padding`, `border`, `width`,
`display`, `background`. Y la razón es de sentido común: si el `padding` se
heredara, un contenedor con relleno se lo impondría a cada uno de sus
descendientes.

> **⚠️ OJO ACÁ**
> Sobre `!important`, la regla es simple y conviene tomarla en serio: **casi nunca
> lo necesitás, y usarlo es endeudarte.**
>
> La secuencia es siempre la misma. Ponés un `!important` para ganarle a una regla
> que no entendés. Semanas después alguien necesita sobrescribir la tuya, y como no
> puede por especificidad, pone otro `!important`. Y así hasta que la hoja de
> estilos es una pila de importantes peleándose entre ellos, donde ya no se puede
> cambiar nada sin romper otra cosa.
>
> Cuando sientas la necesidad de usarlo, **abrí el inspector y averiguá qué regla te
> está ganando y por qué.** El noventa por ciento de las veces la solución es
> arreglar un selector, no escalar la guerra.
>
> La excepción legítima existe: sobrescribir estilos de una biblioteca de terceros
> que no podés editar. Ahí es una herramienta, no una deuda.

---

## 2.6. El modelo de caja

### 2.6.1. Las cuatro cajas

Todo elemento del árbol de render genera al menos una caja rectangular. Esa caja
tiene cuatro áreas concéntricas, y cada una responde a una pregunta distinta:

| Área | Delimitada por | Contiene | Se ve el fondo |
| --- | --- | --- | --- |
| Contenido | `width`, `height` | El texto o los hijos | Sí |
| Relleno (*padding*) | `padding` | Espacio interior | Sí |
| Borde | `border` | La línea del borde | El borde mismo |
| Margen | `margin` | Espacio exterior | No, siempre transparente |

*(Ver Figura 2.1: las cuatro áreas del modelo de caja.)*

La distinción entre relleno y margen es la que más se confunde, y el criterio para
elegir es preciso: **el relleno es espacio de adentro, el margen es espacio de
afuera**. El fondo del elemento llega hasta el borde exterior del relleno, así que
si el elemento tiene color de fondo, se ve en el relleno y no en el margen. Y como
se verá enseguida, sólo los márgenes colapsan.

### 2.6.2. `box-sizing` y el modelo "equivocado"

Acá aparece la trampa más conocida de CSS, y tiene una historia que vale la pena
contar porque el estándar terminó adoptando la solución de quien se había
equivocado.

Por defecto, `width` define el ancho del **área de contenido solamente**. El
relleno y el borde se suman por fuera. Un elemento declarado así:

```css
.tarjeta {
  width: 300px;
  padding: 20px;
  border: 2px solid #999999;
}
```

ocupa en pantalla `300 + 20 + 20 + 2 + 2 = 344` píxeles.

Ese comportamiento es correcto según CSS1 y es contraintuitivo para casi todo el
mundo. Cuando alguien dice "esta caja mide 300 píxeles" está pensando en lo que
ocupa, no en lo que le queda adentro.

La ironía histórica es la siguiente. Internet Explorer 5, en su modo de
compatibilidad, implementó el modelo **al revés**: `width` incluía relleno y borde.
Durante años eso se consideró un error de Microsoft y fue una de las principales
fuentes de incompatibilidad entre navegadores. Con el tiempo quedó claro que ese
"error" era el modelo que la gente realmente quería, y CSS3 lo incorporó como
opción:

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

Con esa declaración, `width` pasa a incluir relleno y borde, y la tarjeta del
ejemplo mide exactamente 300 píxeles.

*(Ver Figura 2.2: `content-box` frente a `border-box`.)*

Prácticamente todo proyecto moderno incluye esa regla, y **Tailwind la trae en su
capa base**. Vale la pena saber que está ahí y qué hace: es la primera línea de
todo lo que se va a maquetar.

> **📌 NOTA**
> Esta historia es de las mejores del CSS y conviene que la tengas presente:
>
> **El modelo que hoy usa todo el mundo era el "error" de Internet Explorer.**
>
> Durante años, `border-box` fue *el bug de Microsoft*. Los estándares decían
> `content-box`, IE hacía otra cosa, y eso era una de las principales fuentes de
> incompatibilidad entre navegadores.
>
> Con el tiempo quedó claro que ese "error" era **el modelo que la gente realmente
> quería**, y CSS3 lo incorporó como opción. Hoy no vas a encontrar un proyecto serio
> que no lo active en la primera línea.
>
> ¿Y qué te llevás de esto? Que **"cumple el estándar" y "es lo correcto" no siempre
> coinciden.** A veces el estándar se equivocó y tarda quince años en corregirse.
> Saber cuál es cuál es criterio, y eso no te lo da ninguna documentación.

### 2.6.3. Colapso de márgenes

Los márgenes verticales adyacentes **no se suman: se fusionan**, y el resultado es
el mayor de los dos. Un párrafo con 20 píxeles de margen inferior seguido de otro
con 30 de margen superior quedan separados por 30, no por 50.

El comportamiento hereda de la composición tipográfica, donde el espacio entre dos
bloques es una propiedad de la relación entre ellos y no la suma de dos pedidos
independientes. Ocurre en tres situaciones: entre hermanos adyacentes, entre un
padre y su primer o último hijo, y en un elemento vacío consigo mismo.

Lo relevante en la práctica es cómo se evita, porque el colapso entre padre e hijo
produce el efecto desconcertante de un margen que "se escapa" del contenedor. Se
interrumpe con relleno o borde en el padre, o estableciendo un contexto de formato
nuevo —por ejemplo con `display: flex` o `display: grid`—.

Y ahí está la razón de fondo por la que en un contenedor flex los márgenes ya no
colapsan: **el colapso es una propiedad del flujo normal, y Flexbox no es flujo
normal.** La sección siguiente explica qué significa eso.

> **🧪 EXPERIMENTO**
> El colapso entre padre e hijo es el que más desconcierta, porque parece que el
> margen se escapara de la caja. Comprobalo:
>
> 1. Hacé un `div` con fondo de color y adentro un `<p>` con `margin-top: 40px`.
> 2. Mirá el resultado. **El que se movió hacia abajo es el `div` entero**, no el
>    párrafo dentro de él. El margen del hijo salió por arriba del padre.
> 3. Ahora agregale al `div` un `padding-top: 1px`. El párrafo se acomoda adentro y
>    el `div` deja de moverse.
> 4. Sacá el relleno y probá con `display: flow-root` en el `div`. Mismo resultado,
>    sin agregar un píxel de nada.
>
> ¿Por qué pasa? Porque si no hay nada entre el borde del padre y el margen del
> hijo —ni relleno, ni borde, ni un contexto de formato nuevo—, para el motor de
> disposición **son el mismo margen**. Un píxel de relleno alcanza para separarlos.
>
> Cuando veas un espacio que no pusiste o un contenedor que se corrió solo,
> **sospechá de esto primero.**

---

## 2.7. El flujo normal

### 2.7.1. Bloque y línea

El **flujo normal** es la disposición por defecto: cómo se ubican las cajas cuando
nadie indica lo contrario. Tiene dos comportamientos según el elemento.

Los elementos de **bloque** —`div`, `p`, `h1`, `section`— ocupan todo el ancho
disponible, se apilan uno debajo del otro y aceptan dimensiones y márgenes en las
cuatro direcciones.

Los elementos **en línea** —`span`, `a`, `strong`, `em`— ocupan sólo lo que su
contenido necesita, se ubican uno al lado del otro y siguen el sentido del texto.
Y tienen dos restricciones que sorprenden: **ignoran `width` y `height`**, y
**aceptan márgenes horizontales pero no verticales**. Un `<span>` con
`margin-top: 40px` no se mueve.

La razón es coherente: un elemento en línea es parte del renglón, y un renglón
tiene su altura determinada por la tipografía. Permitir que un fragmento de texto
empuje verticalmente al renglón que lo contiene rompería la composición del
párrafo. Cuando se necesitan dimensiones verticales existe `display: inline-block`,
que se comporta como línea hacia afuera y como bloque hacia adentro.

### 2.7.2. Contextos de formato

Un **contexto de formato** es una región del documento con sus propias reglas de
disposición. El flujo normal es uno; Flexbox y Grid crean otros distintos.

Este concepto explica varios comportamientos que de otro modo parecen arbitrarios:
por qué los márgenes dejan de colapsar dentro de un contenedor flex (sección
2.6.3), por qué un elemento flotante deja de desbordar a su contenedor cuando se
establece un contexto nuevo, y por qué `display` cambia tantas cosas a la vez.
**`display` no cambia una propiedad: cambia el conjunto de reglas bajo el cual el
elemento y sus hijos se disponen.**

### 2.7.3. Posicionamiento

La propiedad `position` permite sacar un elemento del flujo o desplazarlo respecto
de él. Sus cinco valores y sus diferencias reales:

| Valor | ¿Sigue en el flujo? | Referencia del desplazamiento |
| --- | --- | --- |
| `static` | Sí | No admite desplazamiento; es el valor por defecto |
| `relative` | **Sí** | Su propia posición original |
| `absolute` | **No** | El ancestro posicionado más cercano |
| `fixed` | No | La ventana del navegador |
| `sticky` | Sí | Alterna entre relativo y fijo según el desplazamiento |

La distinción entre `relative` y `absolute` es la que más consecuencias tiene.
`relative` desplaza visualmente el elemento **pero le conserva su lugar en el
flujo**: el hueco sigue ahí y los demás no se corren. `absolute` lo saca del flujo
por completo: los demás elementos se acomodan como si no existiera.

Y de ahí sale el patrón más usado de posicionamiento: un contenedor con
`position: relative` que no se mueve —porque no se le dan valores de
desplazamiento— y existe únicamente para servir de referencia a un hijo con
`position: absolute`. Sin ese ancestro, el hijo absoluto se posiciona respecto del
documento y aparece en cualquier parte.

> **💡 PARA ENTENDER**
> Ese `position: relative` que no mueve nada parece código al pedo. **No lo es: es
> lo más importante de la regla.**
>
> Un elemento `absolute` busca hacia arriba, padre por padre, hasta encontrar el
> primero que tenga `position` distinto de `static`. Ese es su marco de referencia.
> Si no encuentra ninguno, usa el documento entero.
>
> Por eso el síntoma clásico es tan raro: **el badge del carrito, en vez de quedar
> en la esquina del ícono, aparece arriba a la izquierda de toda la página.** No
> está roto el `top: 0; right: 0` — está midiendo contra la página porque nadie le
> dio un marco más cercano.
>
> Regla mental: **cada `absolute` necesita su `relative`.** Si el hijo se te fue de
> viaje, no toques al hijo: fijate qué le falta al padre.

---

## 2.8. Flexbox

Flexbox resuelve la distribución de elementos **en un solo eje**. Nació para
reemplazar los flotantes, que se usaban para maquetar aunque estaban diseñados
para otra cosa: hacer que el texto rodee una imagen.

El modelo se organiza alrededor de dos ejes, y esta es la clave para no perderse:

- El **eje principal**, cuya dirección define `flex-direction`.
- El **eje cruzado**, siempre perpendicular al principal.

Las propiedades de alineación se refieren a los ejes, no a "horizontal" y
"vertical". `justify-content` alinea sobre el eje principal y `align-items` sobre
el cruzado. Cuando `flex-direction` es `column`, el eje principal pasa a ser el
vertical y las dos propiedades intercambian su efecto visual.

*(Ver Figura 2.4: los ejes de Flexbox y el efecto de `flex-direction`.)*

Las propiedades del contenedor:

| Propiedad | Qué controla | Valores frecuentes |
| --- | --- | --- |
| `flex-direction` | Dirección del eje principal | `row`, `column` |
| `justify-content` | Distribución en el eje principal | `flex-start`, `center`, `space-between` |
| `align-items` | Alineación en el eje cruzado | `stretch`, `center`, `flex-start` |
| `flex-wrap` | Si los elementos saltan de línea | `nowrap`, `wrap` |
| `gap` | Separación entre elementos | Cualquier longitud |

Y las de cada hijo, que se resumen en la abreviatura `flex`:

| Propiedad | Qué controla | Valor inicial |
| --- | --- | --- |
| `flex-grow` | Cuánto crece si sobra espacio | `0` |
| `flex-shrink` | Cuánto se encoge si falta | `1` |
| `flex-basis` | Tamaño de partida antes de repartir | `auto` |

`gap` merece una mención aparte. Antes de existir, separar elementos exigía poner
margen a todos y quitárselo al último con un selector como `:last-child`. `gap`
declara la separación **entre** elementos, sin agregar nada en los extremos. Es un
buen ejemplo de cómo el CSS moderno reemplaza patrones que fueron obligatorios
durante años.

---

## 2.9. Grid

Grid resuelve la distribución **en dos ejes simultáneos**. Es el reemplazo legítimo
de la maquetación con tablas de la sección 2.2: hace lo que se intentaba hacer con
ellas, pero sin tocar la estructura del documento.

La diferencia con Flexbox conviene enunciarla con precisión, porque no es "uno es
para poco y otro para mucho":

- **Flexbox parte del contenido.** Los elementos se acomodan según su tamaño y el
  espacio disponible. Es un modelo de una dimensión.
- **Grid parte del contenedor.** Se define primero la grilla y después se colocan
  los elementos en ella. Es un modelo de dos dimensiones.

Se usan juntos permanentemente: Grid para la disposición general de la página,
Flexbox para el interior de cada componente.

> **📌 NOTA**
> Para decidir cuál usar, no te preguntes cuál es más moderno ni cuál es más
> potente. Preguntate una sola cosa:
>
> **¿Quién manda sobre el tamaño, el contenido o vos?**
>
> - Si querés que los elementos se acomoden según lo que miden —una barra de
>   navegación donde cada ítem ocupa lo que dice su texto— **eso es Flexbox**.
> - Si querés que los elementos entren en una estructura que definiste de antemano
>   —un catálogo donde todas las tarjetas miden igual sin importar el nombre del
>   producto— **eso es Grid**.
>
> Y ojo con la trampa de "Flexbox es para cosas chicas". No es una cuestión de
> escala: es una cuestión de **quién decide la medida**. Podés tener un Grid de dos
> celdas y un Flexbox con cuarenta elementos, y estar bien en los dos casos.

```css
.catalogo {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}
```

Esas tres líneas producen una grilla adaptable sin una sola consulta de medios, y
conviene desarmarlas porque cada función hace algo específico:

- **`1fr`** es una unidad propia de Grid que significa "una fracción del espacio
  sobrante", repartido después de descontar lo fijo.
- **`minmax(220px, 1fr)`** declara que cada columna mide como mínimo 220 píxeles y
  como máximo una fracción del sobrante.
- **`repeat(auto-fill, ...)`** crea tantas columnas como entren, calculado por el
  navegador según el ancho real del contenedor.

*(Ver Figura 2.5: una grilla con `auto-fill` y `minmax` en tres anchos distintos.)*

---

## 2.10. Unidades y diseño adaptable

La elección de unidad no es estilística: determina si el diseño responde a las
preferencias del usuario o las ignora.

| Unidad | Relativa a | Uso recomendado |
| --- | --- | --- |
| `px` | Nada; es absoluta | Bordes, sombras, detalles que no deben escalar |
| `rem` | Tamaño de fuente de la raíz | **Tipografía y espaciados** |
| `em` | Tamaño de fuente del propio elemento | Espaciados que deben acompañar al texto |
| `%` | La misma propiedad del contenedor | Anchos dentro de un contenedor |
| `vw` / `vh` | Ancho / alto de la ventana | Secciones a pantalla completa |
| `ch` | Ancho del carácter "0" | Ancho de columnas de texto |

La distinción entre `rem` y `px` en la tipografía es la que tiene consecuencias
reales, y es donde la sección 2.2 se vuelve concreta.

Todo navegador permite configurar un tamaño de fuente base. Por defecto son 16
píxeles, y una persona con dificultades de visión puede subirlo. **Un tamaño
declarado en `rem` se multiplica por esa base y respeta la preferencia. Uno
declarado en `px` la ignora por completo.**

Poner `font-size: 14px` en el cuerpo de un documento significa, en la práctica,
decidir que la preferencia de accesibilidad de esa persona no se aplica en tu
sitio. Rara vez es una decisión consciente, y casi siempre es lo que termina
pasando.

> **🧪 EXPERIMENTO**
> Esto lo vas a recordar toda la carrera, así que hacelo de verdad.
>
> 1. Entrá a la configuración de tu navegador y buscá el tamaño de fuente. Subilo a
>    24 píxeles, que es lo que usa mucha gente con baja visión.
> 2. Ahora navegá tres o cuatro sitios que uses todos los días.
>
> Vas a ver tres comportamientos distintos. Algunos sitios agrandan todo y se leen
> perfecto: usaron `rem`. Otros no cambian nada: usaron `px`. Y otros agrandan
> **sólo una parte** y se rompen, con textos que se salen de sus cajas y botones
> pisados: mezclaron las dos unidades sin darse cuenta.
>
> 3. Anotá cuál es cuál. Volvé a 16 antes de seguir.
>
> Lo que acabás de ver no es un detalle de accesibilidad para una minoría. **Es lo
> que le pasa todos los días a alguien que necesita letra más grande para leer**, y
> es la diferencia entre poder comprar en un sitio o no poder.

Las **consultas de medios** permiten aplicar reglas según características del
dispositivo. La práctica establecida es escribir primero para pantalla angosta y
agregar reglas hacia arriba, y la razón es concreta: el diseño angosto es el caso
restrictivo, y partir de él obliga a resolver lo difícil primero.

```css
.catalogo { grid-template-columns: 1fr; }

@media (min-width: 48rem) {
  .catalogo { grid-template-columns: repeat(2, 1fr); }
}
```

Existe además una consulta que no habla del tamaño sino de una preferencia
declarada del usuario, y que conviene incorporar como hábito:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Para muchas personas con trastornos vestibulares, una animación de desplazamiento
produce mareo real. Esa consulta lee una preferencia que ya está configurada en el
sistema operativo. **Es de los pocos lugares donde `!important` está plenamente
justificado**, porque debe ganarle a cualquier animación declarada después.

---

## 2.11. Tailwind: qué problema resuelve el enfoque *utility-first*

El stack del TPI declara Tailwind CSS 3.x. Antes de usarlo conviene entender qué
vino a resolver, porque el problema no es el que suele suponerse.

### 2.11.1. El problema de las hojas que sólo crecen

Durante años la buena práctica fue el llamado *CSS semántico*: nombrar las clases
según **lo que el elemento es**, no según cómo se ve. Metodologías como BEM
formalizaron ese enfoque con convenciones de nombre estrictas.

La promesa era reutilización y mantenibilidad. En proyectos grandes el resultado
observado fue otro, y se manifestó en tres síntomas.

**Nadie borra CSS.** Cuando se elimina un componente, su CSS queda. Borrarlo exige
estar seguro de que ninguna otra parte lo usa, y esa certeza es difícil de
alcanzar. Ante la duda, se deja. **La hoja de estilos sólo crece.**

**Nombrar cuesta más de lo que parece.** Decidir si un contenedor es `.tarjeta`,
`.item-catalogo` o `.producto-preview` consume tiempo real y nunca hay una
respuesta correcta. Y cuando el diseño cambia, el nombre queda mintiendo: una clase
llamada `.barra-lateral` que ahora es una fila superior.

**Modificar da miedo.** Cambiar una regla existente puede afectar lugares que no se
tienen a la vista, y eso lleva a una estrategia defensiva: en vez de modificar, se
agrega otra clase más específica. Lo que refuerza el primer síntoma.

Adam Wathan publicó Tailwind en 2017 con una inversión de la premisa: **las clases
no describen qué es el elemento, describen cómo se ve.**

```html
<article class="rounded-lg border border-slate-200 p-4 shadow-sm">
  <h3 class="text-lg font-semibold text-slate-900">Milanesa napolitana</h3>
  <p class="mt-1 text-sm text-slate-600">Con papas fritas</p>
</article>
```

Las tres consecuencias son el reverso exacto de los tres síntomas. **La hoja de
estilos deja de crecer**, porque el conjunto de utilidades es finito y se comparte:
agregar un componente nuevo no agrega CSS. **No hay que nombrar nada.** Y **modificar
deja de dar miedo**, porque el alcance de un cambio es visiblemente el elemento que
se está editando.

### 2.11.2. Cómo funciona realmente

Tailwind no es una hoja de estilos que se enlaza: es una herramienta que se ejecuta
durante la construcción del proyecto. Su funcionamiento tiene tres pasos:

1. **Escanea** los archivos de origen configurados, buscando texto que parezca un
   nombre de clase.
2. **Genera** únicamente el CSS de las clases que encontró.
3. **Emite** una hoja que en producción suele pesar unos pocos kilobytes.

Del paso 1 se desprende una limitación que causa problemas reales y que conviene
saber de antemano: **el escaneo es textual, no ejecuta el código.** Una clase
construida por concatenación en tiempo de ejecución no se encuentra, y por lo tanto
su CSS no se genera:

```ts
// NO funciona: la cadena completa no existe en el archivo
const clase = `text-${color}-500`;

// Sí funciona: las dos cadenas completas están escritas
const clase = activo ? "text-green-500" : "text-slate-500";
```

Este es el error número uno de quien empieza con Tailwind, y es especialmente
desconcertante porque **funciona en desarrollo y falla en producción** en algunas
configuraciones. El diagnóstico correcto es buscar la clase en el CSS generado: si
no está, el problema es el escaneo, no el estilo.

### 2.11.3. Qué se gana y qué se pierde

Fiel a la pregunta del Capítulo 1, corresponde enunciar lo que se resigna.

**El marcado se vuelve ruidoso.** Un elemento con doce utilidades es más difícil de
leer que uno con una clase. Es una crítica válida y no tiene refutación: se acepta
a cambio de lo demás.

**La abstracción se muda al componente.** Cuando una combinación de utilidades se
repite, la solución no es crear una clase sino extraer un componente. Eso funciona
bien en un proyecto con componentes y no funciona en uno que no los tiene.

**Aparece una dependencia de construcción.** Sin la herramienta ejecutándose no hay
estilos. Es el mismo intercambio que el Capítulo 7 va a estudiar con Vite.

> **📌 NOTA**
> Tailwind **no te exime de entender CSS**: te exime de nombrar cosas.
>
> `flex items-center justify-between` es exactamente `display: flex;
> align-items: center; justify-content: space-between`. Si no entendiste la sección
> 2.8, esas tres utilidades son tres palabras mágicas que copiás de algún lado y no
> sabés por qué a veces funcionan y a veces no.
>
> Esto importa especialmente ahora que vas a trabajar con agentes de IA. Un agente
> te va a escribir Tailwind sin dudar y le va a salir plausible. Para saber si está
> bien —si ese `items-center` alinea sobre el eje que vos querés, si ese `px` debería
> ser `rem`, si ese contraste alcanza— **tenés que saber CSS.** La herramienta te
> ahorra tipeo, no criterio.

---

## 2.12. Herramientas de diagnóstico

El panel de elementos del navegador es el instrumento central de este capítulo.
Cuatro zonas concentran lo que hace falta.

**El panel de estilos** muestra todas las reglas que aplican al elemento
seleccionado, **ordenadas por prioridad de la cascada**: la ganadora arriba. Las
declaraciones perdedoras aparecen **tachadas**, y ahí se ve directamente el
resultado del algoritmo de la sección 2.5. Cada regla indica además de qué archivo
y línea proviene, y las reglas del navegador aparecen identificadas como tales.

*(Ver Figura 2.6: el panel de estilos con reglas tachadas por la cascada.)*

**El panel de valores calculados** muestra el valor final de cada propiedad después
de las cuatro etapas de la sección 2.3. Es el lugar para responder "¿cuánto mide
realmente este `2em`?".

**El diagrama del modelo de caja** presenta las cuatro áreas de la sección 2.6 con
sus medidas reales. Es la forma más rápida de descubrir que un espacio inesperado
es un margen y no un relleno.

*(Ver Figura 2.7: el inspector del modelo de caja.)*

**Las superposiciones de Flexbox y Grid** dibujan sobre la página las líneas de la
grilla y los ejes del contenedor flex. Para Grid, además, numera las líneas, que es
lo que permite entender por qué un elemento cayó donde cayó.

Vale mencionar dos comprobaciones adicionales que el navegador ofrece y que se usan
poco. La **verificación de contraste** aparece en el selector de color e indica si
la combinación de texto y fondo alcanza el mínimo exigido por las pautas de
accesibilidad. Y la **emulación de preferencias** permite forzar
`prefers-reduced-motion` o el esquema de color oscuro sin cambiar la configuración
del sistema.

---

## 2.13. Seguridad y evolución

CSS no tiene la superficie de ataque de JavaScript, pero tampoco es inocuo. Dos
consideraciones son pertinentes.

**CSS puede exfiltrar información.** Un selector de atributo combinado con una
imagen de fondo permite deducir el contenido de un campo carácter por carácter,
porque cada coincidencia dispara una petición a un servidor externo. Es la razón
por la que el encabezado `Content-Security-Policy` de la sección 16.5 del TPI
también restringe los orígenes de las hojas de estilo y no sólo los de los scripts.

**CSS puede destruir la accesibilidad.** Es el riesgo real y el más frecuente.
Tres formas de conseguirlo sin proponérselo:

- Eliminar el indicador de foco con `outline: none` sin reemplazarlo. Quien navega
  con teclado pierde toda referencia de dónde está parado. Si el contorno por
  defecto no gusta, se reemplaza con `:focus-visible`, **nunca se elimina**.
- Ocultar contenido con `display: none` cuando se pretendía sólo ocultarlo
  visualmente. Ese contenido desaparece también para los lectores de pantalla. Para
  texto que debe ser leído pero no visto existe el patrón conocido como
  *visually hidden*.
- Reordenar visualmente con `order` de Flexbox o con Grid. **El orden de tabulación
  sigue el DOM, no el visual.** Un reordenamiento importante produce un recorrido de
  teclado que salta por la pantalla sin lógica aparente.

En cuanto a la evolución del lenguaje, cuatro incorporaciones recientes resuelven
problemas que durante años exigieron herramientas externas:

Las **propiedades personalizadas** —las variables de CSS— son valores nombrados que
se heredan y pueden leerse y modificarse desde JavaScript, algo que las variables
de los preprocesadores nunca pudieron hacer porque se resolvían antes de llegar al
navegador.

Las **capas en cascada** (`@layer`) agregan un nivel al algoritmo de la sección
2.5, entre el origen y la especificidad. Permiten declarar que un conjunto de
reglas siempre le gana a otro **sin recurrir a la especificidad ni a `!important`**,
que era exactamente el problema que llevaba a la deuda descrita más arriba.

Las **consultas de contenedor** (`@container`) permiten que un componente responda
al ancho de su contenedor y no al de la ventana. Es lo que las consultas de medios
nunca pudieron hacer, y resuelve el caso de un mismo componente que debe verse
distinto en la barra lateral y en el cuerpo principal.

La pseudoclase **`:has()`** permite seleccionar un elemento según lo que contiene
—lo que durante veinte años se pidió como "el selector del padre"—, y hace posible
resolver con CSS cosas que antes exigían JavaScript.

---

## 2.14. Verificación

1. Abrir el inspector sobre un elemento cualquiera y **enumerar las reglas que le
   aplican en orden de prioridad**, identificando cuál ganó y por qué.
2. Encontrar una declaración tachada y explicar cuál de los criterios de la sección
   2.5 la dejó afuera.
3. Calcular a mano la especificidad de tres selectores del proyecto y verificar el
   resultado ordenándolos en el inspector.
4. Medir un elemento con el diagrama del modelo de caja y **verificar la suma** de
   contenido, relleno y borde según el valor de `box-sizing`.
5. Producir deliberadamente un colapso de márgenes entre padre e hijo y
   neutralizarlo de dos maneras distintas.
6. Construir una fila con Flexbox y comprobar qué propiedades cambian de efecto al
   pasar `flex-direction` de `row` a `column`.
7. Construir una grilla adaptable con `auto-fill` y `minmax` y verificar en el
   inspector cuántas columnas genera en tres anchos distintos.
8. Cambiar el tamaño de fuente base del navegador a 24 píxeles y **verificar que la
   interfaz propia sigue siendo utilizable**.
9. Recorrer la interfaz propia con la tecla Tab y confirmar que el indicador de foco
   es visible en todos los elementos interactivos.

---

## 2.15. Errores frecuentes

**Buscar errores de CSS en la consola.** No hay ninguno: el lenguaje descarta en
silencio. El lugar correcto es el panel de estilos, con los tres síntomas de la
sección 2.4 (secciones 2.1 y 2.4).

**Escalar la guerra de `!important`.** Se pone uno para ganarle a una regla que no
se entiende, y el siguiente necesita otro. La salida es diagnosticar qué regla gana
y por qué (sección 2.5.4).

**Creer que la especificidad se acumula.** Diez clases no le ganan a un
identificador: la comparación es lexicográfica, no numérica (sección 2.5.2).

**Olvidar `box-sizing: border-box`.** Produce desbordes que se atribuyen a otras
causas, sobre todo en anchos porcentuales combinados con relleno (sección 2.6.2).

**Sumar márgenes verticales que en realidad colapsan.** La separación medida no
coincide con la esperada y se compensa con más margen, lo que empeora el problema
(sección 2.6.3).

**Aplicar `width` o `margin-top` a un elemento en línea.** Se ignoran, sin aviso.
Hace falta `inline-block` o cambiar el contexto (sección 2.7.1).

**Posicionar en absoluto sin ancestro posicionado.** El elemento se ubica respecto
del documento y aparece en un lugar imprevisto (sección 2.7.3).

**Confundir `justify-content` con `align-items`.** Se refieren a ejes, no a
direcciones fijas, y su efecto visual se invierte con `flex-direction: column`
(sección 2.8).

**Construir nombres de clase de Tailwind por concatenación.** El escaneo es textual
y no encuentra la clase, así que su CSS no se genera. Suele funcionar en desarrollo
y fallar en producción (sección 2.11.2).

**Fijar la tipografía en píxeles.** Anula la preferencia de tamaño del usuario, que
es la decisión de diseño de la sección 2.2 (sección 2.10).

**Eliminar el contorno de foco.** Deja inutilizable la navegación por teclado. Se
reemplaza con `:focus-visible`, no se elimina (sección 2.13).

---

## 2.16. Actividades

1. **Auditoría de cascada.** Elegir tres elementos de un sitio real y documentar,
   para la propiedad `color` de cada uno, todas las declaraciones que compiten,
   cuál ganó y en qué criterio de la sección 2.5 se decidió.

2. **Especificidad a mano.** Calcular el vector de especificidad de ocho selectores
   dados, ordenarlos, y verificar el orden construyendo un documento donde todos
   apunten al mismo elemento con colores distintos.

3. **El modelo de caja medido.** Construir una tarjeta de producto con ancho,
   relleno y borde declarados, medir su ancho real en el inspector con
   `box-sizing: content-box`, cambiar a `border-box` y volver a medir. Explicar la
   diferencia con la suma correspondiente.

4. **Catálogo adaptable.** Maquetar una grilla de tarjetas de producto que pase de
   una a cuatro columnas según el ancho disponible, **sin usar consultas de
   medios**, con `auto-fill` y `minmax`. Documentar en qué anchos exactos cambia el
   número de columnas.

5. **Traducción de Tailwind.** Tomar un componente escrito con doce utilidades de
   Tailwind y escribir el CSS equivalente con una sola clase. Comparar ambos en
   cantidad de líneas y en facilidad para modificar un valor.

6. **Exploración: la preferencia del usuario.** Configurar el navegador con tamaño
   de fuente de 24 píxeles y auditar tres sitios de uso cotidiano, documentando cuál
   escala correctamente, cuál no escala y cuál se rompe. Relacionar lo observado con
   la segunda decisión de diseño de la sección 2.2 y explicar qué unidad usó cada
   uno. *(Requiere revertir la configuración al terminar.)*

7. **Exploración: el costo del reordenamiento visual.** Construir una fila con
   Flexbox de cinco elementos interactivos y reordenarlos visualmente con la
   propiedad `order`. Recorrerla con la tecla Tab y documentar el recorrido
   resultante. Relacionar lo observado con la afirmación de la sección 2.13 sobre el
   orden de tabulación, y proponer una solución que no dependa de `order`.
   *(Requiere navegación por teclado.)*

---

## 2.17. Síntesis

1. CSS existe porque **mezclar presentación y estructura destruye la estructura**.
   Las etiquetas de presentación de los noventa produjeron documentos ilegibles para
   toda herramienta que no fuera un navegador gráfico, y esa pérdida es la que el
   Capítulo 1 describió al hablar del árbol de accesibilidad.

2. La decisión de diseño más importante del lenguaje es que **el control está
   repartido entre navegador, usuario y autor**, y que en caso de conflicto marcado
   como importante **gana el usuario**. Todo lo que impide esa adaptación —empezando
   por la tipografía en píxeles— trabaja en contra del diseño del lenguaje.

3. **CSS nunca falla ruidosamente.** No hay excepciones ni errores de compilación:
   lo inválido se descarta en silencio. Por eso el trabajo con CSS es principalmente
   diagnóstico, y el panel de estilos es la herramienta central.

4. La cascada resuelve conflictos en un orden fijo: **origen e importancia, luego
   capas, luego especificidad, y por último orden de aparición.** La especificidad
   no es lo primero, aunque casi todos lo crean.

5. La especificidad **se compara lexicográficamente, no se suma**. Un identificador
   le gana a cualquier cantidad de clases, y por eso `!important` no es una solución
   sino una deuda que el siguiente va a tener que pagar.

6. `width` **no define lo que el elemento ocupa** salvo que se declare
   `box-sizing: border-box`. El modelo que hoy se considera correcto fue durante
   años el error de Internet Explorer.

7. Los márgenes verticales **colapsan**: se fusionan tomando el mayor. Es una
   propiedad del flujo normal, y por eso desaparece dentro de un contenedor flex o
   grid, que establecen contextos de formato distintos.

8. **`display` no cambia una propiedad: cambia el conjunto de reglas** bajo el cual
   el elemento y sus hijos se disponen. Eso explica por qué cambia tantas cosas a la
   vez.

9. Flexbox y Grid no compiten: **uno parte del contenido en un eje, el otro del
   contenedor en dos.** Se usan juntos, Grid para la página y Flexbox para el
   interior de los componentes.

10. Tailwind no resuelve un problema de estética sino de **crecimiento sin límite de
    las hojas de estilo**. Resigna legibilidad del marcado a cambio de que agregar
    componentes deje de agregar CSS. Y no exime de saber CSS: exime de nombrar.

11. **El orden de tabulación sigue el DOM, no lo visual.** Todo reordenamiento hecho
    con CSS que altere el orden lógico produce una interfaz que se ve bien y se
    recorre mal.

---

## 2.18. Referencias y lecturas complementarias

La especificación de CSS no es un documento único sino un conjunto de módulos
independientes del W3C, todos accesibles desde `www.w3.org/Style/CSS/`. Los
pertinentes a este capítulo son **CSS Cascading and Inheritance Level 5**, que
define el algoritmo de la sección 2.5 y las capas en cascada; **CSS Display Level
3**, que formaliza el flujo normal y los contextos de formato de la sección 2.7;
**CSS Box Model Level 3** y **CSS Box Sizing Level 3** para el modelo de caja y
`box-sizing`; **CSS Flexible Box Layout Level 1** y **CSS Grid Layout Level 2**
para las secciones 2.8 y 2.9; **CSS Values and Units Level 4** para las unidades de
la sección 2.10; y **CSS Containment Level 3**, que introduce las consultas de
contenedor mencionadas en la sección 2.13. La propuesta original de Håkon Wium Lie
de octubre de 1994 sigue disponible en `www.w3.org/People/howcome/p/cascade.html` y
su lectura muestra con claridad qué problema se intentaba resolver y qué se
descartó. Las pautas de accesibilidad citadas son las **WCAG 2.2**, en particular
sus criterios de contraste mínimo y de visibilidad del foco.

Como bibliografía de estudio, Meyer y Weyl, *CSS: The Definitive Guide* (5.ª
edición, O'Reilly, 2023) es la referencia completa del lenguaje y la más adecuada
para consultar un comportamiento puntual con precisión normativa. Para el modelo de
disposición, Andrew, *The New CSS Layout* (A Book Apart, 2017) explica Flexbox y
Grid desde el problema que resuelven en lugar de desde su sintaxis, que es el
enfoque de este capítulo. Sobre accesibilidad aplicada a la presentación, Pickering,
*Inclusive Components* (2018) documenta patrones de componentes que funcionan con
teclado y lector de pantalla, y es la mejor respuesta práctica a los riesgos de la
sección 2.13. La documentación de Tailwind en `tailwindcss.com` incluye un artículo
de su autor sobre el razonamiento detrás del enfoque *utility-first* que
corresponde a la sección 2.11.

---

**Continúa en:** Capítulo 3 — JavaScript: el lenguaje del navegador y su bucle de
eventos, donde se estudia el tercer lenguaje de la plataforma, por qué tiene las
rarezas que tiene, y cómo se ejecuta el código que a partir del Capítulo 4 va a
modificar el DOM construido en el Capítulo 1.
