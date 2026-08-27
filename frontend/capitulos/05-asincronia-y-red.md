# Capítulo 5 — Asincronía y red: promesas, `fetch`, errores y eventos del servidor

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 5.1. Alcance de la clase

Este capítulo cierra el arco que abrió el primero. El Capítulo 1 describió el
protocolo que trae los documentos; este estudia cómo se emiten peticiones **desde
el código**, sin recargar la página, y cómo se reacciona a lo que el servidor
manda por iniciativa propia.

El punto de partida es la restricción del Capítulo 3: **un solo hilo, que además
dibuja la pantalla**. Una petición de red tarda entre decenas y miles de
milisegundos, y durante todo ese tiempo el hilo no puede quedarse esperando: si lo
hiciera, la página estaría muerta. Toda la maquinaria que este capítulo estudia
—promesas, `async`/`await`, el bucle de eventos— existe para resolver esa tensión.

Conviene enunciar de entrada la distinción que más confusión genera, porque
atraviesa el capítulo entero: **asincronía no es concurrencia.** No hay dos cosas
ejecutándose a la vez. Hay una sola cosa ejecutándose, que en algún momento cede el
control y vuelve más tarde. Quien piense en hilos paralelos va a predecir mal el
orden de ejecución de casi todo.

Tres de las once reglas obligatorias del TPI nacen en este capítulo, todas en torno
al canal de eventos del servidor:

**RN-F09** establece que un evento recibido nunca escribe datos en la caché de
consultas: invalida la clave y deja que se recargue. **RN-F10** exige una sola
conexión de eventos por sesión. **RN-F11** exige que la interfaz nunca dependa de
haber recibido un evento, declarando además un intervalo de recarga de respaldo.

Las tres parecen restricciones arbitrarias hasta que se entiende una limitación del
diseño que el propio TPI declara en su sección 11.3: **el mecanismo de publicación
del backend no persiste los mensajes.** Lo que se publica mientras un cliente no
está conectado, ese cliente no lo recibe. Las tres reglas son la respuesta del
frontend a ese hecho.

El capítulo también resuelve un problema que el Capítulo 1 dejó planteado y no
cerró: **el servidor no puede iniciar la conversación.** La sección 5.9 estudia el
mecanismo que el TPI eligió para hacerlo posible, y por qué eligió ese y no el
más conocido.

Al finalizar la clase, el alumno debe poder escribir una función que consulte la
API, **distinga un fallo de red de un error de aplicación**, se cancele si la vista
se desmonta, y traduzca los códigos del catálogo de errores del TPI a mensajes
útiles.

**Contenidos**

1. Origen y objetivos de diseño de la petición en segundo plano.
2. Promesas: estados, encadenamiento y combinadores.
3. `async` y `await`: qué resuelven y qué esconden.
4. Anatomía de `fetch` y su decisión más polémica.
5. Cancelación y plazos de espera.
6. La política de mismo origen y CORS.
7. Errores de red, de protocolo y de aplicación.
8. El catálogo de errores del TPI y dónde se traduce.
9. Almacenamiento del token y sus riesgos.
10. Eventos enviados por el servidor: protocolo y reconexión.
11. Las tres reglas del canal de eventos.
12. Herramientas de diagnóstico.

---

## 5.2. Por qué existe la petición en segundo plano

Hasta fines de los noventa, toda interacción con un servidor implicaba **reemplazar
la página entera**. Marcar una casilla, filtrar una lista, agregar un producto al
carrito: cada acción enviaba un formulario, el servidor construía un documento
nuevo y el navegador lo pintaba desde cero. La pantalla parpadeaba en blanco, la
posición de desplazamiento se perdía y todo lo escrito en otros campos se
descartaba.

El costo no era sólo de comodidad. Cada interacción **transmitía el documento
completo** —cabecera, menú, pie— aunque hubiera cambiado una sola línea.

La solución llegó de un lugar inesperado. Microsoft necesitaba que **Outlook Web
Access** se pareciera al cliente de escritorio, y para eso hacía falta traer correos
nuevos sin recargar. El equipo agregó a Internet Explorer 5, en 1999, un objeto que
permitía emitir una petición HTTP desde el código: **`XMLHTTP`**, disponible como
componente ActiveX. Mozilla lo implementó de forma nativa poco después con el
nombre `XMLHttpRequest`, y los demás navegadores lo copiaron. **Se estandarizó
años después de ser universal**, y el nombre quedó pegado a XML aunque casi nunca se
usó para eso.

La técnica existió durante años sin nombre y sin uso masivo. Lo que la volvió
ubicua fue un ensayo: en febrero de 2005, Jesse James Garrett publicó *Ajax: A New
Approach to Web Applications*, que le puso nombre y mostró que Google Maps y Gmail
ya la usaban a gran escala. **La técnica tenía seis años; el nombre le dio
visibilidad.**

El problema siguiente fue de forma, no de capacidad. `XMLHttpRequest` se programaba
con funciones de retorno, y como cada petición dependía del resultado de la
anterior, el código se anidaba:

```js
obtenerUsuario(id, function (usuario) {
  obtenerDirecciones(usuario.id, function (direcciones) {
    obtenerPedidos(usuario.id, function (pedidos) {
      // tres niveles, y falta manejar los errores de cada uno
    }, alFallar);
  }, alFallar);
}, alFallar);
```

Ese patrón se conoció como **infierno de funciones de retorno**, y su problema real
no era la indentación sino el manejo de errores: **cada nivel necesitaba su propio
tratamiento**, no había forma de capturar un fallo de todo el conjunto, y una
excepción lanzada dentro de una función de retorno no podía atraparse desde afuera.

Las **promesas** resolvieron eso con una idea precisa: **representar el resultado
futuro como un valor**. Un valor se puede guardar en una variable, pasar como
argumento, devolver de una función y combinar con otros. Se especificaron primero
como acuerdo comunitario —Promises/A+, 2012— y se incorporaron al lenguaje en
ES2015. **`async`/`await`** llegó en ES2017 para escribirlas con la forma del código
secuencial, y **`fetch`** reemplazó a `XMLHttpRequest` con una interfaz basada en
promesas.

De ese recorrido salen cuatro decisiones de diseño que gobiernan el capítulo.

**Primera: la asincronía no es concurrencia.** Sigue habiendo un solo hilo. Una
operación asincrónica no corre en paralelo: **cede el control y se reanuda después**,
mediante el bucle de eventos de la sección 3.10.

**Segunda: el resultado futuro es un valor.** Es la diferencia esencial con las
funciones de retorno, y lo que permite componer operaciones.

**Tercera: `fetch` no considera un error el error del servidor.** Una respuesta 404
o 500 **cumple** la promesa. Es la decisión más discutida de la interfaz y la fuente
de errores más frecuente; la sección 5.5.3 explica su lógica.

**Cuarta: el navegador restringe por origen de forma predeterminada.** Un documento
de un sitio no puede leer respuestas de otro salvo autorización explícita. La
sección 5.6 explica a quién protege eso, que no es a quien parece.

> **💡 PARA ENTENDER**
> Guardate la primera decisión, porque es la que más gente entiende mal y la que te
> va a hacer predecir bien el orden de ejecución.
>
> **`await` no significa "esperá acá".** Significa: *"guardá dónde estoy, soltá el
> hilo para que haga otra cosa, y volvé a este punto cuando llegue el resultado"*.
>
> Es la misma idea del Capítulo 3: nadie corre en paralelo. Hay uno solo que se va y
> vuelve.
>
> Y de ahí sale algo práctico: si adentro de una función `async` hacés un cálculo
> pesado y sincrónico, **la función es `async` y bloquea igual**. La palabra no tiene
> ningún poder mágico sobre el hilo. Sólo el `await` cede el control, y sólo en el
> punto exacto donde está escrito.

---

## 5.3. Promesas

### 5.3.1. Estados

Una promesa está en uno de tres estados:

| Estado | Significado |
| --- | --- |
| Pendiente | La operación no terminó |
| Cumplida | Terminó bien y tiene un valor |
| Rechazada | Terminó mal y tiene un motivo |

Dos propiedades importan. La transición es **de una sola vía**: una vez que una
promesa se resuelve, su estado y su valor no cambian más. Y las continuaciones se
ejecutan como **microtareas**, lo que —por el algoritmo de la sección 3.10.2—
significa que una promesa ya resuelta siempre se procesa antes que un
`setTimeout(0)`.

*(Ver Figura 5.1: los estados de una promesa y sus transiciones.)*

La inmutabilidad tiene una consecuencia que conviene tener presente: **una promesa
no se puede reiniciar ni cancelar.** Es un valor, no una operación en curso. Lo que
sí se puede cancelar es la operación subyacente —una petición de red— mediante el
mecanismo de la sección 5.5.4, pero la promesa en sí simplemente termina rechazada.

De ahí sale también una fuente de confusión: **llamar a la función que crea la
promesa dispara la operación de inmediato**, aunque nadie haga `await`. Guardar una
promesa en una variable no es guardar una intención de pedir algo; el pedido ya
salió.

```js
const promesa = obtenerPedido(id);   // la petición YA se emitió acá
// ... otro código ...
const pedido = await promesa;        // acá sólo se espera el resultado
```

Ese comportamiento, que sorprende a quien viene de lenguajes con evaluación
perezosa, es en realidad útil: permite **lanzar varias operaciones y esperarlas
después**, que es la base de los combinadores de la sección 5.3.3.

### 5.3.2. Encadenamiento

`then` devuelve **una promesa nueva**, y de ahí sale el encadenamiento:

```js
obtenerUsuario(id)
  .then(usuario => obtenerPedidos(usuario.id))   // devuelve otra promesa
  .then(pedidos => mostrar(pedidos))
  .catch(error => manejar(error))                // captura cualquiera de los tres
  .finally(() => ocultarCargando());             // se ejecuta siempre
```

La diferencia con las funciones de retorno está en la línea del `catch`: **un solo
manejador cubre toda la cadena.** Si cualquiera de los pasos falla, el control salta
directamente ahí. Eso es lo que el patrón anterior no podía hacer.

`finally` se ejecuta tanto si la cadena terminó bien como si terminó mal, y es el
lugar correcto para ocultar un indicador de carga.

### 5.3.3. Combinadores

Cuatro funciones combinan varias promesas, y elegir la equivocada produce
comportamientos difíciles de diagnosticar:

| Combinador | Espera a | Falla si | Devuelve |
| --- | --- | --- | --- |
| `Promise.all` | Todas | **Falla una** | Arreglo de valores |
| `Promise.allSettled` | Todas | Nunca | Arreglo de `{status, value \| reason}` |
| `Promise.race` | La primera en resolverse | Si esa primera falla | El valor de esa |
| `Promise.any` | La primera **cumplida** | Fallan todas | El valor de esa |

La distinción entre las dos primeras es la que importa en la práctica. `Promise.all`
falla apenas una de las promesas falla, y **descarta los resultados de las que sí
funcionaron**. Sirve cuando el conjunto no tiene sentido incompleto: no se puede
mostrar una pantalla de pedido sin el pedido.

`Promise.allSettled` espera a todas y devuelve el resultado de cada una, exitoso o
no. Sirve cuando cada resultado es útil por separado: un panel con cuatro tarjetas
de estadísticas puede mostrar tres y un mensaje de error en la cuarta.

```js
const [productos, categorias] = await Promise.all([
  listarProductos(), listarCategorias()
]);   // sin categorías no hay catálogo que mostrar

const resultados = await Promise.allSettled([
  ventasDelDia(), pedidosPendientes(), stockCritico(), ticketPromedio()
]);   // cada tarjeta se muestra o falla por su cuenta
```

> **⚠️ OJO ACÁ**
> El error más caro de esta sección no es elegir mal el combinador: es **no usar
> ninguno.**
>
> ```js
> const productos  = await listarProductos();
> const categorias = await listarCategorias();
> ```
>
> Eso se ve prolijo y es **el doble de lento de lo necesario**. Las dos peticiones no
> dependen una de la otra, pero la segunda no arranca hasta que termina la primera.
> Si cada una tarda 300 ms, tenés 600 ms de espera para algo que podía tardar 300.
>
> Con cuatro peticiones independientes en un panel de estadísticas, la diferencia es
> más de un segundo de pantalla en blanco.
>
> **Regla: si dos peticiones no dependen entre sí, van juntas en un combinador.**
> Sólo encadenás con `await` cuando la segunda realmente necesita el resultado de la
> primera. Y ojo, que **este error un agente de IA te lo va a escribir siempre**: es
> lo que sale natural al traducir "traé A y traé B".

---

## 5.4. `async` y `await`

### 5.4.1. Qué son exactamente

Una función `async` **siempre devuelve una promesa**, aunque su cuerpo devuelva un
valor común. `await` suspende la función hasta que la promesa se resuelva, y
devuelve su valor. Si la promesa se rechaza, `await` **lanza** el motivo como una
excepción, lo que permite usar `try`/`catch`:

```js
async function cargarCatalogo() {
  try {
    const productos = await listarProductos();
    mostrar(productos);
  } catch (error) {
    mostrarError(error);
  } finally {
    ocultarCargando();
  }
}
```

Esa última propiedad es lo que hace valiosa la sintaxis. Antes de `async`/`await`,
un error asincrónico **no se podía capturar con `try`/`catch`**, porque para cuando
ocurría, el bloque ya había terminado.

### 5.4.2. El `await` en un bucle

El error de rendimiento más común del código asincrónico:

```js
// Serializa: cada petición espera a la anterior
for (const id of idsDePedidos) {
  const pedido = await obtenerPedido(id);
  procesar(pedido);
}

// Paraleliza: todas salen juntas
const pedidos = await Promise.all(idsDePedidos.map(id => obtenerPedido(id)));
pedidos.forEach(procesar);
```

Con veinte pedidos y 200 milisegundos cada uno, la primera versión tarda **cuatro
segundos** y la segunda **doscientos milisegundos**. El código de arriba no está
mal escrito en el sentido sintáctico: está mal en el sentido de que serializa algo
que no necesitaba ser serializado.

Hay un caso donde la versión secuencial es la correcta: cuando cada petición depende
del resultado de la anterior, o cuando emitir veinte peticiones simultáneas superaría
un límite del servidor —como el de la sección 5.7.4—.

> **📌 NOTA**
> Un detalle que muerde y que casi nadie ve venir: **`forEach` no espera nada.**
>
> ```js
> pedidos.forEach(async (p) => {
>   await guardar(p);
> });
> console.log("listo");     // se imprime ANTES de que se guarde ninguno
> ```
>
> `forEach` no sabe qué hacer con la promesa que le devuelve la función: la ignora y
> sigue. El `console.log` sale de inmediato, con las veinte operaciones todavía en el
> aire.
>
> Si necesitás esperar, tenés dos formas según lo que quieras:
>
> ```js
> for (const p of pedidos) await guardar(p);              // de a uno, en orden
> await Promise.all(pedidos.map(p => guardar(p)));        // todas juntas
> ```
>
> `for...of` **sí** respeta el `await`. `forEach`, `map`, `filter` y compañía, no.

---

## 5.5. `fetch`

### 5.5.1. La petición

```js
const respuesta = await fetch("/api/v1/pedidos", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`,
    "Idempotency-Key": crypto.randomUUID(),
  },
  body: JSON.stringify({ direccion_id: 42, items }),
});
```

Cada campo corresponde a un elemento de la anatomía de la sección 1.5. El
`Idempotency-Key` es el de la sección 1.4.2, que la regla RN-F07 exige en el
checkout; nótese que `crypto.randomUUID()` es una función del navegador y no de una
biblioteca.

Un detalle que produce errores: **`body` debe ser una cadena.** Pasar un objeto
directamente no falla con un mensaje claro; envía el resultado de convertirlo a
texto, que es `[object Object]`.

### 5.5.2. La respuesta

```js
respuesta.ok         // true si el código está entre 200 y 299
respuesta.status     // el número: 200, 404, 500
respuesta.headers    // los encabezados
await respuesta.json();   // parsea el cuerpo como JSON
```

El cuerpo llega como flujo y **se puede consumir una sola vez**. Un segundo intento
lanza un error. Si hace falta leerlo dos veces —por ejemplo, intentar `json()` y
caer a `text()` si falla— hay que clonar la respuesta antes con `respuesta.clone()`.

### 5.5.3. La decisión más discutida

Esta es la fuente de errores más frecuente de toda la interfaz:

> **`fetch` no rechaza la promesa ante un error HTTP.** Un 404, un 422 o un 500
> **cumplen** la promesa.

```js
// MAL: el catch nunca se ejecuta ante un 500
try {
  const r = await fetch("/api/v1/pedidos/9999");
  const pedido = await r.json();     // el cuerpo es el error, no un pedido
} catch (e) {
  // sólo llega acá si falló la RED
}
```

`fetch` rechaza únicamente en tres situaciones: **fallo de red** —no hubo
respuesta—, **bloqueo por origen** (sección 5.6) y **cancelación** (sección 5.5.4).

*(Ver Figura 5.2: cuándo `fetch` rechaza y cuándo cumple.)*

La lógica de la decisión, una vez explicada, es coherente: **un 404 es una respuesta
exitosa del protocolo.** La petición viajó, el servidor la entendió y contestó. Que
la respuesta comunique un problema de la aplicación es información, no un fallo de
la operación de red. `fetch` modela la capa de transporte, y en esa capa todo salió
bien.

Coherente o no, obliga a comprobar siempre:

```js
const respuesta = await fetch(url, opciones);
if (!respuesta.ok) {
  const cuerpo = await respuesta.json().catch(() => null);
  throw new ErrorDeApi(respuesta.status, cuerpo?.code, cuerpo?.message);
}
return respuesta.json();
```

Esa comprobación **se escribe una sola vez**, en la capa `api/` que el Capítulo 8
estudia. Repetirla en cada vista es la garantía de que en algún lado va a faltar.

> **📌 NOTA**
> Un aviso para cuando abras el TPI y no te lleves una sorpresa: **el stack declara
> Axios, no `fetch`.**
>
> ¿Y entonces por qué estudiamos `fetch`? Por dos razones. Es **la interfaz de la
> plataforma** —Axios está construido sobre ella y en algún momento vas a leer un
> error que viene de abajo—, y porque el comportamiento que acabás de ver es
> justamente el que Axios decidió cambiar:
>
> **Axios sí rechaza ante un `4xx` o un `5xx`.** Con Axios, un 500 cae en el `catch`,
> que es lo que la mayoría espera. Y el error trae `error.response.status` y
> `error.response.data`.
>
> Fijate lo que eso significa: **no son dos interfaces distintas, son dos decisiones
> distintas sobre el mismo problema.** `fetch` modela la capa de transporte; Axios
> modela lo que uno quiere de un cliente HTTP.
>
> Lo que **no** cambia es el principio de la sección 5.7: distinguir red, protocolo y
> aplicación sigue siendo tu trabajo. Axios te lo acerca al `catch`; no lo resuelve.
> Y el TPI usa además sus **interceptores**, que son el lugar donde el token y la
> traducción de errores se aplican una sola vez para toda la aplicación.

> **⚠️ OJO ACÁ**
> Este es el error más común del código que escriben los agentes de IA, así que
> prestale atención especial.
>
> Cuando le pidas "escribime una función que traiga los productos", te va a salir
> algo así:
>
> ```js
> try {
>   const r = await fetch("/api/v1/productos");
>   return await r.json();
> } catch (e) {
>   mostrarError("No se pudieron cargar los productos");
> }
> ```
>
> Se ve perfecto. Tiene su `try`/`catch`. **Y no maneja ningún error del servidor.**
>
> Si el backend responde 401 porque venció el token, ese `catch` no se ejecuta. La
> función devuelve el objeto de error parseado como si fuera la lista de productos, y
> el bug aparece tres capas más arriba, donde algo espera un arreglo y recibe otra
> cosa.
>
> **Si no ves un `if (!respuesta.ok)`, el código está mal.** No importa lo prolijo que
> se vea el resto.

### 5.5.4. Cancelación

El `AbortController` de la sección 4.9.4 también cancela peticiones:

```js
const controlador = new AbortController();
fetch(url, { signal: controlador.signal });

controlador.abort();   // la promesa se rechaza con un AbortError
```

El caso que lo hace necesario es concreto: **una vista que se desmonta mientras
espera una respuesta.** Sin cancelación, la respuesta llega, el código intenta
actualizar un elemento que ya no está en el documento, y en el mejor caso falla
silenciosamente; en el peor, mantiene vivo todo el subárbol, que es la fuga de la
sección 4.9.

El otro caso es la búsqueda mientras se escribe: cada tecla dispara una petición y
las respuestas pueden llegar **desordenadas**, de modo que un resultado viejo pise a
uno nuevo. Cancelar la anterior antes de emitir la siguiente resuelve las dos cosas.

Para un plazo de espera existe una función nativa que evita armarlo a mano:

```js
fetch(url, { signal: AbortSignal.timeout(5000) });
```

Vale la pena señalar por qué hace falta: **`fetch` no tiene plazo de espera
propio.** Sin uno, una petición puede quedar pendiente hasta que el sistema
operativo decida cortarla, que pueden ser minutos.

> **⚠️ OJO ACÁ**
> Que `fetch` no tenga plazo de espera propio suena a detalle y produce el peor tipo
> de falla: **la que no falla.**
>
> Pensá el caso. El usuario aprieta "Confirmar pedido" con mala señal. La petición
> sale y **queda colgada**. No falla, no responde, no pasa nada.
>
> - El botón sigue en "Enviando…"
> - No hay error que mostrar, porque no hubo error
> - El `catch` no se ejecuta, porque nada se rechazó
> - El usuario espera treinta segundos, se cansa, y **aprieta de nuevo**
>
> Y ahí tenés dos pedidos. Por eso RN-F07 —la clave de idempotencia— existe: porque
> este escenario **va a pasar**, no es hipotético.
>
> Regla: **toda petición lleva plazo de espera.** Sin excepciones. Un error explícito
> a los cinco segundos es infinitamente mejor que un botón que gira para siempre.

---

## 5.6. La política de mismo origen y CORS

### 5.6.1. Qué protege

Dos direcciones tienen el **mismo origen** si coinciden en esquema, host y puerto.
Por defecto, un documento no puede leer respuestas de otro origen.

La razón se entiende con un escenario. Alguien tiene sesión abierta en su banco y
visita un sitio cualquiera. Ese sitio emite una petición al banco desde el
navegador de la víctima, con sus cookies, y lee el saldo. **Sin la política de mismo
origen, eso funcionaría.**

De ahí la precisión que casi nadie tiene clara: **CORS no protege al servidor.
Protege al usuario de que un sitio lea respuestas de otro sitio usando sus
credenciales.** El servidor debe autorizar cada petición por su cuenta —lo hace el
token del Capítulo 1—, porque un programa fuera del navegador ignora CORS por
completo. Un `curl` no tiene política de mismo origen.

### 5.6.2. Verificación previa

Algunas peticiones se emiten directamente y otras van precedidas de una consulta.
La distinción es histórica: **las peticiones que un formulario HTML podía hacer
antes de que CORS existiera se admiten sin consulta**, porque prohibirlas habría
roto la web.

| Se emite directo | Requiere verificación previa |
| --- | --- |
| `GET`, `HEAD`, `POST` | Cualquier otro método: `PUT`, `PATCH`, `DELETE` |
| Sin encabezados propios | Con encabezados propios: `Authorization`, `Idempotency-Key` |
| `Content-Type` de formulario o texto plano | `Content-Type: application/json` |

La consecuencia práctica es que **casi toda petición a la API del TPI dispara una
verificación previa**, porque manda JSON y lleva `Authorization`.

Esa verificación es una petición `OPTIONS` que el navegador emite solo, declarando
qué método y qué encabezados pretende usar. El servidor responde qué admite, y sólo
entonces se emite la petición real. El encabezado `Access-Control-Max-Age` permite
al navegador recordar la respuesta y no repetir la consulta en cada petición.

*(Ver Figura 5.3: la verificación previa y la petición real.)*

Esa distinción explica un detalle que confunde al diagnosticar: **en el panel de red
aparecen dos peticiones donde el código escribió una sola.** La primera, con método
`OPTIONS`, no la emitió el código: la emitió el navegador. Y si esa primera falla, la
segunda **nunca se emite**, de modo que el servidor jamás se entera de que alguien
quiso hacer algo.

Cuando se envían cookies, la configuración se vuelve estricta: **el servidor no
puede responder con el comodín `*`**; debe devolver el origen exacto y declarar
explícitamente que admite credenciales.

> **💡 PARA ENTENDER**
> Tres cosas sobre los errores de CORS que te van a ahorrar horas.
>
> **Una: el error es del navegador, no del servidor.** El servidor contestó
> perfecto. El navegador recibió la respuesta, no encontró la autorización, y
> **decidió no dejarte leerla**. Por eso el mensaje aparece en la consola y no en el
> panel de red como un código de error.
>
> **Dos: la petición sí llegó.** En una petición simple, el servidor la recibió y la
> procesó. Si era un `POST` que creaba algo, **lo creó** — vos no viste la respuesta,
> pero el efecto ocurrió.
>
> **Tres, y es la que importa: CORS se arregla en el servidor. Siempre.** No hay nada
> que puedas escribir en el frontend que lo resuelva. Cuando busques el error y
> encuentres un plugin del navegador que "desactiva CORS", entendé lo que estás
> haciendo: **lo desactivás para vos, en tu máquina.** Tus usuarios lo van a seguir
> teniendo. Es tapar el testigo del tablero.

---

## 5.7. Errores: tres categorías distintas

### 5.7.1. La clasificación

Un cliente serio distingue tres cosas que suelen tratarse igual:

| Categoría | Qué pasó | Cómo se detecta | ¿Reintentar? |
| --- | --- | --- | --- |
| **Red** | La petición no llegó o no volvió | `fetch` **rechaza** | Sí, con espera creciente |
| **Protocolo** | Llegó y el servidor falló | `!respuesta.ok` con `5xx` | A veces |
| **Aplicación** | Llegó, se entendió, y la operación no procede | `!respuesta.ok` con `4xx` | **No** |

La tercera fila es la que más se maltrata. Un `409` porque el producto se quedó sin
stock **no es un error técnico**: es información de negocio que el usuario tiene que
ver. Mostrar "error de conexión" ante un `409` es mentirle.

### 5.7.2. El catálogo del TPI

La sección 14.1 del TPI define un catálogo de códigos de error, cada uno con su
código HTTP y la situación que lo produce. Que exista ese catálogo tiene una
consecuencia de diseño importante para el frontend: **el cliente puede distinguir
casos por un código estable en lugar de leer el texto del mensaje.**

Comparar textos es frágil —cambian, se traducen, se corrigen— y el código no. La
capa `api/` traduce el código a un tipo de error propio, y las vistas deciden qué
mostrar según ese tipo.

La sección 14.2 del TPI responde la pregunta de **dónde** ocurre esa traducción, y
la respuesta es la misma que este capítulo viene sosteniendo: en un solo lugar. Un
error que llega a la vista ya debe ser un objeto con significado, no una respuesta
HTTP cruda.

En la práctica eso se resuelve con un tipo de error propio que conserva el código y
lo que haga falta para decidir:

```js
export class ErrorDeApi extends Error {
  constructor(estado, codigo, mensaje, reintentarEn) {
    super(mensaje);
    this.estado = estado;             // 409
    this.codigo = codigo;             // "STOCK_INSUFICIENTE"
    this.reintentarEn = reintentarEn; // de Retry-After, si vino
  }
  get esDeNegocio()  { return this.estado >= 400 && this.estado < 500; }
  get esReintentable() { return this.estado >= 500 || this.estado === 429; }
}
```

Con eso, la vista deja de mirar números y pasa a preguntar por significado:

```js
try {
  await crearPedido(datos);
} catch (error) {
  if (error.codigo === "STOCK_INSUFICIENTE") mostrarFaltanteDeStock(error);
  else if (error.esDeNegocio) mostrarAviso(error.message);
  else mostrarErrorGenerico();
}
```

Nótese lo que **no** hace esa vista: no revisa `respuesta.ok`, no parsea el cuerpo,
no compara textos de mensajes. Todo eso ocurrió una vez, en la capa `api/`. Ese es
el sentido de la respuesta de la sección 14.2.

### 5.7.3. Reintento y el `429`

Ante un `429`, el servidor indica cuánto esperar mediante el encabezado
`Retry-After`. El TPI lo usa en su límite de intentos de autenticación, descrito en
su sección 4.4.

**Un cliente que ignora ese encabezado y reintenta de inmediato empeora exactamente
el problema que el límite intenta contener.** Y como el límite del TPI cuenta por
dirección de red además de por cuenta, un cliente mal escrito puede dejar sin
servicio a todos los usuarios de la misma red.

Cuando el reintento corresponde —fallo de red, o `5xx`—, la práctica correcta es
esperar cada vez más entre intentos, con una pequeña variación aleatoria. Sin esa
variación, todos los clientes que fallaron a la vez reintentan a la vez, y el
servidor que se estaba recuperando recibe otra avalancha.

---

## 5.8. El token: dónde vive y qué implica

El Capítulo 1 estableció que el token viaja en cada petición. Queda por resolver
dónde se guarda entre una y otra, y ninguna opción es enteramente satisfactoria.

| Lugar | Sobrevive al cierre | Accesible por script | Se envía solo |
| --- | --- | --- | --- |
| `localStorage` | Sí | **Sí** | No |
| `sessionStorage` | No | **Sí** | No |
| Cookie común | Sí | **Sí** | Sí |
| Cookie `HttpOnly` | Sí | **No** | Sí |
| Memoria | No | Sí | No |

Las tres primeras filas comparten un riesgo: **si hay un XSS, el token se puede
leer**, que es exactamente el ataque de la sección 4.7.2. La cookie `HttpOnly` es
inaccesible desde el código, pero al enviarse automáticamente introduce otro
problema —la falsificación de petición entre sitios— que exige su propia defensa.

**No hay una opción sin costo**, y por eso la defensa de fondo no es dónde se guarda
sino **que no haya XSS**: RN-F02 otra vez.

> **⚠️ OJO ACÁ**
> Vas a encontrar mucha discusión en internet sobre dónde guardar el token, con gente
> muy segura de que su opción es la correcta. Quedate con esto:
>
> **Si tenés un XSS, ya perdiste, guardes el token donde lo guardes.**
>
> ¿Lo tenés en una cookie `HttpOnly` que el script no puede leer? Bárbaro. El
> atacante no lee el token — **hace las peticiones desde tu propia página, con tu
> sesión.** No necesita robarlo: le alcanza con usarlo.
>
> Por eso la discusión sobre `localStorage` contra cookies es secundaria. Cambia
> **qué** puede hacer el atacante, no **si** puede hacer algo.
>
> La defensa que importa es la del Capítulo 4: que no haya XSS. Todo lo demás es
> reducir el daño de algo que no debería poder pasar.

Sobre esto, el TPI hace una elección explícita que conviene entender. Su sección
11.4 establece que, como la interfaz nativa de eventos **no permite fijar
encabezados**, el token viaja como parámetro de consulta **únicamente en el endpoint
de eventos**. Eso contradice lo que el Capítulo 1 advirtió sobre no poner datos
sensibles en la cadena de consulta, y la contradicción es real: es una concesión a
una limitación de la plataforma, acotada a un solo endpoint y acompañada de
mitigaciones del lado del servidor.

Y queda la regla **RN-F04**, que el Capítulo 1 anticipó y que acá se completa:

> Las guardas de ruta son usabilidad, no seguridad: el backend revalida siempre el
> rol y la propiedad del recurso.

Ocultar un botón de administración evita que un usuario común se confunda. **No
evita nada más.** Cualquiera puede emitir la petición con `curl`, y el único lugar
donde esa petición se puede rechazar es el servidor.

---

## 5.9. Eventos enviados por el servidor

### 5.9.1. Por qué SSE y no WebSockets

El Capítulo 1 dejó planteado que el servidor no puede iniciar la conversación. Hay
dos formas de sortearlo, y el TPI documenta en su sección 11.1 los cinco criterios
por los que eligió la menos conocida:

**Dirección.** El flujo es unidireccional: el servidor avisa y el cliente no manda
nada por ese canal. Todo lo que el cliente quiere hacer ya tiene su endpoint REST.
Un canal bidireccional resolvería un problema que no existe.

**Protocolo.** SSE **es HTTP**. Pasa por los mismos intermediarios, la misma
infraestructura y la misma autenticación. WebSockets exige un cambio de protocolo
que a menudo hay que habilitar explícitamente.

**Reconexión.** La interfaz nativa reconecta sola y reenvía el identificador del
último evento recibido, sin escribir una línea. Con WebSockets, la reconexión con
recuperación de estado es código propio.

**Costo por conexión.** Sobre un backend asincrónico, una conexión abierta cuesta
una corrutina y un socket.

**Lo que se pierde.** El cliente no puede mandar nada por el canal, y existe un
límite histórico de seis conexiones por dominio sobre HTTP/1.1. El TPI señala que
ese límite es irrelevante en su caso **porque el frontend abre una sola**, que es
justamente RN-F10.

### 5.9.2. El protocolo y su uso

El formato es texto plano. Cada evento es un bloque de líneas con etiqueta, y un
**doble salto de línea** lo cierra:

```
id: 1043
event: pedido_actualizado
data: {"pedido_id": 1043, "estado": "en_preparacion"}

```

Del lado del cliente, la interfaz nativa es breve:

```js
const canal = new EventSource(`/api/v1/eventos?token=${token}`);

canal.addEventListener("pedido_actualizado", (evento) => {
  const datos = JSON.parse(evento.data);      // data siempre es texto
  invalidar(["pedidos", datos.pedido_id]);    // ver RN-F09
});

canal.addEventListener("error", () => { /* reconecta solo */ });
```

Dos detalles: **`event.data` es siempre una cadena** y hay que parsearla; y el
`token` en la dirección corresponde a la concesión de la sección 5.8.

### 5.9.3. El hueco de la reconexión

Acá está la limitación que funda las tres reglas, y el TPI la declara sin
disimulo en su sección 11.3: **el mecanismo de publicación del backend no persiste
los mensajes.** Lo que se publica mientras un cliente no está suscripto, ese cliente
no lo recibe.

El TPI resuelve el hueco **del lado del servidor**, y conviene conocer el
mecanismo porque explica qué puede y qué no puede esperar el cliente:

- En la **conexión inicial** el servidor emite un evento de sincronización.
- En una **reconexión**, el navegador reenvía el identificador del último evento
  recibido, y el servidor emite lo que haya quedado pendiente desde ese punto.
- Si el cliente estuvo desconectado **mucho tiempo**, la recuperación se acota: pasado
  cierto límite el servidor emite un evento de resincronización y el cliente vuelve a
  cargar desde cero.
- Un **comentario periódico** cada quince segundos mantiene viva la conexión, porque
  sin él un intermediario cierra la conexión inactiva y el cliente entra en un ciclo
  de reconexión permanente.

*(Ver Figura 5.4: el hueco de la reconexión y su recuperación.)*

**Ninguno de esos mecanismos garantiza la entrega en todos los casos.** El propio
diseño admite que puede haber un salto. De ahí las tres reglas.

### 5.9.4. Las tres reglas

**RN-F09 — el evento invalida, no escribe.**

> Un evento recibido por SSE nunca escribe datos en la caché de consultas: invalida
> la clave correspondiente y deja que se recargue. El evento dice **qué** cambió, no
> **cuál** es el valor nuevo.

La razón es directa: si un evento se pierde, escribir con el contenido de los
eventos que sí llegaron deja la interfaz mostrando un estado **inventado**, que no
corresponde a ningún momento real del servidor. Invalidar y recargar produce siempre
un estado consistente, aunque se hayan perdido eventos por el camino.

```js
// MAL: si se perdió un evento intermedio, el estado queda inventado
canal.addEventListener("pedido_actualizado", (e) => {
  const d = JSON.parse(e.data);
  cache.set(["pedidos", d.pedido_id], d);
});

// BIEN: el evento sólo dice qué mirar de nuevo
canal.addEventListener("pedido_actualizado", (e) => {
  const d = JSON.parse(e.data);
  cache.invalidar(["pedidos", d.pedido_id]);
});
```

**RN-F10 — una sola conexión por sesión.**

> La conexión de eventos es una sola por sesión: se abre en el arranque si hay
> sesión, contra el único endpoint de la sección 6.11, y se cierra en el logout.

Dos razones. El límite de seis conexiones por dominio sobre HTTP/1.1, que con
varias pestañas y varias vistas se alcanza rápido y **deja al resto de la aplicación
sin poder hacer peticiones**. Y el diseño del servidor: la sección 11.4 del TPI
establece que el servidor resuelve a qué canales corresponde suscribir a cada actor
y **multiplexa todo por la misma conexión**.

**RN-F11 — la interfaz nunca depende del evento.**

> Toda vista que muestra datos vivos declara además su intervalo de recarga de
> respaldo, más largo; si el canal se cae, la pantalla se actualiza igual.

Es la consecuencia lógica de todo lo anterior. Si el canal puede fallar y el
mecanismo no garantiza la entrega, **una interfaz que sólo se actualiza por eventos
puede quedarse mostrando información vieja indefinidamente**, sin que nadie lo note.

El canal es una **optimización de latencia**, no la fuente de verdad: con canal, la
pantalla se actualiza en el momento; sin canal, se actualiza más lento. Nunca deja
de actualizarse.

> **💡 PARA ENTENDER**
> Fijate en el razonamiento completo, porque es el mejor ejemplo del módulo de cómo
> una limitación técnica se convierte en tres reglas:
>
> **El mecanismo de publicación no persiste** → un evento se puede perder → por lo
> tanto:
>
> - No escribas con lo que llega (**RN-F09**), porque construirías un estado que
>   nunca existió en el servidor.
> - No abras más canales de los necesarios (**RN-F10**), porque cada uno es otra
>   cosa que se puede caer, y encima te comés el límite de conexiones.
> - No dependas del canal (**RN-F11**), porque se va a caer alguna vez.
>
> Y ahora lo importante para el TPI: **el panel de cocina va a funcionar perfecto en
> tu demo de quince minutos aunque violes las tres.** Los eventos van a llegar todos,
> nada se va a caer, y va a parecer que las reglas sobran.
>
> Se rompe a las tres horas de turno, cuando el wifi de la cocina parpadea y la
> pantalla queda mostrando pedidos viejos. **Y nadie se va a dar cuenta de que está
> mostrando pedidos viejos**, porque no hay ningún error: hay una pantalla que dejó
> de actualizarse.

---

## 5.10. Herramientas de diagnóstico

El **panel de red** es el instrumento central. Cuatro observaciones que se usan
poco y rinden mucho:

- El filtro **Fetch/XHR** aísla las peticiones del código de las del documento y sus
  recursos.
- La columna de **tiempos**, desplegada, separa la espera de resolución, la conexión,
  el tiempo hasta el primer byte y la descarga. Distinguirlos dice si la lentitud es
  del servidor o de la red.
- La **limitación de red** simula una conexión lenta. Es la única forma práctica de
  probar los estados de carga y los plazos de espera de la sección 5.5.4.
- El modo **sin conexión** provoca el fallo de red de la sección 5.7.1 y permite
  verificar que el cliente lo distingue de un error del servidor.

*(Ver Figura 5.5: el panel de red con la limitación activada.)*

Para SSE, el panel tiene una vista específica: al seleccionar la conexión del canal
aparece una pestaña de **eventos recibidos**, con su identificador, tipo y contenido
en orden cronológico. Es donde se comprueba que la reconexión de la sección 5.9.3
funcionó: **tras reconectar deben aparecer los eventos que se habían perdido**.

*(Ver Figura 5.6: el flujo de eventos en el panel de red.)*

> **🧪 EXPERIMENTO**
> Este es el experimento que hace tangible RN-F11, y conviene hacerlo sobre el TPI
> apenas tengas el canal andando.
>
> 1. Abrí la vista de pedidos con el canal conectado y verificá en el panel de red
>    que los eventos llegan.
> 2. Activá el modo **sin conexión** en el panel de red.
> 3. Desde otra pestaña o con `curl`, hacé avanzar un pedido de estado.
> 4. Volvé a la vista. **Sigue mostrando el estado viejo, y no hay ningún error.**
> 5. Desactivá el modo sin conexión y mirá cuánto tarda en actualizarse.
>
> Ese paso 4 es el punto. **No hay mensaje, no hay ícono rojo, no hay nada**: hay una
> pantalla que se ve perfectamente normal y está mintiendo.
>
> Ahora imaginate esa pantalla en la cocina, con el cocinero mirándola para saber qué
> preparar. Por eso RN-F11 no es opcional.

---

## 5.11. Seguridad y evolución

Tres consideraciones cierran el capítulo.

**Todo lo que llega al cliente es visible.** El token, las respuestas, la lógica de
las guardas. Es la base de RN-F04 y no tiene solución técnica del lado del cliente:
la autorización se decide en el servidor.

**La cancelación es también una cuestión de corrección.** Una petición que se
resuelve después de que su vista desapareció puede escribir sobre estado que ya no
corresponde. El `AbortController` de la sección 5.5.4 evita esa clase de error, no
sólo el desperdicio.

**El límite de intentos es una defensa compartida.** El servidor lo impone, pero un
cliente que respeta `Retry-After` y espera cada vez más entre reintentos es parte de
la defensa. Un cliente que no lo hace es parte del problema.

En cuanto a la evolución, tres incorporaciones recientes resuelven cosas que hasta
hace poco exigían código propio: **`AbortSignal.timeout()`** reemplaza el plazo de
espera armado a mano; **`Array.fromAsync()`** permite recorrer flujos asincrónicos
con la comodidad de un arreglo; y la **interfaz de flujos** permite procesar una
respuesta grande a medida que llega, en lugar de esperar a tenerla completa en
memoria.

Vale una observación final sobre el diseño del TPI. Un canal de eventos con
recuperación por identificador, sincronización inicial y recarga de respaldo es
**la misma estrategia que usa cualquier sistema distribuido serio**: no confiar en la
entrega, sino diseñar para que la pérdida sea recuperable. Lo que se aprende acá no
es una particularidad del TPI.

---

## 5.12. Verificación

1. Predecir el orden de salida de un fragmento con código síncrono, `setTimeout`,
   promesas y `await`, y verificarlo.
2. Emitir una petición a un endpoint inexistente y **comprobar que el `catch` no se
   ejecuta**; corregirlo con `respuesta.ok`.
3. Convertir dos `await` independientes en un `Promise.all` y **medir la diferencia**
   con la limitación de red activada.
4. Provocar un error de CORS y explicar, mirando el panel de red, **si la petición
   llegó al servidor**.
5. Cancelar una petición en curso con `AbortController` y verificar en el panel de
   red que figura como cancelada.
6. Distinguir en el código el manejo de un fallo de red, un `500` y un `409`,
   mostrando un mensaje distinto para cada uno.
7. Simular un `429` y verificar que el cliente respeta el `Retry-After`.
8. Abrir un canal de eventos, cortar la conexión, provocar un cambio y **verificar
   tras reconectar que el evento perdido se recupera**.
9. Explicar por qué RN-F09 exige invalidar en vez de escribir, con un ejemplo de
   estado inconsistente concreto.

---

## 5.13. Errores frecuentes

**Creer que `fetch` falla ante un `500`.** No lo hace: la promesa se cumple. Sin
`if (!respuesta.ok)` el cuerpo del error se procesa como si fuera un resultado
válido (sección 5.5.3).

**Encadenar `await` de peticiones independientes.** Duplica o cuadruplica el tiempo
de carga sin ninguna razón (sección 5.4.2).

**Usar `forEach` con una función `async`.** No espera nada; el código sigue con las
operaciones en el aire (sección 5.4.2).

**Elegir `Promise.all` cuando corresponde `allSettled`.** Un fallo descarta todos
los resultados, incluidos los que sí funcionaron (sección 5.3.3).

**Mostrar "error de conexión" ante un `4xx`.** El servidor respondió, y con
información que el usuario necesita ver (sección 5.7.1).

**Intentar arreglar CORS desde el frontend.** No se puede. Y el complemento que lo
desactiva sólo lo desactiva en la máquina de quien lo instaló (sección 5.6.2).

**Omitir el plazo de espera.** `fetch` no tiene uno propio; una petición puede
quedar pendiente durante minutos (sección 5.5.4).

**No cancelar al desmontar.** Produce escrituras sobre estado obsoleto y la fuga de
la sección 4.9 (sección 5.5.4).

**Reintentar de inmediato ante un `429`.** Empeora la situación que el límite intenta
contener, y puede afectar a todos los usuarios de la misma red (sección 5.7.3).

**Escribir en la caché con el contenido del evento.** Si se perdió un evento
intermedio, el estado resultante no corresponde a ningún momento real del servidor.
Viola RN-F09 (sección 5.9.4).

**Abrir un canal de eventos por vista.** Consume el límite de conexiones y
contradice el diseño del servidor. Viola RN-F10 (sección 5.9.4).

**Confiar en que el evento siempre llega.** La pantalla se queda con datos viejos y
**sin ningún error visible**. Viola RN-F11 (sección 5.9.4).

---

## 5.14. Actividades

1. **Predicción de orden.** Dado un fragmento que combine `setTimeout`, tres
   promesas y dos `await`, escribir el orden de salida antes de ejecutarlo y explicar
   cada diferencia con lo observado, usando el modelo de la sección 3.10.2.

2. **Capa `api/` mínima.** Escribir una función `pedir(ruta, opciones)` que agregue
   el token, verifique `respuesta.ok`, traduzca el código del catálogo del TPI a un
   error propio y aplique un plazo de espera. Usarla para tres endpoints distintos y
   verificar que ninguna vista repite esa lógica.

3. **Serie contra paralelo.** Implementar la carga de un panel con cuatro
   estadísticas de las dos formas. Medir ambas con la limitación de red en tres
   megabits y documentar la diferencia. Justificar cuál combinador corresponde.

4. **Las tres categorías.** Construir una vista que muestre un mensaje distinto ante
   un fallo de red, un `500` y un `409` por falta de stock. Provocar los tres casos y
   documentar cómo se distingue cada uno en el código.

5. **Cancelación en una búsqueda.** Implementar un buscador de productos que cancele
   la petición anterior en cada tecla. Verificar en el panel de red que las
   peticiones aparecen canceladas, y explicar qué problema evita además del
   desperdicio.

6. **Exploración: el hueco de la reconexión.** Con el canal de eventos abierto,
   cortar la conexión, provocar tres cambios de estado desde otra pestaña, y
   reconectar. Documentar qué eventos se recuperan y cuáles no, y relacionar lo
   observado con el mecanismo de la sección 11.3 del TPI y con la regla RN-F11.
   *(Requiere el backend del TPI en ejecución.)*

7. **Exploración: qué protege CORS.** Emitir la misma petición desde una página de
   otro origen y desde `curl`. Documentar cuál es bloqueada y cuál no, y explicar a
   partir de eso a quién protege la política de mismo origen y por qué el servidor
   debe autorizar igual. *(Requiere `curl` y un servidor local.)*

---

## 5.15. Síntesis

1. La petición en segundo plano nació para que Outlook Web Access se pareciera a un
   cliente de escritorio, existió seis años sin nombre, y se volvió ubicua cuando un
   ensayo de 2005 la nombró.

2. **Asincronía no es concurrencia.** Sigue habiendo un solo hilo: `await` no espera,
   **cede el control y vuelve**. Una función `async` con un cálculo pesado adentro
   bloquea igual.

3. Las promesas resolvieron el manejo de errores, no la indentación: **un solo
   `catch` cubre toda la cadena**, algo que las funciones de retorno no podían hacer.

4. **`fetch` no rechaza ante un error HTTP.** Un 404 o un 500 cumplen la promesa,
   porque la operación de red salió bien. Sin `respuesta.ok`, el cuerpo del error se
   procesa como resultado válido.

5. Encadenar `await` de peticiones independientes **multiplica el tiempo de carga
   sin motivo**, y `forEach` no espera promesas.

6. **CORS no protege al servidor: protege al usuario** de que un sitio lea respuestas
   de otro con sus credenciales. Se arregla en el servidor y sólo ahí, y el error lo
   emite el navegador después de que la respuesta llegó.

7. Red, protocolo y aplicación son **tres categorías distintas** de error. Un `409`
   por falta de stock es información de negocio, no una falla técnica.

8. **Todo lo que llega al cliente es visible.** Las guardas de ruta son usabilidad
   —RN-F04— y ninguna forma de guardar el token es segura si hay un XSS.

9. El TPI eligió SSE por cinco criterios, y el decisivo es que **SSE es HTTP**: pasa
   por la misma infraestructura y la misma autenticación, y reconecta solo.

10. El mecanismo de publicación **no persiste los mensajes**, y de ese hecho salen
    las tres reglas: invalidar en vez de escribir (RN-F09), una sola conexión
    (RN-F10) y no depender del canal (RN-F11).

11. El canal es una **optimización de latencia, no la fuente de verdad**. Una
    interfaz que sólo se actualiza por eventos puede quedarse mostrando datos viejos
    **sin ningún error visible**, que es la peor forma de fallar.

---

## 5.16. Referencias y lecturas complementarias

Las fuentes normativas son estándares vivientes del WHATWG. El **Fetch Standard**,
en `fetch.spec.whatwg.org`, define la interfaz de la sección 5.5, el modelo de
respuestas y —lo más pertinente acá— el algoritmo de intercambio de recursos entre
orígenes de la sección 5.6, incluida la lista de condiciones que evitan la
verificación previa. La interfaz de eventos enviados por el servidor de la sección
5.9 está en el **HTML Living Standard**, en su sección sobre `EventSource`, que
documenta el formato del flujo, el reenvío del último identificador y el
comportamiento de reconexión. Las promesas y `async`/`await` están en **ECMA-262**,
mientras que el bucle de eventos que determina su orden de ejecución está en el
estándar HTML, distinción ya señalada en el Capítulo 3. La política de mismo origen
está descrita en la **RFC 6454** del IETF, y los códigos de estado citados
corresponden a la **RFC 9110**.

Del TPI conviene tener presentes cuatro secciones al leer este capítulo: la **11.1**,
con los cinco criterios de la elección de SSE; la **11.3**, que documenta el hueco de
la reconexión y su recuperación del lado del servidor; la **11.4**, sobre la
autorización del canal y la concesión del token en la cadena de consulta; y la
**14.1** con su catálogo de errores, que es lo que la capa `api/` traduce.

Como bibliografía de estudio, Archibald, *Tasks, microtasks, queues and schedules*
(2015) sigue siendo la explicación más precisa del orden de ejecución de la sección
5.3.1. Para el diseño de clientes resistentes a fallos, el capítulo sobre reintentos
y espera creciente de Beyer y otros, *Site Reliability Engineering* (O'Reilly, 2016,
de lectura libre en `sre.google/books`) explica por qué la variación aleatoria de la
sección 5.7.3 no es un detalle. Sobre CORS, la documentación de MDN y la
**OWASP HTML5 Security Cheat Sheet** cubren los casos que la especificación deja
implícitos. Y el ensayo original de Garrett, *Ajax: A New Approach to Web
Applications* (Adaptive Path, 2005), se lee en veinte minutos y muestra con claridad
qué se consideraba imposible antes de que la técnica se difundiera.

---

**Continúa en:** Capítulo 6 — TypeScript: tipos sobre JavaScript y el contrato de la
API, donde las respuestas que este capítulo trae sin forma conocida adquieren una,
y donde el `total` que viaja como cadena decimal —RN-F08— encuentra su tipo
correcto.
