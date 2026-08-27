# Capítulo 3 — El bucle de eventos del servidor

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 3.1. Alcance de la clase

Esta es la clase más importante del módulo, y conviene decir por qué con las
palabras del propio TPI. Su sección 1.4 se abre así:

> Esta sección es **normativa** y es la que más consecuencias tiene sobre el código;
> **todo lo demás del documento la presupone.**

Ocho de las treinta y siete reglas del backend viven ahí, identificadas como
**EA-01 a EA-08**, y este capítulo las funda todas. No están repartidas por el
documento: están juntas, en una sola sección, porque responden a un mismo hecho.

Ese hecho es el que el Capítulo 1 dejó enunciado y no desarrolló: **el servidor
atiende todas las peticiones sobre un único bucle de eventos, y una sola línea que
no ceda el control lo detiene para todos.** No para el usuario que la disparó: para
todos los usuarios conectados, al mismo tiempo.

Hay una coincidencia que esta clase debe aprovechar. **Esta misma semana, la otra
mitad de la cursada estudia el bucle de eventos del navegador**: un solo hilo que
ejecuta y dibuja, y que al bloquearse deja la página muerta. Es el mismo modelo
mental, en otro lenguaje y del otro lado del cable. Verlo dos veces el mismo día lo
fija de una manera que una sola exposición no consigue, y conviene que los dos
docentes usen el mismo dibujo.

El capítulo también estudia el error que el TPI señala como **"el que más tiempo
hace perder"**: la excepción que aparece cuando el ORM intenta emitir una consulta
desde un lugar donde no puede. Su nombre no dice nada —`MissingGreenlet`— y su causa
está siempre lejos de donde salta. Entenderla exige entender cómo SQLAlchemy
implementa su capa asincrónica, y esta clase lo desarma.

Y hay una sección que rara vez se enseña y que este capítulo incluye porque el TPI
la declara: **qué hacía bien el modelo sincrónico que ahora hay que reponer a
mano.** El modelo asincrónico no es gratis, y saber qué se resignó es lo que separa
usarlo de padecerlo.

Al finalizar la clase, el alumno debe poder **explicar qué hace cada una de las ocho
reglas EA y qué problema previene**, reconocer una llamada bloqueante en código
ajeno, y diagnosticar una excepción de greenlet a partir de su traza.

**Contenidos**

1. Origen y objetivos de diseño de la asincronía en Python.
2. Concurrencia y paralelismo: la distinción que ordena todo.
3. Anatomía del bucle de eventos.
4. Corrutinas, tareas y puntos de cesión.
5. Qué significa "bloquear" y por qué acá duele más.
6. Las tres operaciones bloqueantes del sistema.
7. Clientes asincrónicos para toda entrada y salida.
8. La regla del greenlet, explicada.
9. El N+1 que dejó de ser un problema de rendimiento.
10. Grupos de tareas y por qué no se lanzan tareas sueltas.
11. Recursos y ciclo de vida de la aplicación.
12. Lo que la sincronía hacía bien y hay que reponer.
13. Herramientas de diagnóstico.

---

## 3.2. Por qué existe la asincronía en Python: origen y diseño

El Capítulo 1 estableció el problema: un servidor pasa su tiempo esperando, y un
hilo por conexión no escala. Falta la otra mitad de la historia, que es **cómo
Python llegó a poder expresar eso**, porque el camino explica la forma que tiene hoy.

**Primera etapa: las funciones de retorno.** Los primeros marcos de trabajo
asincrónicos de Python —Twisted en 2002, Tornado a partir de 2009— resolvieron la
concurrencia con el mismo mecanismo que el navegador usó durante años: registrar una
función que se ejecuta cuando algo termina. Funcionaba, y tenía el problema que la
otra mitad de la cursada estudia con el mismo nombre: **el código se anidaba y los
errores no se podían capturar desde afuera.**

**Segunda etapa: los generadores como corrutinas.** Python tenía desde 2001 una
herramienta que resultó ser exactamente lo que hacía falta. Un generador **puede
suspenderse y reanudarse**, que es justamente el comportamiento de una corrutina. El
PEP 342, en 2005, lo hizo bidireccional —el generador podía recibir valores al
reanudarse— y el PEP 380, en 2009, agregó `yield from` para delegar a otro generador.

Con esas dos piezas se podía escribir código asincrónico que **se leía como
secuencial**, y durante años se hizo así. El costo era que la sintaxis mentía: lo
que parecía un generador era una corrutina, y no había forma de distinguirlos.

**Tercera etapa: la biblioteca estándar.** El PEP 3156, de 2012, incorporó
`asyncio` al lenguaje, y llegó con Python 3.4 en 2014. Por primera vez hubo **un
bucle de eventos estándar**, lo que permitió que bibliotecas de distintos autores
funcionaran juntas.

**Cuarta etapa: la sintaxis propia.** El PEP 492, de 2015, agregó `async` y `await`
como palabras del lenguaje, disponibles desde Python 3.5. Eso resolvió la mentira de
la etapa anterior: **una corrutina se declara como tal y los puntos donde cede el
control se ven a simple vista.**

**Y una quinta, que el TPI exige.** Python 3.11, de 2022, incorporó los **grupos de
tareas** y la sintaxis `except*` con los grupos de excepciones del PEP 654. Eso
resolvió un problema real que la sección 3.10 desarrolla: qué pasa cuando varias
tareas concurrentes fallan a la vez. **Es la razón por la que el TPI fija Python
3.12 como piso** y no una versión anterior.

De ese recorrido salen las cuatro decisiones de diseño que gobiernan el capítulo.

**Primera: la concurrencia es cooperativa, no preventiva.** Nadie interrumpe a una
corrutina: **ella cede el control cuando quiere.** Y de ahí se deduce todo lo demás
de este capítulo, incluida la razón por la que una línea bloqueante es tan grave.

**Segunda: los puntos de cesión son visibles.** Cada `await` es un lugar donde el
control puede irse a otra parte. Eso permite razonar sobre qué puede ocurrir entre
dos líneas, algo que con hilos es imposible.

**Tercera: una corrutina no hace nada hasta que se la agenda.** Llamar a una función
asincrónica **no la ejecuta**: devuelve un objeto. Es lo contrario de lo que ocurre
del otro lado del cable, donde una promesa arranca su operación al crearse.

**Cuarta: las excepciones se propagan por el árbol de tareas.** Con los grupos de
tareas, una tarea que falla cancela a sus hermanas y su error llega a quien las
lanzó. Sin eso, una tarea suelta que falla **desaparece en silencio**, que es lo que
EA-07 previene.

> **💡 PARA ENTENDER**
> La primera decisión es la que hay que entender de verdad, porque de ella se
> deducen las ocho reglas de esta clase:
>
> **Nadie te interrumpe. Vos cedés.**
>
> Con hilos, el sistema operativo te saca del procesador cuando se le da la gana.
> Podés escribir un bucle infinito y el resto del programa sigue andando, porque
> alguien más te va a interrumpir.
>
> Con corrutinas **no hay nadie que te interrumpa.** Si tu código no llega a un
> `await`, el bucle de eventos **no puede hacer absolutamente nada** hasta que
> termines. No es que sea lento: no existe el mecanismo.
>
> Por eso la palabra "bloquear" significa algo mucho más grave de este lado. Y por
> eso hay ocho reglas dedicadas a que nunca pase.
>
> Del otro lado del cable pasa exactamente lo mismo, y tus compañeros lo están viendo
> hoy: un solo hilo que ejecuta y dibuja. **Cambia el lenguaje, no el modelo.**

---

## 3.3. Concurrencia no es paralelismo

Esta distinción se confunde permanentemente y sin ella nada de lo que sigue se
entiende.

**Paralelismo** es hacer dos cosas **al mismo tiempo**, lo que exige dos unidades de
ejecución: dos núcleos, dos procesos.

**Concurrencia** es **avanzar en varias cosas** durante el mismo período, sin que
necesariamente ocurran a la vez. Una sola unidad de ejecución que alterna entre
tareas es concurrente y no es paralela.

*(Ver Figura 3.1: concurrencia frente a paralelismo.)*

El modelo asincrónico de Python es **concurrente y no paralelo**: hay un solo hilo,
que va alternando. Y para un servidor web eso alcanza, por la razón del Capítulo 1:
si el trabajo dominante es esperar, no hace falta ejecutar en paralelo. Hace falta
**no quedarse quieto mientras se espera**.

Conviene ubicar acá el bloqueo global del intérprete, que se nombra siempre y se
explica poco. Ese mecanismo impide que dos hilos ejecuten instrucciones de Python
simultáneamente, y por lo tanto **impide el paralelismo real dentro de un proceso**.
Para trabajo de procesador eso es una limitación seria. Para trabajo de espera no lo
es: **el bloqueo se libera mientras se espera**, así que muchos hilos esperando
funcionan bien.

De ahí que el modelo asincrónico no sea una manera de esquivar esa limitación, sino
algo mejor: **una manera de no necesitar hilos en absoluto** para lo que un servidor
hace la mayor parte del tiempo.

> **📌 NOTA**
> El bloqueo global del intérprete se nombra en toda discusión sobre Python y casi
> siempre mal. Quedate con esto:
>
> | Tipo de trabajo | ¿El bloqueo molesta? | Qué corresponde |
> | --- | --- | --- |
> | **Esperar** (red, disco, base) | **No.** Se libera mientras esperás | Corrutinas |
> | **Calcular** (hash, imágenes, cifrado) | **Sí.** Dos hilos no aceleran nada | Otro proceso, o un hilo si es corto |
>
> Un servidor web es abrumadoramente la primera fila. Por eso el bloqueo global
> **no es el argumento** a favor de la asincronía en este proyecto: el argumento es el
> del Capítulo 1, que esperar no necesita un hilo por espera.
>
> Y ahí está el caso interesante del TPI: **bcrypt es de la segunda fila.** Es la
> única operación del sistema que calcula en serio, y por eso tiene dos reglas
> dedicadas —EA-02 y EA-06— más un semáforo. La excepción confirma la regla.

---

## 3.4. Anatomía del bucle de eventos

El bucle de eventos es un ciclo con cuatro pasos:

1. **Preguntar al sistema operativo** qué operaciones de entrada y salida están
   listas.
2. **Despertar** las corrutinas que esperaban esas operaciones.
3. **Ejecutar** cada una hasta su próximo punto de cesión.
4. **Volver al paso 1.**

*(Ver Figura 3.2: cómo una petición cede el control y vuelve.)*

Toda la clase está en el paso 3, en las palabras **"hasta su próximo punto de
cesión"**. Si una corrutina no llega a un `await`, el paso 3 no termina, y el bucle
nunca vuelve al paso 1. Nadie más es atendido.

Con un ejemplo del dominio:

```python
@router.get("/pedidos/{pedido_id}")
async def obtener_pedido(pedido_id: int, uow: UnitOfWork = Depends(get_uow)):
    pedido = await uow.pedidos.obtener(pedido_id)      # ① cede acá
    usuario = await uow.usuarios.obtener(pedido.usuario_id)  # ② y acá
    return armar_respuesta(pedido, usuario)            # ③ no cede: es rápido
```

En ① la corrutina le pide a la base de datos y **cede el control**. El bucle, en ese
momento, atiende otras peticiones. Cuando la base responde, la corrutina se reanuda
exactamente en ese punto. Lo mismo en ②. En ③ no hay cesión, y está bien: es
trabajo de milisegundos.

Esa es la forma correcta. La incorrecta se ve igual y no lo es:

```python
@router.get("/pedidos/{pedido_id}")
async def obtener_pedido(pedido_id: int):
    pedido = requests.get(f"{URL}/pedidos/{pedido_id}").json()   # NO cede
    return pedido
```

Esa línea usa un cliente sincrónico. No hay `await`, así que **no hay punto de
cesión**: el bucle se queda ahí, esperando la red, sin atender nada. Es EA-03, y la
sección 3.7 la desarrolla.

> **💡 PARA ENTENDER**
> Hay una forma de leer código asincrónico que te va a servir siempre, y es
> mecánica:
>
> **Buscá los `await`. Esos son los únicos lugares donde tu función puede pausarse.**
>
> Entre dos `await` consecutivos, tu código corre **sin que nadie lo interrumpa**.
> Nadie más toca nada. Eso tiene dos caras:
>
> - **La buena:** no necesitás candados para proteger una variable compartida entre
>   dos líneas sin `await`. Con hilos sí los necesitarías, porque el sistema
>   operativo te puede sacar en cualquier momento.
> - **La mala:** si entre dos `await` hay algo que tarda, **nadie más existe** hasta
>   que termine.
>
> Y de ahí sale el criterio para leer código ajeno: **una función `async` sin ningún
> `await` adentro es sospechosa.** O no hace entrada y salida —y entonces no
> necesitaba ser `async`— o la hace de forma bloqueante, que es el problema de este
> capítulo entero.

---

## 3.5. Corrutinas y tareas

Una función declarada con `async def` es una **función corrutina**. Llamarla
**no la ejecuta**:

```python
resultado = calcular_total(pedido)      # NO se ejecutó: es un objeto corrutina
resultado = await calcular_total(pedido)  # ahora sí
```

Esa es la tercera decisión de diseño de la sección 3.2, y merece atención porque es
**lo contrario de lo que ocurre del otro lado del cable**: en el navegador, llamar a
una función que devuelve una promesa **dispara la operación de inmediato**. Acá no
pasa nada hasta que alguien la agenda.

Para ejecutar varias cosas a la vez hace falta convertirlas en **tareas**, y el TPI
exige hacerlo con un grupo:

```python
async with asyncio.TaskGroup() as tg:
    t_productos = tg.create_task(listar_productos())
    t_categorias = tg.create_task(listar_categorias())

productos = t_productos.result()
categorias = t_categorias.result()
```

El grupo de tareas hace tres cosas que una tarea suelta no hace: **espera a todas
antes de salir del bloque**; si una falla, **cancela a las demás**; y **propaga los
errores** a quien abrió el grupo, agrupados si fueron varios —para eso existe la
sintaxis `except*`—.

Nótese el paralelo con lo que la otra mitad de la cursada ve esta semana: **dos
operaciones independientes se lanzan juntas y se esperan juntas.** Encadenarlas con
dos `await` seguidos las serializa sin motivo, y el tiempo total pasa a ser la suma
en lugar del máximo.

> **⚠️ OJO ACÁ**
> Este error es sutil y no falla con estruendo: **falla siendo lento.**
>
> ```python
> # Serializa: la segunda no arranca hasta que termina la primera
> productos = await listar_productos()
> categorias = await listar_categorias()
>
> # Concurrente: las dos salen juntas
> async with asyncio.TaskGroup() as tg:
>     tp = tg.create_task(listar_productos())
>     tc = tg.create_task(listar_categorias())
> ```
>
> Si cada consulta tarda 40 ms, la primera versión tarda 80 y la segunda 40. Con
> cuatro consultas independientes, 160 contra 40.
>
> Y acá va lo importante: **el código serializado no está mal escrito.** Es
> perfectamente correcto, hace lo que dice y pasa cualquier test. Simplemente tarda
> el doble sin necesidad.
>
> La pregunta que te tenés que hacer en cada `await` es una sola: **¿lo que viene
> después necesita este resultado?** Si la respuesta es no, esas dos operaciones van
> juntas.

---

## 3.6. Qué significa bloquear, y las tres del sistema

Una operación **bloquea** cuando ocupa el hilo sin ceder el control. Hay dos formas
de hacerlo y conviene distinguirlas porque tienen soluciones distintas:

**Entrada y salida sincrónica.** Leer un archivo, consultar la base con un cliente
sincrónico, hacer una petición HTTP con una biblioteca sincrónica. El hilo espera
una respuesta externa sin ceder.

**Trabajo de procesador.** Un cálculo largo, un cifrado, procesar una imagen. No hay
espera: hay trabajo, y mientras dure, no hay cesión posible.

El TPI enumera **las tres operaciones bloqueantes del sistema** en EA-02, y la lista
es corta a propósito:

> Las tres del sistema son **bcrypt**, la **lectura de archivos de configuración** y
> **cualquier llamada de librería sin variante asincrónica**; se ejecutan con
> `anyio.to_thread.run_sync()`.

La solución para las tres es la misma: **sacarlas a un hilo aparte.** El hilo se
bloquea, el bucle no.

```python
from anyio import to_thread

hash_almacenado = await to_thread.run_sync(bcrypt.hashpw, password, salt)
```

Esa línea sí tiene `await`: la corrutina cede mientras el trabajo ocurre en otro
lado, y se reanuda cuando termina.

Sobre el trabajo de procesador, EA-06 pone un umbral concreto que vale la pena
citar porque casi nadie da un número:

> **EA-06.** Ninguna corrutina hace trabajo de CPU de **más de un milisegundo** sin
> ceder. El único caso del sistema es bcrypt, que sale a un hilo por EA-02, y su
> concurrencia se acota con un semáforo.

Un milisegundo parece poco y es una elección razonable: con cien peticiones por
segundo, un milisegundo de cálculo por petición ya consume el diez por ciento del
hilo.

> **⚠️ OJO ACÁ**
> El umbral de un milisegundo suena exagerado hasta que hacés la cuenta, así que
> hacela:
>
> - **1 ms** por petición × 100 peticiones/s = **10 %** del hilo consumido en calcular
> - **10 ms** × 100 = **100 %**. El servidor no hace otra cosa.
> - bcrypt con factor 12 tarda del orden de **250 ms**. Cuatro logins por segundo
>   saturan el proceso completo.
>
> Ese último número es el que explica por qué bcrypt tiene dos reglas dedicadas y un
> semáforo. **No es que bcrypt sea lento por estar mal hecho: es lento a propósito**,
> justamente para que probar contraseñas por fuerza bruta sea caro.
>
> Lo que es una virtud contra un atacante es un problema contra tu bucle de eventos.
> Por eso sale a un hilo (EA-02) y por eso se acota cuántos pueden correr a la vez.
>
> Y ojo con esta trampa, que es la que engaña: **en tu máquina, probando solo, cuatro
> logins por segundo no van a pasar nunca.** Anda perfecto. El problema aparece el
> día que treinta personas entran a la vez al empezar el turno.

Y falta explicar el semáforo, porque es la parte que sorprende. Sacar bcrypt a un
hilo evita bloquear el bucle, pero **no evita que cien intentos de login simultáneos
lancen cien hilos** haciendo un cálculo deliberadamente caro. El semáforo acota
cuántos pueden ejecutarse a la vez. La clase 5 lo desarrolla.

Ahora bien, la regla más contraintuitiva de las ocho es EA-01, y conviene leerla
completa:

> **EA-01.** Todos los handlers se declaran con `async def`; no hay ningún handler
> con `def`. **La mezcla —un handler asincrónico que adentro llama a una función
> bloqueante— es peor que la sincronía completa**, porque bloquea el bucle de eventos
> y **detiene el proceso entero, no un hilo de un pool.**

Esa última frase es la clave y explica por qué la regla existe. El marco de trabajo
**admite** handlers sincrónicos: si se declara uno con `def`, lo ejecuta en un hilo
de un grupo reservado. Eso es lento pero contenido: bloquea un hilo de veinte, y el
resto sigue.

Un handler `async` con una línea bloqueante adentro **no va a ningún hilo**. Corre
en el bucle, y esa línea detiene el proceso completo.

*(Ver Figura 3.3: qué pasa cuando una línea bloquea, en los tres casos.)*

> **⚠️ OJO ACÁ**
> Grabate esta comparación, porque es la que explica por qué EA-01 dice lo que dice:
>
> | Qué escribiste | Qué bloquea |
> | --- | --- |
> | Handler `def` con código sincrónico | **Un hilo** de un grupo de veinte |
> | Handler `async def` bien escrito | **Nada** |
> | Handler `async def` con una línea sincrónica | **El proceso entero** |
>
> La tercera fila es la trampa, y es la que más se escribe: **tiene la apariencia de
> la segunda y el comportamiento peor que la primera.**
>
> Y el síntoma es engañoso. En desarrollo, con vos solo probando, **anda igual de
> bien que la versión correcta.** No hay diferencia visible.
>
> Se nota el día que hay treinta personas usando el sistema al mismo tiempo, y ahí
> no se nota como "está lento": se nota como **el servidor no responde**, incluidos
> los endpoints que no tienen nada que ver.

---

## 3.7. Clientes asincrónicos para toda entrada y salida

De todo lo anterior sale EA-03, que es la regla más mecánica de las ocho:

> **EA-03.** Toda la I/O usa clientes asincrónicos: **psycopg asincrónico** para
> PostgreSQL, **`redis.asyncio`** para Redis, **`httpx.AsyncClient`** para cualquier
> llamada saliente. **No se importa el módulo `redis` síncrono en ninguna parte del
> backend.**

La última frase es la que la vuelve verificable. No dice "usá el cliente
asincrónico": dice que **el otro no aparece en ningún import**, y eso se puede
comprobar con una búsqueda de texto.

El problema práctico que la regla previene es que muchas bibliotecas ofrecen las dos
variantes con nombres parecidos, y la sincrónica suele ser la que aparece en los
ejemplos de internet:

| Sincrónico —**prohibido**— | Asincrónico —**el del TPI**— |
| --- | --- |
| `import redis` | `import redis.asyncio as redis` |
| `import requests` | `import httpx` con `AsyncClient` |
| `psycopg.connect(...)` | `psycopg` asincrónico vía `create_async_engine` |
| `time.sleep(n)` | `await asyncio.sleep(n)` |

La última fila merece mención porque aparece en código de prueba todo el tiempo:
`time.sleep` **bloquea el bucle** durante el tiempo indicado. Su equivalente
asincrónico cede el control y permite atender otras peticiones mientras tanto.

> **⚠️ OJO ACÁ**
> EA-03 tiene una virtud que la separa de las otras siete, y conviene aprovecharla:
> **se puede verificar con una búsqueda de texto.**
>
> El TPI no dice "usá el cliente asincrónico". Dice que el sincrónico **no aparece en
> ningún import del backend**. Eso es comprobable:
>
> ```bash
> grep -rn "^import requests\|^import redis$\|time.sleep" app/
> ```
>
> Si eso devuelve algo, hay una violación. Sin discusión, sin criterio, sin revisión
> humana.
>
> Fijate por qué eso importa: **una regla que se puede verificar automáticamente es
> una regla que se cumple.** Una que depende de que alguien revise, se cumple hasta
> que hay apuro.
>
> Cuando armes el proyecto, ese `grep` va en el mismo lugar donde corren los tests.
> Y lo mismo vale para el resto: cada vez que puedas convertir una regla en una
> verificación automática, hacelo.

---

## 3.8. La regla del greenlet

Acá está lo que el TPI señala como **"la que más tiempo hace perder"**, y lo explica
en detalle en lugar de limitarse a prohibirla. Vale la pena seguir su razonamiento
completo, porque entender el mecanismo es lo que permite diagnosticar el error.

### 3.8.1. Cómo funciona la capa asincrónica del ORM

El TPI lo dice así:

> SQLAlchemy implementa su capa asincrónica **ejecutando el ORM síncrono dentro de un
> greenlet** y saltando al bucle de eventos cada vez que necesita I/O.

Un *greenlet* es una corrutina de bajo nivel: una unidad de ejecución que puede
suspenderse y reanudarse, implementada por fuera del lenguaje. Lo que SQLAlchemy
hace es no reescribir su ORM —que tiene años de trabajo y es sincrónico— sino
**ejecutarlo adentro de uno de estos greenlets**, y cada vez que ese código
sincrónico necesita hablar con la base, saltar al bucle de eventos, esperar ahí, y
volver.

Y sigue la parte importante:

> El mecanismo es transparente **mientras la I/O ocurra donde SQLAlchemy la espera**:
> dentro de un `await` sobre uno de sus métodos.

Ahí está la condición. El salto al bucle sólo es posible **desde adentro del
greenlet**, y sólo se entra al greenlet cuando se hace `await` sobre un método del
ORM.

### 3.8.2. Cuándo falla y por qué el mensaje no ayuda

> Cuando el ORM intenta emitir una consulta **desde un lugar donde no hay `await`**
> —al leer un atributo de una relación no cargada, o al tocar un objeto expirado
> después del commit— **no hay a dónde saltar**, y la excepción es `MissingGreenlet`.

Dos causas, y las dos tienen su regla.

**Primera causa: leer una relación que no se precargó.** El objeto está en memoria,
se accede a `pedido.usuario`, y el ORM decide que necesita ir a buscarlo. Pero ese
acceso ocurre en una línea común, sin `await`. No hay greenlet. Excepción.

De ahí sale **EA-05**:

> La carga perezosa de relaciones **está prohibida**. Toda relación que una respuesta
> vaya a leer se precarga explícitamente con `selectinload()` en la consulta del
> repositorio, según la tabla de precarga de la sección 8.3.

**Segunda causa: tocar un objeto después del commit.** Por defecto, al confirmar una
transacción el ORM marca sus objetos como expirados, para que la próxima lectura
traiga datos frescos. Esa próxima lectura **también intenta emitir I/O implícita**, y
también falla.

De ahí sale **EA-04**, cuya redacción vale citar porque anticipa el malentendido:

> La sesión se construye con `async_sessionmaker(expire_on_commit=False)`. **El valor
> `False` no es una optimización**: con `True`, el objeto queda expirado tras el
> commit y su primera lectura posterior intenta emitir I/O implícita, que en modo
> asincrónico lanza `MissingGreenlet`.

*(Ver Figura 3.4: dónde el ORM puede saltar al bucle y dónde no.)*
*(Ver Figura 3.6: una traza de la excepción y dónde está su causa real.)*

### 3.8.3. El N+1 que dejó de ser un problema de rendimiento

Y acá viene lo mejor del razonamiento del TPI, que conviene leer entero:

> La consecuencia práctica es **buena** y conviene verla así: **el N+1 deja de ser un
> problema de rendimiento y pasa a ser un error en tiempo de ejecución.** La tabla de
> precarga de la sección 8.3 es **una condición para que el endpoint funcione, no una
> recomendación.** El sistema **no puede tener un N+1 accidental**: lo que tendría,
> tiene una excepción.

Conviene desarmar por qué eso es una ventaja y no un castigo.

El problema conocido como N+1 consiste en emitir una consulta para traer una lista y
después **una consulta más por cada elemento** para traer su relación. Con cien
pedidos son ciento una consultas donde debía haber dos.

En un sistema sincrónico eso **funciona**. Es lento, y sólo se descubre cuando
alguien mira los registros de la base o cuando la lentitud molesta lo suficiente. Es
un problema silencioso, y los problemas silenciosos sobreviven años.

En este sistema **no funciona**: lanza una excepción en la primera iteración. No hay
forma de que un N+1 llegue a producción sin que nadie lo note, porque no llega a
producción en absoluto.

> **💡 PARA ENTENDER**
> Este es el mejor ejemplo del módulo de una restricción que parece un castigo y es
> un regalo, así que vale la pena verlo bien:
>
> **En un sistema sincrónico, el N+1 anda.** Lento, pero anda. Y por eso vive
> escondido durante años, hasta que un día la tabla creció y alguien nota que una
> pantalla tarda ocho segundos.
>
> **Acá el N+1 no anda: explota.** En la primera iteración, en tu máquina, mientras
> lo estás escribiendo.
>
> Fijate lo que eso significa: no es que el sistema sea más frágil. Es que **un
> problema de rendimiento invisible se convirtió en un error visible**, y los errores
> visibles se arreglan.
>
> Es la misma idea que atraviesa todo el material, del backend y del frontend: **las
> reglas que dependen de que alguien se acuerde fallan; las que hacen que
> equivocarse sea imposible, no.** Acá ni siquiera hay una regla que recordar — el
> sistema directamente no te deja.

---

## 3.9. Tareas en segundo plano

EA-07 prohíbe algo que parece la solución natural:

> Las tareas en segundo plano de una petición **no se lanzan con
> `asyncio.create_task()`**. Se encolan en taskiq o, si deben ocurrir sin falta, se
> escriben en el outbox. **Una tarea que no se puede repetir sin daño es un defecto.**

El razonamiento es directo cuando se ve el caso. Alguien confirma un pedido y hay
que mandar un correo. El correo tarda, así que la tentación es lanzarlo suelto y
responder de inmediato:

```python
asyncio.create_task(enviar_correo(pedido))   # prohibido por EA-07
return respuesta
```

Eso responde rápido y tiene tres problemas, cada uno peor que el anterior.

**Si el proceso se reinicia, la tarea desaparece.** Vive en la memoria de ese
proceso; un despliegue o una caída se la lleva, y nadie se entera de que ese correo
nunca salió.

**Si falla, el error no llega a ningún lado.** Nadie está esperando ese resultado, y
una excepción en una tarea suelta que nadie observa se descarta con una advertencia
en el registro, si es que se descarta con algo.

**No hay reintento.** No existe nada que sepa que esa tarea existió.

La alternativa que el TPI declara —encolar en la cola de tareas, o escribir en el
outbox si el hecho no se puede perder— resuelve las tres: **el trabajo vive fuera del
proceso**, alguien lo va a buscar, y si falla se reintenta. La clase 8 lo desarrolla,
junto con las siete reglas del trabajo diferido.

Nótese la última frase de la regla, que enuncia un principio más general: **una tarea
que no se puede repetir sin daño es un defecto.** Como el sistema va a reintentar, la
tarea tiene que tolerar ejecutarse dos veces. Eso es TB-02, y es la razón por la que
el planificador del TPI corre en exactamente una instancia.

> **📌 NOTA**
> Esa frase del TPI merece leerse dos veces porque invierte la carga de la prueba:
>
> **"Una tarea que no se puede repetir sin daño es un defecto."**
>
> No dice "cuidado con reintentar". Dice que **si tu tarea se rompe al ejecutarse dos
> veces, el problema es tu tarea**, no el reintento.
>
> Y hay una razón dura detrás: **ningún sistema de colas garantiza que algo se
> ejecute exactamente una vez.** Puede garantizar al menos una, que es lo que hacen
> casi todos, o como mucho una. "Exactamente una" es, en un sistema distribuido, un
> problema sin solución general.
>
> Entonces el reintento no es una decisión que podés evitar: **va a pasar**, porque
> un worker puede morir después de hacer el trabajo y antes de confirmar el mensaje.
> Lo único que podés decidir es si tu tarea lo tolera.
>
> Del otro lado del cable pasa exactamente lo mismo y tus compañeros lo van a ver:
> el checkout genera una clave de idempotencia justamente porque **la red tampoco
> garantiza que algo llegue exactamente una vez.**

---

## 3.10. Recursos y ciclo de vida

EA-08 cierra el conjunto:

> El pool de conexiones y el cliente de Redis se crean en el **lifespan** de la
> aplicación y se cierran ahí. **No se crean por petición ni a nivel de módulo.** La
> suite de tests dispara el lifespan con `asgi-lifespan`.

Las dos prohibiciones responden a problemas distintos.

**No por petición**, porque establecer una conexión es caro y un pool existe
justamente para evitarlo. Crear uno por petición es tener un pool de uno.

**No a nivel de módulo**, y esta es la que produce errores desconcertantes. Un
cliente creado como variable global **se construye al importar el archivo**, que es
un momento en el que puede no haber un bucle de eventos corriendo. El síntoma
clásico es que el servidor levanta bien y **los tests fallan**, o al revés, con
mensajes sobre bucles distintos que no señalan la causa.

Y la última frase explica una dependencia del stack que de otro modo parece
arbitraria: como esos recursos se crean en el ciclo de vida, **la suite de tests
tiene que dispararlo**, y para eso el TPI declara una herramienta específica.

> **💡 PARA ENTENDER**
> Fijate la cadena completa, porque muestra cómo una decisión arrastra a otra hasta
> llegar a una línea del archivo de dependencias:
>
> **EA-08** dice que el pool va en el ciclo de vida →
> los tests necesitan ese pool →
> entonces **los tests tienen que disparar el ciclo de vida** →
> y para eso hace falta una herramienta específica →
> **por eso está `asgi-lifespan` en el stack.**
>
> Si mirás la lista de diecinueve tecnologías del TPI, `asgi-lifespan` parece la más
> arbitraria de todas. No lo es: **está ahí porque EA-08 la hace necesaria.**
>
> Y esto vale como método de lectura para todo el documento: cuando algo del stack
> te parezca raro, buscá qué regla lo obliga. Casi siempre hay una.

---

## 3.11. Lo que la sincronía hacía bien

Esta sección rara vez se enseña, y el TPI la declara. Es la contracara del modelo
asincrónico, y saberla es lo que separa usarlo de padecerlo.

> En un modelo síncrono, el grupo de hilos del marco de trabajo **pone un techo
> natural** a la cantidad de operaciones concurrentes contra la base. Con corrutinas
> ese techo **desaparece** —se pueden tener diez mil tareas esperando— y el recurso
> que se agota primero pasa a ser **el pool de conexiones**, con un error mucho menos
> legible.

Conviene desarmarlo, porque es un intercambio real y no una advertencia menor.

Con hilos, la cantidad de operaciones simultáneas contra la base **está limitada por
la cantidad de hilos**. Si hay veinte, no puede haber veintiuna consultas a la vez.
Ese techo nadie lo puso a propósito: es una consecuencia del modelo, y protege sin
que nadie lo decida.

Con corrutinas, crear una tarea es tan barato que **puede haber diez mil esperando a
la vez**. El techo desapareció. Y el primer recurso que se agota es el pool de
conexiones, con un error de espera agotada que no dice "hay demasiada concurrencia"
sino algo mucho más opaco.

*(Ver Figura 3.5: el techo que desaparece.)*

Por eso el TPI cierra la sección con dos decisiones de configuración que ahora se
entienden:

> La sección 16.1 fija `DB_POOL_SIZE` **contra la concurrencia esperada y no contra
> la cantidad de workers**, y **el timeout de adquisición del pool es una variable
> declarada y no un valor por defecto.**

La primera dice que el tamaño del pool ya no se calcula como antes. La segunda es más
sutil: **dejar el plazo de espera en su valor por defecto significa aceptar el que
venga**, y cuando ese plazo se agota el sistema tiene que hacer algo previsto en
lugar de fallar de la forma que le toque.

> **📌 NOTA**
> Guardá esta sección, porque es la respuesta honesta a "¿asincrónico es mejor?".
>
> **No es mejor: es distinto, y el intercambio está declarado.**
>
> Ganás que un servidor atienda miles de conexiones sin gastar un hilo en cada una.
> Perdés un techo que te venía de regalo y que ahora tenés que poner vos.
>
> Y fijate el detalle más importante: **el sistema no te avisa que perdiste ese
> techo.** Anda perfecto hasta que un día hay suficiente carga, y ahí falla con un
> error de pool agotado que no dice nada sobre la causa real.
>
> Por eso el TPI declara esas dos variables en vez de dejarlas en su valor por
> defecto. **Cuando algo deja de estar garantizado por el modelo, hay que
> garantizarlo explícitamente** — o aceptar que un día te va a sorprender.

---

## 3.12. Herramientas de diagnóstico

**El modo de depuración de asyncio** es la herramienta más útil y la que menos se
usa. Activándolo, el bucle **avisa cuando una corrutina tardó demasiado sin ceder**,
indicando cuál fue y cuánto tardó. Eso convierte el problema de la sección 3.6 —que
es invisible— en un mensaje concreto. También advierte sobre corrutinas que nunca se
esperaron, que es el error de la sección 3.5.

**La traza de una excepción de greenlet** hay que aprender a leerla, porque su
mensaje no menciona la causa. Lo que aparece es una operación de entrada y salida
que se intentó fuera de contexto; **la causa real está en el acceso a un atributo,
unas líneas más arriba**, o en el repositorio que no declaró la precarga, que puede
estar en otro archivo. El procedimiento es: ubicar qué relación se estaba leyendo,
buscar la consulta que trajo ese objeto, y verificar si declaró su precarga.

**El registro de consultas del ORM** muestra cada sentencia emitida. Es la forma de
verificar que una consulta con precarga emite dos y no ciento una, y también de
descubrir consultas que nadie esperaba.

**La cantidad de conexiones en uso del pool** es lo que hay que mirar cuando aparecen
errores de espera agotada. Si el pool está lleno de forma sostenida, el problema es
el de la sección 3.11 y no una consulta lenta.

> **🧪 EXPERIMENTO**
> Este experimento hace visible en treinta segundos lo que este capítulo explica en
> veinte páginas. Hacelo sí o sí.
>
> 1. Escribí dos endpoints: uno que haga `await asyncio.sleep(5)` y otro que responda
>    de inmediato.
> 2. Abrí dos pestañas. Pedí el lento en una y el rápido en la otra.
>    **El rápido responde al instante**, aunque el lento siga esperando.
> 3. Ahora cambiá el primero por `time.sleep(5)` —sin `await`— y repetí.
>
> **El rápido no responde hasta que el lento termina.** Y no es que esté encolado
> detrás: el proceso entero está detenido.
>
> 4. Abrí cinco pestañas más y pedí cualquier endpoint. Ninguno contesta.
> 5. Probá también `/docs`. Tampoco.
>
> Una línea. Un solo carácter de diferencia entre `time.sleep` y `await
> asyncio.sleep`. **Y el servidor entero deja de existir durante cinco segundos.**
>
> Eso es lo que EA-01, EA-02 y EA-06 previenen, y por eso son tres reglas y no una
> recomendación.

---

## 3.13. Seguridad y evolución

Tres consideraciones cierran el capítulo.

**Una operación bloqueante es una denegación de servicio sin atacante.** No hace
falta mala intención: alcanza con un endpoint que procese un archivo subido por el
usuario de forma sincrónica. Quien quiera tirar el servicio sólo tiene que llamar a
ese endpoint unas cuantas veces, y el costo del ataque es ridículamente bajo
comparado con el daño.

**El plazo de espera es parte de la defensa.** Una llamada saliente sin plazo puede
quedar pendiente indefinidamente, ocupando una conexión del pool. Con suficientes
llamadas en ese estado, el pool se agota y el sistema deja de responder sin que
nadie haya hecho nada malo.

**Una tarea que falla en silencio es un problema de auditoría.** Si una operación que
debía ocurrir no ocurrió y nadie se enteró, el sistema quedó en un estado que sus
registros no reflejan. Es una de las razones de EA-07 y del patrón que la clase 8
estudia.

Sobre la evolución, dos observaciones. La primera es que **el bloqueo global del
intérprete está siendo revisado**: existe una modalidad experimental sin él desde
Python 3.13. Eso no cambia nada de este capítulo, porque **el modelo asincrónico no
se eligió por el bloqueo** sino por lo que estableció el Capítulo 1: un servidor pasa
su tiempo esperando, y esperar no necesita un hilo por espera.

La segunda es que la comunidad viene reduciendo la cantidad de operaciones
bloqueantes disponibles: cada vez más bibliotecas ofrecen variante asincrónica, y
las herramientas de análisis estático detectan llamadas sincrónicas dentro de
corrutinas. **Lo que hoy exige disciplina, mañana lo va a marcar una herramienta** —y
esa es siempre la evolución deseable de una regla.

---

## 3.14. Verificación

1. Reproducir el experimento de la sección 3.12 y **documentar la diferencia** entre
   las dos versiones.
2. Explicar por qué un handler `def` con código sincrónico es **menos grave** que uno
   `async def` con una línea sincrónica adentro.
3. Escribir una operación bloqueante y sacarla a un hilo, verificando que el bucle
   sigue atendiendo.
4. Enumerar las tres operaciones bloqueantes que el TPI declara y **justificar por
   qué cada una lo es**.
5. Buscar en un proyecto propio importaciones de clientes sincrónicos y **listar las
   violaciones de EA-03**.
6. Provocar una excepción de greenlet por relación no precargada, y **corregirla**.
7. Provocar la misma excepción por objeto expirado tras el commit, y corregirla con
   la opción que EA-04 declara.
8. Escribir dos consultas independientes con dos `await` seguidos y con un grupo de
   tareas, y **medir la diferencia**.
9. Explicar qué techo desaparece al pasar de hilos a corrutinas, y qué hay que
   configurar para reponerlo.

---

## 3.15. Errores frecuentes

**Declarar un handler `async def` y llamar adentro a una función sincrónica.** Es la
mezcla que EA-01 declara peor que la sincronía completa: detiene el proceso entero
(sección 3.6).

**Usar un cliente sincrónico "porque es el que sale en los ejemplos".** Viola EA-03,
y en desarrollo no se nota (sección 3.7).

**Usar `time.sleep` en lugar de su equivalente asincrónico.** Bloquea el bucle
durante todo ese tiempo (sección 3.7).

**Encadenar `await` de operaciones independientes.** No falla: tarda el doble sin
motivo (sección 3.5).

**Llamar a una corrutina sin `await` y suponer que se ejecutó.** No se ejecuta:
devuelve un objeto (sección 3.5).

**Leer una relación que no se precargó.** Excepción de greenlet, con una traza que no
menciona la causa (sección 3.8).

**Dejar `expire_on_commit` en su valor por defecto.** El objeto queda expirado tras el
commit y la primera lectura falla. Viola EA-04 (sección 3.8.2).

**Lanzar trabajo en segundo plano con una tarea suelta.** Se pierde al reiniciar, el
error no llega a nadie y no hay reintento. Viola EA-07 (sección 3.9).

**Crear el pool o el cliente de Redis a nivel de módulo.** Se construyen al importar,
cuando puede no haber bucle. Viola EA-08 (sección 3.10).

**Calcular el tamaño del pool contra la cantidad de workers.** Con corrutinas el techo
lo pone la concurrencia esperada, no los procesos (sección 3.11).

**Omitir el plazo de espera en una llamada saliente.** Una llamada colgada ocupa una
conexión del pool indefinidamente (sección 3.13).

---

## 3.16. Actividades

1. **El bloqueo medido.** Implementar tres endpoints —uno correcto, uno con handler
   sincrónico y uno `async` con línea bloqueante— y medir con veinte peticiones
   simultáneas cuánto tarda cada configuración en responderlas todas. Explicar los
   tres resultados con la tabla de la sección 3.6.

2. **Las ocho reglas auditadas.** Tomar un proyecto de ejemplo con FastAPI y revisar
   una por una las ocho reglas EA, documentando para cada una si se cumple, cómo se
   verificó, y qué habría que cambiar si no.

3. **La excepción de greenlet, las dos veces.** Provocar la excepción por sus dos
   causas —relación no precargada y objeto expirado—, capturar ambas trazas, y
   documentar **qué parte de cada traza señala la causa real** y cuál despista.

4. **El N+1 que no puede existir.** Escribir un endpoint que liste pedidos con su
   usuario sin declarar la precarga y documentar qué ocurre. Corregirlo con
   `selectinload` y **contar las consultas emitidas** en ambos casos con el registro
   del ORM. Relacionar con la afirmación de la sección 3.8.3.

5. **Serie contra concurrencia.** Implementar un endpoint que necesite cuatro
   consultas independientes, resolverlo de las dos formas, y medir. Justificar en qué
   casos la versión secuencial sería la correcta.

6. **Exploración: el techo que desaparece.** Configurar un pool de cinco conexiones y
   lanzar cincuenta peticiones concurrentes contra un endpoint que consulte la base.
   Documentar qué error aparece, en qué momento, y qué dice exactamente su mensaje.
   Relacionar lo observado con la sección 3.11 y proponer los dos valores de
   configuración que el TPI declara. *(Requiere una base de datos en ejecución.)*

7. **Exploración: los dos lados del mismo bucle.** Junto con alguien del turno de
   frontend, comparar el modelo de ejecución de los dos lados: qué es una corrutina
   acá y una promesa allá, qué cede el control en cada caso, y qué pasa cuando algo
   bloquea. Armar **un solo diagrama que sirva para los dos** y documentar en qué se
   diferencian. *(Requiere coordinar con la otra mitad de la cursada.)*

---

## 3.17. Síntesis

1. La sección 1.4 del TPI es **normativa y todo el resto del documento la
   presupone**. Sus ocho reglas no están repartidas: están juntas porque responden a
   un mismo hecho.

2. La concurrencia asincrónica es **cooperativa**: nadie interrumpe a una corrutina,
   **ella cede**. De ahí se deduce todo lo demás, incluida la gravedad de una línea
   bloqueante.

3. **Concurrencia no es paralelismo.** Un solo hilo alternando es concurrente y no
   paralelo, y para un servidor eso alcanza porque el trabajo dominante es esperar.

4. Los puntos de cesión **son visibles**: cada `await` es un lugar donde el control
   puede irse. Eso permite razonar sobre qué puede pasar entre dos líneas.

5. Una corrutina **no hace nada hasta que se la agenda**, al revés de lo que ocurre
   del otro lado del cable, donde una promesa arranca al crearse.

6. **Un handler `async` con una línea bloqueante es peor que un handler sincrónico
   completo**: el segundo bloquea un hilo de un grupo, el primero detiene el proceso
   entero.

7. El TPI enumera **tres operaciones bloqueantes** y les da una única solución:
   sacarlas a un hilo. Y pone un umbral concreto: **un milisegundo** de trabajo de
   procesador sin ceder.

8. SQLAlchemy ejecuta su ORM sincrónico **dentro de un greenlet** y salta al bucle
   cuando necesita entrada y salida. Cuando el ORM intenta consultar desde un lugar
   sin `await`, **no hay a dónde saltar**.

9. **El N+1 dejó de ser un problema de rendimiento y pasó a ser un error de
   ejecución.** Eso no es un castigo: es que un problema silencioso se volvió
   visible, y los problemas visibles se arreglan.

10. Una **tarea suelta** se pierde al reiniciar, falla en silencio y no se reintenta.
    Y una tarea que no se puede repetir sin daño **es un defecto**.

11. **El modelo asincrónico no es gratis.** El grupo de hilos ponía un techo que
    ahora desapareció, y el primer recurso que se agota es el pool de conexiones.
    Cuando algo deja de estar garantizado por el modelo, hay que garantizarlo
    explícitamente.

---

## 3.18. Referencias y lecturas complementarias

Las fuentes normativas de este capítulo son las propuestas de mejora del lenguaje,
todas en `peps.python.org`. El **PEP 342** (2005) convirtió los generadores en
corrutinas bidireccionales y el **PEP 380** (2009) agregó la delegación; los dos
explican por qué la sintaxis previa a `async`/`await` era como era. El **PEP 3156**
(2012) incorporó `asyncio` a la biblioteca estándar, y su sección de fundamentos
discute las alternativas que se descartaron. El **PEP 492** (2015) agregó `async` y
`await` como palabras del lenguaje, y su motivación enuncia con claridad el problema
que resolvía: que una corrutina y un generador fueran indistinguibles. El **PEP 654**
(2021) introdujo los grupos de excepciones y la sintaxis `except*`, sin los cuales
los grupos de tareas de la sección 3.5 no podrían propagar varios errores a la vez;
es la razón directa del piso de versión que el TPI fija. Y el **PEP 703** documenta
la modalidad experimental sin bloqueo global mencionada en la sección 3.13.

Para la implementación, la documentación de **asyncio** en la referencia de Python
cubre el bucle de eventos, las tareas y el modo de depuración de la sección 3.12. La
documentación de **AnyIO** explica la ejecución en hilos que EA-02 exige y su
relación con la biblioteca estándar. Y la sección de **SQLAlchemy** sobre extensión
asincrónica es la fuente directa de la sección 3.8: documenta el mecanismo de
greenlet, enumera las operaciones que no pueden ocurrir fuera de él, y explica por
qué la carga perezosa es incompatible con ese modelo.

Como bibliografía de estudio, Ramalho, *Fluent Python* (2.ª edición, O'Reilly, 2022)
dedica tres capítulos al modelo asincrónico y es la mejor explicación disponible para
quien ya programa; su tratamiento de la diferencia entre concurrencia y paralelismo
es más claro que el de la documentación oficial. Para el contexto histórico, la
charla de David Beazley *Generators: The Final Frontier* (PyCon 2014) muestra cómo se
construía código asincrónico con generadores antes de que existiera la sintaxis
propia, y su lectura hace evidente qué resolvió el PEP 492. Y sobre el problema
general de la concurrencia cooperativa, el artículo de Nathaniel J. Smith *Notes on
structured concurrency* (2018) es el texto que introdujo las ideas que después
llegaron al lenguaje como grupos de tareas.

Del TPI, este capítulo se apoya casi enteramente en la sección **1.4**, que conviene
leer completa y tener a mano durante todo el módulo. Se anticipan además la **5.5**
—bcrypt fuera del bucle y su semáforo—, la **8.3** con la tabla de precarga que EA-05
exige, y la **16.1** con las dos variables de configuración que la sección 3.11
justifica.

---

**Continúa en:** Capítulo 4 — Persistencia: SQLModel, PostgreSQL y el modelo de
datos, donde las reglas EA-04 y EA-05 dejan de ser advertencias y pasan a ser líneas
de código concretas, y donde las asociaciones y composiciones de las actividades 5 y
6 de POO se convierten en tablas, claves foráneas e índices.
