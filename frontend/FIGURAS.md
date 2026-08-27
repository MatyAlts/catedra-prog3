# Catálogo de figuras — Frontend desde cero

Toda figura del módulo se declara acá antes de referenciarse en un capítulo.
Regla del material: si un esquema necesita cajas y flechas, **es una figura**, no
arte ASCII (ver [`CLAUDE.md`](CLAUDE.md) §4).

Columna **Origen**: `diagrama` (Mermaid, en [`DIAGRAMAS.md`](DIAGRAMAS.md)) o
`captura` (la toma el profesor sobre pantalla real).

---

## Capítulo 1 — La web como plataforma

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 1.1 | El recorrido de una petición | Los ocho pasos de la sección 1.3, del nombre de dominio al pintado. Los pasos 1 a 4 en un color y los 5 a 8 en otro, para hacer visible dónde termina la red y empieza el navegador | diagrama | ⬜ pendiente |
| 1.2 | Anatomía de una petición HTTP | La petición de la sección 1.5 con cada zona rotulada: línea de petición, bloque de encabezados, línea en blanco delimitadora y cuerpo. La línea en blanco destacada, porque es el delimitador que casi nadie ve | diagrama | ⬜ pendiente |
| 1.3 | Anatomía de una URL | Los seis componentes de la sección 1.6 sobre la URL de ejemplo, con el fragmento marcado como "no viaja al servidor" | diagrama | ⬜ pendiente |
| 1.4 | Del byte al píxel | Las etapas de la sección 1.7: bytes → DOM y CSSOM → árbol de render → disposición → pintado. Debe hacerse visible que el árbol de render contiene **menos** nodos que el DOM | diagrama | ⬜ pendiente |
| 1.5 | El panel Network | Captura del panel de red con una petición seleccionada y sus encabezados a la vista. Sobre el sitio del TPI si ya está desplegado; si no, cualquier sitio con varias peticiones | captura | ⬜ pendiente |
| 1.6 | El árbol de accesibilidad | Captura del panel de accesibilidad mostrando, lado a lado, el rol que recibe un `<button>` y el que recibe un `<div>` con manejador de clic. Es la evidencia visual de la sección 1.9.1 | captura | ⬜ pendiente |

---

## Capítulo 2 — CSS

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 2.1 | Las cuatro áreas del modelo de caja | Contenido, relleno, borde y margen como rectángulos concéntricos. El margen debe verse **transparente** y el fondo llegando sólo hasta el borde exterior del relleno: es la diferencia que la sección 2.6.1 explica con palabras | diagrama | ⬜ pendiente |
| 2.2 | `content-box` frente a `border-box` | La misma tarjeta (`width: 300px`, `padding: 20px`, `border: 2px`) con los dos valores, cada una con su ancho real acotado: 344 px y 300 px | diagrama | ⬜ pendiente |
| 2.3 | El orden de la cascada | Los cuatro criterios de desempate como decisiones sucesivas: origen e importancia → capas → especificidad → orden de aparición. Debe verse que en cuanto uno decide, los siguientes no se consultan | diagrama | ⬜ pendiente |
| 2.4 | Los ejes de Flexbox | El mismo contenedor con `flex-direction: row` y `column`, con el eje principal y el cruzado rotulados en cada caso. Es la evidencia de que `justify-content` y `align-items` intercambian su efecto visual | diagrama | ⬜ pendiente |
| 2.5 | Grid adaptable con `auto-fill` y `minmax` | La misma grilla de tarjetas en tres anchos de contenedor, mostrando cómo el navegador decide 1, 2 y 4 columnas sin ninguna consulta de medios | diagrama | ⬜ pendiente |
| 2.6 | El panel de estilos y la cascada | Captura del panel con un elemento que recibe la misma propiedad de varias reglas: la ganadora arriba y las perdedoras **tachadas**. Debe verse también el archivo y la línea de origen de cada regla | captura | ⬜ pendiente |
| 2.7 | El inspector del modelo de caja | Captura del diagrama de caja del navegador con las medidas reales de las cuatro áreas sobre un elemento del proyecto | captura | ⬜ pendiente |

## Capítulo 3 — JavaScript

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 3.1 | De Mocha al ciclo anual | Línea de tiempo: Mocha (may 1995) → LiveScript (sep) → JavaScript (dic) → JScript (1996) → ECMA-262 (1997) → ES3 (1999) → **ES4 abandonado (2008)** → ES5 (2009) → ES2015 → anual. El abandono de ES4 debe destacarse: de esa crisis sale el ciclo actual | diagrama | ⬜ pendiente |
| 3.2 | Valor y referencia en memoria | Dos primitivos con cajas independientes frente a dos nombres apuntando al mismo objeto. Debe verse que `p2.precio = 5000` cambia lo que ve `p1` | diagrama | ⬜ pendiente |
| 3.3 | Pila, colas y bucle de eventos | Las cuatro piezas del modelo y el flujo entre ellas. La cola de microtareas y la de tareas deben verse **separadas**, con distinta regla de vaciado | diagrama | ⬜ pendiente |
| 3.4 | El orden de vaciado | Los cuatro pasos del algoritmo: vaciar pila → vaciar microtareas **por completo** → renderizar → tomar **una sola** tarea. La asimetría entre "por completo" y "una sola" es el contenido de la figura | diagrama | ⬜ pendiente |
| 3.5 | La cadena de prototipos | Una instancia de `Producto` → `Producto.prototype` → `Object.prototype` → `null`, con la búsqueda de una propiedad recorriendo la cadena hasta encontrarla | diagrama | ⬜ pendiente |
| 3.6 | El depurador detenido | Captura del depurador en un punto de interrupción **dentro de una clausura**, con el panel de ámbitos mostrando la variable capturada y la pila de llamadas. Es la evidencia visual de la sección 3.6.3 | captura | ⬜ pendiente |
| 3.7 | Una tarea larga bloqueando | Captura del panel de rendimiento con una tarea larga marcada en rojo, mostrando el bloqueo del hilo principal descrito en la sección 3.10.1 | captura | ⬜ pendiente |

## Capítulo 4 — El DOM

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 4.1 | El árbol de nodos | Un `<ul>` con dos `<li>` indentados y su árbol real: **cinco** hijos, no dos. Los tres nodos de texto (saltos de línea e indentación) deben verse con distinto color que los elementos: son el contenido de la figura | diagrama | ⬜ pendiente |
| 4.2 | Las tres fases de propagación | El recorrido de un clic: `document` → contenedor → botón (captura), el botón (objetivo), y la vuelta botón → contenedor → `document` (burbujeo). Debe verse que es **un solo evento** recorriendo el árbol dos veces | diagrama | ⬜ pendiente |
| 4.3 | Delegación frente a un manejador por elemento | A la izquierda, cien botones con cien manejadores; a la derecha, cien botones y **uno** en el contenedor. Anotar en cada lado qué pasa cuando se agrega un botón nuevo | diagrama | ⬜ pendiente |
| 4.4 | Cómo una clausura mantiene vivo un nodo removido | El nodo fuera del documento pero con la flecha de referencia desde el manejador todavía registrada en el canal. Debe verse que el nodo **no se ve en pantalla y sigue en memoria** | diagrama | ⬜ pendiente |
| 4.5 | Nodos separados y cadena de retención | Captura del panel de memoria filtrado por nodos separados, con la cadena de retención desplegada mostrando qué mantiene vivo al nodo. Es la evidencia de la sección 4.9 | captura | ⬜ pendiente |
| 4.6 | El panel de escuchas de eventos | Captura del panel mostrando los manejadores registrados en un elemento y sus ancestros. Idealmente, la misma vista montada dos veces, para que se vea el manejador duplicado | captura | ⬜ pendiente |

## Capítulo 5 — Asincronía y red

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 5.1 | Estados de una promesa | Pendiente → cumplida o rechazada, con las transiciones marcadas como **de una sola vía**. Debe quedar claro que una vez resuelta ya no cambia | diagrama | ⬜ pendiente |
| 5.2 | Cuándo `fetch` rechaza y cuándo cumple | Las tres situaciones que rechazan (fallo de red, bloqueo por origen, cancelación) frente a las que **cumplen** aunque comuniquen un error: 404, 422, 500. Es la figura que previene el error más común del capítulo | diagrama | ⬜ pendiente |
| 5.3 | La verificación previa de CORS | El `OPTIONS` que el navegador emite solo, la respuesta del servidor, y recién después la petición real. Debe verse que si la primera falla, **la segunda nunca se emite** | diagrama | ⬜ pendiente |
| 5.4 | El hueco de la reconexión | Línea de tiempo: cliente conectado, caída, tres eventos publicados que no recibe, reconexión con el último identificador, y recuperación desde el servidor. Marcar el tramo perdido | diagrama | ⬜ pendiente |
| 5.5 | El panel de red con limitación | Captura del panel con la limitación de red activada y la columna de tiempos desplegada, mostrando la separación entre espera del servidor y descarga | captura | ⬜ pendiente |
| 5.6 | El flujo de eventos en el panel de red | Captura de la pestaña de eventos de una conexión SSE, con identificador, tipo y contenido en orden. Idealmente tomada **después de una reconexión**, para que se vean los eventos recuperados | captura | ⬜ pendiente |

## Capítulo 6 — TypeScript

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 6.1 | Del `.ts` al `.js`: el borrado | El mismo fragmento antes y después de compilar, con las anotaciones tachadas en el origen y ausentes en la salida. Debe verse que **el JavaScript se emite aunque haya errores de tipo** | diagrama | ⬜ pendiente |
| 6.2 | Tipado estructural frente a nominal | `Punto` y `Coordenada` con la misma forma y distinto nombre: compatible en TypeScript, incompatible en un lenguaje nominal. La columna de la derecha debe rotularse "Java / C#" para el contraste | diagrama | ⬜ pendiente |
| 6.3 | El estrechamiento de una unión discriminada | La unión `Resultado` de tres formas, y dentro de cada rama del `switch` qué propiedades existen y cuáles no. El caso `never` del `default` va destacado como red de seguridad | diagrama | ⬜ pendiente |
| 6.4 | Dónde mienten los tipos | La frontera entre lo verificado y lo afirmado: de un lado el código tipado, del otro `json()`, `JSON.parse()` y `as`. La línea de la frontera es el contenido de la figura | diagrama | ⬜ pendiente |
| 6.5 | Un error de verificación de nulos | Captura del editor sobre `document.querySelector(...)` seguido de un uso directo, con el error de posible `null` visible. Es el bug del Capítulo 4 atajado antes de existir | captura | ⬜ pendiente |
| 6.6 | El tipo inferido al pasar el cursor | Captura del editor mostrando el tipo inferido de una variable. Idealmente **una que quedó en `any` sin que nadie lo pidiera**, que es lo que hay que aprender a detectar | captura | ⬜ pendiente |

## Capítulo 7 — Herramientas y componentes

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 7.1 | Del script suelto al empaquetado | Línea de tiempo con el problema que resolvió cada paso: etiquetas en orden manual → CommonJS (no sirve en el navegador) → AMD → Browserify → Webpack → Rollup → esbuild y Vite. Cada nodo lleva **qué problema resolvía**, no sólo su nombre | diagrama | ⬜ pendiente |
| 7.2 | Vite: desarrollo frente a producción | La figura central del capítulo. A la izquierda, el navegador pidiendo módulo por módulo sin empaquetar; a la derecha, Rollup produciendo unos pocos archivos con huella en el nombre. Las dependencias pre-procesadas aparecen en ambos lados | diagrama | ⬜ pendiente |
| 7.3 | El ciclo de vida de un elemento personalizado | `constructor` → `connectedCallback` → `attributeChangedCallback` → `disconnectedCallback`, con la **flecha de retorno** que muestra que mover el elemento vuelve a disparar el ciclo. Esa flecha es el punto de la figura | diagrama | ⬜ pendiente |
| 7.4 | Qué aísla el DOM en la sombra | La frontera con lo que cruza (propiedades heredables, propiedades personalizadas, contenido en ranuras) y lo que no (estilos globales, **incluidas las clases de Tailwind**, y los selectores desde el documento) | diagrama | ⬜ pendiente |
| 7.5 | Módulos ES nativos en desarrollo | Captura del panel de red en desarrollo, mostrando decenas de peticiones a archivos `.ts`. Idealmente al lado de la misma vista tras construir para producción, para el contraste | captura | ⬜ pendiente |
| 7.6 | Un elemento personalizado en el inspector | Captura del panel de elementos con un `fs-*` desplegado. Si el proyecto usa sombra, con el nodo de sombra visible; si no, mostrando que el contenido vive en el DOM claro | captura | ⬜ pendiente |

## Capítulo 8 — Arquitectura y cierre

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 8.1 | Por tipo frente a por funcionalidad | El mismo proyecto organizado de las dos formas. A la izquierda, los archivos del carrito **desperdigados en cinco carpetas**; a la derecha, todos juntos. La figura debe hacer evidente qué se borra fácil y qué no | diagrama | ⬜ pendiente |
| 8.2 | Las capas y la dirección de las dependencias | La figura central del capítulo: Arranque → Router → Vistas → Features → Stores/API/Eventos → Types, con las flechas **en un solo sentido**. Deben verse tachadas las dos prohibiciones: la flecha hacia arriba y la horizontal entre features. `api/eventos.ts` aparte, marcada como transversal | diagrama | ⬜ pendiente |
| 8.3 | Estado del cliente frente a estado del servidor | Los seis stores de un lado y las claves de la caché del otro, separados por la pregunta "¿quién es el dueño del dato?". `CartItem` va en el medio, marcado como **la excepción declarada** | diagrama | ⬜ pendiente |
| 8.4 | Los siete pasos del arranque | Diagrama de secuencia con las dos ramas (con token y sin token), el estado de carga del paso 2 **marcado como el que evita el parpadeo del login**, y la apertura del canal recién en el paso 7 | diagrama | ⬜ pendiente |
| 8.5 | El ciclo de vida de la clave de idempotencia | Línea de tiempo: se genera al entrar al último paso, se persiste, sobrevive a una recarga, viaja en el encabezado, y **se descarta recién al confirmarse el éxito**. Los tres momentos donde hacerlo mal produce un pedido duplicado van marcados | diagrama | ⬜ pendiente |
| 8.6 | Stores y claves de caché en vivo | Captura del panel de aplicación con el almacenamiento local a la vista durante el checkout: el token, los ítems del carrito y la clave de idempotencia. Es la evidencia del experimento de la sección 8.11 | captura | ⬜ pendiente |
