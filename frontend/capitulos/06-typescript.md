# Capítulo 6 — TypeScript: tipos sobre JavaScript y el contrato de la API

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 6.1. Alcance de la clase

Los cinco capítulos anteriores construyeron una aplicación posible: se pueden pedir
datos, mostrarlos, reaccionar a eventos y recibir avisos del servidor. Todo eso
funciona sin TypeScript. **La pregunta que abre este capítulo es por qué el TPI lo
exige igual.**

La respuesta habitual —"para evitar errores"— es incompleta y por eso no convence.
El problema que TypeScript resuelve no es que JavaScript permita sumar un número y
un texto. Es otro, más aburrido y mucho más caro: **a partir de cierto tamaño, nadie
recuerda qué forma tiene cada objeto que circula por el programa.** ¿La respuesta de
pedidos trae `estado` o `estado_actual`? ¿`direccion` es un objeto o un
identificador? ¿`total` puede venir nulo?

En doscientas líneas esas preguntas se responden mirando. En un sistema con setenta
endpoints y veintitrés entidades, se responden mal, y el error aparece en ejecución,
tarde y lejos de su causa.

Este capítulo se ubica sexto y no primero por una razón deliberada, que ya se
anunció al cerrar el Capítulo 3: **para entender una solución hay que haber tenido
el problema.** Quien aprende TypeScript antes que JavaScript escribe anotaciones
para que el editor deje de subrayar, sin saber qué está previniendo.

Hay además una conexión directa y explícita con el TPI. La regla **RN-F08** —el
dinero que viaja como cadena decimal, fundada en el modelo numérico de la sección
3.5.4— declara cuál es su garante, y lo dice con todas las letras:

> Garante: revisión, y **el tipo TypeScript, que declara `string`**.

Es decir: **el mecanismo que este capítulo enseña es literalmente lo que hace
cumplir esa regla.** No es una herramienta de apoyo; es la que impide que alguien
escriba `total * cantidad` sin darse cuenta.

Y hay una advertencia que conviene anticipar, porque contradice lo que todo el mundo
supone. **TypeScript no promete que si compila, funciona.** Su propia
documentación de diseño declara como objetivo *no perseguido* el tener un sistema de
tipos demostrablemente correcto. Es una decisión, no una carencia, y entenderla es
la diferencia entre usar la herramienta y confiarle cosas que no puede garantizar.
La sección 6.10 muestra exactamente dónde los tipos mienten.

Al finalizar la clase, el alumno debe poder **traducir un esquema de la sección 7
del TPI a tipos**, escribir la capa de acceso a la API con esos tipos, y explicar
por qué el compilador no lo protege de una respuesta del servidor que no coincida.

**Contenidos**

1. Origen y objetivos de diseño de TypeScript.
2. Compilación y borrado de tipos.
3. Anotaciones, inferencia y los tres tipos especiales.
4. Formas de objeto: interfaces y alias.
5. Uniones, estrechamiento y guardas de tipo.
6. Genéricos con moderación.
7. El modo estricto: qué activa cada opción.
8. Del esquema del TPI al tipo.
9. El dinero y la regla RN-F08.
10. Dónde mienten los tipos: el borde de la red.
11. Herramientas de diagnóstico.
12. Evolución del lenguaje y de la plataforma.

---

## 6.2. Por qué existe TypeScript: origen y diseño

Para 2010, JavaScript ya no se usaba para validar formularios. Gmail, Google Maps y
las aplicaciones que siguieron a la técnica del Capítulo 5 tenían decenas de miles
de líneas, y aparecieron problemas que el lenguaje no había sido diseñado para
enfrentar: **no había forma de saber qué recibía una función sin leer su cuerpo, ni
de encontrar todos los usos de una propiedad, ni de renombrar algo con seguridad.**

Hubo tres intentos previos y conviene saber por qué fallaron, porque explican la
forma de TypeScript.

**ECMAScript 4** propuso incorporar tipado estático al lenguaje mismo. Se abandonó
en 2008, como vio el Capítulo 3, y con él la idea de que la solución viniera del
estándar.

**Closure Compiler**, de Google, anotaba los tipos en comentarios de documentación y
los verificaba con una herramienta externa. Funcionaba, pero los tipos vivían en
comentarios: el editor no los usaba, y nada obligaba a mantenerlos al día.

**Dart**, presentado por Google en 2011, fue el intento más ambicioso: **reemplazar
JavaScript** por un lenguaje nuevo con tipos. Fracasó como reemplazo, y el motivo es
la lección central: **nadie iba a reescribir su aplicación entera para empezar a
usarlo.**

Microsoft anunció TypeScript el 1 de octubre de 2012, con Anders Hejlsberg
—responsable de Turbo Pascal, Delphi y C#— al frente. Su apuesta partía
precisamente del fracaso de Dart, y de ahí salen las cuatro decisiones de diseño que
gobiernan todo el capítulo.

**Primera: es un superconjunto de JavaScript.** Todo archivo de JavaScript válido es
un archivo de TypeScript válido. **No hay migración**: se cambia la extensión, se
compila, y a partir de ahí se agregan tipos donde convenga. Esa decisión, que parece
menor, es la que resolvió el problema de adopción que hundió a Dart.

**Segunda: el tipado es estructural, no nominal.** Dos tipos son compatibles si
**tienen la misma forma**, sin importar cómo se llamen ni si uno declara implementar
al otro. Es lo opuesto a Java o C#, donde la compatibilidad depende del nombre y de
la jerarquía declarada. La razón es de coherencia: los objetos de JavaScript no
tienen clase en el sentido clásico, como estableció la sección 3.8, así que un
sistema nominal no habría podido describir el código real.

**Tercera: los tipos se borran.** El compilador **quita todas las anotaciones** y
emite JavaScript común. No hay biblioteca de TypeScript en ejecución, no hay
verificación en tiempo de ejecución, no hay costo. Y no hay garantía: la sección
6.10 desarrolla las consecuencias.

**Cuarta, y la menos conocida: el sistema de tipos no es sólido, a propósito.** Los
objetivos de diseño publicados por el equipo declaran explícitamente como **objetivo
no perseguido** aplicar un sistema de tipos demostrablemente correcto, y dan la
razón: buscar un equilibrio entre corrección y productividad. TypeScript admite
operaciones que pueden fallar en ejecución porque prohibirlas volvería imposible
tipar patrones de JavaScript perfectamente razonables.

> **💡 PARA ENTENDER**
> La cuarta decisión es la que más te va a servir y la que casi nadie te va a
> explicar. Léela dos veces:
>
> **TypeScript no te promete que si compila, anda.** Nunca lo prometió. Está escrito
> en sus objetivos de diseño, en la lista de cosas que **decidieron no hacer**.
>
> ¿Y por qué renunciaron a eso? Porque un sistema de tipos que no te deja mentir
> nunca **no puede describir el JavaScript que la gente realmente escribe.** Habrían
> tenido un lenguaje impecable que nadie podía usar sobre su código existente. Es el
> mismo intercambio de Dart, y ya sabían cómo terminaba.
>
> Entonces, ¿qué es TypeScript? **Una herramienta de productividad muy buena, no una
> prueba matemática.** Te va a atajar el noventa y pico por ciento de los errores de
> forma. El resto lo tenés que atajar vos, y la sección 6.10 te dice exactamente
> dónde mirar.
>
> El que cree que "compila, entonces está bien" es el que se lleva la peor sorpresa.

---

## 6.3. Compilación y borrado

El navegador no ejecuta TypeScript. Un compilador transforma el código y emite
JavaScript, y esa transformación tiene dos partes independientes:

1. **Verificación de tipos.** Se analizan las anotaciones y se reportan
   inconsistencias.
2. **Emisión.** Se quitan las anotaciones y se produce JavaScript.

Lo importante es que **son independientes**. Por defecto, el compilador emite
JavaScript **aunque haya encontrado errores de tipo**. La verificación es un informe,
no una traba, y eso sorprende a quien viene de un lenguaje compilado.

```ts
// Lo que se escribe
function calcularSubtotal(precio: number, cantidad: number): number {
  return precio * cantidad;
}

// Lo que se ejecuta
function calcularSubtotal(precio, cantidad) {
  return precio * cantidad;
}
```

*(Ver Figura 6.1: de la anotación al JavaScript emitido.)*

De ese borrado se desprenden tres consecuencias que hay que tener presentes desde el
primer día:

- **No se puede preguntar por un tipo en ejecución.** No existe nada equivalente a
  `if (x es Pedido)`. En ejecución no hay tipos: hay objetos.
- **Los tipos no cuestan nada.** El código que llega al navegador es idéntico al que
  se habría escrito a mano.
- **Los tipos no validan nada.** Declarar que algo es un `Pedido` no hace que lo sea.

El Capítulo 7 estudia la herramienta que el TPI usa para compilar. Vale adelantar un
detalle relevante: **esa herramienta no verifica los tipos.** Los borra y sigue de
largo, para ser rápida. La verificación es un paso aparte, y de ahí sale una
situación que confunde: **el proyecto arranca perfecto con errores de tipo
adentro.**

> **🧪 EXPERIMENTO**
> Comprobá el borrado con tus propias manos, porque es la base de todo lo que sigue.
>
> 1. Escribí un archivo `.ts` con una función tipada y un error de tipo deliberado
>    —pasarle un `string` donde va un `number`, por ejemplo—.
> 2. Compilalo con `tsc archivo.ts`.
> 3. Vas a ver el error en la consola. **Y ahora fijate que el archivo `.js` se generó
>    igual.**
> 4. Abrilo. Las anotaciones no están. Es JavaScript común y corriente.
> 5. Ejecutalo. Anda, o falla, según lo que hiciera — **pero el error de tipo no
>    aparece por ningún lado.**
>
> Eso es lo que hay que entender: **la verificación de tipos es un informe, no una
> traba.** Podés ignorarlo y seguir.
>
> Y de ahí sale algo práctico para el TPI: si tu proyecto arranca bien, **eso no
> significa que no tenga errores de tipo.** Hay que correr la verificación aparte, y
> el Capítulo 7 muestra dónde va ese paso.

---

## 6.4. Anotaciones, inferencia y tres tipos especiales

### 6.4.1. Anotar e inferir

```ts
const nombre: string = "Milanesa";     // anotación explícita
const nombre = "Milanesa";             // inferido: string
```

La segunda forma es preferible cuando el tipo es evidente. **Anotar lo obvio agrega
ruido y una cosa más que puede quedar desactualizada.** El lugar donde la anotación
sí es valiosa es en los límites: parámetros de función, valores de retorno públicos
y estructuras que cruzan módulos.

La inferencia distingue además según la declaración:

```ts
let estado = "pendiente";      // string  — se puede reasignar
const estado = "pendiente";    // "pendiente" — tipo literal
```

Con `const`, el tipo inferido es **el valor exacto**, no la categoría. Ese
comportamiento es la base de las uniones literales de la sección 6.9.4.

### 6.4.2. `any`, `unknown` y `never`

Tres tipos especiales, con propósitos muy distintos:

| Tipo | Significa | Efecto |
| --- | --- | --- |
| `any` | "No verifiques nada" | **Desactiva el sistema de tipos** para ese valor |
| `unknown` | "No sé qué es" | Obliga a estrechar antes de usarlo |
| `never` | "Esto no puede ocurrir" | El tipo vacío |

La diferencia entre los dos primeros es central:

```ts
function procesar(dato: any) {
  dato.loQueSea.queNoExiste();     // compila; explota en ejecución
}

function procesar(dato: unknown) {
  dato.loQueSea;                   // error de compilación: hay que verificar antes
  if (typeof dato === "object" && dato !== null && "id" in dato) {
    dato.id;                       // ahora sí
  }
}
```

**`any` es un agujero en el sistema de tipos.** Y su efecto se propaga: todo lo
derivado de un valor `any` también lo es, de modo que un solo `any` mal puesto puede
desactivar la verificación de una rama entera del programa.

`unknown` expresa la misma incertidumbre **sin renunciar a la verificación**, y es
el tipo correcto para todo dato que entra desde afuera. La sección 6.10 lo retoma.

> **⚠️ OJO ACÁ**
> `any` no es "un tipo flexible". Es **un agujero**, y lo peor es que se agranda solo.
>
> ```ts
> const config: any = leerConfiguracion();
> const limite  = config.paginacion.limite;   // any
> const paginas = calcular(limite);           // any
> const texto   = paginas.toUpperCase();      // compila. Y paginas es un número.
> ```
>
> Fijate lo que pasó: **un solo `any` al principio desactivó la verificación de toda
> la cadena.** Nadie escribió `any` en las tres líneas siguientes; lo heredaron.
>
> Y esto no te lo avisa nadie, porque técnicamente no hay error. Por eso el hábito
> más útil que podés adoptar es este: **pasá el cursor por tus variables y fijate si
> alguna quedó en `any` sin que la pidieras.** Si la encontraste, buscá para atrás
> hasta el `any` original. Ahí está el problema, no donde explotó.

`never` aparece en dos lugares: como retorno de una función que nunca termina
normalmente, y —lo más útil— para **verificar exhaustividad**, como muestra la
sección 6.6.

---

## 6.5. Formas de objeto

Dos maneras de nombrar la forma de un objeto:

```ts
interface Producto {
  id: number;
  nombre: string;
  descripcion?: string;         // opcional
  readonly creado_en: string;   // sólo lectura
}

type Producto = {
  id: number;
  nombre: string;
};
```

Las diferencias prácticas son pocas. Las interfaces admiten **fusión de
declaraciones** —dos declaraciones con el mismo nombre se combinan—, lo que sirve
para extender tipos de bibliotecas ajenas. Los alias admiten uniones,
intersecciones y tipos calculados, que las interfaces no. **La convención de la
mayoría de los proyectos es usar `interface` para formas de objeto y `type` para
todo lo demás**, y lo importante es elegir una y sostenerla.

> **📌 NOTA**
> Vas a encontrar discusiones larguísimas sobre `interface` contra `type`. Te ahorro
> el tiempo: **en el 95 % de los casos son intercambiables y no importa cuál elijas.**
>
> Lo que sí importa es ser consistente dentro del proyecto, porque un archivo con las
> dos formas mezcladas al azar hace pensar que la diferencia significa algo cuando no
> significa nada.
>
> Las dos diferencias reales, por si alguna vez te topás con ellas:
>
> - **`interface` se puede reabrir.** Dos declaraciones con el mismo nombre se
>   fusionan. Sirve para extender tipos de una biblioteca ajena; es una molestia
>   cuando pasa sin querer.
> - **`type` puede ser cualquier cosa**, no sólo un objeto: uniones, intersecciones,
>   tipos calculados. Una unión literal como `EstadoPedido` **tiene** que ser `type`.
>
> Regla práctica para el TPI: `interface` para las respuestas de la API, `type` para
> los estados y todo lo demás.

Acá se manifiesta el tipado estructural de la sección 6.2:

```ts
interface Punto { x: number; y: number; }
interface Coordenada { x: number; y: number; }

const p: Punto = { x: 1, y: 2 };
const c: Coordenada = p;          // válido: misma forma
```

En Java esto sería un error. En TypeScript no, porque **lo que importa es la forma y
no el nombre**.

*(Ver Figura 6.2: tipado estructural frente a nominal.)*

Hay una excepción a esa regla que confunde la primera vez. Al asignar un **objeto
literal** directamente, el compilador aplica una verificación adicional y rechaza
las propiedades de más:

```ts
const p: Punto = { x: 1, y: 2, z: 3 };   // error: 'z' no existe en Punto

const temp = { x: 1, y: 2, z: 3 };
const q: Punto = temp;                    // válido: ya no es un literal
```

La razón es pragmática: una propiedad de más en un literal casi siempre es un error
de tipeo, y avisar ahí resulta más útil que ser consistente.

---

## 6.6. Uniones, estrechamiento y guardas

Una **unión** expresa que un valor es una cosa u otra:

```ts
type EstadoPedido = "pendiente" | "confirmado" | "en_preparacion" | "entregado" | "cancelado";
```

Esa es la forma correcta de representar la máquina de estados de la sección 3.4 del
TPI. Con `string` a secas, `"entregdo"` compila. Con la unión literal, el compilador
lo rechaza **y además el editor autocompleta los cinco valores válidos**.

Para usar un valor de tipo unión hay que **estrechar**: convencer al compilador de
cuál de las alternativas es. Las herramientas para hacerlo:

| Guarda | Sirve para |
| --- | --- |
| `typeof x === "string"` | Primitivos |
| `x instanceof Error` | Clases |
| `"codigo" in x` | Presencia de una propiedad |
| `x !== null` | Descartar ausencia |
| `x.tipo === "exito"` | Uniones discriminadas |

La última es la más potente y merece detalle. Una **unión discriminada** es un
conjunto de formas que comparten una propiedad con valor literal distinto:

```ts
type Resultado =
  | { estado: "cargando" }
  | { estado: "exito"; pedidos: Pedido[] }
  | { estado: "error"; mensaje: string };

function render(r: Resultado) {
  switch (r.estado) {
    case "cargando": return mostrarCargando();
    case "exito":    return mostrarLista(r.pedidos);   // acá sí existe .pedidos
    case "error":    return mostrarError(r.mensaje);   // acá sí existe .mensaje
  }
}
```

Dentro de cada rama, el compilador **sabe exactamente qué propiedades existen**. Es
lo que hace imposible leer `r.pedidos` en la rama de error.

*(Ver Figura 6.3: el estrechamiento de una unión discriminada.)*

Y acá aparece el uso valioso de `never`, que convierte al compilador en un guardián
de la exhaustividad:

```ts
function render(r: Resultado) {
  switch (r.estado) {
    case "cargando": return mostrarCargando();
    case "exito":    return mostrarLista(r.pedidos);
    case "error":    return mostrarError(r.mensaje);
    default:
      const imposible: never = r;   // error si se agregó un caso sin contemplar
      throw new Error(`Estado no contemplado: ${imposible}`);
  }
}
```

Si mañana se agrega un cuarto estado al tipo `Resultado` y alguien olvida agregarlo
al `switch`, **el compilador falla en esa línea**, señalando exactamente el lugar. Sin
ese `default`, el olvido pasa silenciosamente y produce una pantalla en blanco.

> **💡 PARA ENTENDER**
> Este patrón es de lo más valioso que te llevás del capítulo, así que fijate en lo
> que realmente hace.
>
> El caso `default` **no maneja un error**: hace que el compilador te avise cuando
> agregaste un estado nuevo y te olvidaste de contemplarlo en algún lado.
>
> Pensalo en el TPI. La máquina de estados del pedido tiene cinco estados. Si mañana
> la cátedra agrega un sexto —"demorado", digamos— vos tenés que actualizar todas las
> vistas que muestran estado.
>
> Sin este patrón, las buscás a mano y **te vas a olvidar de una.** Con este patrón,
> **el compilador te lista todos los lugares** que hay que tocar, uno por uno, y no
> te deja compilar hasta que los arreglaste.
>
> Eso es lo que TypeScript te da de verdad: no te evita escribir bugs, **te evita
> olvidarte de lugares.**

---

## 6.7. Genéricos, con moderación

Un genérico permite escribir algo que funciona con muchos tipos **sin perder la
información del tipo concreto**:

```ts
async function pedir<T>(ruta: string): Promise<T> {
  const respuesta = await fetch(ruta);
  if (!respuesta.ok) throw new ErrorDeApi(respuesta.status);
  return respuesta.json() as T;
}

const productos = await pedir<Producto[]>("/api/v1/productos");
// productos es Producto[], no any
```

Sin el genérico, la función tendría que devolver `any` y cada uso perdería el tipo.

Se pueden restringir con `extends`, lo que permite usar propiedades dentro de la
función genérica:

```ts
function porId<T extends { id: number }>(items: T[], id: number): T | undefined {
  return items.find(item => item.id === id);
}
```

> **⚠️ OJO ACÁ**
> Los genéricos son el lugar donde el código de TypeScript se vuelve ilegible, y casi
> siempre por la misma razón: **se agregan por si acaso.**
>
> Si escribiste un tipo con tres parámetros genéricos anidados y tenés que pensar
> treinta segundos para leerlo, la pregunta no es cómo simplificarlo. La pregunta es
> **cuántos tipos distintos van a pasar realmente por ahí.**
>
> Si la respuesta es "uno", no necesitás un genérico: necesitás ese tipo.
>
> El caso donde sí valen la pena es claro y en el TPI es uno solo: **la capa `api/`**,
> donde una única función tiene que devolver `Producto[]`, `Pedido` o `Usuario` según
> a quién se llame. Ahí el genérico está haciendo algo real.
>
> En la lógica de una vista concreta, casi nunca.

Una advertencia de criterio: **los genéricos son adictivos y la mayoría del código
de una aplicación no los necesita.** Sirven en utilidades reutilizables —la capa de
acceso a la API es el caso típico— y estorban en la lógica de una vista concreta. Un
tipo genérico anidado en tres niveles suele indicar que la abstracción está mal
puesta, no que el problema sea complejo.

Nótese además el `as T` del primer ejemplo: **eso es una mentira al compilador**, y
la sección 6.10 explica por qué es inevitable ahí y qué hay que hacer al respecto.

---

## 6.8. El modo estricto

El TPI declara en su sección 1.3 que el frontend usa **tipado estricto**. Esa
palabra corresponde a una opción del compilador que activa un conjunto de
verificaciones. Las que más cambian el día a día:

| Opción | Qué exige |
| --- | --- |
| `noImplicitAny` | Todo parámetro sin tipo evidente debe anotarse |
| **`strictNullChecks`** | `null` y `undefined` **no son asignables a cualquier tipo** |
| `strictFunctionTypes` | Verificación más estricta de parámetros de función |
| `strictPropertyInitialization` | Las propiedades de clase deben inicializarse |
| `noImplicitThis` | `this` no puede quedar implícitamente en `any` |
| `useUnknownInCatchVariables` | La variable de un `catch` es `unknown`, no `any` |

**La decisiva es la segunda**, y merece explicación porque es la que más errores
previene. Sin ella, `null` es asignable a todo, de modo que este código compila sin
protestar:

```ts
function nombreDelCliente(pedido: Pedido): string {
  return pedido.cliente.nombre;   // ¿y si cliente es null?
}
```

Con la verificación activada, si el tipo declara que `cliente` puede faltar, esa
línea **no compila** hasta que se contemple el caso. El compilador obliga a decidir
qué pasa cuando no hay cliente, en lugar de descubrirlo cuando la pantalla queda en
blanco.

La opción existe por separado por una razón histórica: llegó en TypeScript 2.0, en
2016, cuando ya había mucho código escrito que no la resistía. Hoy **no hay motivo
para no activarla** en un proyecto nuevo, y el TPI la exige.

> **💡 PARA ENTENDER**
> Cuando actives la verificación estricta de nulos en código que no la tenía, te van
> a aparecer decenas de errores de golpe y la reacción natural es pensar que la
> opción es demasiado molesta.
>
> Dale vuelta la lectura: **cada uno de esos errores es un lugar donde tu programa
> puede explotar en producción.** No los creó la opción. Ya estaban. Lo único que
> cambió es que ahora los ves.
>
> El error clásico es este:
>
> ```ts
> const boton = document.querySelector("#pagar");
> boton.addEventListener("click", pagar);   // ERROR: boton puede ser null
> ```
>
> ¿Te acordás del Capítulo 4? `querySelector` devuelve `null` cuando no encuentra
> nada, y el famoso *Cannot read properties of null* aparece en ejecución.
>
> **El compilador acaba de atajarte ese bug antes de que exista.** No es una molestia:
> es exactamente para lo que pagás el costo de escribir tipos.

La última fila de la tabla también merece atención porque cambia un hábito:

```ts
try {
  await crearPedido(datos);
} catch (error) {           // error es unknown, no any
  error.message;            // error de compilación
  if (error instanceof ErrorDeApi) error.codigo;   // así sí
}
```

Es correcto: en JavaScript **se puede lanzar cualquier cosa**, no sólo errores.
Asumir que lo capturado tiene `message` es una suposición, y el modo estricto obliga
a verificarla.

---

## 6.9. Del contrato del TPI al tipo

### 6.9.1. Traducir un esquema

La sección 7 del TPI define los esquemas de request y response de cada endpoint.
Esa sección **es la especificación de los tipos del frontend**, y traducirla es la
tarea central de esta clase.

```ts
// Estados: unión literal, no string (sección 3.4 del TPI)
export type EstadoPedido =
  | "pendiente" | "confirmado" | "en_preparacion" | "entregado" | "cancelado";

export interface PedidoResponse {
  id: number;
  estado: EstadoPedido;
  total: string;               // ← cadena decimal. Ver 6.9.2
  creado_en: string;           // fecha en formato ISO
  items: ItemPedidoResponse[];
  direccion: DireccionResponse | null;
}
```

Dos decisiones ya visibles. `estado` es una unión literal y no `string`, por lo
visto en la sección 6.6. Y las fechas son `string`, no `Date`: **lo que llega por la
red es texto**, y declararlo `Date` sería declarar algo falso. La conversión, si hace
falta, ocurre explícitamente en la capa `api/`.

> **💡 PARA ENTENDER**
> Lo de las fechas parece un detalle y es el mismo principio que RN-F08, aplicado a
> otro campo.
>
> Si declarás `creado_en: Date`, el compilador te deja escribir
> `pedido.creado_en.getFullYear()`. Compila perfecto. **Y explota en ejecución**,
> porque lo que hay ahí es la cadena `"2026-08-25T14:30:00Z"`, y las cadenas no
> tienen `getFullYear`.
>
> El tipo mintió, y mintió porque vos se lo pediste.
>
> La regla general, y vale para todo el capítulo: **el tipo tiene que describir lo que
> realmente hay, no lo que te gustaría que hubiera.** Si el JSON trae texto, el tipo
> dice texto. Si querés un `Date`, lo construís vos, explícitamente, en la capa
> `api/` — el mismo lugar donde se convierte el importe de RN-F08.

### 6.9.2. El dinero

Acá converge todo. La sección 3.5.4 estableció que el tipo numérico de JavaScript no
puede representar exactamente ciertos decimales. La regla del TPI dice:

> **RN-F08.** Todo importe recibido llega como string decimal y se convierte a
> number en la capa `api/`, nunca en la vista; ninguna operación aritmética sobre
> dinero ocurre en el frontend **salvo el subtotal de exhibición del carrito**.
> Garante: revisión, y **el tipo TypeScript, que declara `string`**.

Esa última frase es la que le da sentido a este capítulo entero. **El tipo no es
documentación: es el mecanismo que hace cumplir la regla.**

```ts
interface PedidoResponse {
  total: string;      // ← el garante
}

const p: PedidoResponse = await pedir("/api/v1/pedidos/1043");
const doble = p.total * 2;   // ERROR de compilación
```

Si el tipo dijera `number`, esa multiplicación compilaría, produciría un resultado
con error de punto flotante, y nadie se enteraría hasta que las cuentas del mes no
cerraran. **Con `string`, el compilador la rechaza.** No porque entienda de dinero,
sino porque no se puede multiplicar texto — y esa restricción tonta es exactamente
la que hace falta.

Nótese además la excepción declarada: el subtotal de exhibición del carrito. Está
enunciada explícitamente porque es una excepción, no un permiso general. Todo lo
demás se calcula en el servidor.

> **📌 NOTA**
> Este es el punto que anticipé en el Capítulo 3, así que quiero que lo veas
> completo.
>
> Cuando le pidas a un agente que te tipe la respuesta del endpoint de pedidos, **te
> va a escribir `total: number`.** Sin dudar, sin advertencia, con total seguridad.
>
> Y va a tener razón en un sentido: es lo que hace todo el mundo, es lo que aprendió
> de millones de ejemplos, y `total` **suena** a número.
>
> El agente no sabe que ese campo cruzó una frontera donde el formato de punto
> flotante rompe la exactitud. Vos sí.
>
> **Ese es el módulo entero en un campo de un tipo.** Corregir ese `number` por
> `string` no es un detalle de estilo: es la diferencia entre un sistema que factura
> bien y uno que acumula centavos de diferencia hasta que alguien tiene que auditar
> el mes entero a mano.

### 6.9.3. Distinguir identificadores

Un problema que aparece cuando hay muchas entidades: todos los identificadores son
`number`, y por lo tanto son intercambiables para el compilador.

```ts
function cancelarPedido(pedidoId: number) { ... }
cancelarPedido(producto.id);     // compila. Y está mal.
```

Un **tipo de marca** resuelve eso agregando una propiedad imposible que sólo existe
para el sistema de tipos:

```ts
type PedidoId = number & { readonly __marca: "PedidoId" };
type ProductoId = number & { readonly __marca: "ProductoId" };

function cancelarPedido(id: PedidoId) { ... }
cancelarPedido(producto.id);     // ERROR: ProductoId no es PedidoId
```

Como los tipos se borran (sección 6.3), **en ejecución siguen siendo números
comunes**: la marca no existe fuera del compilador y no cuesta nada.

Es una técnica avanzada y no hace falta aplicarla en todas partes. Vale la pena
cuando hay muchos identificadores del mismo tipo primitivo circulando, que es
exactamente el caso de un sistema con veintitrés entidades.

### 6.9.4. Los tipos de la capa `api/`

Con todo lo anterior, la capa de acceso queda así:

```ts
export async function obtenerPedido(id: PedidoId): Promise<Pedido> {
  const respuesta = await fetch(`/api/v1/pedidos/${id}`, {
    headers: { Authorization: `Bearer ${token()}` },
    signal: AbortSignal.timeout(10_000),
  });
  if (!respuesta.ok) throw await construirError(respuesta);
  const crudo = (await respuesta.json()) as PedidoResponse;
  return aPedidoDeDominio(crudo);          // acá, y sólo acá, se convierte
}
```

Esa función concentra todo lo que los capítulos anteriores establecieron: el token
del Capítulo 1, la verificación de `respuesta.ok` del Capítulo 5, el plazo de espera,
y la conversión de RN-F08 **en un solo lugar**. Ninguna vista repite nada de esto.

---

## 6.10. Dónde mienten los tipos

Esta sección es la más importante del capítulo y la que casi nunca se enseña.

### 6.10.1. El borde de la red

```ts
const datos = await respuesta.json();
```

**`json()` devuelve `any`.** No puede hacer otra cosa: parsea texto en tiempo de
ejecución y el compilador no tiene forma de saber qué va a venir. En cuanto ese
valor se asigna a algo tipado, **el compilador acepta la afirmación sin verificarla**:

```ts
const pedido = (await respuesta.json()) as PedidoResponse;
```

Esa línea no comprueba nada. Es una **afirmación del programador**: "confiá en que
esto tiene esta forma". Si el servidor cambió un nombre de campo, si un campo
opcional vino nulo, si la respuesta es un error con otra estructura, **el compilador
no se entera** y el programa sigue como si todo estuviera bien. El error aparece
después, en cualquier parte, con un mensaje que no menciona el origen.

*(Ver Figura 6.4: dónde mienten los tipos.)*

Los tres lugares donde entra información sin verificar son siempre los mismos:

| Entrada | Por qué miente |
| --- | --- |
| `respuesta.json()` | Devuelve `any`; nadie comprueba la forma |
| `JSON.parse()` | Ídem: lo guardado en el navegador puede ser de otra versión |
| `as` y `any` | Son afirmaciones del programador, no verificaciones |

El caso del almacenamiento del navegador merece mención porque muerde en el arranque
de la aplicación: lo que se guardó con una versión anterior **sigue ahí** cuando el
código cambió, y se lee con la forma nueva sin que nada avise.

### 6.10.2. Validar en el borde

La solución conceptual es simple de enunciar: **verificar en ejecución, una sola
vez, en el punto de entrada.** El patrón es una función que recibe `unknown`,
comprueba lo que tiene que comprobar y devuelve el tipo, o falla:

```ts
function aPedidoResponse(dato: unknown): PedidoResponse {
  if (typeof dato !== "object" || dato === null) {
    throw new ErrorDeContrato("Se esperaba un objeto");
  }
  const d = dato as Record<string, unknown>;
  if (typeof d.id !== "number")     throw new ErrorDeContrato("id");
  if (typeof d.total !== "string")  throw new ErrorDeContrato("total");
  if (!ESTADOS.includes(d.estado as EstadoPedido)) {
    throw new ErrorDeContrato(`estado desconocido: ${d.estado}`);
  }
  return dato as PedidoResponse;
}
```

Nótese que el parámetro es `unknown` y no `any`: el compilador **obliga** a
verificar antes de tocar nada, que es exactamente lo que se quiere.

El TPI no declara en su stack ninguna biblioteca para validar **respuestas de la
API** —sí declara `@tanstack/form-core`, que valida formularios, que es otro
problema—, así que esta verificación es código propio y hay que dosificarla con
criterio. La recomendación
razonable es validar **las respuestas de los endpoints críticos** —los que mueven
dinero o cambian estados— y lo que se lee del almacenamiento del navegador al
arrancar, que es donde el desajuste de versiones es más probable.

Y conviene recordar dónde está la validación **real**: en el servidor, con los
esquemas de la sección 7 del TPI. Lo del cliente es defensa contra el desajuste de
contrato, no contra un atacante — porque, como estableció el Capítulo 5, **el
atacante no usa tu cliente.**

> **⚠️ OJO ACÁ**
> Esta es la trampa mental más peligrosa de TypeScript, y le pasa a todo el mundo:
>
> **Ves los tipos, ves que compila, y creés que el dato tiene esa forma.**
>
> No. Vos **declaraste** que la tiene. Es distinto.
>
> El momento exacto donde la ilusión se rompe es este:
>
> ```ts
> const pedido = (await respuesta.json()) as PedidoResponse;
> ```
>
> Ahí no hay ninguna verificación. **Cero.** Le estás diciendo al compilador "confiá
> en mí", y el compilador confía, porque para eso está el `as`.
>
> Si el backend renombra `total` a `monto_total`, tu tipo sigue diciendo `total`,
> todo compila igual de lindo, y en pantalla aparece `undefined`. El compilador no
> falló: **hizo exactamente lo que le pediste.**
>
> Regla para todo el módulo: **cada `as` que escribas es una promesa que hacés vos, no
> una verificación que hace la herramienta.** Contá los `as` de tu código. Cada uno es
> un lugar donde podés estar equivocado.

---

## 6.11. Herramientas de diagnóstico

El **editor** es la herramienta principal, y conviene usarla más allá del subrayado
rojo. Pasar el cursor sobre un identificador muestra **el tipo inferido**, que suele
ser más informativo que el declarado: es la forma de descubrir que una variable
quedó en `any` sin que nadie lo pidiera. Los comandos de ir a la definición y buscar
todas las referencias funcionan sobre el análisis de tipos y son la razón práctica
por la que renombrar deja de dar miedo.

*(Ver Figura 6.6: el tipo inferido al pasar el cursor.)*

El **compilador en línea de comandos** conviene ejecutarlo en modo de sólo
verificación, sin emitir archivos, y dejarlo corriendo en modo de observación
durante el desarrollo. Es lo que evita la situación de la sección 6.3: que la
aplicación arranque perfecta con errores de tipo adentro, porque la herramienta de
construcción no verifica.

*(Ver Figura 6.5: un error de verificación de nulos en el editor.)*

Dos opciones adicionales del compilador vale la pena conocer, porque atrapan una
clase de error que el modo estricto no cubre. Una advierte sobre **el acceso a un
índice de un arreglo**, que puede no existir aunque el tipo diga lo contrario. La
otra advierte sobre **propiedades opcionales** que se asignan explícitamente como
`undefined`. Ambas son estrictas hasta la incomodidad y no todos los proyectos las
activan; conocerlas ayuda a entender qué queda fuera del modo estricto.

---

## 6.12. Seguridad y evolución

Tres consideraciones cierran el capítulo.

**Los tipos no son un control de seguridad.** Se borran; no existen en ejecución. Un
atacante no compila el código: emite peticiones. Toda la validación con
consecuencias vive en el servidor, y esto es RN-F04 una vez más.

**`any` es una renuncia y se propaga.** Un `any` en un punto de entrada desactiva la
verificación de todo lo que se derive de él, sin ninguna señal. El modo estricto
prohíbe los implícitos, pero los explícitos siguen siendo legales.

**Las dependencias traen sus propios tipos, de calidad variable.** Un paquete puede
declarar tipos que no corresponden exactamente a su comportamiento real, y el
compilador confía en esa declaración igual que confía en un `as`.

Sobre la evolución, dos incorporaciones recientes y una tendencia de fondo.

El operador **`satisfies`** permite verificar que un valor cumple un tipo **sin
perder la inferencia del tipo concreto**, que era una tensión clásica entre anotar y
dejar inferir.

Las **anotaciones de tipo como comentarios**, una propuesta en curso ante el comité
de ECMAScript, plantea que el lenguaje ignore explícitamente las anotaciones para
que el navegador pueda ejecutar código anotado sin compilar. Si prospera, cambiaría
el paso de construcción del Capítulo 7.

Y la tendencia de fondo: cada vez más herramientas del ecosistema derivan tipos
**directamente de la especificación de la API** —de un documento OpenAPI, por
ejemplo— en lugar de escribirlos a mano. Eso ataca justamente el problema de la
sección 6.10: si los tipos se generan desde el contrato, no pueden desincronizarse
del contrato.

---

## 6.13. Verificación

1. Compilar un archivo con un error de tipo deliberado y **verificar que el
   JavaScript se emitió igual**.
2. Declarar una variable con `const` y otra con `let` con el mismo valor, y explicar
   por qué el tipo inferido difiere.
3. Escribir una función con parámetro `unknown` y otra con `any`, y documentar qué
   permite cada una.
4. Traducir un esquema de la sección 7 del TPI a una interfaz, respetando la unión
   literal para los estados y `string` para los importes.
5. Intentar una operación aritmética sobre un campo de importe y **verificar que el
   compilador la rechaza**.
6. Implementar una unión discriminada con verificación de exhaustividad, agregar un
   caso al tipo y **comprobar que el compilador señala el `switch` incompleto**.
7. Escribir un `as` sobre el resultado de `json()`, provocar un desajuste con la
   respuesta real y documentar **dónde aparece el error** y cuánto se aleja de su
   causa.
8. Activar la verificación estricta de nulos en un archivo que no la resistía y
   documentar cuántos errores aparecen y de qué tipo.
9. Pasar el cursor sobre cinco variables del proyecto y verificar que ninguna quedó
   inferida como `any`.

---

## 6.14. Errores frecuentes

**Creer que si compila, funciona.** El sistema de tipos no es sólido por decisión
explícita de diseño, y los datos externos no se verifican (secciones 6.2 y 6.10).

**Usar `any` para que deje de subrayar.** Desactiva la verificación y se propaga a
todo lo derivado. El tipo correcto para lo desconocido es `unknown` (sección 6.4.2).

**Confiar en un `as` sobre el resultado de `json()`.** Es una afirmación, no una
verificación. El error aparece lejos de su causa (sección 6.10.1).

**Declarar los importes como `number`.** Reintroduce el error de punto flotante que
RN-F08 previene, y anula el garante que el propio TPI declara (sección 6.9.2).

**Declarar las fechas como `Date`.** Lo que llega por la red es texto; la conversión
es explícita y ocurre en la capa `api/` (sección 6.9.1).

**Usar `string` para los estados del pedido.** Pierde el autocompletado y admite
valores inexistentes. Corresponde una unión literal (sección 6.6).

**Omitir la verificación de exhaustividad.** Al agregar un estado, los `switch`
incompletos fallan en silencio (sección 6.6).

**Anotar todo, incluso lo obvio.** Agrega ruido y una cosa más para desactualizar.
La inferencia alcanza salvo en los límites (sección 6.4.1).

**Abusar de los genéricos.** La mayoría del código de una aplicación no los
necesita; un genérico anidado suele indicar una abstracción mal puesta (sección
6.7).

**Suponer que lo capturado en un `catch` es un `Error`.** En JavaScript se puede
lanzar cualquier cosa; el modo estricto lo tipa como `unknown` (sección 6.8).

**Confiar en la herramienta de construcción para verificar tipos.** No los verifica:
los borra. La verificación es un paso aparte (sección 6.3).

---

## 6.15. Actividades

1. **Del esquema al tipo.** Tomar tres esquemas de la sección 7 del TPI —uno de
   pedidos, uno de catálogo y uno de usuarios— y escribir sus interfaces completas,
   documentando cada decisión: por qué una unión literal, por qué `string` en los
   importes, por qué opcional o no.

2. **El garante en acción.** Escribir una función que calcule el total de un carrito
   a partir de las respuestas del servidor, y documentar exactamente en qué línea el
   compilador impide la operación aritmética. Implementar después la excepción
   declarada de RN-F08 —el subtotal de exhibición— y justificar dónde ocurre la
   conversión.

3. **Exhaustividad obligatoria.** Implementar la vista de estado de un pedido con
   una unión discriminada y verificación de exhaustividad. Agregar un sexto estado al
   tipo y documentar **todos** los lugares que el compilador señala.

4. **Capa `api/` tipada.** Escribir una función genérica de acceso a la API que
   incorpore el token, la verificación de `respuesta.ok` del Capítulo 5, el plazo de
   espera y el tipado del resultado. Usarla para cuatro endpoints y verificar que
   ninguna vista repite esa lógica.

5. **Identificadores distinguibles.** Implementar tipos de marca para tres
   identificadores del TPI y demostrar que el compilador rechaza pasar uno donde va
   otro. Verificar en el JavaScript emitido que **la marca desapareció**.

6. **Exploración: dónde mienten los tipos.** Tomar un endpoint del TPI, tiparlo, y
   modificar deliberadamente la respuesta del servidor renombrando un campo.
   Documentar en qué punto del programa aparece el error, cuánto se aleja de su
   causa y qué mensaje da. Escribir después una función de validación en el borde y
   repetir el experimento. *(Requiere el backend del TPI o un servidor simulado.)*

7. **Exploración: la solidez que no está.** Buscar en los objetivos de diseño
   publicados de TypeScript la lista de objetivos no perseguidos, e identificar tres
   construcciones del lenguaje que puedan compilar y fallar en ejecución. Para cada
   una, escribir un ejemplo mínimo que lo demuestre y explicar qué se ganó
   permitiéndola. *(Requiere consultar el repositorio del proyecto.)*

---

## 6.16. Síntesis

1. TypeScript no resuelve que JavaScript permita sumar un número y un texto:
   resuelve que **a escala nadie recuerda qué forma tiene cada objeto**. Es un
   problema de memoria humana, no de aritmética.

2. Dart fracasó porque exigía reescribir todo. **TypeScript es un superconjunto**, y
   esa decisión —adopción sin migración— es la que explica su éxito.

3. El tipado es **estructural**: lo que importa es la forma, no el nombre. Es
   coherente con el modelo de objetos dinámico del Capítulo 3.

4. **Los tipos se borran.** No cuestan nada en ejecución y no garantizan nada en
   ejecución. No hay forma de preguntar por un tipo cuando el programa corre.

5. **El sistema de tipos no es sólido, por decisión explícita.** Sus objetivos de
   diseño declaran no perseguir la corrección demostrable, a cambio de poder tipar
   JavaScript real. Es una herramienta de productividad, no una prueba.

6. `any` desactiva la verificación y **se propaga**; `unknown` expresa la misma
   incertidumbre sin renunciar a nada. Para lo que entra de afuera, `unknown`.

7. La **unión discriminada con verificación de exhaustividad** convierte al
   compilador en un buscador de lugares olvidados. Es lo más valioso del capítulo
   para un sistema con una máquina de estados.

8. **El tipo `string` en los importes es el garante de RN-F08**, y el TPI lo dice
   con esas palabras. Un `number` ahí reintroduce el error de punto flotante del
   Capítulo 3 y nadie se entera hasta que las cuentas no cierran.

9. **Los tipos mienten en el borde.** `json()` devuelve `any`, y un `as` es una
   afirmación del programador, no una verificación. Cada `as` es un lugar donde se
   puede estar equivocado.

10. Validar en ejecución, **una sola vez y en el punto de entrada**, es la forma de
    cerrar ese hueco. La validación con consecuencias sigue estando en el servidor.

11. Un agente de IA va a escribir `total: number` con total seguridad, porque es lo
    más común. **Lo más común y lo correcto no siempre coinciden**, y saber
    distinguirlos es el objetivo de todo el módulo.

---

## 6.17. Referencias y lecturas complementarias

TypeScript no tiene una especificación normativa vigente: la que existió se
abandonó en 2016 por resultar imposible de mantener al ritmo del lenguaje, de modo
que **la implementación es la referencia**. La documentación oficial en
`typescriptlang.org/docs` cumple ese papel, y su *Handbook* cubre en detalle la
inferencia, el estrechamiento y los genéricos de las secciones 6.4 a 6.7. Los
objetivos de diseño citados en la sección 6.2 —incluida la declaración explícita de
**no** perseguir un sistema de tipos demostrablemente correcto— están publicados en
el repositorio del proyecto, en el documento *TypeScript Design Goals* de su wiki, y
su lectura completa toma diez minutos que valen mucho la pena. Las opciones del
compilador de la sección 6.8 están documentadas una por una en la referencia de
`tsconfig`, con ejemplos de qué error atrapa cada una. El lenguaje que TypeScript
extiende sigue siendo **ECMA-262**, y todo lo que este capítulo no menciona sobre
semántica de ejecución está allí.

Como bibliografía de estudio, Cherny, *Programming TypeScript* (O'Reilly, 2019)
sigue siendo la mejor introducción sistemática para quien ya programa, y su capítulo
sobre el sistema de tipos explica el tipado estructural con más rigor que la
documentación. Para el uso avanzado, Vanderkam, *Effective TypeScript* (2.ª edición,
O'Reilly, 2024) está organizado en recomendaciones breves y trata explícitamente los
temas de la sección 6.10: el borde de los datos externos, el costo de `any` y cuándo
una aserción es legítima. El sitio comunitario *Type Challenges*, en su repositorio
público, ofrece ejercicios graduados sobre el sistema de tipos que exceden lo que
este módulo necesita pero muestran hasta dónde llega. Y sobre validación en tiempo
de ejecución, conviene revisar la documentación de alguna biblioteca del ecosistema
—aunque el TPI no declare ninguna en su stack— para conocer el patrón de derivar el
tipo estático a partir de un esquema verificable, que es la respuesta madura al
problema de la sección 6.10.

---

**Continúa en:** Capítulo 7 — Herramientas y componentes: Vite, Web Components y
Chart.js, donde el código tipado de este capítulo se convierte en algo que el
navegador puede ejecutar, y donde las suscripciones del Capítulo 4 encuentran por
fin el lugar donde darse de baja.
