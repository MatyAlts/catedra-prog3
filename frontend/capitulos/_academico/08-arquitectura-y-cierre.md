# Capítulo 8 — Arquitectura: Feature-Sliced Design, estado y el TPI

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 8.1. Alcance de la clase

Los siete capítulos anteriores dejaron todas las piezas construidas: un documento,
sus estilos, un lenguaje, el árbol que ese lenguaje modifica, la red, los tipos y
los componentes. **Este capítulo las ordena.**

La pregunta que lo abre no es técnica sino de método: cuando un proyecto tiene
setenta endpoints, veintitrés entidades y cinco personas trabajando en paralelo,
**¿dónde va cada cosa, y qué le puede pedir cada pieza a las demás?** Un sistema sin
respuesta a eso no falla de golpe: se vuelve progresivamente más lento de modificar,
hasta que cada cambio requiere entender el conjunto entero.

Cuatro de las once reglas obligatorias se fundan acá, y con ellas el módulo cierra
las once. **RN-F03** separa el estado del cliente del estado del servidor. **RN-F06**
ordena la secuencia de arranque. **RN-F07** resuelve el problema que el Capítulo 1
dejó planteado sobre la idempotencia del checkout. Y **RN-F04** —anticipada dos
veces— encuentra acá su lugar definitivo como decisión de arquitectura.

Hay además un cierre que este capítulo debe a todo el módulo. El TPI declara en su
sección 2.4 que la modalidad de entrega **asume que el estudiante trabajará junto
con un agente de IA**, y enuncia el criterio pedagógico que lo gobierna:

> La herramienta no sustituye la comprensión: el documento está escrito para que
> **ninguna de sus decisiones pueda copiarse sin entenderse**, porque cada una viene
> acompañada de su porqué y de su alternativa descartada.

Ese es, palabra por palabra, el método de los ocho capítulos de este módulo. La
sección 8.10 lo convierte en algo operativo: qué pedirle a un agente, qué revisarle,
y cuáles de las once reglas rompe **por defecto** si nadie se lo impide.

Al finalizar la clase, el alumno debe poder **ubicar cualquier archivo del frontend
del TPI en su capa**, justificar qué puede importar y qué no, y explicar las once
reglas como un sistema y no como una lista.

**Contenidos**

1. Por qué la organización por tipo de archivo colapsa.
2. Las capas del TPI y su regla de dependencias.
3. Las nueve piezas y sus responsabilidades.
4. Estado del cliente y estado del servidor: la regla RN-F03.
5. Los seis stores y la excepción declarada.
6. El estado del servidor y la invalidación por eventos.
7. El arranque en siete pasos y la regla RN-F06.
8. Guardas de ruta: la regla RN-F04 como decisión de arquitectura.
9. El checkout y la regla RN-F07.
10. Las once reglas como sistema.
11. Trabajar con agentes de IA sobre esta base.

---

## 8.2. Por qué la organización por tipo de archivo colapsa

La forma más difundida de organizar un proyecto de frontend agrupa los archivos por
**qué son**:

| Carpeta | Contiene |
| --- | --- |
| `src/components/` | `Boton.ts` · `TarjetaProducto.ts` · `FilaPedido.ts` · `Grafico.ts` … |
| `src/services/` | `productos.ts` · `pedidos.ts` · `auth.ts` · `estadisticas.ts` … |
| `src/utils/` | `formato.ts` · `validacion.ts` · `fechas.ts` … |
| `src/types/` | `producto.ts` · `pedido.ts` · `usuario.ts` … |
| `src/store/` | `carrito.ts` · `sesion.ts` · `ui.ts` … |

Cinco carpetas, y **ninguna dice de qué se trata el sistema**.

Funciona perfecto hasta unos cuantos miles de líneas, y después empieza a producir
cuatro problemas que conviene enumerar porque de cada uno sale una decisión de FSD.

**Primero: un cambio se reparte por todo el proyecto.** Modificar cómo funciona el
carrito exige abrir `components/`, `services/`, `store/`, `types/` y `utils/`. Las
cinco carpetas tienen archivos de todo lo demás mezclados, y ninguna dice cuáles
pertenecen al carrito.

**Segundo: la estructura no dice qué hace el sistema.** Mirando ese árbol no se sabe
si es una tienda, un sistema de facturación o un juego. **Dice con qué está hecho,
no de qué se trata.** Robert C. Martin llamó a lo contrario *arquitectura que grita*:
la estructura de carpetas debería anunciar el dominio.

**Tercero: todo puede importar todo.** No hay ninguna dirección declarada, así que
nada impide que un componente importe otro componente de una parte no relacionada, o
que una utilidad importe un store. Con el tiempo el grafo de dependencias se vuelve
una maraña, y aparecen las importaciones circulares del Capítulo 3.

**Cuarto: borrar es imposible.** Eliminar una funcionalidad exige encontrar sus
archivos entre los de todos los demás y averiguar si alguien más los usa. Como no se
puede estar seguro, **no se borra**, y el proyecto acumula código muerto. Es el mismo
fenómeno que el Capítulo 2 describió para las hojas de estilo.

La respuesta a esos problemas no es nueva. La **arquitectura hexagonal** de Alistair
Cockburn (2005) y la **arquitectura limpia** de Robert C. Martin (2012) ya proponían
lo esencial: **organizar por dominio, y declarar una dirección para las
dependencias.** Ambas nacieron del lado del backend —y son, de hecho, lo que el TPI
aplica en su sección 2.1—.

**Feature-Sliced Design** es la adaptación de esas ideas al frontend, formalizada
por la comunidad alrededor de 2021. Sus dos decisiones son:

**Primera: organizar por funcionalidad, no por tipo de archivo.** Todo lo que
pertenece al carrito vive junto, sin importar si es componente, servicio o tipo.

**Segunda: declarar capas con una dirección de dependencia obligatoria.** Cada capa
puede importar de las de abajo y **nunca** de las de arriba.

*(Ver Figura 8.1: organización por tipo frente a organización por funcionalidad.)*

> **💡 PARA ENTENDER**
> El cuarto problema es el más caro y el que menos se nota, así que fijate bien.
>
> **Un proyecto donde no se puede borrar sólo puede crecer.** Y no crece con cosas
> útiles: crece con restos de funcionalidades que ya nadie usa, que nadie se anima a
> tocar, y que igual hay que leer cada vez que alguien busca algo.
>
> Cuando todo lo de una funcionalidad vive en una carpeta y las dependencias tienen
> una sola dirección, borrar es trivial: **borrás la carpeta y el compilador te dice
> quién la extrañaba.** Si no protesta nadie, no la necesitaba nadie.
>
> Esa es la prueba de fuego de cualquier arquitectura de frontend, y te la podés
> hacer hoy sobre cualquier proyecto tuyo: *¿puedo borrar esta funcionalidad y saber
> en treinta segundos qué se rompió?* Si la respuesta es no, la estructura te está
> costando plata aunque no lo veas.

---

## 8.3. Las capas del TPI

### 8.3.1. La regla de dependencias

El TPI declara la regla en su sección 2.4, y es una sola frase con dos
prohibiciones:

> Los imports fluyen de arriba hacia abajo: **Arranque → Router → Vistas → Features
> (ui y service) → Stores, Cliente API y Cliente de eventos → Types.** Ninguna capa
> importa la capa superior y ninguna feature importa de otra feature en horizontal.

*(Ver Figura 8.2: las capas y la dirección de las dependencias.)*

Las dos prohibiciones resuelven problemas distintos:

**No importar hacia arriba** garantiza que las capas de abajo sean independientes de
las de arriba. Un store no sabe qué vista lo usa, y por eso se puede probar solo,
reutilizar en otra pantalla y entender sin leer el resto del sistema.

**No importar en horizontal entre funcionalidades** es la que sostiene la promesa de
la sección 8.2. Si la funcionalidad de pedidos importara de la de catálogo, borrar
catálogo rompería pedidos, y la carpeta dejaría de ser una unidad. Cuando dos
funcionalidades necesitan lo mismo, ese algo **baja a una capa inferior** donde ambas
pueden verlo.

### 8.3.2. Las nueve piezas

La sección 2.4 del TPI declara cada archivo y su responsabilidad:

| Pieza | Archivo | Responsabilidad |
| --- | --- | --- |
| Arranque | `app/main.ts` | Rehidrata la sesión antes de resolver la primera ruta |
| Router | `app/router.ts` | Mapea la ruta a una vista; invoca `destroy()` y `mount()` |
| Vista | `pages/<n>/index.ts` | Expone `mount(container, params)` y `destroy()` |
| Componente | `features/<f>/ui/<c>.ts` | Elemento personalizado con su ciclo de vida. **Recibe datos** |
| Servicio | `features/<f>/service.ts` | Encapsula el observador de consultas |
| Store | `store/<n>Store.ts` | Estado del cliente |
| Cliente API | `api/<recurso>.ts` | Funciones tipadas. **Convierte los importes** |
| Cliente de eventos | `api/eventos.ts` | Abre y cierra el canal; traduce eventos en invalidaciones |
| Tipos | `types/<dominio>.ts` | Interfaces espejo de los esquemas. **Sin lógica** |

Cada línea de esa tabla es un capítulo de este módulo puesto en su lugar. El
componente es el Capítulo 7; el cliente API es el Capítulo 5 con los tipos del
Capítulo 6; el cliente de eventos es la sección 5.9; los tipos son la sección 6.9.

Dos detalles de la tabla merecen atención porque son decisiones, no descripciones.

**El componente recibe datos.** No los busca. Un componente que llama a la API deja
de ser reutilizable y deja de ser probable sin servidor, como estableció el Capítulo
7.

**El cliente API convierte los importes.** Ese es el lugar único donde ocurre la
conversión de RN-F08. Si estuviera en la vista, habría tantas conversiones como
vistas, y bastaría con que una faltara.

### 8.3.3. La pieza transversal

Hay una excepción, y el TPI la declara explícitamente en lugar de dejarla implícita:

> La pieza `api/eventos.ts` es **transversal**: es el segundo lugar del frontend que
> conoce una ruta del backend, y **el primero que recibe datos sin haberlos pedido**.

Esa segunda mitad es lo interesante. Todo el resto del sistema funciona por
petición: alguien pide, algo responde, y el que pidió sabe qué hacer con la
respuesta. **El canal de eventos rompe ese modelo**: llegan datos que nadie pidió, en
cualquier momento, sin que haya una vista esperándolos.

Por eso no encaja en ninguna capa, y por eso su responsabilidad está acotada con
precisión: **traduce cada evento en una invalidación de clave** y nada más. No
actualiza vistas, no escribe en stores, no decide nada. Es RN-F09 expresada como
arquitectura y no como recomendación.

> **📌 NOTA**
> Fijate en cómo el TPI trata esta excepción, porque es una lección de diseño que
> vale para cualquier sistema que escribas.
>
> **La excepción está declarada, nombrada y acotada.** Dice cuál pieza es, por qué es
> distinta y qué puede hacer.
>
> Compará eso con la alternativa habitual: una arquitectura con una regla linda en el
> README y, en el código, tres o cuatro lugares que la violan porque "era más
> práctico". Esas violaciones no están documentadas, así que el próximo que llega no
> sabe si son excepciones legítimas o descuidos — y ante la duda, agrega la suya.
>
> **Una regla con excepciones declaradas es una regla. Una regla con excepciones
> silenciosas es una sugerencia.** Vas a ver lo mismo en RN-F03 y en RN-F08: las dos
> tienen su excepción escrita en la propia regla.

---

## 8.4. Estado del cliente y estado del servidor

### 8.4.1. La distinción

Esta es la distinción central del capítulo, y la que más ordena un frontend.

**El estado del servidor** es información que vive en la base de datos y de la que el
cliente tiene una **copia temporal**: los productos, los pedidos, el stock. El cliente
no es su dueño. Puede estar desactualizada en cualquier momento, y otro usuario
puede haberla cambiado hace un segundo.

**El estado del cliente** es información que **sólo existe en el navegador**: qué modal
está abierto, qué filtro se eligió, qué hay en el carrito antes de confirmarlo. No
tiene copia en el servidor y no puede quedar desactualizada, porque no hay nada
contra qué compararla.

Tratar a los dos igual es el error que produce la mayoría de los bugs de estado.
Poner el estado del servidor en un store del cliente obliga a resolver a mano
—cuándo recargarlo, cómo invalidarlo, qué hacer si otro lo cambió— todo lo que una
caché de consultas ya resuelve. De ahí la regla:

> **RN-F03.** El estado del servidor vive únicamente en el QueryClient y el del
> cliente únicamente en los stores; **la única excepción declarada son los campos de
> exhibición de `CartItem`**. Garante: revisión —sin garante automatizado, declarado
> como tal.

*(Ver Figura 8.3: estado del cliente frente a estado del servidor.)*

Vale señalar la honestidad de la última frase. La regla **declara que no tiene
garante automatizado**, en lugar de fingir que sí. Eso le dice al equipo dónde poner
la atención humana.

### 8.4.2. Los seis stores

La sección 13.1 del TPI declara los stores y —lo más importante— **qué persiste cada
uno**:

| Store | Gestiona | Persiste |
| --- | --- | --- |
| `authStore` | Token, usuario, autenticado | **Sólo el token** |
| `cartStore` | El carrito | Los ítems completos |
| `uiStore` | Modales, panel, notificaciones, tema | **Nada** |
| `filterStore` | Filtros del catálogo y del panel | **Nada** |
| `checkoutStore` | Paso, dirección, forma de pago, **clave de idempotencia** | Paso, forma, modalidad y clave |
| `eventosStore` | Estado de la conexión y último id recibido | **Sólo el último id** |

Los seis se componen igual, y esa uniformidad es deliberada: una sola forma de
declarar un store significa que quien entiende uno entiende los seis.

Tres decisiones de esa tabla vale la pena entender, porque ninguna es obvia.

**`authStore` persiste sólo el token, no el usuario.** El usuario se vuelve a pedir
en cada arranque, como muestra la sección 8.6. La razón: **los datos del usuario
pueden haber cambiado** —su rol, por ejemplo— y un usuario persistido sería estado
del servidor guardado en un store del cliente, exactamente lo que RN-F03 prohíbe.

**`uiStore` y `filterStore` no persisten nada.** Un modal abierto o un filtro elegido
no deberían sobrevivir a cerrar el navegador: reabrir la aplicación y encontrarla
como se dejó tres días antes es desconcertante, no cómodo.

**`eventosStore` persiste el último identificador recibido.** El TPI explica el
motivo: es lo que permite que **una recarga completa de la página no pierda el hueco
de eventos**. Sin eso, cada recarga vuelve a conectarse sin punto de referencia, y
todo lo publicado mientras tanto se pierde. Es la sección 5.9.3 llevada al caso del
usuario que aprieta F5.

### 8.4.3. La excepción declarada

`CartItem` guarda `nombre` y `precio_ref` —una copia de exhibición de datos que
pertenecen al servidor—, y es la excepción declarada a RN-F03.

La razón es concreta: **el carrito tiene que poder mostrarse sin pedir nada.** Si sólo
guardara identificadores, abrir la aplicación sin conexión mostraría un carrito vacío
o un cargando eterno.

Pero una copia puede quedar vieja: el precio pudo cambiar entre que el producto se
agregó y que el usuario abre el carrito. Por eso la excepción viene con su
contrapartida —al montar la vista del carrito se revalida— y por eso el campo se
llama `precio_ref`: **es una referencia de exhibición, no el precio de la
transacción.** El precio que vale es el que el servidor calcula al confirmar, que es
también lo que RN-F08 sostiene.

> **⚠️ OJO ACÁ**
> Esta distinción es la que más bugs te va a evitar en el TPI, así que llevátela
> clara:
>
> **Preguntate siempre: ¿quién es el dueño de este dato?**
>
> - Si el dueño es el servidor y vos tenés una copia → **QueryClient**. Puede quedar
>   vieja, y hay que tener una estrategia para eso.
> - Si el dato **sólo existe acá** → **store**. Nadie más lo puede cambiar.
>
> El error clásico es meter la lista de pedidos en un store "para tenerla a mano". Y
> ahí empezás: ¿cuándo la recargo? ¿qué hago si llegó un evento? ¿y si el usuario
> volvió después de dos horas? **Estás reimplementando a mano una caché de consultas,
> mal y sin darte cuenta.**
>
> Y cuidado con esto: si le pedís a un agente que te maneje "el estado de la
> aplicación", **te va a meter todo en un solo store.** Es el patrón más común que
> vio. Vos tenés que hacer el corte.

---

## 8.5. El estado del servidor y el puente con los eventos

El servicio de cada funcionalidad encapsula un **observador de consultas**: una pieza
que pide un dato, lo cachea bajo una clave, avisa cuando cambia y lo vuelve a pedir
cuando corresponde.

Lo relevante para la arquitectura es qué resuelve, porque es todo lo que no hay que
escribir a mano: caché por clave, deduplicación de peticiones simultáneas, estados
de carga y error, recarga en segundo plano, y el **intervalo de respaldo que RN-F11
exige**.

Y acá se cierra el arco del Capítulo 5. La regla **RN-F09** dice que un evento
invalida en lugar de escribir, y ahora se ve por qué esa regla es también una
decisión de arquitectura: **la invalidación es el único punto de contacto entre el
canal de eventos y el resto del sistema.**

```ts
// api/eventos.ts — la pieza transversal, y todo lo que hace
canal.addEventListener("pedido_actualizado", (evento) => {
  const { pedido_id } = JSON.parse(evento.data);
  queryClient.invalidateQueries({ queryKey: ["pedidos", pedido_id] });
});
```

Tres líneas, y ninguna toca una vista. El evento dice **qué mirar de nuevo**; quién
lo mira y cómo lo muestra es problema de las capas de arriba, que no saben que
existe un canal de eventos.

Esa indiferencia es la prueba de que la arquitectura está bien puesta: **si mañana
el canal se reemplaza por otra cosa, ninguna vista se entera.**

> **💡 PARA ENTENDER**
> Hay una prueba muy simple para saber si tu arquitectura está bien puesta, y te
> sirve para cualquier proyecto:
>
> **Elegí una pieza y preguntate: ¿cuántos archivos tendría que tocar para
> reemplazarla?**
>
> Con el canal de eventos bien puesto, la respuesta es **uno**: `api/eventos.ts`. Las
> vistas no saben que existe un canal — sólo saben que a veces sus datos se
> invalidan y se recargan.
>
> Con el canal mal puesto —cada vista suscribiéndose por su cuenta— la respuesta es
> *"todas las vistas que muestran datos vivos"*, y ahí ya no reemplazás nada: convivís
> con lo que hay.
>
> Hacé esa cuenta con las piezas de tu TPI: la caché de consultas, el cliente HTTP,
> el store del carrito. **El número que te dé es la medida real de tu
> arquitectura**, mucho más honesta que cualquier diagrama.

---

## 8.6. El arranque y la regla RN-F06

La sección 13.3 del TPI describe la secuencia de arranque en siete pasos, y cada uno
resuelve un problema concreto:

1. **Lee el estado persistido.** Sin token, marca la rehidratación como terminada y
   cede el control al enrutador sin abrir ningún canal.
2. **Con token, muestra el estado de carga** —nunca la vista de login— y pide los
   datos del usuario.
3. **Con respuesta exitosa**, completa el usuario y termina la rehidratación.
4. **Con 401**, limpia la sesión, termina la rehidratación como anónima y no abre el
   canal.
5. **Recién con la rehidratación terminada**, el enrutador resuelve la ruta y monta la
   vista sobre una sesión ya poblada.
6. **Precarga en paralelo** las claves de catálogo y el árbol de categorías, que
   quedan disponibles para todos los formularios de la sesión.
7. **Si hay sesión, abre el único canal**, enviando el último identificador
   persistido. No elige canal: el servidor los resuelve del actor.

*(Ver Figura 8.4: los siete pasos del arranque.)*

El paso 2 es la regla:

> **RN-F06.** Ninguna vista se monta antes de que termine la rehidratación de la
> sesión; mientras está en curso, el arranque muestra un estado de carga **y nunca la
> vista de login**. Garante: revisión.

El énfasis en "nunca la vista de login" no es estilístico. Sin esa regla ocurre lo
siguiente: hay un token guardado, pero verificarlo tarda trescientos milisegundos. En
ese lapso el estado dice "no autenticado" —todavía no se sabe—, el enrutador aplica
su guarda y **manda al login a alguien que tiene la sesión abierta**. Trescientos
milisegundos después la verificación vuelve bien y la aplicación lo saca del login.

El usuario ve un parpadeo de la pantalla de login en cada recarga. Es de los defectos
que más desconfianza generan, y su causa es exactamente esta: **confundir "todavía no
sé" con "no".**

> **💡 PARA ENTENDER**
> Guardate este principio, porque excede al TPI y se aplica a cualquier interfaz que
> escribas:
>
> **"Todavía no sé" es un estado, y hay que representarlo.**
>
> La mayoría de los frontends tienen dos: autenticado y no autenticado. Y ahí nace el
> parpadeo, porque durante la verificación **estás en un tercer estado que tu código
> no contempla**, así que cae en el que esté por defecto.
>
> ¿Te acordás del Capítulo 6, la unión discriminada? Es exactamente esto:
>
> ```ts
> type Sesion =
>   | { estado: "rehidratando" }        // ← el que casi todos se olvidan
>   | { estado: "anonima" }
>   | { estado: "autenticada"; usuario: Usuario };
> ```
>
> Con ese tipo, el compilador **no te deja** olvidarte del tercer caso: te lo va a
> exigir en cada `switch`. El bug del parpadeo se vuelve imposible de escribir, y
> eso es mucho mejor que acordarse de evitarlo.

---

## 8.7. Las guardas de ruta y la regla RN-F04

El enrutador aplica guardas antes de montar una vista: si la ruta exige un rol y el
usuario no lo tiene, no la monta. Y el TPI aclara qué significa eso exactamente:

> **RN-F04.** Las guardas de ruta son **usabilidad, no seguridad**: el backend
> revalida siempre el rol y la propiedad del recurso. Garante: **TST-06, TST-07 y
> TST-27, que ejercitan el backend sin pasar por la interfaz.**

El garante es lo más elocuente de la regla. **Los tres tests no usan el frontend en
absoluto**: le pegan directamente al backend, que es exactamente lo que haría un
atacante. Si el backend responde bien sin la interfaz de por medio, la seguridad está
donde tiene que estar.

Eso convierte una advertencia en una verificación. No dice "acordate de que el
cliente no protege": **demuestra que el servidor protege solo**, y lo demuestra
salteándose el cliente.

Lo que las guardas sí aportan es una experiencia coherente: no mostrar botones que
van a fallar, no cargar una vista cuyos datos van a devolver 403. Es valioso, y es
otra cosa.

---

## 8.8. El checkout y la regla RN-F07

El Capítulo 1 estableció que `POST` no es idempotente y que de esa propiedad de la
norma sale la necesidad de una clave. Acá está la regla completa:

> **RN-F07.** El checkout genera una clave de idempotencia con
> `crypto.randomUUID()` **al entrar al último paso**, la persiste en `checkoutStore`
> y la envía en el encabezado `Idempotency-Key`; **la clave se descarta recién en el
> `onSuccess` de la mutación**. Garante: TST-23 y TST-38 del lado del servidor.

Cada detalle de esa regla responde a un caso de fallo distinto, y vale desarmarlos.

**Se genera al entrar al último paso**, no al confirmar. Si se generara al confirmar,
cada clic produciría una clave nueva, y dos clics apurados crearían dos pedidos —que
es justamente lo que se quiere evitar—.

**Se persiste en el store**, y por lo tanto sobrevive a una recarga. Si el usuario
confirma, la red se corta y recarga la página, **al reintentar manda la misma
clave**, y el servidor reconoce el reenvío en lugar de crear un segundo pedido.

**Se descarta recién al confirmarse el éxito**, no al emitir la petición. Mientras la
respuesta no llegue, la clave debe seguir disponible para cualquier reintento. Sólo
cuando hay confirmación del servidor se puede descartar con seguridad.

*(Ver Figura 8.5: el ciclo de vida de la clave de idempotencia.)*

> **⚠️ OJO ACÁ**
> Los tres detalles de esa regla son tres bugs reales, y son de los que terminan en
> un reclamo de un cliente:
>
> - **Generar la clave al confirmar** → doble clic, dos pedidos, doble cobro.
> - **No persistirla** → se corta el wifi, el usuario recarga y reintenta, dos
>   pedidos.
> - **Descartarla al emitir** → la respuesta tarda, el usuario reintenta, y como ya no
>   hay clave, dos pedidos.
>
> Los tres terminan igual: **alguien recibe dos veces la misma comida y ve dos cargos
> en su cuenta.**
>
> Y ahora lo que más me interesa que veas: **un agente de IA te va a escribir la
> versión con los tres bugs.** No porque esté mal entrenado, sino porque la versión
> ingenua es la que aparece en el noventa por ciento de los ejemplos de checkout de
> internet.
>
> Vos vas a tener que mirar ese código y preguntarte las tres cosas: *¿cuándo se
> genera? ¿sobrevive a una recarga? ¿cuándo se borra?* **Esas tres preguntas son el
> módulo entero aplicado a diez líneas de código.**

---

## 8.9. Las once reglas como sistema

Llegado este punto conviene verlas juntas, porque no son once recomendaciones sino
**cuatro problemas con sus respuestas**.

| Problema de fondo | Reglas | Capítulo donde se demostró |
| --- | --- | --- |
| **Lo que se monta hay que desmontarlo** | RN-F01, RN-F05 | 4 y 7 |
| **Todo dato externo es hostil hasta prueba en contrario** | RN-F02, RN-F04, RN-F08 | 4, 5 y 6 |
| **La red no garantiza nada** | RN-F07, RN-F09, RN-F10, RN-F11 | 1 y 5 |
| **Cada dato tiene un dueño y un lugar** | RN-F03, RN-F06 | 8 |

Y hay un patrón de método que atraviesa las once y que vale más que la lista: **cada
regla declara su garante.** Algunas nombran un test —TST-45, TST-23, TST-06—; otras
dicen honestamente "revisión, sin garante automatizado".

Esa honestidad es una decisión de diseño. Una regla que declara no tener garante
automatizado **le dice al equipo dónde poner los ojos humanos**. Una que finge tenerlo
produce falsa confianza, que es peor que ninguna.

> **📌 NOTA**
> Prestá atención a lo que hace el TPI cuando una regla **no** tiene garante
> automático. No lo esconde: lo escribe.
>
> > Garante: revisión —**sin garante automatizado, declarado como tal**.
>
> Eso parece una confesión de debilidad y es exactamente lo contrario. Compará las
> dos formas de quedar:
>
> - **Declarar que no hay test:** el equipo sabe que RN-F03 depende de que alguien
>   mire, y sabe dónde poner atención en la revisión.
> - **No decir nada:** todos suponen que está cubierto, nadie mira, y el día que se
>   rompe nadie entiende cómo pasó.
>
> **La falsa confianza es peor que la ausencia de confianza.** Un sistema donde sabés
> qué está verificado y qué no es mucho más seguro que uno donde suponés que todo lo
> está.
>
> Y esto te sirve para la entrega: si hay algo que no llegaste a testear, **decilo**.
> El TPI mismo te da el permiso en su fundamentación — entender y declarar vale más
> que construir sin entender.

Y tres de las once resuelven el problema del olvido de la misma manera, que es la
lección de arquitectura del módulo:

- **RN-F01** no dice "acordate": exige una clase base que acumule las bajas.
- **RN-F08** no dice "cuidado con el dinero": declara un tipo que impide la
  operación.
- **RN-F06** no dice "esperá la sesión": ordena una secuencia donde montar antes es
  imposible.

> **💡 PARA ENTENDER**
> Si te llevás una sola idea de los ocho capítulos, que sea esta:
>
> **Las reglas que dependen de que alguien se acuerde, fallan. Las que hacen que
> equivocarse sea difícil, no.**
>
> Mirá la diferencia:
>
> | En vez de... | El TPI hace... |
> |---|---|
> | "acordate de dar de baja" | una clase base que da de baja sola |
> | "no operes con dinero en el front" | un tipo `string` que no se puede multiplicar |
> | "esperá la rehidratación" | una secuencia donde montar antes no existe |
>
> Eso no es rigor por rigor. Es reconocer algo simple: **a las dos de la mañana antes
> de entregar, nadie se acuerda de nada.** Y no es un problema de disciplina personal
> — es que las recomendaciones siempre fallan a escala, con cualquier equipo.
>
> Cuando diseñes algo, tuyo o del trabajo, preguntate: *¿estoy confiando en la
> memoria de alguien, o estoy haciendo que el camino fácil sea el correcto?*

---

## 8.10. Trabajar con agentes de IA sobre esta base

Acá cierra el módulo, y conviene empezar por lo que el TPI declara en su sección
2.4. La modalidad **asume** el trabajo con un agente y lo regula de dos maneras.

**El repositorio debe reflejar el proceso**: un historial de commits, **no un único
commit final**. Un commit único no permite distinguir un trabajo comprendido de uno
pegado, y el historial es la evidencia del proceso.

**Y si el plazo no alcanza**, el TPI indica el camino honesto: priorizar el núcleo
—arquitectura, modelo de datos, autenticación, API, stock y su concurrencia— y dejar
Redis, la cola de tareas y el tiempo real **declaradas y con su diseño entendido**,
aunque no se construyan enteras.

Esa segunda instrucción dice mucho sobre qué se evalúa: **entender y declarar vale
más que construir sin entender.**

El criterio que las une es el que este módulo viene sosteniendo desde el Capítulo 1:

> La herramienta no sustituye la comprensión: el documento está escrito para que
> **ninguna de sus decisiones pueda copiarse sin entenderse**, porque cada una viene
> acompañada de su porqué y de su alternativa descartada.

Ahora bien, ¿qué significa eso en la práctica, sentado frente a un agente?

**Un agente propone lo más frecuente, no lo más correcto.** Aprendió de una enorme
cantidad de código, y en esa masa lo mayoritario pesa más que lo bueno. Cuando lo
mayoritario coincide con lo correcto —y coincide muchas veces— el resultado es
excelente. Cuando no coincide, el resultado es plausible, compila, y está mal.

Este módulo mostró exactamente dónde no coinciden. Vale la pena tener la lista
junta, porque es la lista de revisión del TPI:

| Un agente escribe... | Y viola... | Capítulo |
| --- | --- | --- |
| `contenedor.innerHTML = \`...${dato}...\`` | RN-F02 | 4 |
| `addEventListener` sin su baja | RN-F01 | 4 y 7 |
| `try { await fetch(...) }` sin mirar `ok` | El manejo de errores | 5 |
| `total: number` en el tipo de la respuesta | RN-F08 | 3 y 6 |
| `await` encadenado de peticiones independientes | El tiempo de carga | 5 |
| Escribir en la caché con el contenido del evento | RN-F09 | 5 |
| `new Chart(...)` en cada actualización | RN-F05 | 7 |
| El `fetch` adentro del componente | La tabla de piezas | 7 y 8 |
| Todo el estado en un solo store | RN-F03 | 8 |
| Clave de idempotencia al confirmar, o sin persistir | RN-F07 | 8 |

**Diez patrones.** Ninguno es un disparate: todos son lo que aparece en la mayoría de
los ejemplos de internet. Y los diez producen código que funciona en una demo de
quince minutos.

De ahí salen tres formas de trabajar que conviene adoptar:

**Pedir con el porqué, no sólo el qué.** "Escribime la vista de pedidos" produce el
promedio de internet. "Escribime la vista de pedidos: los datos entran por
propiedad, las suscripciones se registran en `Disposable`, y los importes se
muestran sin operar sobre ellos" produce otra cosa. **El contexto que le des es la
diferencia entre las dos.**

**Revisar contra las once reglas, no contra la intuición.** "Se ve bien" no es un
criterio: los diez patrones de la tabla se ven bien. La lista de reglas sí es un
criterio, y se puede recorrer en dos minutos.

**Y si no entendés lo que devolvió, no lo integres.** No por purismo, sino por algo
práctico: **el código que no entendés no lo podés arreglar**, y el día que falle vas a
estar depurando algo que nunca leíste, contra un plazo. El TPI lo dice con otras
palabras al pedir que se declare lo que no se construyó: **entender y declarar vale
más que construir sin entender.**

> **📌 NOTA**
> Cerrando el módulo, quiero que veas para qué sirvió todo esto.
>
> No aprendiste HTTP para saber HTTP. No aprendiste el modelo de caja para saber CSS.
> No aprendiste el bucle de eventos para pasar una entrevista.
>
> Aprendiste todo eso para poder mirar cien líneas que te escribió un agente en tres
> segundos y decir: **"esto está bien, esto está mal, y esto de acá me falta".**
>
> Esa capacidad tiene un nombre viejo y es criterio técnico. **Y no se puede
> delegar** — es lo único de todo el proceso que no se puede delegar.
>
> El agente escribe más rápido que vos y siempre lo va a hacer. Bienvenido sea. Pero
> alguien tiene que saber **qué pedirle y cómo revisarlo**, y ese sos vos. Para eso
> fueron los ocho capítulos.

---

## 8.11. Herramientas de diagnóstico

Tres verificaciones específicas de este capítulo.

**El grafo de dependencias.** Existen herramientas que lo generan a partir de los
`import` estáticos del Capítulo 3 y **detectan violaciones de la regla de la sección
8.3.1**: importaciones hacia arriba, importaciones horizontales entre
funcionalidades, ciclos. Es la única forma práctica de que la regla se sostenga en un
proyecto de cinco personas, porque revisar a mano no escala.

**El estado en vivo.** Un store expone su estado actual y su cantidad de
suscriptores, y la caché de consultas expone sus claves con su antigüedad. Dos
comprobaciones valen la pena: **contar suscriptores** al montar y desmontar, que es
TST-45; y **mirar las claves** de la caché, donde una que no debería estar ahí suele
ser estado del servidor guardado en el lugar equivocado.

*(Ver Figura 8.6: el estado de los stores y las claves de la caché.)*

**El almacenamiento persistido.** El panel de aplicación del navegador muestra lo que
cada store guardó. Es donde se verifica lo de la sección 8.4.2: que `authStore`
guarde el token **y no el usuario**, que `uiStore` no guarde nada, y que la clave de
idempotencia esté ahí durante el checkout y desaparezca después.

> **🧪 EXPERIMENTO**
> El experimento que cierra el módulo, y es el que más te va a servir para el TPI.
>
> Abrí el panel de aplicación del navegador, andá al almacenamiento local y dejalo a
> la vista. Ahora recorré la aplicación mirando **sólo eso**:
>
> 1. Iniciá sesión. **Debe aparecer el token, y no el usuario.** Si aparece el usuario,
>    hay estado del servidor guardado en un store: RN-F03.
> 2. Agregá algo al carrito. Aparecen los ítems, con `nombre` y `precio_ref` — la
>    excepción declarada.
> 3. Abrí un modal y aplicá un filtro. **No debe aparecer nada nuevo.**
> 4. Entrá al último paso del checkout. **Debe aparecer la clave de idempotencia.**
> 5. Recargá la página con F5. **La clave sigue ahí** — eso es RN-F07 funcionando.
> 6. Confirmá el pedido. La clave desaparece recién ahora.
>
> Seis pasos, y verificaste RN-F03, RN-F06 y RN-F07 **sin abrir un solo archivo de
> código.**
>
> Eso es lo que te da una arquitectura declarada: **se puede auditar desde afuera.**

---

## 8.12. Seguridad y evolución

Tres consideraciones cierran el capítulo y el módulo.

**La arquitectura no es una defensa.** Ninguna capa del frontend protege nada: RN-F04
lo dice y sus tres tests lo demuestran salteándose la interfaz. Lo que la
arquitectura sí hace es **concentrar las decisiones sensibles en pocos lugares**
—el token en un store, la conversión de importes en la capa de acceso, la
sanitización en un solo punto—, y pocos lugares se pueden revisar; muchos, no.

**Lo persistido sobrevive al código.** Lo que se guardó con una versión anterior sigue
ahí cuando el código cambió, y se lee con la forma nueva sin que nada avise. Es el
caso de la sección 6.10.1, y por eso lo que se persiste conviene mantenerlo mínimo:
exactamente lo que la tabla de la sección 8.4.2 declara.

**El estado compartido es el que más difícil se depura.** Cuantas más piezas escriben
en el mismo lugar, menos se puede saber quién lo cambió. RN-F03 y la regla de
dependencias son, en el fondo, dos formas de acotar quién puede escribir qué.

Sobre la evolución, una observación de fondo. Feature-Sliced Design no es una
tecnología: **es un acuerdo sobre dónde va cada cosa.** Las herramientas de este
módulo van a cambiar —Vite va a ser reemplazada, Tailwind va a tener competencia,
TypeScript va a incorporar cosas nuevas— y el acuerdo va a seguir sirviendo, porque
los cuatro problemas de la sección 8.2 no dependen de ninguna herramienta.

Y lo mismo vale para lo aprendido en los ocho capítulos. La semántica de HTTP no
cambió en treinta años. El modelo de caja tiene veinticinco. El bucle de eventos, el
mismo desde 1995. **Lo que cambia rápido son las herramientas; lo que se aprende acá
dura.**

---

## 8.13. Verificación

1. Ubicar diez archivos cualesquiera del frontend del TPI en su capa y **justificar
   qué puede importar cada uno**.
2. Encontrar una importación que viole la regla de dependencias y explicar cuál de
   las dos prohibiciones rompe.
3. Clasificar diez datos del sistema como estado del cliente o del servidor,
   justificando por su dueño.
4. Explicar por qué `authStore` persiste el token y no el usuario.
5. Explicar por qué `eventosStore` persiste el último identificador, relacionándolo
   con la sección 5.9.3.
6. Reproducir el parpadeo de la pantalla de login quitando el estado de rehidratación,
   y corregirlo con la unión discriminada de la sección 8.6.
7. Verificar en el panel de aplicación que la clave de idempotencia **aparece al
   entrar al último paso, sobrevive a una recarga y desaparece al confirmar**.
8. Explicar por qué los garantes de RN-F04 no usan el frontend.
9. Tomar código generado por un agente y **revisarlo contra los diez patrones** de la
   sección 8.10, documentando cuáles aparecieron.

---

## 8.14. Errores frecuentes

**Organizar por tipo de archivo.** Reparte cada cambio entre cinco carpetas y hace
imposible borrar una funcionalidad (sección 8.2).

**Importar hacia arriba.** Un store que importa de una vista deja de ser
independiente y arrastra medio sistema (sección 8.3.1).

**Importar de otra funcionalidad en horizontal.** Rompe la unidad de la carpeta; lo
compartido baja a una capa inferior (sección 8.3.1).

**Poner el estado del servidor en un store.** Obliga a reimplementar a mano caché,
invalidación y recarga. Viola RN-F03 (sección 8.4.1).

**Persistir el usuario junto con el token.** Los datos del usuario pueden haber
cambiado; se vuelven a pedir en cada arranque (sección 8.4.2).

**Confundir "todavía no sé" con "no".** Produce el parpadeo del login en cada
recarga. Viola RN-F06 (sección 8.6).

**Creer que las guardas de ruta protegen algo.** Son usabilidad; el backend revalida
siempre. Es RN-F04 (sección 8.7).

**Generar la clave de idempotencia al confirmar.** Un doble clic produce dos pedidos
(sección 8.8).

**No persistir la clave de idempotencia.** Una recarga tras un corte de red produce
dos pedidos (sección 8.8).

**Descartar la clave al emitir la petición.** Un reintento antes de la respuesta
produce dos pedidos (sección 8.8).

**Llamar a la API desde un componente.** Lo vuelve improbable sin servidor y
dependiente de una ruta (secciones 8.3.2 y 7.6.4).

**Integrar código de un agente que no se entiende.** El día que falle hay que
depurar algo que nunca se leyó, contra un plazo (sección 8.10).

---

## 8.15. Actividades

1. **Mapa del proyecto.** Dibujar el árbol de carpetas completo del frontend del TPI
   siguiendo la tabla de la sección 8.3.2, ubicando al menos tres funcionalidades.
   Para cada capa, escribir qué le está permitido importar.

2. **Auditoría de dependencias.** Sobre un proyecto propio, generar el grafo de
   importaciones y documentar todas las violaciones de la regla de la sección 8.3.1.
   Proponer para cada una si corresponde bajar algo de capa o invertir la dependencia.

3. **La distinción, aplicada.** Listar quince datos del sistema del TPI y clasificar
   cada uno como estado del cliente o del servidor, **justificando por su dueño**.
   Identificar los casos dudosos y explicar por qué lo son.

4. **El arranque completo.** Implementar los siete pasos de la sección 8.6 con la
   unión discriminada de tres estados. Demostrar que la vista de login **no puede
   montarse** durante la rehidratación, y explicar por qué el compilador ayuda.

5. **El ciclo de la clave.** Implementar RN-F07 completa y verificar los tres casos de
   fallo de la sección 8.8: doble clic, recarga tras corte de red, y reintento antes
   de la respuesta. Documentar qué pasa en cada uno con la implementación correcta y
   con cada una de las tres versiones defectuosas.

6. **Exploración: revisión de código generado.** Pedirle a un agente de IA una vista
   completa del TPI —catálogo o carrito— sin darle ninguna instrucción sobre las
   reglas. Revisar el resultado contra los diez patrones de la sección 8.10 y
   documentar cuáles aparecieron. Repetir el pedido dando el contexto de las reglas
   y comparar ambos resultados, midiendo cuántos patrones desaparecieron.

7. **Exploración: la arquitectura auditada desde afuera.** Sobre la aplicación en
   ejecución, verificar RN-F03, RN-F06 y RN-F07 **usando únicamente el panel de
   aplicación y el de red**, sin abrir el código. Documentar el procedimiento paso a
   paso y qué evidencia sostiene cada regla. Relacionar lo observado con la
   afirmación de la sección 8.11 sobre auditar desde afuera.

---

## 8.16. Síntesis

1. Organizar por tipo de archivo colapsa por cuatro razones, y la más cara es la
   menos visible: **un proyecto donde no se puede borrar sólo puede crecer.**

2. Feature-Sliced Design adapta al frontend dos ideas viejas del backend: **organizar
   por dominio y declarar una dirección para las dependencias.**

3. Las dos prohibiciones del TPI resuelven cosas distintas: **no importar hacia
   arriba** hace independientes las capas de abajo; **no importar en horizontal**
   mantiene cada funcionalidad como una unidad que se puede borrar.

4. La pieza transversal del canal de eventos **está declarada, nombrada y acotada**.
   Una regla con excepciones declaradas es una regla; con excepciones silenciosas es
   una sugerencia.

5. **Cada dato tiene un dueño.** Si el dueño es el servidor, es una copia que puede
   quedar vieja y va en la caché de consultas; si sólo existe en el navegador, va en
   un store. Confundirlos es reimplementar a mano una caché, mal.

6. `authStore` persiste el token **y no el usuario**, porque un usuario persistido
   sería estado del servidor en un store. `eventosStore` persiste el último
   identificador para que **una recarga no pierda el hueco de eventos**.

7. **"Todavía no sé" es un estado y hay que representarlo.** No hacerlo produce el
   parpadeo del login en cada recarga, y una unión discriminada lo vuelve imposible
   de escribir.

8. El garante de RN-F04 **no usa el frontend**: ejercita el backend directamente, que
   es lo que haría un atacante. Convierte una advertencia en una verificación.

9. Los tres detalles de RN-F07 —cuándo se genera la clave, que se persista, cuándo se
   descarta— son **tres bugs distintos**, y los tres terminan en un cliente con doble
   cargo.

10. Las once reglas son **cuatro problemas con sus respuestas**, y cada una declara su
    garante, incluso cuando ese garante es "revisión, sin automatizar". Esa honestidad
    le dice al equipo dónde poner los ojos.

11. **Las reglas que dependen de que alguien se acuerde, fallan. Las que hacen que
    equivocarse sea difícil, no.** Es la lección de arquitectura del módulo entero.

12. Un agente propone **lo más frecuente, no lo más correcto**, y este módulo mostró
    los diez lugares donde eso no coincide. Saber cuáles son —y poder revisarlos— es
    la capacidad que ningún agente reemplaza.

---

## 8.17. Referencias y lecturas complementarias

Las fuentes de la primera mitad del capítulo no son especificaciones sino
literatura de arquitectura. La **arquitectura hexagonal** fue formulada por Alistair
Cockburn en 2005 con el nombre de *puertos y adaptadores*, y su artículo original
sigue disponible en `alistair.cockburn.us`. Robert C. Martin desarrolló la
**arquitectura limpia** en su artículo homónimo de 2012 y en el libro *Clean
Architecture* (Prentice Hall, 2017), cuyo capítulo sobre la regla de dependencia
—las dependencias apuntan siempre hacia adentro— es el fundamento directo de la
sección 8.3.1; su noción de *arquitectura que grita* corresponde a la segunda crítica
de la sección 8.2. La metodología **Feature-Sliced Design** está documentada en
`feature-sliced.design`, con su vocabulario de capas y segmentos, y conviene leerla
sabiendo que el TPI la adapta: usa su principio de dependencias y su organización por
funcionalidad, con una nomenclatura propia.

Para las bibliotecas de estado, la documentación de **TanStack Query** —en particular
su discusión sobre la distinción entre estado del cliente y estado del servidor, que
es el tema de la sección 8.4.1— explica el problema mejor que la mayoría de los
textos de arquitectura, porque parte del caso concreto. La documentación de
**Zustand** cubre la composición de middlewares que el TPI declara idéntica en sus
seis stores, incluidos los mecanismos de persistencia parcial y de suscripción por
selector.

Del TPI conviene tener presentes cinco secciones al leer este capítulo: la **2.4**,
con la regla de dependencias y la tabla de piezas; la **2.5**, con las once reglas y
sus garantes; la **13.1**, con los seis stores y qué persiste cada uno; la **13.3**,
con los siete pasos del arranque; y la **2.4 de la Primera Parte**, sobre el trabajo
con agentes de IA, que es la que cierra la sección 8.10.

Y como cierre del módulo, tres lecturas que exceden lo técnico y ordenan el criterio.
Hunt y Thomas, *The Pragmatic Programmer* (2.ª edición, Addison-Wesley, 2019) trata
en su primer capítulo la responsabilidad sobre el propio trabajo, que es exactamente
lo que la sección 8.10 discute respecto de integrar código que no se entiende.
Brooks, *No Silver Bullet* (1986) explica por qué ninguna herramienta elimina la
complejidad esencial de un problema —sólo la accidental—, y se lee distinto hoy que
hace cuarenta años. Y Petzold, *Code* (2.ª edición, Microsoft Press, 2022) recorre el
camino desde una lamparita hasta una computadora, y es la mejor respuesta a la
pregunta que este módulo intentó responder ocho veces: **por qué conviene entender lo
que hay debajo de la herramienta que uno usa.**

---

## Cierre del módulo

Ocho capítulos, ocho problemas, ocho conjuntos de decisiones de diseño que alguien
tomó y que hoy explican por qué la web es como es.

El TPI espera un sistema funcionando. Pero lo que evalúa —y lo dice explícitamente en
su fundamentación— es otra cosa: **que ninguna de sus decisiones se haya copiado sin
entenderse.**

Para eso fue este módulo. No para que nadie sepa escribir un `addEventListener`, que
eso lo escribe un agente en un segundo. Para que cuando ese agente lo escriba, del
otro lado haya alguien que sepa preguntar **dónde está la baja.**
