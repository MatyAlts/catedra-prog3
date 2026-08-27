# Frontend desde cero — temario del módulo

Módulo de **8 clases de 4 horas** (32 h) que lleva al alumno desde no saber qué es
el DOM hasta poder encarar el frontend del **TPI Food Store** trabajando con
agentes de IA.

**Punto de partida real:** el alumno viene de Programación 1 y 2. Sabe qué es una
variable, una función, un condicional y una estructura de datos. **No sabe nada de
la plataforma web.** Este módulo no enseña a programar: enseña la web.

**Punto de llegada:** poder leer `trabajo integrador/docs-tpi/03-frontend/`, entender las once reglas
obligatorias RN-F01 a RN-F11, y dirigir a un agente de IA para implementarlas
sabiendo qué pedir y —sobre todo— **por qué lo que el agente responda puede estar
mal**.

---

## La tensión que ordena el módulo

El TPI pide **TypeScript 5 estricto, Vite, Tailwind, Web Components, History API,
EventSource, `@tanstack/query-core`, `@tanstack/form-core`, `zustand/vanilla`,
Axios, Chart.js y DOMPurify. Sin framework de interfaz.**

Conviene leer esa lista con atención: **"sin framework" no significa "sin
dependencias".** El TPI prohíbe React o Vue —lo que oculta el DOM y su ciclo de
vida— pero declara doce tecnologías, varias de ellas bibliotecas de peso. El
alumno no reimplementa una caché de consultas ni un store: los usa. Lo que no
puede delegar es **el ciclo de vida de la interfaz**, y eso es exactamente lo que
las once reglas RN-F gobiernan.

Esa decisión no es capricho del director: sin React que esconda el DOM, el alumno
queda obligado a entender qué hace el navegador de verdad. Todo el módulo se
apoya en eso. Cada tema se enseña respondiendo la misma pregunta:

> ¿Qué problema real apareció, que hizo falta inventar esto?

Un alumno que sabe *qué problema resuelve* Vite puede juzgar si el código que le
propone un agente resuelve ese problema. Uno que sólo sabe *qué comando se
escribe* no puede juzgar nada.

---

## Recorrido

| # | Clase | Del TPI habilita | Reglas |
| --- | --- | --- | --- |
| 1 | La web como plataforma: HTTP, el navegador y HTML semántico | 1.2, 1.3, sección 6 | — |
| 2 | CSS: modelo de caja, flujo y cascada. Tailwind como capa | 1.3 | — |
| 3 | JavaScript: el lenguaje del navegador y su bucle de eventos | 1.4 | — |
| 4 | El DOM: programar la página sin framework | 2.4 | RN-F02 |
| 5 | Asincronía y red: promesas, `fetch`, errores y SSE | 11, 14.1 | RN-F09, RN-F10, RN-F11 |
| 6 | TypeScript: tipos sobre JavaScript y el contrato de la API | 7, 14 | RN-F08 |
| 7 | Herramientas y componentes: Vite, Web Components, Chart.js | 2.5 | RN-F01, RN-F05 |
| 8 | Arquitectura: Feature-Sliced Design, estado y el TPI | 2.4, 2.5, 13 | RN-F03, RN-F04, RN-F06, RN-F07 |

Las once reglas quedan cubiertas. Ninguna se enuncia sin haber enseñado antes el
problema que la origina: **RN-F02 no se entiende sin haber visto un XSS
funcionando**, y RN-F01 no se entiende sin haber visto una fuga de memoria por un
listener que nadie dio de baja.

---

## Clase 1 — La web como plataforma

**Génesis.** Qué había antes de la web (FTP, Gopher, sistemas de hipertexto
cerrados) y por qué ninguno escaló. Berners-Lee en el CERN, 1989-1991: la decisión
de diseño que lo cambió todo fue **un protocolo sin estado sobre documentos
enlazados por identificadores universales**. De ahí sale todo lo demás, incluidas
las molestias.

**Contenido.** El ciclo petición-respuesta. Anatomía de una petición HTTP campo por
campo: método, ruta, encabezados, cuerpo. Códigos de estado y qué significa
realmente cada familia. URL: esquema, autoridad, ruta, query, fragmento. Qué hace
el navegador cuando recibe HTML: parseo, construcción del DOM y del CSSOM, árbol
de render, layout, pintado. Anatomía del documento HTML. HTML semántico y por qué
la semántica no es decoración: es la interfaz con el lector de pantalla y con el
buscador.

**Seguridad y evolución.** El HTML no valida nada y nunca lo hizo: acá nace la
necesidad de validar en el servidor, que en el TPI son los schemas Pydantic de la
sección 7.

**Puente al TPI.** La sección 6 del TPI es una tabla de peticiones HTTP. Al
terminar esta clase el alumno la puede leer.

## Clase 2 — CSS

**Génesis.** Håkon Wium Lie, 1994. Antes se maquetaba con `<font>` y tablas
anidadas: por qué eso colapsó y cuál fue la decisión de diseño que lo reemplazó
—separar contenido de presentación y resolver conflictos por cascada en vez de por
orden de aparición.

**Contenido.** Modelo de caja y `box-sizing`. Flujo normal, y por qué entenderlo
antes que Flexbox evita el 80% de la frustración. Cascada, especificidad y
herencia. Flexbox y Grid: qué problema resuelve cada uno. Diseño responsive y
unidades relativas. Tailwind: qué problema resuelve *utility-first*, qué se gana y
qué se pierde, y por qué el TPI lo pide.

**Seguridad y evolución.** Variables CSS, capas en cascada, y por qué el CSS
moderno vuelve innecesarias muchas herramientas que fueron obligatorias.

## Clase 3 — JavaScript

**Génesis.** Brendan Eich, Netscape, 1995, diez días. La guerra de navegadores, la
estandarización en ECMA-262 y por qué **el lenguaje tiene las rarezas que tiene**:
casi todas se explican por compatibilidad hacia atrás, no por mal diseño.

**Contenido.** Tipos primitivos y objetos. Valor contra referencia. Coerción: las
reglas reales, no el folklore. Funciones, ámbito, closures. `this` y por qué las
funciones flecha existen. Módulos ES. **El bucle de eventos**: pila, cola de
tareas, cola de microtareas, y por qué bloquear el hilo congela la página.

**Puente al TPI.** La sección 1.4 explica el modelo asincrónico del backend. Es el
mismo concepto del otro lado del cable: acá se ve por qué.

**Seguridad y evolución.** `strict mode`, y por qué apareció TypeScript.

## Clase 4 — El DOM

**Génesis.** DOM Level 0 y las incompatibilidades entre navegadores. Por qué
existió jQuery, qué resolvió realmente, y por qué hoy ya no hace falta. El TPI
prohíbe el framework precisamente para que esto se vea.

**Contenido.** El árbol del documento. Selección, creación y modificación de
nodos. **`textContent` contra `innerHTML`**: la diferencia entre las dos es la
RN-F02 entera. Eventos: captura, burbujeo, delegación. Formularios. El ciclo de
vida de un nodo y las **fugas de memoria por listeners que nadie dio de baja** —el
problema que RN-F01 obliga a resolver.

**Seguridad y evolución.** XSS demostrado en vivo sobre una página propia, y
DOMPurify como el único mecanismo que el TPI admite para insertar HTML.

## Clase 5 — Asincronía y red

**Génesis.** XMLHttpRequest nació en Outlook Web Access y se estandarizó de hecho.
Del *callback hell* a las promesas y de ahí a `async/await`: cada paso resolvió un
problema concreto de legibilidad y de manejo de errores.

**Contenido.** Promesas: estados, encadenamiento, `Promise.all`. `async/await` y
qué pasa realmente por debajo. `fetch`: anatomía de la petición y de la respuesta.
CORS explicado por lo que protege, no como un error molesto. Manejo de errores de
red contra errores de aplicación, y el catálogo de errores de la sección 14.1 del
TPI. **Server-Sent Events**: por qué el TPI eligió SSE y no WebSockets, el hueco de
la reconexión, y por qué un evento invalida en vez de escribir (RN-F09).

**Seguridad y evolución.** Dónde no guardar un token, y por qué las guardas del
cliente son usabilidad y no seguridad (anticipo de RN-F04).

## Clase 6 — TypeScript

**Génesis.** Anders Hejlsberg, Microsoft, 2012. El problema que resuelve no es
"JavaScript tiene errores": es que **a partir de cierto tamaño nadie recuerda qué
forma tiene un objeto**, y el compilador sí.

**Contenido.** Tipado estructural y por qué no es como el de Java. Inferencia.
Uniones y estrechamiento. Genéricos, con moderación. `strict` de verdad: qué
activa cada flag y qué error atrapa cada uno. **Tipar el contrato de la API** de la
sección 7 del TPI. Dinero como string decimal y conversión en la capa `api/`
—RN-F08 y por qué existe.

**Seguridad y evolución.** Los tipos se borran en tiempo de ejecución: validar en
el borde sigue siendo obligatorio. Acá se entiende por qué el backend valida
igual aunque el frontend esté tipado.

## Clase 7 — Herramientas y componentes

**Génesis.** Por qué hizo falta empaquetar: HTTP/1.1, la ausencia de módulos y
cientos de archivos. Browserify, Webpack, y el salto de Vite —usar módulos ES
nativos en desarrollo y empaquetar sólo para producción.

**Contenido.** Vite con la plantilla `vanilla-ts` que el TPI declara: servidor de
desarrollo, HMR, build. Configuración de Tailwind. **Custom Elements**:
`connectedCallback`, `disconnectedCallback`, atributos observados. Shadow DOM: qué
aísla y qué complica. **RN-F01 en acción**: guardar la función de baja y ejecutarla
al desmontar. Chart.js y RN-F05: crear una vez, mutar y actualizar, destruir al
desmontar.

## Clase 8 — Arquitectura y cierre

**Génesis.** Por qué organizar por tipo de archivo (`components/`, `utils/`,
`services/`) colapsa al crecer, y qué propone Feature-Sliced Design en su lugar.

**Contenido.** Las capas de FSD y la regla de dependencias del TPI (sección 2.4).
**Estado del cliente contra estado del servidor**: `zustand/vanilla` para lo
primero y `@tanstack/query-core` para lo segundo, y por qué mezclarlos es el error
que RN-F03 prohíbe. Rehidratación de la sesión y por qué
ninguna vista se monta antes de que termine (RN-F06). Idempotencia en el checkout
con `crypto.randomUUID()` (RN-F07). Guardas de ruta como usabilidad (RN-F04).
Refetch de respaldo: la interfaz nunca depende de haber recibido un evento
(RN-F11).

**Cierre del módulo.** Cómo trabajar con agentes de IA sobre esta base, enlazado
con la sección 2.4 del encuadre del TPI: qué pedir, cómo verificar lo que
devuelven, y cuáles de las once reglas un agente rompe **por defecto** si nadie se
lo impide.

---

## Trazabilidad con el TPI

Cada capítulo cierra citando por número las secciones del TPI trozado
(`trabajo integrador/docs-tpi/`) que quedan habilitadas. Esa numeración es la del documento del director y no se altera: sirve
para que el alumno vaya y vuelva.

## Estado

- [x] Clase 1 — La web como plataforma ✅
- [x] Clase 2 — CSS ✅
- [x] Clase 3 — JavaScript ✅
- [x] Clase 4 — El DOM ✅
- [x] Clase 5 — Asincronía y red ✅
- [x] Clase 6 — TypeScript ✅
- [x] Clase 7 — Herramientas y componentes ✅
- [x] Clase 8 — Arquitectura y cierre ✅
