# Capítulo 7 — Herramientas y componentes: Vite, Web Components y Chart.js

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 7.1. Alcance de la clase

Los seis capítulos anteriores enseñaron a escribir código. Este enseña a
**convertirlo en algo que un navegador pueda ejecutar** y a **empaquetarlo en piezas
reutilizables con un ciclo de vida propio**. Son los dos problemas que aparecen
cuando un proyecto deja de ser un archivo y pasa a ser un sistema.

Conviene empezar deshaciendo un malentendido sobre el enunciado. El TPI dice **sin
framework de interfaz**, y eso suele leerse como "sin dependencias". Es falso: la
sección 1.3 declara **doce tecnologías** para el frontend, varias de ellas
bibliotecas de peso.

| Tecnología | Versión | Rol |
| --- | --- | --- |
| TypeScript | 5.x | Lenguaje único del cliente, tipado estricto |
| Vite | 5.x | Construcción y servidor de desarrollo, plantilla `vanilla-ts` |
| DOM API + Web Components | nativo | Interfaz, componentes y ciclo de vida |
| History API | nativo | Enrutamiento del lado del cliente |
| EventSource | nativo | Consumo de los eventos de la sección 11 |
| Tailwind CSS | 3.x | Estilos *utility-first* |
| `@tanstack/query-core` | 5.x | Estado del servidor: consulta, caché e invalidación |
| `@tanstack/form-core` | 0.x | Estado y validación de formularios |
| `zustand/vanilla` | 4.x | Estado del cliente: carrito, sesión e interfaz |
| Axios | 1.x | Cliente HTTP con interceptores |
| Chart.js | 4.x | Gráficos del panel de administración |
| DOMPurify | 3.x | Sanitizador, único mecanismo admitido por RN-F02 |

La distinción que hace el TPI es precisa y vale la pena entenderla: **lo prohibido
no son las bibliotecas, es el framework de interfaz.** React o Vue se hacen cargo del
ciclo de vida —cuándo se monta un componente, cuándo se desmonta, cuándo se
actualiza— y lo ocultan detrás de su propia maquinaria. Todo lo demás de esa lista
resuelve problemas puntuales sin tocar ese ciclo.

**El ciclo de vida es exactamente lo que el alumno no puede delegar**, porque es
donde viven las once reglas. Y este capítulo es donde ese ciclo aparece por primera
vez de forma explícita: `connectedCallback` y `disconnectedCallback` son los métodos
que RN-F01 nombra por su nombre.

Dos reglas se fundan acá, y las dos tienen el mismo garante declarado, que es un
caso de prueba concreto: **TST-45, que monta y desmonta una vista tres veces y
verifica que el store quede con cero suscriptores.**

Al finalizar la clase, el alumno debe poder crear un proyecto con la plantilla que
el TPI declara, escribir un componente que se monte y **se desmonte sin dejar nada
atrás**, y explicar por qué su aplicación puede arrancar perfectamente con errores
de tipo adentro.

**Contenidos**

1. Origen y objetivos de diseño del empaquetado.
2. Vite: desarrollo y producción como problemas distintos.
3. Verificación de tipos y variables de entorno.
4. Origen de los componentes web.
5. Elementos personalizados y su ciclo de vida.
6. La regla RN-F01 en su lugar definitivo.
7. El DOM en la sombra: qué aísla y qué complica.
8. Plantillas.
9. Chart.js y la regla RN-F05.
10. Herramientas de diagnóstico.
11. Seguridad y evolución.

---

## 7.2. Por qué hizo falta empaquetar

En 2005, incluir código en una página consistía en escribir etiquetas de script en
el orden correcto. Ese "en el orden correcto" era el problema entero: **no había
módulos en el lenguaje**, todo compartía el ámbito global, y el orden de las
etiquetas era la única forma de expresar una dependencia. Agregar una biblioteca en
el lugar equivocado rompía el sitio, sin ningún error que dijera por qué.

Las estrategias de la época fueron dos, y ninguna resolvió el fondo. Envolver cada
archivo en una función que se invoca a sí misma daba un ámbito privado, pero las
dependencias seguían siendo variables globales. Y agrupar todo bajo un objeto —una
sola variable global con todo adentro— sólo movía el problema.

El primer sistema de módulos real llegó de fuera del navegador. **CommonJS**,
adoptado por Node.js en 2009, definió `require` y `module.exports`. Funcionaba
perfecto en un servidor y **no servía en el navegador**, porque `require` es
síncrono: leer un archivo del disco es inmediato, pedirlo por red no.

La respuesta fue partir la comunidad en dos. **AMD** propuso una sintaxis asincrónica
pensada para el navegador; CommonJS siguió en el servidor. Durante años, una
biblioteca tenía que publicarse en los dos formatos.

**Browserify**, en 2011, planteó la salida: si el problema es que `require` es
síncrono, **resolvamos las dependencias antes de que el código llegue al
navegador**. Analizar el grafo, juntar todo en un archivo, y que el navegador reciba
algo que ya no necesita pedir nada.

**Webpack**, desde 2012, llevó esa idea al extremo: no sólo JavaScript, sino
cualquier cosa —estilos, imágenes, tipografías— como nodo del mismo grafo de
dependencias. Y **Rollup**, en 2015, introdujo la eliminación de código muerto sobre
módulos ES, aprovechando exactamente la propiedad que el Capítulo 3 señaló: **los
`import` son estáticos y por lo tanto analizables sin ejecutar el código.**

El costo apareció con el tamaño. Empaquetar un proyecto grande en cada cambio
tardaba, y a mediados de la década era normal esperar **decenas de segundos** para
ver un cambio de una línea. Se había resuelto el problema de las dependencias y
creado uno de espera.

Dos cosas cambiaron eso, ambas en 2020. **esbuild**, escrito en Go por Evan Wallace,
demostró que las herramientas eran lentas en parte porque estaban escritas en
JavaScript: hacía lo mismo entre diez y cien veces más rápido. Y **Vite**, de Evan
You, hizo una observación más profunda:

> **Los navegadores ya entienden `import`.** ¿Por qué empaquetar en desarrollo?

De ahí salen las cuatro decisiones de diseño de la herramienta que el TPI declara.

**Primera: desarrollo y producción son problemas distintos, y se resuelven
distinto.** En desarrollo importa la velocidad de recarga; en producción, el tamaño
y la cantidad de peticiones. Usar la misma estrategia para ambos es lo que hacían
las herramientas anteriores.

**Segunda: en desarrollo no se empaqueta.** Los archivos se sirven como módulos ES
nativos y el navegador pide lo que necesita, cuando lo necesita.

**Tercera: las dependencias sí se pre-empaquetan, una sola vez.** Una biblioteca
puede tener cientos de módulos internos, y servirlos sin empaquetar produciría
cientos de peticiones. Se convierten a un archivo con esbuild al arrancar y se
cachean.

**Cuarta: en producción sí se empaqueta**, con Rollup, porque servir módulos nativos
sin agrupar produce una cascada de peticiones encadenadas que en una conexión real
es mucho peor que un archivo grande.

*(Ver Figura 7.1: del script suelto al empaquetado.)*

> **💡 PARA ENTENDER**
> Fijate en el patrón, porque es el mismo del Capítulo 4 con jQuery y va a volver a
> pasarte en tu carrera:
>
> **Empaquetar en desarrollo era una solución a un problema que dejó de existir.**
>
> Cuando Browserify apareció, el navegador no entendía módulos: había que
> empaquetar sí o sí. Cuando los módulos ES llegaron a todos los navegadores, esa
> necesidad se evaporó — **pero las herramientas siguieron empaquetando durante
> años**, porque nadie se detuvo a preguntarse por qué lo hacían.
>
> Vite no inventó una técnica nueva ni un algoritmo más rápido. **Se preguntó por qué
> se estaba haciendo algo, y la respuesta ya no era válida.**
>
> Esa pregunta —*¿qué problema resuelve esto, y sigue existiendo?*— es la más
> rentable de toda la carrera. Y es exactamente la que un agente de IA **no** se
> hace: te va a proponer lo que era correcto en la mayor cantidad de ejemplos que
> vio, que suele ser lo que era correcto hace tres años.

---

## 7.3. Vite

### 7.3.1. En desarrollo

Al arrancar, el servidor de desarrollo hace dos cosas y ninguna es empaquetar el
código propio:

1. **Pre-empaqueta las dependencias** con esbuild y las guarda en caché.
2. **Sirve el código propio como módulos ES**, transformando cada archivo bajo
   demanda cuando el navegador lo pide.

El navegador recibe el documento, encuentra el módulo de entrada, y a partir de ahí
**pide por sí solo cada `import` que va encontrando**. El servidor transforma
únicamente lo que se pidió: quita los tipos de TypeScript, resuelve rutas, aplica lo
que haga falta, y responde.

> **🧪 EXPERIMENTO**
> Esto se entiende mucho mejor viéndolo que leyéndolo, y son dos minutos.
>
> 1. Arrancá el proyecto en desarrollo y abrí el panel de red.
> 2. Recargá con el panel abierto y **contá las peticiones**.
>
> Vas a ver decenas, quizá cientos: **una por cada archivo `.ts` de tu proyecto**, más
> las dependencias pre-procesadas. Si venís de otras herramientas, eso parece un
> desastre de rendimiento.
>
> 3. Hacé clic en una de esas peticiones y mirá la respuesta.
>
> Es tu archivo, con los tipos ya quitados, servido tal cual. **El servidor lo
> transformó recién cuando el navegador lo pidió.**
>
> 4. Ahora construí para producción, serví el resultado y contá otra vez.
>
> Un puñado de archivos. La misma aplicación.
>
> Esa diferencia **es** la primera decisión de diseño de la sección 7.2. Y las decenas
> de peticiones de desarrollo no son un problema: contra `localhost` cuestan casi
> nada, y a cambio el arranque no depende de cuán grande sea tu proyecto.

La consecuencia es que el tiempo de arranque **no depende del tamaño del proyecto**,
porque no hay ningún trabajo proporcional al total. Y cuando un archivo cambia, la
herramienta reemplaza **ese módulo** en la página sin recargar, preservando el estado
—el carrito lleno, el formulario a medio escribir— en lugar de perderlo.

*(Ver Figura 7.2: desarrollo frente a producción.)*
*(Ver Figura 7.5: módulos ES nativos en el panel de red.)*

### 7.3.2. En producción

La construcción de producción sí empaqueta, con Rollup, y hace tres cosas más:

- **Elimina lo que no se usa**, gracias a que los `import` son estáticos.
- **Divide el resultado** en fragmentos, de modo que cada `import()` dinámico del
  Capítulo 3 se convierte en un archivo aparte que se descarga sólo si hace falta.
- **Agrega una huella al nombre** de cada archivo. Cuando el contenido cambia, cambia
  el nombre, lo que permite cachear agresivamente sin riesgo de servir una versión
  vieja.

Ese resultado es lo que el TPI declara que sirve el proceso estático de su sección
16.

### 7.3.3. Vite no verifica los tipos

Este punto ya se anunció en el Capítulo 6 y acá se vuelve operativo, porque es
fuente de confusión permanente:

> **La herramienta de construcción no verifica los tipos. Los borra.**

Lo hace a propósito: esbuild quita las anotaciones sin analizarlas, y esa es una de
las razones por las que es tan rápido. Verificar exige construir el grafo de tipos
completo, que es un trabajo del todo distinto.

La consecuencia práctica sorprende a todo el mundo la primera vez: **el proyecto
arranca perfecto y funciona, con errores de tipo adentro.** El editor los subraya, y
la aplicación anda igual.

Por eso la verificación es un paso aparte, que hay que ejecutar explícitamente y
—esto es lo importante— **incluir en el paso de construcción**, para que un error de
tipo impida publicar. Un proyecto donde la verificación es opcional termina teniendo
errores de tipo permanentes que nadie mira.

### 7.3.4. Variables de entorno

La configuración que cambia entre desarrollo y producción —la dirección de la API,
por ejemplo— se declara en archivos de entorno y se lee mediante `import.meta.env`.

Hay una regla que **no es una convención sino un control de seguridad**: sólo las
variables cuyo nombre empieza con un prefijo declarado se incorporan al código del
cliente. Las demás quedan fuera.

La razón es directa: **todo lo que llega al cliente es público.** Una variable
expuesta al frontend queda escrita literalmente en el archivo que se descarga, y
cualquiera puede leerla abriendo el código fuente. El prefijo obliga a **declarar
explícitamente** que algo puede ser público, en lugar de que se filtre por descuido.

> **⚠️ OJO ACÁ**
> Esto es de las cosas que más caro salen y más fácil pasan, así que grabátelo:
>
> **Todo lo que exponés al frontend es público. Todo. Sin excepción.**
>
> No es que "sea difícil de encontrar" o que "esté ofuscado". Está **escrito en texto
> plano** dentro de un archivo que cualquiera se baja. Se busca con Ctrl+F.
>
> Entonces: una URL de API va bien ahí. Una clave pública de un servicio de mapas,
> también. **Una contraseña de base de datos, una clave secreta de un servicio de
> pagos o el secreto con el que se firman los tokens, jamás.**
>
> Esto pasa todo el tiempo, y casi siempre de la misma forma: alguien copia una
> variable del `.env` del backend al del frontend "para probar", y queda. Después ese
> repositorio se hace público —como el del TPI trozado, por ejemplo— y la clave está
> ahí para siempre en el historial de git.
>
> Si alguna vez te pasa: **no alcanza con borrarla. Hay que rotarla.** El commit
> viejo sigue existiendo.

---

## 7.4. Tailwind en el proyecto

El Capítulo 2 explicó qué problema resuelve el enfoque *utility-first* y cómo
funciona el escaneo. Acá se agrega lo operativo: la herramienta se integra al
proceso de construcción, y su configuración declara **qué archivos escanear**.

Ese detalle tiene una consecuencia que conviene anticipar, porque produce un error
difícil de diagnosticar: si un archivo con clases de Tailwind **no está en la lista
de rutas escaneadas**, sus clases no se generan. El componente se ve sin estilo, sin
ningún error, y el estilo "no funciona" por una razón que no está en el estilo.

Combinado con el escaneo textual de la sección 2.11.2 —las clases construidas por
concatenación no se encuentran—, esas son las dos causas del noventa por ciento de
los casos de "Tailwind no me aplica la clase".

---

## 7.5. Por qué existen los componentes

El Capítulo 4 dejó una carencia planteada sin nombrarla: **el DOM no tiene forma de
empaquetar estructura, estilo y comportamiento en una unidad reutilizable.** Un
"componente" era, en la práctica, una convención: un fragmento de marcado, unas
reglas de CSS con un prefijo para no colisionar, y una función que registraba
manejadores.

Esa convención fallaba en tres puntos concretos, y de los tres salen las tres
tecnologías de esta sección:

- **Los estilos escapaban.** Una regla escrita para un componente afectaba a
  cualquier elemento del documento que coincidiera con el selector, por la cascada
  del Capítulo 2.
- **No había ciclo de vida.** Nada avisaba cuándo un fragmento entraba o salía del
  documento, y por eso la baja de suscripciones del Capítulo 4 dependía enteramente
  de que el programador se acordara.
- **No había forma de declarar un componente en el marcado.** Había que invocarlo
  desde código.

Los frameworks resolvieron eso por su cuenta, cada uno con su propio modelo. La
plataforma respondió con un conjunto de especificaciones que se conocieron como
**componentes web**, propuestas alrededor de 2011 y estabilizadas a lo largo de la
década siguiente. Son tres piezas independientes que se pueden usar por separado:

| Pieza | Resuelve |
| --- | --- |
| **Elementos personalizados** | Declarar un elemento propio, con ciclo de vida |
| **DOM en la sombra** | Aislar estructura y estilos |
| **Plantillas** | Marcado inerte, listo para clonar |

Hubo una cuarta —un mecanismo para importar fragmentos de HTML— que **se abandonó**,
y su reemplazo son los módulos ES del Capítulo 3. Vale mencionarlo porque explica
por qué la documentación vieja menciona una pieza que ya no existe.

---

## 7.6. Elementos personalizados

### 7.6.1. Definir y registrar

```ts
class TarjetaProducto extends HTMLElement {
  connectedCallback() {
    this.textContent = this.getAttribute("nombre") ?? "";
  }
}

customElements.define("fs-tarjeta-producto", TarjetaProducto);
```

```html
<fs-tarjeta-producto nombre="Milanesa napolitana"></fs-tarjeta-producto>
```

Dos requisitos que la especificación impone. **El nombre debe llevar un guion**, y no
es una convención estética: garantiza que nunca colisione con un elemento que el
estándar incorpore en el futuro, porque los elementos nativos jamás llevan guion.
Y **la clase debe extender `HTMLElement`**.

El prefijo de dos letras —`fs-` por Food Store— es una convención razonable para
agrupar los componentes propios y evitar choques con bibliotecas.

> **⚠️ OJO ACÁ**
> Hay un detalle del registro que produce un síntoma desconcertante: **un elemento
> personalizado que no está registrado no falla. Simplemente no hace nada.**
>
> El navegador lo trata como un elemento desconocido, lo mete en el árbol como si
> fuera un `<span>` cualquiera, y sigue. Tu componente aparece vacío en la pantalla,
> sin ningún error en la consola.
>
> Las tres causas, en orden de frecuencia:
>
> 1. **El módulo que llama a `customElements.define` nunca se importó.** Pasa
>    constantemente: definiste el componente, lo usaste en el marcado, y nadie
>    importó el archivo que lo registra. Como los `import` son estáticos (Capítulo 3),
>    si nadie lo importa, ese código **no existe** en el paquete.
> 2. El nombre del marcado no coincide exactamente con el registrado.
> 3. El marcado se parseó antes de que el registro ocurriera — se resuelve solo
>    cuando el registro llega, pero si nunca llega, nunca se resuelve.
>
> Diagnóstico en un segundo, desde la consola:
> `customElements.get("fs-tarjeta-producto")`. Si devuelve `undefined`, el problema
> es el registro y no tu componente.

### 7.6.2. El ciclo de vida

Cuatro métodos, que el navegador invoca solo:

| Método | Cuándo |
| --- | --- |
| `constructor` | Al crear la instancia |
| `connectedCallback` | Cada vez que se **inserta** en el documento |
| `disconnectedCallback` | Cada vez que se **quita** del documento |
| `attributeChangedCallback` | Al cambiar un atributo observado |
| `adoptedCallback` | Al moverse a otro documento |

*(Ver Figura 7.3: el ciclo de vida de un elemento personalizado.)*

Dos precisiones que evitan errores concretos.

**En el constructor no se debe tocar el DOM ni leer atributos.** El elemento puede
existir sin estar completo: sus atributos pueden no haberse aplicado todavía y sus
hijos pueden no existir. La especificación lo prohíbe explícitamente. El trabajo
real va en `connectedCallback`.

**`connectedCallback` puede ejecutarse más de una vez.** Si el elemento se mueve de
lugar en el documento, se dispara `disconnectedCallback` y después
`connectedCallback` otra vez. Un componente que asume que se monta una sola vez
**duplica sus suscripciones** cada vez que alguien lo reordena.

### 7.6.3. Atributos observados

`attributeChangedCallback` sólo se invoca para los atributos declarados:

```ts
class EstadoPedido extends HTMLElement {
  static observedAttributes = ["estado"];

  attributeChangedCallback(nombre: string, anterior: string, nuevo: string) {
    if (anterior === nuevo) return;
    this.render();
  }
}
```

El `if` de la primera línea no es una optimización menor: **asignar un atributo con
el mismo valor dispara el método igual**, y sin esa comprobación un componente que
se actualiza a sí mismo puede entrar en un ciclo.

### 7.6.4. Atributos y propiedades, otra vez

La distinción del Capítulo 4 vuelve con más fuerza acá, porque un componente propio
tiene que decidir cómo recibe sus datos.

**Los atributos son siempre cadenas.** Sirven para configuración simple y para que el
componente se pueda declarar en el marcado. **Las propiedades admiten cualquier
valor**: objetos, arreglos, funciones.

La consecuencia es directa: **un objeto no se pasa por atributo.** Convertirlo a
texto y volver a parsearlo es frágil y caro. La forma correcta es asignar la
propiedad desde el código:

```ts
const tarjeta = document.createElement("fs-tarjeta-producto");
tarjeta.producto = producto;      // propiedad: el objeto entero
tarjeta.setAttribute("compacta", "");   // atributo: una bandera
contenedor.appendChild(tarjeta);
```

La tabla de piezas de la sección 2.4 del TPI lo dice de otra manera, describiendo la
responsabilidad de un componente: **recibe datos**, y expone el ciclo de vida. No los
busca por su cuenta.

> **💡 PARA ENTENDER**
> Esa frase de la consigna —"recibe datos"— es más importante de lo que parece, y el
> Capítulo 8 la va a convertir en una regla de arquitectura.
>
> Significa que un componente **no llama a la API**. No sabe qué endpoint existe, no
> sabe qué es Axios, no sabe si el dato vino de la red o de una prueba.
>
> ¿Y por qué conviene tanto? Por tres cosas concretas:
>
> - **Se puede probar** pasándole un objeto, sin levantar ningún servidor.
> - **Se puede reusar** en otra pantalla que consiga el dato de otra forma.
> - **Cuando algo se ve mal, sabés dónde mirar**: si el dato llegó bien y se ve mal,
>   es el componente; si llegó mal, es la capa de arriba. **Sin esa separación,
>   cada bug se busca en todos lados.**
>
> Cuando le pidas un componente a un agente, fijate en esto: **te va a meter el
> `fetch` adentro del componente** si no se lo prohibís. Es lo más común en los
> ejemplos, y es exactamente lo que la tabla de piezas del TPI no quiere.

---

## 7.7. RN-F01 en su lugar definitivo

El Capítulo 4 demostró el problema: una clausura mantiene vivo lo que referencia, y
una suscripción sin baja produce una fuga que **no se ve mirando la pantalla**. Acá
aparece el lugar donde esa baja va, y el TPI lo nombra explícitamente:

> **RN-F01.** Toda llamada a `subscribe()` devuelve su función de baja; hay que
> guardarla y ejecutarla en `destroy()` o `disconnectedCallback()`, que es
> obligatorio. **Ninguna suscripción se hace fuera de la clase base `Disposable`**,
> que acumula las bajas y las ejecuta en bloque. Garante: **TST-45**, que monta y
> desmonta una vista tres veces y verifica que el store quede con cero suscriptores.

La regla no dice sólo "acordate de dar de baja". Dice algo más fuerte: **que exista
una clase base que lo haga por vos**, y que ninguna suscripción ocurra fuera de ella.

La diferencia es de método. "Acordate" es una instrucción que falla el día que
alguien está apurado. Una clase base que acumula las bajas convierte el olvido en
algo estructuralmente difícil:

```ts
abstract class Disposable extends HTMLElement {
  private bajas: Array<() => void> = [];

  protected registrar(baja: () => void): void {
    this.bajas.push(baja);
  }

  disconnectedCallback(): void {
    for (const baja of this.bajas) baja();
    this.bajas = [];          // importante: puede volver a montarse (7.6.2)
  }
}
```

Y su uso:

```ts
class PanelDePedidos extends Disposable {
  connectedCallback() {
    this.registrar(pedidosStore.subscribe(this.alCambiar));
    this.registrar(observador.subscribe(this.alLlegarDatos));

    const c = new AbortController();
    window.addEventListener("resize", this.alRedimensionar, { signal: c.signal });
    this.registrar(() => c.abort());        // el AbortController del Capítulo 4
  }
}
```

Nótese que `PanelDePedidos` **no define `disconnectedCallback`**: lo hereda. No hay
nada que olvidar, porque no hay nada que escribir.

Sobre el garante conviene detenerse, porque es de lo mejor del diseño del TPI:

> **TST-45** monta y desmonta una vista **tres veces** y verifica que el store quede
> con **cero suscriptores**.

Tres veces, y no una. Con un solo ciclo, una baja faltante puede pasar
desapercibida; con tres, el contador de suscriptores queda en dos y el test falla
con un número que dice exactamente qué pasó. **Es una prueba diseñada para detectar
la acumulación, no la ausencia.**

> **💡 PARA ENTENDER**
> Acá hay una lección de diseño que vale más que la regla misma, y quiero que la
> veas:
>
> **La diferencia entre "acordate de dar de baja" y "no podés suscribirte fuera de
> `Disposable`" es la diferencia entre una recomendación y un diseño.**
>
> Una recomendación depende de que todos los integrantes del grupo, todos los días,
> a las dos de la mañana antes de entregar, se acuerden. Va a fallar. No porque sean
> descuidados: porque las recomendaciones siempre fallan a escala.
>
> Un diseño hace que la forma fácil sea la correcta. Si suscribirse pasa por
> `registrar()`, y `registrar()` guarda la baja, **el olvido deja de ser posible sin
> salirse del camino.**
>
> Cuando en el TPI armes tu arquitectura, preguntate esto en cada regla que tengas
> que cumplir: *¿estoy confiando en que alguien se acuerde, o estoy haciendo que sea
> difícil equivocarse?*
>
> Y ojo con los agentes: si le pedís a uno que escriba un componente que se suscribe
> a un store, **te va a escribir el `subscribe` y no la baja.** El `subscribe` hace
> falta para que funcione; la baja hace falta para que *siga* funcionando, y eso no
> aparece en la demo.

---

## 7.8. El DOM en la sombra

### 7.8.1. Qué aísla

Un elemento puede tener un subárbol propio, separado del documento principal:

```ts
class TarjetaProducto extends HTMLElement {
  connectedCallback() {
    const sombra = this.attachShadow({ mode: "open" });
    sombra.innerHTML = `
      <style>
        .titulo { font-weight: 600; }   /* no escapa */
      </style>
      <h3 class="titulo"><slot name="nombre"></slot></h3>
    `;
  }
}
```

El aislamiento funciona **en las dos direcciones**: los estilos declarados adentro no
afectan al resto del documento, y los estilos del documento no entran. Los
selectores tampoco cruzan: un `querySelectorAll(".titulo")` sobre el documento **no
encuentra** los elementos que están dentro de una sombra.

*(Ver Figura 7.4: qué aísla el DOM en la sombra.)*

Lo que sí atraviesa la frontera son las propiedades heredables del Capítulo 2
—tipografía, color— y las propiedades personalizadas, que son el mecanismo previsto
para permitir personalización controlada desde afuera.

### 7.8.2. Ranuras

Una **ranura** es un hueco donde se proyecta el contenido que el usuario del
componente escribió entre las etiquetas. El contenido sigue viviendo en el documento
principal —y por lo tanto **conserva sus estilos**—, sólo que se muestra en el lugar
que la ranura indica.

### 7.8.3. Lo que complica, y una decisión concreta

El aislamiento tiene un costo que en este proyecto es determinante, y conviene
enunciarlo sin vueltas:

**Las clases de Tailwind no cruzan la frontera.** Tailwind genera una hoja de
estilos global, y una hoja global no entra en un DOM en la sombra. Un componente con
sombra que use `class="flex items-center p-4"` **no recibe ninguno de esos estilos**.

Hay formas de sortearlo, todas incómodas: inyectar la hoja dentro de cada sombra,
usar hojas adoptables, o duplicar estilos. Y hay una salida simple: **usar elementos
personalizados sin DOM en la sombra**, lo que se conoce como quedarse en el DOM
claro.

Eso es perfectamente legítimo. **Las tres tecnologías de la sección 7.5 son
independientes**: se puede usar el ciclo de vida sin usar el aislamiento. Se pierde
el encapsulamiento de estilos, que con Tailwind importa menos —las utilidades ya
acotan el alcance—, y se conserva lo que este capítulo necesita: `connectedCallback`,
`disconnectedCallback` y la posibilidad de declarar el elemento en el marcado.

El aislamiento tiene además dos costos de accesibilidad que conviene conocer: **una
etiqueta de formulario no puede referenciar por identificador a un campo que está
dentro de una sombra**, y las relaciones de accesibilidad que se expresan por
identificador tampoco cruzan la frontera.

> **📌 NOTA**
> El TPI declara **Web Components** en su stack y declara **Tailwind**. Como acabás
> de ver, esas dos cosas tienen una fricción real.
>
> No es una contradicción del enunciado: **es una decisión de diseño que te toca tomar
> a vos**, y conviene tomarla a conciencia y una sola vez para todo el proyecto.
>
> La opción razonable, salvo que tengas un motivo concreto para lo contrario, es
> **elementos personalizados sin sombra**. Ganás el ciclo de vida —que es lo que las
> reglas necesitan— y Tailwind sigue funcionando como en cualquier otra parte.
>
> Lo que **no** podés hacer es mezclar sin criterio: algunos componentes con sombra y
> otros sin, según cómo salió. Vas a terminar con estilos que aplican en la mitad de
> la pantalla y no en la otra, y con horas perdidas buscando un problema de CSS que
> en realidad es un problema de arquitectura.

---

## 7.9. Plantillas

El elemento de plantilla contiene marcado que **no se renderiza ni se ejecuta**: sus
imágenes no se descargan y sus scripts no corren. Existe para ser clonado.

```html
<template id="tpl-tarjeta">
  <article class="rounded-lg border p-4">
    <h3 data-campo="nombre"></h3>
    <p data-campo="precio"></p>
  </article>
</template>
```

```ts
const tpl = document.querySelector<HTMLTemplateElement>("#tpl-tarjeta")!;
const nodo = tpl.content.cloneNode(true) as DocumentFragment;
nodo.querySelector('[data-campo="nombre"]')!.textContent = producto.nombre;
```

Dos ventajas sobre construir cada nodo por programa: la estructura queda **legible
como marcado**, y clonar es más rápido que crear elemento por elemento.

Sobre lo segundo conviene ser preciso, porque la diferencia importa recién a partir
de cierta escala. Clonar un fragmento ya parseado evita repetir el trabajo de
construir cada nodo por separado, y con listas de decenas o cientos de elementos
—un catálogo, un historial de pedidos— eso se nota. Con tres elementos, no. La
razón principal para usar plantillas no es el rendimiento sino la legibilidad.

Y una que importa más para este módulo: **el contenido de la plantilla es marcado
estático que escribió el programador**, y los datos se insertan con `textContent`.
Eso cumple RN-F02 **por construcción**, sin que nadie tenga que recordarlo. Es el
mismo principio que la clase `Disposable` de la sección 7.7: hacer que lo correcto
sea el camino fácil.

> **💡 PARA ENTENDER**
> Fijate el patrón que se repite tres veces en este capítulo, porque es el que
> conviene que uses cuando diseñes lo tuyo:
>
> | En vez de recordar… | La estructura lo resuelve |
> | --- | --- |
> | "acordate de dar de baja" | `Disposable` acumula las bajas |
> | "no uses `innerHTML` con datos" | La plantilla es estática, los datos van por `textContent` |
> | "destruí el gráfico al desmontar" | Su destrucción se registra como una baja más |
>
> Las tres cosas se podrían haber escrito como advertencias en un README. **Ninguna
> habría sobrevivido a un cuatrimestre.**
>
> Escritas como estructura, no hay nada que recordar: **el camino fácil es el
> correcto**, y salirse de él da más trabajo que seguirlo.
>
> Cuando diseñes algo —tuyo o del laburo— esa es la pregunta que vale: *¿estoy
> escribiendo una advertencia o estoy cambiando la forma del camino?*

---

## 7.10. Chart.js y la regla RN-F05

El panel de administración del TPI muestra gráficos con Chart.js, y hay una regla
específica para eso:

> **RN-F05.** Toda instancia de Chart.js se crea **una sola vez por montaje** y se
> destruye con `chart.destroy()` al desmontar; la actualización se hace **mutando
> `chart.data` y llamando `chart.update()`**. Garante: TST-45, por la misma vía que
> RN-F01 —la destrucción del gráfico se registra como una baja más.

Esa última frase es la clave del diseño: **el gráfico no es un caso especial.** Su
destrucción se registra en el mismo `Disposable` de la sección 7.7, junto con las
suscripciones. Una sola disciplina cubre las dos reglas.

```ts
class GraficoVentas extends Disposable {
  private chart?: Chart;

  connectedCallback() {
    const canvas = this.querySelector("canvas")!;
    this.chart = new Chart(canvas, configuracion);
    this.registrar(() => this.chart?.destroy());     // una baja más

    this.registrar(ventasStore.subscribe(datos => {
      this.chart!.data.datasets[0].data = datos;      // mutar
      this.chart!.update();                           // y actualizar
    }));
  }
}
```

Vale entender **por qué** hace falta destruir, porque el motivo no es evidente. Una
instancia de Chart.js registra manejadores en la ventana para redimensionar, se
adueña del elemento de dibujo y mantiene sus propias estructuras internas. Si se
crea una instancia nueva sobre el mismo elemento sin destruir la anterior, **las dos
quedan vivas**: las dos responden al redimensionado, las dos dibujan sobre el mismo
lienzo, y aparecen síntomas desconcertantes —globos de información duplicados,
animaciones que se pisan— además de la fuga.

Y la segunda mitad de la regla —mutar y actualizar en lugar de crear de nuevo— tiene
la misma raíz: **crear una instancia nueva en cada actualización es exactamente el
error que la primera mitad prohíbe**, repetido muchas veces por segundo.

> **⚠️ OJO ACÁ**
> Este es el error que te va a escribir un agente de IA con total naturalidad, y en
> el panel del TPI —que recibe eventos por SSE— se pone feo rápido.
>
> Le pedís "que el gráfico se actualice cuando lleguen datos nuevos" y te sale esto:
>
> ```ts
> ventasStore.subscribe(datos => {
>   new Chart(canvas, { ...config, data: datos });   // instancia nueva cada vez
> });
> ```
>
> Anda. Se ve bien. **Y cada evento deja una instancia viva más.** A los cincuenta
> eventos tenés cincuenta gráficos dibujando sobre el mismo lienzo, cincuenta
> manejadores de redimensionado, y globos de información que aparecen duplicados
> porque hay cincuenta escuchando el mismo mouse.
>
> Lo correcto es lo que dice la regla, y son dos líneas:
>
> ```ts
> this.chart.data.datasets[0].data = datos;   // mutar
> this.chart.update();                        // y actualizar
> ```
>
> Fijate que es **el mismo error del Capítulo 4** con otra cara: algo que se crea y no
> se destruye, acumulándose sin que la pantalla lo muestre.

---

## 7.11. Herramientas de diagnóstico

**En desarrollo**, el panel de red muestra algo que sorprende la primera vez:
**decenas o cientos de peticiones**, una por cada módulo del proyecto. Eso es
correcto y es la decisión de diseño de la sección 7.2 funcionando. En producción, la
misma página descarga unos pocos archivos.

Comparar ambas vistas es el mejor ejercicio para entender qué hace la herramienta.

**Para los componentes**, el panel de elementos muestra los elementos
personalizados con su nombre propio, y cuando tienen sombra aparece un nodo
especial que se puede desplegar. La consola permite además inspeccionar el registro:
`customElements.get("fs-tarjeta-producto")` devuelve la clase si está registrada, y
`undefined` si no —que es el diagnóstico de un componente que aparece en el marcado
y no hace nada—.

*(Ver Figura 7.6: un elemento personalizado y su sombra en el inspector.)*

Y para verificar RN-F01, el procedimiento del Capítulo 4 sigue siendo el mismo, con
un agregado: **contar los suscriptores del store**, que es lo que hace TST-45.

> **🧪 EXPERIMENTO**
> Reproducí TST-45 a mano antes de escribirlo como test. Es el experimento que cierra
> el capítulo.
>
> 1. Escribí un componente que se suscriba a un store en `connectedCallback` **sin**
>    dar de baja.
> 2. Desde la consola, montalo y desmontalo **tres veces** —agregándolo y quitándolo
>    del documento—.
> 3. Contá los suscriptores del store.
>
> Te van a quedar **tres**. La pantalla está vacía y hay tres componentes fantasma
> escuchando cambios y actualizando nodos que ya nadie ve.
>
> 4. Hacé que el componente herede de `Disposable` y repetí los tres ciclos.
> 5. Contá otra vez: **cero**.
>
> Ese conteo es literalmente el garante que el TPI declara. Y fijate por qué el test
> hace **tres** ciclos y no uno: con un solo ciclo, un contador en 1 puede confundirse
> con otra cosa. **Con tres, el número te dice exactamente cuántas bajas te
> olvidaste.**

---

## 7.12. Seguridad y evolución

Tres consideraciones cierran el capítulo.

**Todo lo que entra al paquete es público.** Vale para las variables de entorno de la
sección 7.3.4 y para cualquier constante escrita en el código. El paquete de
producción se puede leer, y aunque los nombres estén acortados, **las cadenas de
texto quedan intactas**.

**Cada dependencia es código de terceros que se ejecuta con los mismos privilegios
que el propio.** Un paquete comprometido puede leer el token, modificar el DOM o
emitir peticiones. La lista de doce tecnologías de la sección 7.1 es corta a
propósito, y ampliarla tiene un costo que no se ve en el momento.

**Un elemento personalizado que arma su contenido con `innerHTML` a partir de datos
recibidos reintroduce el problema del Capítulo 4.** El aislamiento del DOM en la
sombra **no protege de la inyección**: un script inyectado dentro de una sombra se
ejecuta igual. RN-F02 vale adentro y afuera.

Sobre la evolución, tres incorporaciones recientes atacan justamente las fricciones
de la sección 7.8.3: las **hojas de estilo adoptables** permiten compartir una misma
hoja entre muchas sombras sin duplicarla; los **elementos personalizados asociados a
formularios** permiten que un componente participe de un formulario nativo, que era
una de las carencias más molestas; y las **consultas de contenedor** del Capítulo 2
resuelven que un componente responda a su contenedor y no a la ventana, que es
exactamente lo que un componente reutilizable necesita.

---

## 7.13. Verificación

1. Crear un proyecto con la plantilla que el TPI declara y **contar las peticiones**
   del panel de red en desarrollo.
2. Construir el proyecto para producción y **volver a contarlas**, explicando la
   diferencia.
3. Introducir un error de tipo deliberado y **verificar que el proyecto arranca
   igual**; ejecutar después la verificación por separado y ver el error.
4. Declarar una variable de entorno con el prefijo requerido y otra sin él, y
   **buscar ambas en el paquete de producción**.
5. Escribir un elemento personalizado que muestre un mensaje en `connectedCallback` y
   otro en `disconnectedCallback`, y **moverlo de lugar** en el documento observando
   la consola.
6. Implementar la clase base `Disposable` y un componente que la use, y demostrar que
   no define `disconnectedCallback` propio.
7. Reproducir TST-45 a mano: montar y desmontar tres veces y **contar suscriptores**.
8. Crear un componente con DOM en la sombra que use clases de Tailwind y **verificar
   que no se aplican**; resolverlo quitando la sombra.
9. Crear una instancia de Chart.js dos veces sobre el mismo lienzo sin destruir, y
   **documentar los síntomas**.

---

## 7.14. Errores frecuentes

**Creer que "sin framework" significa "sin dependencias".** El TPI declara doce
tecnologías; lo prohibido es el framework de interfaz, que se haría cargo del ciclo
de vida (sección 7.1).

**Suponer que el proyecto arranca porque los tipos están bien.** La herramienta de
construcción borra los tipos sin verificarlos (sección 7.3.3).

**Exponer un secreto en una variable de entorno del cliente.** Queda en texto plano
en el paquete público, y borrarlo después no alcanza: hay que rotarlo (sección
7.3.4).

**Olvidar un archivo en las rutas escaneadas de Tailwind.** Sus clases no se generan
y el componente aparece sin estilo, sin ningún error (sección 7.4).

**Definir un elemento personalizado sin guion en el nombre.** El registro falla
(sección 7.6.1).

**Tocar el DOM o leer atributos en el constructor.** El elemento puede no estar
completo; el trabajo va en `connectedCallback` (sección 7.6.2).

**Asumir que `connectedCallback` se ejecuta una sola vez.** Mover el elemento lo
vuelve a disparar, y las suscripciones se duplican (sección 7.6.2).

**Pasar un objeto por atributo.** Los atributos son cadenas; los objetos van por
propiedad (sección 7.6.4).

**Suscribirse fuera de la clase base.** Viola RN-F01 explícitamente, que exige que
ninguna suscripción ocurra fuera de `Disposable` (sección 7.7).

**No vaciar la lista de bajas tras ejecutarlas.** Si el componente se vuelve a
montar, acumula (sección 7.7).

**Usar DOM en la sombra con Tailwind sin resolver el aislamiento.** Los estilos
globales no cruzan la frontera (sección 7.8.3).

**Crear una instancia de Chart.js nueva en cada actualización.** Deja instancias
vivas superpuestas. La regla exige mutar y actualizar (sección 7.10).

---

## 7.15. Actividades

1. **Desarrollo contra producción, medido.** Crear el proyecto, documentar la
   cantidad de peticiones y el tiempo de arranque en desarrollo, construir para
   producción y repetir la medición sobre el resultado servido. Explicar cada
   diferencia a partir de las cuatro decisiones de diseño de la sección 7.2.

2. **La verificación que falta.** Introducir tres errores de tipo en el proyecto,
   comprobar que arranca igual, y configurar el paso de construcción para que un
   error de tipo impida publicar. Documentar qué comando lo hace y dónde se ubica.

3. **Un componente completo.** Implementar `fs-tarjeta-producto` que reciba el
   producto por propiedad, muestre su nombre e importe respetando RN-F08, se suscriba
   al store del carrito y se dé de baja al desmontarse. Sin DOM en la sombra.

4. **La clase base.** Implementar `Disposable` con `registrar()` y
   `disconnectedCallback()`, y refactorizar dos componentes para que la usen.
   Verificar que ninguno define su propio `disconnectedCallback`.

5. **TST-45 a mano.** Escribir el procedimiento de conteo de suscriptores, ejecutarlo
   sobre un componente con fuga y sobre uno correcto, y documentar los dos resultados.
   Explicar por qué el test hace tres ciclos y no uno.

6. **Exploración: la frontera de la sombra.** Construir el mismo componente en dos
   versiones, con y sin DOM en la sombra, usando clases de Tailwind y una regla de
   estilo global. Documentar qué se aplica en cada caso, qué encuentra un
   `querySelector` desde el documento, y qué pasa con una etiqueta de formulario que
   referencia un campo interno. Relacionar lo observado con la sección 7.8.3 y
   justificar la elección para el TPI.

7. **Exploración: qué quedó afuera del paquete.** Construir para producción y abrir
   el resultado. Buscar tres cadenas del código propio, una variable de entorno
   expuesta y una no expuesta, y una función que no se usa en ningún lado. Documentar
   qué se encontró y qué no, y relacionarlo con la eliminación de código muerto de la
   sección 7.3.2 y con la propiedad de los `import` estáticos del Capítulo 3.

---

## 7.16. Síntesis

1. **"Sin framework" no es "sin dependencias".** El TPI declara doce tecnologías. Lo
   prohibido es el framework de interfaz, porque se haría cargo del ciclo de vida, y
   **el ciclo de vida es exactamente lo que el alumno no puede delegar**: ahí viven
   las reglas.

2. Empaquetar nació de una carencia del lenguaje —no había módulos— y de una
   limitación del transporte. Cuando los módulos ES llegaron al navegador,
   **empaquetar en desarrollo pasó a resolver un problema que ya no existía**, y
   nadie lo notó durante años.

3. Vite separa **desarrollo y producción como problemas distintos**: sin empaquetar
   en el primero, empaquetado en el segundo, con las dependencias pre-procesadas una
   sola vez.

4. **La herramienta de construcción no verifica los tipos: los borra.** El proyecto
   arranca perfecto con errores adentro, y por eso la verificación debe ser un paso
   explícito del proceso de publicación.

5. **Todo lo que entra al paquete es público**, empezando por las variables de
   entorno. Un secreto expuesto no se arregla borrándolo: se rota.

6. Los componentes web son **tres tecnologías independientes**, y se pueden usar por
   separado. El ciclo de vida sirve sin el aislamiento.

7. `connectedCallback` **puede ejecutarse más de una vez**, y en el constructor no se
   toca el DOM. Los objetos se pasan por propiedad, no por atributo.

8. RN-F01 no dice "acordate de dar de baja": dice que **ninguna suscripción ocurra
   fuera de una clase base que lo haga por vos**. Es la diferencia entre una
   recomendación y un diseño.

9. **TST-45 monta y desmonta tres veces** y cuenta suscriptores. Tres, y no uno,
   porque la prueba está diseñada para detectar **acumulación**.

10. **Tailwind y el DOM en la sombra tienen una fricción real**: los estilos globales
    no cruzan la frontera. La decisión razonable para este proyecto es usar elementos
    personalizados sin sombra, tomada una vez y para todo el proyecto.

11. RN-F05 no trata al gráfico como un caso especial: **su destrucción se registra
    como una baja más** en el mismo mecanismo de RN-F01. Una sola disciplina cubre las
    dos reglas.

---

## 7.17. Referencias y lecturas complementarias

Las fuentes normativas de la segunda mitad del capítulo están en el **HTML Living
Standard** del WHATWG: la sección de elementos personalizados define el registro, los
requisitos del nombre y los cuatro métodos del ciclo de vida de la sección 7.6.2, e
incluye la prohibición explícita de tocar el DOM en el constructor; la sección de
plantillas define el comportamiento inerte del contenido. El **DOM Living Standard**
especifica el árbol en la sombra, las ranuras y el modo de aislamiento de la sección
7.8. La interacción entre estilos y sombra está en **CSS Scoping Level 1**, que
define `:host` y `::part()`, y las hojas adoptables mencionadas en la sección 7.12
están en **CSSOM Level 1**. Los módulos ES que hacen posible el modelo de desarrollo
de la sección 7.3.1 corresponden a **ECMA-262**, con su carga definida en el estándar
HTML.

Para las herramientas, la documentación oficial de Vite en `vite.dev` explica el
pre-procesamiento de dependencias y el reemplazo de módulos en caliente, y su guía
de variables de entorno detalla la regla del prefijo de la sección 7.3.4. La
documentación de **esbuild** incluye una sección sobre por qué es rápido que vale la
pena leer, porque explica decisiones de diseño trasladables a otros contextos. Sobre
Chart.js, su documentación de ciclo de vida y de actualización de datos cubre
exactamente lo que RN-F05 exige.

Como bibliografía de estudio, la guía de **web.dev** sobre componentes web y la
documentación de MDN sobre elementos personalizados son las referencias de consulta
cotidiana. Para el diseño de componentes que funcionan con teclado y lector de
pantalla, Pickering, *Inclusive Components* —ya citado en el Capítulo 2— sigue siendo
la mejor guía práctica, y su tratamiento de los costos de accesibilidad del DOM en
la sombra complementa la sección 7.8.3. Y del TPI conviene tener a mano la tabla de
piezas de la sección **2.4**, que declara la responsabilidad de cada archivo del
frontend y es el mapa que el Capítulo 8 va a recorrer entero.

---

**Continúa en:** Capítulo 8 — Arquitectura: Feature-Sliced Design, estado y el TPI,
donde las piezas de este capítulo se ordenan en capas con una regla de dependencias,
y donde el módulo cierra con lo que lo motivó: cómo dirigir a un agente de IA sobre
una base que uno entiende.
