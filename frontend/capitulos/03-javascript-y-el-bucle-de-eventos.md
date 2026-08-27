# Capítulo 3 — JavaScript: el lenguaje del navegador y su bucle de eventos

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 3.1. Alcance de la clase

Este es el primer capítulo del módulo donde se programa. Los dos anteriores
describieron una plataforma: un protocolo que trae documentos y un lenguaje
declarativo que decide cómo se ven. Este capítulo introduce el tercero, el único
que ejecuta instrucciones.

El alumno que llega acá ya sabe programar. Conoce variables, funciones,
condicionales, bucles y estructuras de datos, y los trabajó en Programación 1 y 2.
**Por eso este capítulo no enseña a programar en JavaScript: enseña en qué se
diferencia JavaScript de lo que ya sabe.** Y las diferencias son más profundas de
lo que parecen, porque no se limitan a la sintaxis.

Tres de ellas gobiernan todo lo demás y conviene enunciarlas de entrada.

**La primera es la coerción.** JavaScript convierte tipos automáticamente en vez de
fallar. En un lenguaje tipado, sumar un número y un texto es un error; acá produce
un resultado, y a veces uno sorprendente. Esa tolerancia no es un descuido: es la
misma decisión de diseño que el Capítulo 1 encontró en el HTML y el Capítulo 2 en
el CSS, aplicada ahora al código.

**La segunda es el modelo numérico.** JavaScript tiene un solo tipo de número, y no
puede representar exactamente `0.1`. Esto suena a curiosidad académica hasta que se
entiende su consecuencia: **es la razón por la que el TPI exige que todo importe
viaje como cadena de texto y no como número.** La regla RN-F08 —que a primera vista
parece una complicación gratuita del enunciado— nace de un límite del formato de
punto flotante que este capítulo estudia en la sección 3.5.4.

**La tercera es el modelo de ejecución.** JavaScript corre en **un solo hilo**, y ese
hilo es el mismo que dibuja la pantalla. Una operación que tarda es una pantalla
congelada: no una pantalla lenta, una pantalla que directamente no responde al
clic. Toda la asincronía que el Capítulo 5 va a estudiar existe para trabajar
alrededor de esa restricción, y el mecanismo que lo hace posible —el bucle de
eventos— es el tema central de la sección 3.10.

Ese último punto tiene un puente directo con el TPI que vale la pena señalar
ahora. La sección 1.4 del TPI dedica varias páginas al modelo de ejecución
asincrónico del backend, y la sección 5.5 exige que el cálculo del hash de
contraseña salga del bucle de eventos. **Es exactamente el mismo problema del otro
lado del cable**, y quien lo entienda acá va a entender aquello sin esfuerzo.

Al finalizar la clase, el alumno debe poder leer un fragmento de código
asincrónico y **predecir el orden en que se van a ejecutar sus partes**, que es la
habilidad que el Capítulo 5 da por supuesta.

**Contenidos**

1. Origen y objetivos de diseño de JavaScript.
2. Cómo y cuándo se ejecuta el código de una página.
3. Tipos primitivos y objetos; valor y referencia.
4. Coerción: las reglas reales y los valores falsos.
5. El modelo numérico y sus límites.
6. Declaraciones, ámbito, elevación y zona muerta temporal.
7. Clausuras.
8. Funciones y el valor de `this`.
9. Objetos, prototipos y clases.
10. Módulos.
11. El bucle de eventos: pila, tareas y microtareas.
12. Herramientas de diagnóstico y depuración.
13. Seguridad y evolución del lenguaje.

---

## 3.2. Por qué JavaScript es como es: origen y diseño

En 1995 las páginas web eran documentos estáticos. Toda interacción exigía enviar
un formulario al servidor y esperar una página nueva: validar que un campo no
estuviera vacío significaba un viaje de ida y vuelta completo. Netscape, que
dominaba el mercado de navegadores, quería resolver eso con lo que en su
documentación interna llamaba **un lenguaje de pegamento**: algo simple, para
autores de páginas que no eran programadores, que permitiera reaccionar a un clic
sin ir al servidor.

Brendan Eich fue contratado en abril de 1995 con ese encargo, y con una
restricción de marketing que resultó determinante: Netscape acababa de firmar un
acuerdo con Sun Microsystems para incorporar Java al navegador, y el lenguaje nuevo
**debía parecerse a Java**. No ser Java —para eso ya estaba Java— sino parecerse lo
suficiente como para presentarlo como su compañero menor.

Eich escribió el prototipo en **diez días**. El dato se repite como anécdota, pero
lo importante no es la velocidad sino lo que esa velocidad implicó: el lenguaje se
publicó sin el período de revisión que hubiera corregido sus decisiones
apresuradas, y una vez publicado ya no se pudo cambiar nada.

El resultado combinó tres linajes que no habían convivido nunca:

- La **sintaxis** de C y Java: llaves, punto y coma, `for`, `if`. Es la parte
  visible y la que produce la ilusión de familiaridad.
- Las **funciones de primera clase** de Scheme: las funciones son valores, se pasan
  como argumento, se devuelven, se guardan en variables. De acá salen las clausuras
  de la sección 3.6.3.
- Los **prototipos** de Self: no hay clases; los objetos heredan de otros objetos
  directamente. De acá sale el modelo de la sección 3.8.

Esa combinación explica la confusión más persistente del lenguaje: **parece Java y
funciona como Scheme.** Quien lo lee esperando lo primero se equivoca en todo lo
que importa.

El nombre siguió al marketing. Internamente fue **Mocha**, se publicó como
**LiveScript** en septiembre de 1995, y en diciembre pasó a llamarse **JavaScript**
al cerrarse el acuerdo con Sun. No tiene relación técnica con Java.

Microsoft respondió en 1996 con **JScript**, una implementación obtenida por
ingeniería inversa para Internet Explorer 3. Las diferencias entre ambas eran
suficientes para que un mismo script funcionara en un navegador y no en el otro, y
esa incompatibilidad —la misma guerra que el Capítulo 2 describió del lado del
CSS— llevó a Netscape a presentar el lenguaje ante ECMA International para su
estandarización. La primera edición de **ECMA-262** es de junio de 1997. El nombre
**ECMAScript** fue un compromiso: "JavaScript" era marca registrada de Sun.

La cronología posterior tiene un episodio que explica la forma actual del lenguaje.
**ECMAScript 4** fue un intento ambicioso de agregar clases, tipado estático y
módulos. El comité se dividió, la propuesta se abandonó en 2008, y de esa crisis
salió la decisión de avanzar en incrementos pequeños. **ES5** llegó en 2009,
**ES2015** en 2015, y desde entonces el estándar se publica **una vez por año**, con
las propuestas que hayan alcanzado la madurez suficiente dentro del comité TC39.

De todo ese recorrido salen cuatro decisiones de diseño, y la primera es la que
explica a las otras tres.

**Primera: no romper la web.** Es el principio rector absoluto del comité. Una
página escrita en 1997 debe seguir funcionando hoy. Esto significa que **ningún
error del diseño original se puede corregir** si hay páginas que dependen de él —y
siempre las hay—. Todo lo que se agrega, se agrega al lado; nada se quita.

**Segunda: tolerancia antes que rigor.** El lenguaje prefiere producir un resultado
antes que detenerse. Convierte tipos, ignora argumentos de más, entrega
`undefined` donde otro lenguaje fallaría. Coherente con el encargo original: estaba
pensado para autores que no eran programadores, y un error críptico los habría
expulsado.

**Tercera: objetos dinámicos y prototipos.** Los objetos no tienen forma fija: se
les agregan y quitan propiedades en cualquier momento. No hay clases en el modelo
subyacente, aunque desde 2015 exista la palabra `class`.

**Cuarta: un solo hilo.** El lenguaje no tiene concurrencia real en el sentido
clásico. Todo ocurre en un hilo, coordinado por el bucle de eventos de la sección
3.10.

*(Ver Figura 3.1: de Mocha al ciclo anual de ECMAScript.)*

> **💡 PARA ENTENDER**
> Acá tenés la clave para no frustrarte con este lenguaje, y te la digo derecho:
> **casi todo lo que te parece mal diseñado no es un error de diseño. Es un error
> de diseño que ya no se pudo corregir.**
>
> El ejemplo canónico es `typeof null`, que devuelve `"object"`. Es un bug de la
> implementación de 1995: los valores se guardaban con una etiqueta de tipo en los
> bits bajos, la etiqueta `000` significaba "objeto", y `null` era el puntero nulo
> —todos ceros—, así que se leía como objeto.
>
> Lo propusieron arreglar en ES4. Se rechazó. ¿Por qué? Porque hay código en
> producción, en algún lado del mundo, que hace `typeof x === "object"` contando con
> ese comportamiento. Arreglarlo rompería esas páginas.
>
> **Treinta años sosteniendo un bug de una tarde de 1995.** Cuando entendés eso,
> dejás de pelearte con el lenguaje y empezás a leerlo como lo que es: una capa de
> decisiones nuevas encima de decisiones viejas que nadie puede tocar.

---

## 3.3. Cómo y cuándo se ejecuta el código

El Capítulo 1 mencionó que un script en medio del documento detiene el parseo. Con
más precisión: existen cuatro formas de incluir código, y la diferencia entre ellas
es **cuándo se descarga y cuándo se ejecuta**.

| Forma | Descarga | Ejecución | Detiene el parseo |
| --- | --- | --- | --- |
| `<script>` | Al encontrarlo | Inmediata | **Sí**, durante ambas |
| `<script async>` | En paralelo | Apenas termina de descargar | Sí, sólo al ejecutar |
| `<script defer>` | En paralelo | Al terminar el parseo, en orden | No |
| `<script type="module">` | En paralelo | Al terminar el parseo, en orden | No |

El comportamiento por defecto —bloquear— tiene una razón histórica concreta:
`document.write()`. En 1995 un script podía escribir marcado en el punto exacto
donde estaba, así que el parser no podía seguir sin saber qué iba a escribir. Esa
función prácticamente no se usa hoy, pero el comportamiento no se puede cambiar,
por la primera decisión de diseño de la sección 3.2.

Los **módulos** son la forma que usa el TPI, y traen tres diferencias que no son
opcionales: se cargan diferidos por defecto, se ejecutan siempre en **modo
estricto** (sección 3.12), y **tienen su propio ámbito**, de modo que una variable
declarada en un módulo no contamina el resto de la página.

> **💡 PARA ENTENDER**
> La diferencia entre `defer` y `async` se explica con una pregunta: **¿tu script
> depende de que existan otros?**
>
> - `async` ejecuta apenas termina de bajar. Si tenés tres scripts, el orden de
>   ejecución es **el orden en que llegaron por la red**, o sea impredecible. Sirve
>   para cosas independientes de todo, como una métrica.
> - `defer` espera a que el documento esté parseado y **respeta el orden en que los
>   escribiste**. Es lo que querés casi siempre.
>
> Y acá está lo práctico: **`type="module"` ya se comporta como `defer`.** No hace
> falta agregarlo. Como el TPI usa módulos, este problema no lo vas a tener — pero
> lo vas a ver en cualquier código heredado que te toque mantener, y ahí la
> diferencia importa.

---

## 3.4. Tipos: primitivos y objetos

### 3.4.1. Los siete primitivos

JavaScript tiene siete tipos primitivos y un único tipo compuesto.

| Tipo | Ejemplo | Notas |
| --- | --- | --- |
| `number` | `42`, `3.14` | Punto flotante de doble precisión. **Uno solo** |
| `string` | `"milanesa"` | Inmutable |
| `boolean` | `true` | |
| `undefined` | `undefined` | "No se asignó valor" |
| `null` | `null` | "Ausencia deliberada de valor" |
| `symbol` | `Symbol("id")` | Identificador único |
| `bigint` | `9007199254740993n` | Enteros de precisión arbitraria |

Todo lo demás —objetos, arreglos, funciones, fechas— es del tipo `object`.

La distinción entre `undefined` y `null` se pregunta siempre, y la respuesta es de
intención: **`undefined` es lo que el lenguaje pone cuando no hay valor; `null` es
lo que el programador pone para decir que deliberadamente no hay valor.** Una
variable declarada sin asignar vale `undefined`; una propiedad que se vacía a
propósito se asigna `null`.

Que haya **un solo tipo numérico** merece atención. No existen enteros separados de
decimales: todo número es un punto flotante de 64 bits según la norma IEEE 754. Las
consecuencias son el tema de la sección 3.5.4.

### 3.4.2. Valor y referencia

Los primitivos se copian **por valor**; los objetos, **por referencia**.

```js
let a = 5;
let b = a;
b = 10;
console.log(a);        // 5 — a no se enteró

let p1 = { nombre: "Milanesa", precio: 4750 };
let p2 = p1;
p2.precio = 5000;
console.log(p1.precio); // 5000 — son el mismo objeto
```

En el segundo caso `p1` y `p2` no son dos objetos parecidos: **son dos nombres para
el mismo objeto**. La asignación copió la referencia, no el contenido.

*(Ver Figura 3.2: valor y referencia en memoria.)*

Esto explica un comportamiento que confunde: `const` **no hace inmutable un
objeto**. Impide reasignar el nombre, no modificar lo que hay del otro lado.

```js
const producto = { precio: 4750 };
producto.precio = 5000;      // válido: se modifica el objeto
producto = { precio: 5000 }; // TypeError: se reasigna el nombre
```

Para copiar de verdad hay dos niveles. El **operador de propagación** copia el
primer nivel:

```js
const copia = { ...producto };
```

Pero si el objeto contiene otros objetos, **esos se siguen compartiendo**. Para una
copia completa existe `structuredClone()`.

> **⚠️ OJO ACÁ**
> Esta es la causa número uno de bugs raros en el frontend, y en el TPI te va a
> aparecer sí o sí.
>
> Guardás un producto en un store, lo pasás a una vista, la vista le toca una
> propiedad para mostrarlo distinto... **y acabás de modificar el original.** No
> hubo error, no hubo advertencia. Simplemente el dato quedó cambiado en un lugar
> que ni estabas mirando.
>
> Y después aparece el otro: hacés `{ ...pedido }` creyendo que copiaste, pero
> `pedido.items` es un arreglo, o sea un objeto, o sea **se sigue compartiendo**.
> Modificás un ítem de la copia y modificaste el del original.
>
> Cuando en el Capítulo 8 veas la regla **RN-F03** —que el estado del servidor vive
> sólo en el QueryClient y el del cliente sólo en los stores— acordate de esto. La
> regla existe para que estas modificaciones cruzadas no puedan ocurrir.

### 3.4.3. El envoltorio automático

Los primitivos no tienen propiedades, y sin embargo esto funciona:

```js
"milanesa".toUpperCase();
```

Lo que ocurre es que el lenguaje **envuelve temporalmente** el primitivo en un
objeto, llama al método y descarta el envoltorio. Es transparente y explica por qué
asignarle una propiedad a un primitivo no falla ni tiene efecto: la propiedad se
guarda en un envoltorio que se descarta de inmediato.

---

## 3.5. Coerción

### 3.5.1. Valores falsos

En un contexto que espera un booleano, cualquier valor se convierte. **Exactamente
ocho valores se convierten a `false`**, y todo el resto a `true`:

`false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`.

Conviene memorizar esa lista corta, porque su complemento genera errores concretos:
**`"0"` es verdadero** —es una cadena no vacía—, **`[]` es verdadero** y **`{}` es
verdadero**. Un arreglo vacío en un `if` entra siempre.

> **⚠️ OJO ACÁ**
> Este error lo comete todo el mundo, y en el TPI lo vas a tener servido en bandeja:
>
> ```js
> if (pedido.items) {
>   mostrarCarrito();     // se ejecuta SIEMPRE, aunque no haya ni un item
> }
> ```
>
> Un arreglo vacío **es verdadero**. Siempre. `[]` no está en la lista de los ocho
> valores falsos, y no lo va a estar nunca.
>
> Lo correcto es preguntar por lo que realmente te importa:
>
> ```js
> if (pedido.items.length > 0) { ... }
> ```
>
> Y ojo con la trampa que viene atrás: si `pedido.items` puede ser `undefined`,
> `pedido.items.length` te tira `TypeError`. Ahí usás encadenamiento opcional:
> `if (pedido.items?.length)`. **Preguntá por el estado real, no por la existencia
> del contenedor.**

### 3.5.2. Igualdad

Existen dos operadores de igualdad y la diferencia importa.

**`===` compara sin convertir.** Si los tipos difieren, el resultado es `false` y no
hay más discusión.

**`==` convierte antes de comparar**, siguiendo un algoritmo de la especificación
que casi nadie recuerda entero. Sus resultados son famosos:

```js
"5" == 5           // true
0 == ""            // true
0 == false         // true
null == undefined  // true
null == 0          // false
NaN == NaN         // false
```

La regla práctica es simple: **usar siempre `===`.** La única excepción defendible
es `== null`, que resulta verdadero para `null` y para `undefined` a la vez, y es
una forma compacta de preguntar por ambos.

### 3.5.3. `NaN` y la ausencia de valor

`NaN` significa "no es un número" y es el resultado de una operación aritmética
imposible. Tiene una propiedad que sorprende: **no es igual a sí mismo.** Por eso
para detectarlo se usa `Number.isNaN()` y no una comparación.

Para trabajar con valores posiblemente ausentes, el lenguaje moderno incorporó dos
operadores que conviene distinguir:

```js
const a = producto.descuento ?? 0;    // usa 0 sólo si es null o undefined
const b = producto.descuento || 0;    // usa 0 también si es 0, "" o false
```

El **coalescente nulo** (`??`) sólo actúa ante `null` o `undefined`. El **o lógico**
(`||`) actúa ante cualquier valor falso, y por eso convierte un descuento legítimo
de `0` en... `0`. Inofensivo ahí, no tanto cuando el valor válido es `0` y el
predeterminado es otro.

El **encadenamiento opcional** (`?.`) accede a una propiedad sólo si el objeto
existe, y devuelve `undefined` en lugar de fallar:

```js
const calle = pedido?.direccion?.calle;
```

### 3.5.4. El modelo numérico y el problema del dinero

Acá está el punto más importante del capítulo para el TPI.

Todo número de JavaScript es un punto flotante de doble precisión IEEE 754. Ese
formato representa los números en **base dos**, y hay decimales que en base dos son
periódicos, igual que un tercio es periódico en base diez. `0.1` es uno de ellos.

La consecuencia es esta:

```js
0.1 + 0.2              // 0.30000000000000004
0.1 + 0.2 === 0.3      // false
```

No es un error de JavaScript. **Es el comportamiento de IEEE 754**, y ocurre igual
en Python, en Java y en C. Lo que hace peligroso el caso de JavaScript es que no
ofrece ninguna alternativa: no tiene un tipo decimal exacto como el `Decimal` de
Python o el `BigDecimal` de Java.

Hay además un segundo límite. Los enteros son exactos sólo hasta 2⁵³ − 1, es decir
`9007199254740991`, disponible como `Number.MAX_SAFE_INTEGER`. Más allá, dos
enteros distintos pueden representarse con el mismo valor.

Ahora bien: **el dinero no tolera ninguno de los dos errores.** Un sistema de
pedidos que suma importes con punto flotante acumula diferencias de centavos que
después no cierran contra la facturación.

Por eso el TPI declara la regla **RN-F08**: todo importe recibido llega como cadena
decimal —`"4750.00"`, no `4750`— y se convierte a número en la capa `api/`, nunca en
la vista; ninguna operación aritmética sobre dinero ocurre en el frontend. Del lado
del servidor, la sección 3 del TPI define esos campos con un tipo decimal exacto de
la base de datos, que no tiene este problema.

> **📌 NOTA**
> Este es el momento del capítulo, así que quiero que quede grabado.
>
> Cuando leas en la consigna que el total del pedido viaja como `"4750.00"` entre
> comillas, tu primera reacción va a ser pensar que es una complicación al pedo. Es
> lo que piensa todo el mundo. **Es exactamente al revés.**
>
> Si ese total llegara como número, JavaScript lo convertiría a punto flotante
> apenas lo toque, y cada suma iría acumulando un error invisible. En un pedido no
> se nota. En el cierre de caja del mes, sí.
>
> **La cadena de texto es lo único que garantiza que el número que salió del backend
> sea idéntico al que se muestra en pantalla.** No es una complicación: es la única
> forma correcta de hacerlo con las herramientas que hay.
>
> Y cuando en el Capítulo 6 le pidas a un agente que te tipe la respuesta de la API,
> fijate bien: **te va a poner `total: number` sin dudarlo.** Es lo natural, es lo
> que parece bien, y está mal. Vas a tener que corregirlo vos.

---

## 3.6. Declaraciones, ámbito y clausuras

### 3.6.1. `var`, `let` y `const`

Existen tres formas de declarar una variable, y la primera sólo debería aparecer en
código heredado.

| Palabra | Ámbito | ¿Se puede reasignar? | ¿Se puede redeclarar? |
| --- | --- | --- | --- |
| `var` | **Función** | Sí | Sí |
| `let` | **Bloque** | Sí | No |
| `const` | **Bloque** | No | No |

La diferencia decisiva es el ámbito. `var` ignora los bloques: una variable
declarada dentro de un `if` o un `for` existe en toda la función que la contiene.
`let` y `const` respetan el bloque, que es el comportamiento de casi todos los
lenguajes y lo que cualquiera espera.

`var` sigue existiendo únicamente por la primera decisión de diseño de la sección
3.2. **La práctica actual es usar `const` por defecto y `let` sólo cuando haga falta
reasignar.**

### 3.6.2. Elevación y zona muerta temporal

Las declaraciones se procesan antes de que el código se ejecute. Ese fenómeno se
llama **elevación**, y se comporta distinto según la palabra usada.

Con `var`, la variable existe desde el principio de la función con valor
`undefined`:

```js
console.log(x);   // undefined — existe, sin valor
var x = 5;
```

Con `let` y `const` la variable también existe, pero **acceder a ella antes de su
declaración lanza un error**:

```js
console.log(y);   // ReferenceError
let y = 5;
```

Ese intervalo entre el comienzo del bloque y la declaración se llama **zona muerta
temporal**, y es deliberado: convierte en error visible lo que con `var` era un
`undefined` silencioso. Es uno de los pocos casos donde el lenguaje eligió fallar
ruidosamente, y lo pudo hacer porque `let` era nuevo y no rompía nada.

Las **declaraciones de función** se elevan completas, por lo que pueden invocarse
antes de aparecer en el archivo. Las funciones asignadas a una variable, no: siguen
las reglas de la variable.

> **⚠️ OJO ACÁ**
> El caso donde `var` muerde de verdad es dentro de un bucle, y vale la pena verlo
> porque combina todo lo de esta sección:
>
> ```js
> for (var i = 0; i < 3; i++) {
>   setTimeout(() => console.log(i), 0);
> }
> // imprime: 3, 3, 3
> ```
>
> ¿Por qué tres veces tres? Porque `var i` **es una sola variable** para todo el
> bucle: no hay una por vuelta. Las tres funciones capturaron la misma, y para
> cuando los temporizadores se ejecutan —después, por lo que viste en la sección
> 3.10— el bucle ya terminó y esa variable única vale 3.
>
> Cambiá `var` por `let` y salen `0, 1, 2`. **`let` crea un enlace nuevo en cada
> iteración**, así que cada función captura el suyo.
>
> Ese comportamiento se agregó a propósito, porque el de `var` era una fuente
> inagotable de bugs. No se pudo arreglar `var` —no romper la web—, así que se
> arregló creando algo nuevo al lado. **Es el patrón de todo el lenguaje.**

### 3.6.3. Clausuras

Una **clausura** es una función junto con el entorno léxico donde fue creada. En
términos prácticos: **una función recuerda las variables del lugar donde se
escribió, aunque se ejecute mucho después y en otro contexto.**

```js
function crearContadorDeCarrito() {
  let cantidad = 0;                    // vive en la clausura
  return {
    agregar() { cantidad += 1; return cantidad; },
    total()   { return cantidad; }
  };
}

const carrito = crearContadorDeCarrito();
carrito.agregar();   // 1
carrito.agregar();   // 2
carrito.cantidad;    // undefined — no hay forma de tocarla desde afuera
```

La variable `cantidad` no existe fuera de la función que la creó y sin embargo
sigue viva, porque las dos funciones devueltas la referencian. Eso es una clausura,
y es el mecanismo con el que JavaScript logra estado privado sin necesidad de
clases.

Las clausuras están en todas partes aunque no se las nombre: cada manejador de
evento del Capítulo 4, cada función pasada a un `setTimeout`, cada suscripción a un
store del Capítulo 8 es una clausura.

Y tienen una contracara que el Capítulo 4 va a estudiar en detalle: **mientras una
clausura viva, todo lo que referencia sigue en memoria.** Un manejador de evento que
nadie dio de baja mantiene vivo el elemento del DOM al que estaba asociado. Ese es
exactamente el problema que la regla RN-F01 del TPI obliga a resolver.

---

## 3.7. Funciones y el valor de `this`

### 3.7.1. Tres formas de escribir una función

```js
function calcularTotal(items) { ... }              // declaración: se eleva completa
const calcularTotal = function (items) { ... };    // expresión: sigue a la variable
const calcularTotal = (items) => { ... };          // flecha
```

Las funciones flecha no son solamente una sintaxis más corta. Tienen dos
diferencias de comportamiento: **no tienen `this` propio** y **no tienen el objeto
`arguments`**. La primera es la que importa.

### 3.7.2. `this`

En la mayoría de los lenguajes orientados a objetos, `this` es el objeto al que
pertenece el método, y se sabe leyendo la definición de la clase. **En JavaScript
`this` depende de cómo se llama la función, no de dónde se escribió.**

Las reglas, en orden de prioridad:

| Forma de invocación | Valor de `this` |
| --- | --- |
| `new Constructor()` | El objeto recién creado |
| `fn.call(obj)`, `fn.apply(obj)`, `fn.bind(obj)` | El objeto indicado |
| `obj.metodo()` | `obj` |
| `fn()` | `undefined` en modo estricto |
| Función flecha | El `this` del ámbito donde se **escribió** |

De acá sale el error clásico, y conviene verlo porque en el Capítulo 7 va a
reaparecer con los componentes:

```js
const carrito = {
  items: [],
  agregar(producto) {
    setTimeout(function () {
      this.items.push(producto);   // this es undefined: la función se llamó suelta
    }, 100);
  }
};
```

La función pasada a `setTimeout` no se invoca como método de nadie: se invoca
sola. La solución es una flecha, que no trae `this` propio y por lo tanto usa el
del método que la contiene:

```js
setTimeout(() => { this.items.push(producto); }, 100);
```

> **💡 PARA ENTENDER**
> La regla para no equivocarte con `this` es una sola pregunta, y no es la que
> creés:
>
> **No mires dónde está escrita la función. Mirá cómo la están llamando.**
>
> ¿Hay un punto antes del paréntesis? `carrito.agregar()` → `this` es `carrito`.
> ¿No hay nada a la izquierda? `agregar()` → `this` es `undefined`.
>
> Y por eso las flechas resuelven el problema: **una flecha no tiene `this`
> propio**, así que no importa cómo la llames. Toma el del lugar donde la
> escribiste, que es lo que uno esperaba desde el principio.
>
> Regla de bolsillo: **para callbacks, flecha siempre.** Te ahorra el noventa por
> ciento de estos líos.

---

## 3.8. Objetos, prototipos y clases

Todo objeto tiene un enlace interno a otro objeto, llamado su **prototipo**. Cuando
se accede a una propiedad que el objeto no tiene, el motor la busca en su
prototipo, y si tampoco está, en el prototipo de ese prototipo, hasta llegar a
`null`. Eso es la **cadena de prototipos**.

*(Ver Figura 3.5: la cadena de prototipos.)*

Este mecanismo explica por qué un arreglo tiene `map` sin que nadie se lo haya
puesto: el método vive en `Array.prototype`, y todos los arreglos lo tienen como
prototipo.

Desde 2015 existe la sintaxis `class`, y es importante entender qué es exactamente:

```js
class Producto {
  constructor(nombre, precio) {
    this.nombre = nombre;
    this.precio = precio;
  }
  descripcion() { return `${this.nombre}`; }
}
```

**`class` es azúcar sintáctica sobre prototipos.** No introduce un modelo de objetos
nuevo: el método `descripcion` termina en `Producto.prototype`, exactamente donde
habría quedado escribiéndolo a mano. La sintaxis es más clara y no cambia el modelo
subyacente.

La diferencia con un lenguaje de clases reales se ve en tres comportamientos:

**Los métodos viven en un solo lugar, las propiedades en cada instancia.** Mil
productos comparten una única copia de `descripcion`, pero cada uno tiene su propio
`nombre` y su propio `precio`. Por eso agregar un método a `Producto.prototype`
después de haber creado los objetos **los afecta a todos**, incluso a los ya
existentes. En un lenguaje de clases eso es imposible.

**La forma del objeto no está fija.** Una instancia puede recibir propiedades que la
clase nunca declaró, y perder las que tenía. La clase describe cómo nace el objeto,
no cómo debe seguir siendo.

**La herencia es delegación, no copia.** Cuando una clase extiende a otra, sus
instancias no reciben una copia de los métodos del padre: reciben un enlace. La
búsqueda recorre la cadena en tiempo de ejecución, cada vez.

Desde 2022 existen los **campos privados**, que se declaran con almohadilla y son la
única forma de privacidad real que ofrece el modelo de objetos:

```js
class Carrito {
  #items = [];                      // inaccesible desde afuera, de verdad
  agregar(p) { this.#items.push(p); }
  get total() { return this.#items.length; }
}
```

A diferencia de la convención de anteponer un guion bajo —que es sólo un pedido de
buena voluntad—, acceder a `carrito.#items` desde afuera **es un error de sintaxis**.
Es el equivalente moderno de la privacidad que la sección 3.6.3 lograba con
clausuras.

Todo esto tiene una consecuencia concreta para el Capítulo 7: los componentes web
**se declaran obligatoriamente con `class`** porque el navegador lo exige, pero el
objeto resultante sigue siendo dinámico, con todo lo que eso implica.

> **💡 PARA ENTENDER**
> Si venís de un lenguaje con clases de verdad, este es el punto donde tenés que
> cambiar el chip, y conviene hacerlo ahora y no en el Capítulo 7.
>
> **En Java o C#, una clase es un molde.** Definís la forma, se fabrican objetos con
> esa forma, y la forma no cambia.
>
> **En JavaScript, un objeto delega en otro objeto.** No hay molde. Hay una cadena
> de objetos, y cuando pedís una propiedad que no está, el motor sube por la cadena
> hasta encontrarla o llegar a `null`.
>
> Por eso podés agregarle un método a `Producto.prototype` a las tres de la tarde y
> **los mil productos que creaste a la mañana lo tienen**. No es un truco sucio: es
> literalmente cómo funciona el modelo.
>
> `class` te da una sintaxis prolija encima de eso. Te ahorra escribir el
> andamiaje, no te cambia el modelo.

---

## 3.9. Módulos

Antes de 2015 el lenguaje no tenía módulos. Todo script compartía el mismo ámbito
global, y evitar colisiones de nombres dependía de convenciones y de patrones
elaborados. Los módulos ES resolvieron eso en el propio lenguaje:

```js
// api/productos.ts
export async function listarProductos(pagina) { ... }
export const PAGINA_POR_DEFECTO = 1;

// vistas/catalogo.ts
import { listarProductos, PAGINA_POR_DEFECTO } from "../api/productos";
```

Cuatro propiedades relevantes:

- **Cada módulo tiene su propio ámbito.** Nada se comparte salvo lo exportado.
- **Los `import` son estáticos**: se declaran arriba y no pueden depender de una
  condición. Esa restricción es lo que permite a las herramientas del Capítulo 7
  analizar el grafo de dependencias sin ejecutar el código, y con eso eliminar lo
  que no se usa.
- **Los módulos se ejecutan una sola vez**, por más veces que se importen.
- **Siempre están en modo estricto.**

Existe también la importación dinámica, `import()`, que devuelve una promesa y
permite cargar un módulo bajo demanda. Es la base de la división del paquete que el
Capítulo 7 estudia.

Hay dos formas de exportar, y la elección no es indistinta:

```js
export function listarProductos() { ... }     // nombrada
export default function listarProductos() { } // por defecto
```

La **exportación nombrada** obliga a quien importa a usar el mismo nombre, lo que
permite que las herramientas detecten un nombre mal escrito y que el editor
autocomplete. La **exportación por defecto** deja que cada archivo la importe con el
nombre que quiera, y esa libertad es justamente el problema: el mismo módulo puede
aparecer con tres nombres distintos en tres archivos, y buscar sus usos se vuelve
imposible. La arquitectura del TPI, que el Capítulo 8 estudia, se apoya en poder
rastrear qué usa qué: **las exportaciones nombradas son la elección coherente con
eso.**

Un problema que conviene conocer de antemano son las **importaciones circulares**:
el módulo A importa del B y el B importa del A. No producen un error inmediato —el
sistema de módulos las tolera—, pero uno de los dos va a ver al otro a medio
inicializar, y el síntoma es un valor `undefined` en un lugar donde debería haber
una función. El diagnóstico es difícil porque el error aparece lejos de la causa. La
solución casi siempre es extraer lo compartido a un tercer módulo del que dependan
los dos.

> **📌 NOTA**
> Fijate en una propiedad de los módulos que parece un detalle y es la base de todo
> el Capítulo 7: **los `import` son estáticos.**
>
> No podés hacer `import` adentro de un `if`. Tiene que estar arriba y tiene que ser
> una ruta literal. Al principio parece una limitación molesta.
>
> Pero eso es exactamente lo que le permite a una herramienta **leer tu código sin
> ejecutarlo** y armar el grafo completo de dependencias. Y con ese grafo puede saber
> qué funciones no usa nadie y borrarlas del paquete final.
>
> Esa es la diferencia entre bajar 400 kilobytes de biblioteca o los 12 que
> realmente usás. **La restricción es la que habilita la optimización** — y es el
> mismo tipo de intercambio que venimos viendo desde el Capítulo 1.

---

## 3.10. El bucle de eventos

### 3.10.1. Un solo hilo

**JavaScript en el navegador tiene un único hilo de ejecución**, y ese hilo es el
mismo que calcula la disposición y pinta la pantalla. No pueden ocurrir dos cosas a
la vez: mientras se ejecuta código, no se dibuja; mientras se dibuja, no se ejecuta
código.

La consecuencia es directa y severa. Una función que tarda dos segundos no produce
una interfaz lenta: produce una interfaz **muerta** durante dos segundos. Los clics
no responden, las animaciones se detienen, el texto no se puede seleccionar. El
navegador incluso puede ofrecer cerrar la pestaña.

### 3.10.2. Pila, tareas y microtareas

El modelo tiene cuatro piezas:

| Pieza | Qué contiene |
| --- | --- |
| **Pila de llamadas** | Las funciones que se están ejecutando ahora |
| **Cola de tareas** | Trabajo pendiente: temporizadores, eventos, respuestas de red |
| **Cola de microtareas** | Continuaciones de promesas y `queueMicrotask` |
| **Bucle de eventos** | El coordinador que decide qué entra a la pila |

El algoritmo del bucle es breve y hay que saberlo de memoria:

1. Ejecutar todo lo que haya en la pila hasta vaciarla.
2. **Vaciar por completo la cola de microtareas.** Si una microtarea encola otra,
   también se ejecuta ahora.
3. Renderizar, si corresponde.
4. Tomar **una sola** tarea de la cola de tareas y volver al paso 1.

Las dos asimetrías del paso 2 son lo importante: las microtareas se vacían
**enteras**, mientras que de las tareas se toma **una por vuelta**. Por eso las
promesas siempre se resuelven antes que un `setTimeout`, incluso uno de cero
milisegundos.

*(Ver Figura 3.3: pila, colas y bucle de eventos.)*
*(Ver Figura 3.4: el orden de vaciado y el momento del renderizado.)*

```js
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
console.log("4");

// Imprime: 1, 4, 3, 2
```

`1` y `4` son código síncrono y salen primero. `3` es una microtarea y se ejecuta al
vaciarse la pila. `2` es una tarea y espera a la vuelta siguiente del bucle.

> **🧪 EXPERIMENTO**
> Poné esto en la consola del navegador, con la página a la vista:
>
> ```js
> const fin = Date.now() + 5000;
> while (Date.now() < fin) { /* no hace nada, pero ocupa el hilo */ }
> ```
>
> Durante cinco segundos, probá:
>
> 1. Hacer clic en cualquier botón de la página.
> 2. Seleccionar texto con el mouse.
> 3. Mirar si alguna animación sigue corriendo.
>
> **Nada responde.** No está lento: está muerto. Y ojo con este detalle, que es el
> que más impresiona: **los clics que hiciste no se perdieron.** Se encolaron. Cuando
> el bucle se libera, se ejecutan todos juntos de golpe.
>
> Eso es exactamente lo que te va a pasar en el TPI si procesás una lista grande de
> pedidos sin cortar el trabajo. El usuario va a clickear tres veces creyendo que no
> anduvo, y después se van a disparar las tres.

### 3.10.3. El mismo problema del otro lado del cable

La sección 1.4 del TPI describe el modelo de ejecución asincrónico del backend, y
la 5.5 exige que el cálculo del hash de contraseña con bcrypt salga del bucle de
eventos mediante un hilo aparte. **Es el mismo problema de esta sección.**

El servidor asincrónico también atiende sobre un bucle de eventos. Una operación
que consume procesador sin ceder el control —y bcrypt está diseñado para consumir
procesador— bloquea ese bucle, y mientras tanto **ninguna otra petición se
atiende**. No sólo se demora quien está iniciando sesión: se demoran todos.

Quien entendió esta sección puede leer la 1.4 y la 5.5 del TPI sin ninguna
explicación adicional. Cambia el lenguaje y cambia el lado del cable; el modelo es
idéntico.

---

## 3.11. Herramientas de diagnóstico

A diferencia de CSS, **JavaScript sí falla ruidosamente**, y la consola es el primer
lugar donde mirar. Un mensaje de error incluye el tipo, la descripción y la traza de
llamadas que llevó hasta ahí; esa traza se lee de arriba hacia abajo, donde lo de
arriba es lo último que se ejecutó.

Más allá de `console.log`, tres métodos rinden mucho y se usan poco:
`console.table()` presenta un arreglo de objetos como tabla legible; `console.dir()`
muestra un elemento del DOM como objeto en lugar de como marcado; y `console.time()`
con `console.timeEnd()` mide cuánto tarda un fragmento.

El **depurador** es la herramienta que separa a quien diagnostica de quien adivina.
Un punto de interrupción detiene la ejecución y permite inspeccionar el estado real:
el valor de cada variable, la cadena de ámbitos —donde se ven las clausuras de la
sección 3.6.3 con su contenido— y la pila de llamadas completa. Los puntos de
interrupción **condicionales**, que sólo detienen cuando se cumple una expresión,
son especialmente útiles dentro de un bucle largo.

*(Ver Figura 3.6: el depurador detenido, con el panel de ámbitos y la pila.)*

El panel de **rendimiento** graba la actividad del hilo principal y marca las
**tareas largas**, que son las que superan los 50 milisegundos y producen el efecto
de la sección 3.10.2. Es la forma de encontrar qué función concreta está congelando
la interfaz.

*(Ver Figura 3.7: una tarea larga bloqueando el hilo principal.)*

> **⚠️ OJO ACÁ**
> Si estás depurando a fuerza de `console.log`, estás perdiendo tiempo.
>
> Un `log` te muestra un valor en un momento. **Un punto de interrupción te muestra
> todo el estado en ese momento**: todas las variables, toda la cadena de ámbitos,
> toda la pila de llamadas. Y podés avanzar paso a paso viendo cómo cambia.
>
> Hay un detalle que casi nadie usa y que vale oro: cuando el depurador está
> detenido, **la consola ejecuta en ese contexto**. Podés escribir el nombre de una
> variable local y ver su valor. Podés probar una expresión antes de escribirla en
> el código.
>
> Dedicale veinte minutos a aprender el depurador. Es la mejor inversión de tiempo
> de todo el módulo, y te va a servir en cualquier lenguaje.

---

## 3.12. Seguridad y evolución

El **modo estricto**, incorporado en ES5, desactiva comportamientos heredados
peligrosos: convierte en error asignar a una variable no declarada, prohíbe
duplicar parámetros y hace que `this` sea `undefined` en una función suelta en vez
de apuntar al objeto global. **Los módulos son estrictos siempre**, sin necesidad de
declararlo, así que todo el código del TPI lo es.

Tres riesgos concretos merecen mención.

**Ejecución de texto como código.** `eval()` y el constructor `Function` ejecutan
una cadena como código. Si esa cadena incluye algo que vino del usuario, el usuario
está ejecutando código en la página. No hay uso legítimo en una aplicación de este
tipo, y el encabezado `Content-Security-Policy` de la sección 16.5 del TPI puede
bloquearlos.

**Contaminación de prototipos.** Como todo objeto hereda de `Object.prototype`,
modificar ese objeto afecta a **todos** los objetos del programa. Un ataque conocido
consiste en enviar un JSON con una clave `__proto__` a una función que fusiona
objetos de forma recursiva sin filtrar. La defensa es no fusionar datos externos sin
validarlos, que es lo que hacen los esquemas de la sección 7 del TPI.

**Datos sensibles en el cliente.** Todo lo que llega al navegador es visible y
modificable por quien lo recibe. Es la base de la regla RN-F04 del TPI —las guardas
de ruta son usabilidad, no seguridad— y el Capítulo 5 vuelve sobre esto al tratar el
almacenamiento del token.

Sobre la evolución del lenguaje, la conclusión de esta sección se conecta con el
Capítulo 6. Todo lo que este capítulo describió —la coerción, el `this` variable,
los objetos sin forma fija, los errores que no aparecen hasta ejecutar— es
manejable en un archivo de doscientas líneas. **A escala de un sistema como el TPI
deja de serlo**, y no por falta de disciplina: simplemente nadie recuerda qué forma
tiene cada objeto que circula por el programa.

De ahí sale TypeScript, y por eso este módulo lo estudia después y no antes: **para
entender qué problema resuelve hay que haber tenido el problema.**

---

## 3.13. Verificación

1. Predecir el orden de salida de un fragmento que combine código síncrono,
   `setTimeout` y promesas, y **verificarlo en la consola**.
2. Explicar por qué modificar una propiedad de un objeto declarado con `const` es
   válido y reasignarlo no lo es.
3. Copiar un objeto anidado con el operador de propagación, modificar el nivel
   interno de la copia y **verificar que el original cambió**.
4. Escribir una función que devuelva un contador con estado privado mediante una
   clausura, y comprobar en el depurador que la variable no es accesible desde
   afuera.
5. Provocar deliberadamente un error de `this` con una función común dentro de un
   método, y corregirlo con una flecha.
6. Enumerar los ocho valores falsos y verificar cada uno en la consola.
7. Evaluar `0.1 + 0.2` y explicar **por qué** el resultado no es `0.3`, y qué
   estrategia adopta el TPI ante ese límite.
8. Detener la ejecución en un punto de interrupción dentro de una clausura y ubicar
   la variable capturada en el panel de ámbitos.
9. Bloquear el hilo principal con un bucle y **documentar qué deja de funcionar** en
   la página durante ese lapso.

---

## 3.14. Errores frecuentes

**Comparar con `==` en lugar de `===`.** Produce igualdades que nadie esperaba, como
`0 == ""`. La regla es usar siempre `===`, con la única excepción de `== null`
(sección 3.5.2).

**Creer que `const` congela un objeto.** Impide reasignar el nombre, no modificar el
contenido. Para inmutabilidad real hace falta copiar (sección 3.4.2).

**Copiar en superficie creyendo que se copió todo.** El operador de propagación
copia un nivel; los objetos anidados se siguen compartiendo (sección 3.4.2).

**Usar `||` para valores por defecto.** Actúa ante cualquier valor falso, así que
descarta un `0` o una cadena vacía legítimos. Para eso está `??` (sección 3.5.3).

**Comparar contra `NaN` con `===`.** `NaN` no es igual a sí mismo. Se detecta con
`Number.isNaN()` (sección 3.5.3).

**Operar con dinero en punto flotante.** Acumula errores de centavos que después no
cierran. Es lo que la regla RN-F08 del TPI previene (sección 3.5.4).

**Perder `this` en un callback.** Una función común pasada a un temporizador o a un
manejador de evento no conserva el `this` del método. Se resuelve con flecha
(sección 3.7.2).

**Suponer que `setTimeout(fn, 0)` ejecuta de inmediato.** Encola una tarea, y todas
las microtareas pendientes se ejecutan antes (sección 3.10.2).

**Bloquear el hilo con un cálculo largo.** La interfaz no se pone lenta: deja de
responder por completo (sección 3.10.1).

**Depurar sólo con `console.log`.** Muestra un valor en un momento; el depurador
muestra todo el estado y permite avanzar paso a paso (sección 3.11).

---

## 3.15. Actividades

1. **Predicción del bucle de eventos.** Dado un fragmento con cinco operaciones que
   combinan código síncrono, dos `setTimeout` y dos promesas encadenadas, escribir el
   orden de salida **antes** de ejecutarlo, ejecutarlo y explicar cada diferencia.

2. **Referencias en el dominio del TPI.** Escribir una función que reciba un pedido
   con sus ítems y devuelva una versión con un descuento aplicado, sin modificar el
   original. Verificar con el depurador que el pedido de entrada quedó intacto, y
   documentar qué falló en el primer intento.

3. **Auditoría de coerción.** Para una lista dada de quince comparaciones con `==`,
   predecir el resultado de cada una, verificarlo y explicar la conversión que aplicó
   el motor en los casos donde la predicción falló.

4. **El problema del dinero.** Sumar cien veces `0.1` en un bucle y comparar el
   resultado con `10`. Calcular la diferencia acumulada. Escribir después la misma
   suma trabajando en centavos con enteros y comparar. Relacionar con RN-F08.

5. **Estado privado con clausuras.** Implementar un carrito de compras con
   `agregar`, `quitar` y `total`, cuyo estado interno **no sea accesible desde
   afuera**. Demostrar en la consola que no hay forma de modificarlo directamente.

6. **Exploración: el costo de bloquear.** Escribir una función que procese un arreglo
   de cincuenta mil elementos de forma síncrona y medir con el panel de rendimiento
   cuánto bloquea el hilo. Reescribirla partiendo el trabajo en fragmentos que cedan
   el control. Comparar ambas grabaciones y relacionar lo observado con la sección
   3.10.1. *(Requiere el panel de rendimiento del navegador.)*

7. **Exploración: la compatibilidad hacia atrás.** Buscar en la especificación de
   ECMAScript tres comportamientos documentados como heredados o desaconsejados que
   no se pueden eliminar. Para cada uno, explicar qué rompería su eliminación y
   relacionarlo con la primera decisión de diseño de la sección 3.2.
   *(Requiere consultar `tc39.es/ecma262`.)*

---

## 3.16. Síntesis

1. JavaScript se diseñó en diez días como **lenguaje de pegamento para no
   programadores**, con la restricción de marketing de parecerse a Java. Parece Java
   y funciona como Scheme, y esa distancia explica la mayoría de las confusiones.

2. La decisión de diseño rectora es **no romper la web**. Ningún error del diseño
   original se corrigió jamás; todo se agregó al lado. `typeof null === "object"` es
   un bug de 1995 que sigue vigente porque arreglarlo rompería páginas existentes.

3. El lenguaje **prefiere producir un resultado antes que detenerse**. Convierte
   tipos, entrega `undefined`, ignora argumentos de más. Es tolerancia deliberada, la
   misma decisión que el HTML y el CSS toman en sus propios terrenos.

4. Los primitivos se copian **por valor** y los objetos **por referencia**. `const`
   impide reasignar el nombre, no modificar el contenido, y el operador de
   propagación copia **un solo nivel**.

5. **`0.1 + 0.2` no es `0.3`**, y no es culpa de JavaScript sino de IEEE 754. Pero a
   diferencia de otros lenguajes, JavaScript no ofrece un tipo decimal exacto. De ese
   límite sale la regla RN-F08 del TPI: el dinero viaja como cadena y no se opera en
   el frontend.

6. `this` **depende de cómo se invoca la función, no de dónde se escribió**. Las
   funciones flecha no tienen `this` propio y por eso son la elección correcta para
   callbacks.

7. Una **clausura** es una función más el entorno donde nació. Da estado privado sin
   clases, y tiene como contracara que **mantiene vivo en memoria todo lo que
   referencia**: el origen del problema que RN-F01 obliga a resolver.

8. `class` es **azúcar sintáctica sobre prototipos**. No introduce un modelo de
   objetos nuevo.

9. El **bucle de eventos** vacía las microtareas **por completo** y toma las tareas
   **de a una**. Por eso una promesa siempre se resuelve antes que un `setTimeout(0)`.

10. **Un solo hilo ejecuta y dibuja.** Bloquearlo no produce una interfaz lenta sino
    una interfaz muerta. Es el mismo problema que el TPI enfrenta del lado del
    servidor en sus secciones 1.4 y 5.5.

11. Todo lo anterior es manejable en doscientas líneas y **deja de serlo a escala de
    sistema**. Ese es el problema que TypeScript resuelve, y por eso se estudia
    después: para entender la solución hay que haber tenido el problema.

---

## 3.17. Referencias y lecturas complementarias

La fuente normativa del lenguaje es la especificación **ECMA-262**, mantenida por el
comité TC39 y publicada como estándar viviente en `tc39.es/ecma262`. Sus secciones
pertinentes a este capítulo son las de tipos y valores, que definen los siete
primitivos de la sección 3.4; las de operaciones abstractas de conversión, que
documentan el algoritmo de coerción de la sección 3.5; y las de tareas y trabajos,
que formalizan la cola de microtareas de la sección 3.10. El comportamiento del
bucle de eventos propiamente dicho **no está en ECMA-262 sino en el estándar HTML
del WHATWG**, en su sección sobre el modelo de procesamiento de eventos: la
distinción importa, porque el bucle es una característica del entorno de ejecución y
no del lenguaje. El proceso de propuestas en cuatro etapas del comité está
documentado en `tc39.es/process-document`, y su repositorio público permite ver el
estado de cada propuesta en curso. El formato numérico de la sección 3.5.4
corresponde a la norma **IEEE 754-2019**, cuya lectura no es necesaria pero sí
saber que existe y que el problema no es propio de JavaScript.

Como bibliografía de estudio, la serie de Simpson, *You Don't Know JS Yet* (2.ª
edición, de lectura libre en su repositorio público) es la que trata con mayor
profundidad los tres temas difíciles de este capítulo —tipos y coerción, ámbito y
clausuras, y `this` con prototipos—, dedicándole un volumen a cada uno. Para una
referencia de consulta cotidiana, la documentación de MDN en
`developer.mozilla.org` es la más confiable y la que conviene adoptar como fuente
por defecto, por encima de resultados de buscador. Sobre el bucle de eventos, la
charla de Philip Roberts *What the heck is the event loop anyway?* (JSConf EU, 2014)
sigue siendo la explicación visual más clara del modelo de la sección 3.10, y
Archibald, *In the Loop* (JSConf Asia, 2018) profundiza en la diferencia entre
tareas y microtareas con el detalle que esa distinción requiere. Para el contexto
histórico de la sección 3.2, el artículo de Wirfs-Brock y Eich *JavaScript: The
First 20 Years* (ACM HOPL IV, 2020) es el relato más completo y está escrito por
quienes participaron del proceso.

---

**Continúa en:** Capítulo 4 — El DOM: programar la página sin framework, donde el
lenguaje de este capítulo se aplica sobre el árbol de nodos del Capítulo 1, y donde
las clausuras de la sección 3.6.3 revelan su costo en memoria.
