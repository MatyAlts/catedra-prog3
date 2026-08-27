# Capítulo 1 — Del objeto al servicio: HTTP del lado del servidor

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 1.1. Alcance de la clase

Este capítulo abre el módulo de backend, y lo hace desde un lugar poco habitual:
**no empieza de cero.** Las ocho actividades de programación orientada a objetos en
Python que preceden a esta clase no fueron un requisito administrativo ni un
repaso. Fueron la construcción del vocabulario con el que se describe la
arquitectura de un servidor, y este capítulo lo va a usar desde la primera página.

Conviene decirlo con precisión, porque cambia cómo se lee lo que sigue. En la
octava actividad se estudió la diferencia entre **dependencia de uso y dependencia
de creación**: una clase que construye adentro suyo lo que necesita queda atada a
esa construcción, y una que lo recibe puede ser reconfigurada y probada. Eso, que
ahí era un principio de diseño, acá tiene un nombre concreto en el marco de trabajo
que el TPI declara —se llama `Depends()`— y una regla explícita en la sección 2.1
del propio TPI:

> El Router importa el tipo `UnitOfWork` **únicamente para anotar la dependencia**
> que resuelve con `Depends(get_uow)`, y lo transporta hacia el Service: **no lo
> construye**, no abre su contexto, no invoca ninguno de sus métodos y no conoce
> los repositorios que expone.

Esa frase es la actividad 8, escrita como requisito de un sistema real.

El capítulo tiene tres objetivos. El primero es **entender qué hace un servidor
web**: qué recibe, qué devuelve y por qué atender a muchas personas a la vez es un
problema difícil que tuvo tres respuestas históricas distintas. El segundo es
**construir el primer endpoint** y entender cada pieza de lo que se escribió. El
tercero, y el más importante para el resto del módulo, es **ubicar cada archivo en
su capa**: el TPI declara un flujo de dependencias estricto, y quien no lo tiene
claro desde la primera clase va a escribir código que funciona y que hay que
reescribir.

Hay además una coincidencia que conviene aprovechar. Este módulo se dicta en
paralelo con el de frontend, y **esta misma semana esa mitad de la cursada estudia
la anatomía de una petición HTTP desde el navegador**. Lo que allá es una tabla de
la sección 6 del TPI —método, ruta, cuerpo, respuesta— acá es el código que la
responde. Es la misma petición vista desde los dos extremos del cable, el mismo
día.

Al finalizar la clase, el alumno debe poder levantar un servicio con varios
endpoints, explicar qué resuelve `Depends()` y **ubicar cualquier archivo del
backend del TPI en su capa**, justificando qué puede importar y qué no.

**Contenidos**

1. Origen y objetivos de diseño de la concurrencia en servidores.
2. De WSGI a ASGI: por qué Python necesitó un contrato nuevo.
3. Anatomía de una aplicación ASGI.
4. El primer endpoint y por qué siempre es asincrónico.
5. Parámetros de ruta, de consulta y de cuerpo.
6. La documentación que no se desactualiza.
7. Inyección de dependencias: la actividad 8 con otro nombre.
8. Dependencias con recursos y ciclo de vida.
9. Las capas del backend y la regla de dependencias.
10. Por qué Redis no es una capa sino un adaptador.
11. Los ocho servicios del sistema.
12. Los doce módulos y la organización por funcionalidad.
13. Herramientas de diagnóstico.

---

## 1.2. Por qué atender a muchos es difícil: origen y diseño

Un servidor web tiene un problema que un programa de escritorio no tiene: **debe
atender a muchas personas simultáneamente, y la mayor parte del tiempo no está
haciendo nada.** Está esperando. Espera que llegue una petición, espera que la base
de datos responda, espera que el cliente termine de recibir los bytes.

Ese detalle —que el trabajo dominante sea esperar y no calcular— es el que explica
las tres respuestas históricas al problema, y por qué la tercera ganó.

**Primera respuesta: un proceso por petición.** La interfaz de pasarela común, de
1993, funcionaba así: el servidor recibía una petición, **creaba un proceso nuevo**
para atenderla, y ese proceso moría al terminar. Era simple y robusto —un fallo no
afectaba a nadie más— y era carísimo. Crear un proceso implica reservar memoria,
copiar el espacio de direcciones y hacer que el sistema operativo lo planifique.
Con decenas de peticiones por segundo, el servidor pasaba más tiempo creando
procesos que atendiendo.

**Segunda respuesta: un hilo por conexión.** Un hilo es mucho más barato que un
proceso: comparte memoria y se crea rápido. Fue el modelo dominante durante años y
sigue funcionando bien hasta cierta escala. Pero tiene dos costos que aparecen al
crecer. Cada hilo reserva su propia pila —del orden de un megabyte—, así que diez
mil conexiones simultáneas son diez gigabytes sólo en pilas. Y el sistema operativo
debe **alternar** entre esos hilos, guardando y restaurando estado cada vez, con un
costo que crece con la cantidad.

Ese límite tuvo nombre propio. En 1999, Dan Kegel publicó un artículo titulado **el
problema C10K**, planteando algo que entonces parecía ambicioso: cómo atender diez
mil conexiones simultáneas en una sola máquina. Su respuesta fue que el modelo de
un hilo por conexión no escalaba, y que hacía falta otra cosa.

**Tercera respuesta: un solo hilo que multiplexa.** La idea es directa: si el
trabajo dominante es esperar, **un solo hilo puede esperar muchas cosas a la vez**.
El sistema operativo ofrece mecanismos para preguntar "de todas estas conexiones,
¿cuál tiene datos listos?" —`select` primero, después `poll`, y finalmente `epoll`
en Linux y `kqueue` en BSD, que resolvieron el problema de escala—. El programa
mantiene un **bucle de eventos**: pregunta qué está listo, atiende eso, vuelve a
preguntar.

Ese modelo tiene una consecuencia que este módulo va a repetir hasta el cansancio,
porque es la fuente de casi todos los errores de un backend asincrónico mal
escrito: **si el hilo se queda haciendo algo que no cede el control, nadie más es
atendido.** No se demora una petición: se demoran todas.

Hay un motivo adicional por el que este modelo encaja especialmente bien con
Python. El intérprete tiene un bloqueo global que impide que dos hilos ejecuten
instrucciones de Python al mismo tiempo. Para trabajo de procesador eso es una
limitación real. **Para trabajo de espera no lo es en absoluto**, porque el bloqueo
se libera mientras se espera. Un servidor web hace, sobre todo, trabajo de espera:
el modelo asincrónico aprovecha exactamente lo que Python puede ofrecer.

De ese recorrido salen las cuatro decisiones de diseño que gobiernan este capítulo
y buena parte del módulo.

**Primera: un solo hilo multiplexando espera.** Es la base del modelo asincrónico,
y su contracara es que nada puede bloquear.

**Segunda: el contrato es código, no un documento aparte.** El marco de trabajo que
el TPI declara genera la especificación de la API a partir de las anotaciones de
tipo del propio código. Una especificación que se escribe aparte se desactualiza;
una que se deriva del código, no puede.

**Tercera: las dependencias se declaran, no se construyen.** Es la actividad 8
convertida en mecanismo del marco de trabajo.

**Cuarta: las capas tienen una dirección.** El TPI la declara explícitamente, y el
resto del módulo la va a respetar sin excepción.

> **💡 PARA ENTENDER**
> Antes de seguir, fijate en una cosa que va a volver todo el módulo:
>
> **Un servidor web pasa casi todo su tiempo esperando, no calculando.**
>
> Esperando que llegue una petición. Esperando que Postgres devuelva las filas.
> Esperando que Redis conteste. Esperando que el cliente termine de recibir.
>
> Si te acordás de eso, el resto se deduce solo. ¿Por qué asincrónico y no hilos?
> Porque esperar no necesita un hilo entero para cada espera. ¿Por qué el GIL de
> Python no molesta acá? Porque se libera justo mientras esperás. ¿Por qué bcrypt es
> un problema (sección 5.5 del TPI)? Porque bcrypt **no espera: calcula**, y es la
> excepción a todo lo anterior.
>
> Todo el modelo asincrónico se apoya en esa suposición. **Donde la suposición no
> vale, el modelo se rompe** — y por eso el TPI dedica una sección entera a esos
> casos.

---

## 1.3. De WSGI a ASGI

Python necesitó definir cómo se hablan un servidor y una aplicación, porque de lo
contrario cada marco de trabajo funcionaría sólo con su propio servidor.

La primera respuesta fue **WSGI**, normado en 2003 y revisado en 2010. Su contrato
es de una simplicidad notable: una aplicación es **un objeto invocable** que recibe
un diccionario con el entorno de la petición y una función para empezar la
respuesta, y devuelve un iterable de bytes.

Esa simplicidad tiene un límite estructural, y no es un descuido sino una
consecuencia inevitable de su forma: **el contrato es sincrónico.** La aplicación
se llama, hace su trabajo, y devuelve. Mientras tanto, quien la llamó está
bloqueado. No hay ningún lugar en ese contrato donde una aplicación pueda decir
"esto va a tardar, seguí atendiendo a otro y volvé después".

Además, WSGI modela **una petición y una respuesta**. No tiene forma de expresar
una conexión que permanece abierta e intercambia mensajes: no puede describir
WebSockets ni el flujo de eventos que el TPI usa en su sección 11.

**ASGI** apareció alrededor de 2016, impulsado por Andrew Godwin en el contexto de
Django Channels, y resolvió las dos cosas con un contrato distinto: una aplicación
es **una corrutina** que recibe tres cosas —el ámbito de la conexión, una función
para recibir mensajes y una función para enviarlos—.

| Aspecto | WSGI (2003) | ASGI (2016) |
| --- | --- | --- |
| La aplicación es | Un invocable común | **Una corrutina** |
| Modelo | Una petición, una respuesta | Un flujo de mensajes |
| Conexiones largas | No las contempla | WebSockets y eventos del servidor |
| Concurrencia | Del servidor: procesos o hilos | **De la aplicación: bucle de eventos** |

La última fila es la que más consecuencias tiene. Con WSGI, **la concurrencia era
problema del servidor**: la aplicación se escribía como si atendiera a uno solo y
el servidor la corría en varios hilos. Con ASGI, la concurrencia pasa a ser
**problema de la aplicación**, que puede hacerlo mucho mejor y también puede
arruinarlo con una sola línea bloqueante.

De ahí sale la primera regla de ejecución asincrónica del TPI, que este módulo va a
fundar en detalle en la clase 3 y que conviene enunciar desde ahora:

> **EA-01.** Todos los handlers de FastAPI se declaran con `async def`; no hay
> ningún handler con `def`.

> **📌 NOTA**
> Una aclaración que evita una confusión muy común: **ASGI no reemplazó a WSGI, y
> WSGI no está "viejo".**
>
> Si estás escribiendo un sistema donde cada petición hace una consulta y devuelve,
> con tráfico moderado, WSGI y un puñado de hilos anda perfecto y es más simple de
> razonar. Muchísimos sistemas en producción funcionan así hoy y están bien.
>
> ASGI resuelve **dos cosas que WSGI no puede expresar**: conexiones que quedan
> abiertas intercambiando mensajes, y concurrencia manejada por la aplicación.
>
> El TPI necesita las dos. Necesita el flujo de eventos de la sección 11 —que es una
> conexión abierta durante minutos— y necesita atender muchas de esas conexiones a
> la vez sin gastar un hilo en cada una.
>
> O sea: **el TPI no eligió ASGI porque sea lo nuevo. Lo eligió porque lo que pide
> no se puede hacer con lo otro.** Esa es siempre la pregunta correcta.

---

## 1.4. Anatomía de una aplicación ASGI

Antes de usar el marco de trabajo conviene ver qué hay debajo, porque después todo
lo demás se entiende como comodidad y no como magia. Esta es una aplicación ASGI
completa, sin ninguna dependencia:

```python
async def app(scope, receive, send):
    assert scope["type"] == "http"
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"application/json")],
    })
    await send({
        "type": "http.response.body",
        "body": b'{"estado": "ok"}',
    })
```

Cada pieza tiene su papel:

| Parte | Qué es | Contiene |
| --- | --- | --- |
| `scope` | El contexto de la conexión | Tipo, método, ruta, encabezados, cliente |
| `receive` | Corrutina para **recibir** | Los mensajes del cliente, como el cuerpo |
| `send` | Corrutina para **enviar** | Los mensajes hacia el cliente |
| `http.response.start` | Primer mensaje de respuesta | Código de estado y encabezados |
| `http.response.body` | Segundo mensaje | El cuerpo, que puede venir en varios |

Nótese que la respuesta se envía en **dos mensajes separados**. Esa separación es
la que hace posible el flujo de eventos de la sección 11 del TPI: se envía el
primer mensaje con los encabezados, y después se van enviando cuerpos a medida que
haya algo para mandar, sin cerrar la conexión.

También conviene observar que **la función es una corrutina y los envíos llevan
`await`**. No es decorativo: cada `await` es un punto donde el hilo puede irse a
atender otra conexión. Un servidor ASGI que ejecuta cien de estas aplicaciones a la
vez lo hace **en un solo hilo**, alternando en esos puntos.

*(Ver Figura 1.1: del proceso por petición al bucle de eventos.)*

Escribir aplicaciones así sería insostenible: habría que parsear rutas a mano,
validar cuerpos, serializar respuestas. Sobre ese contrato se construyeron
herramientas, y el TPI declara una de ellas, publicada en 2018 y construida a su
vez sobre una capa ASGI de bajo nivel y sobre una biblioteca de validación por
anotaciones de tipo. La combinación es lo que permite la segunda decisión de diseño
de la sección 1.2: **el contrato es código**.

---

## 1.5. El primer endpoint

```python
from fastapi import FastAPI

app = FastAPI(title="Food Store API", version="1.0.0")

@app.get("/health/live")
async def salud_del_proceso() -> dict[str, str]:
    return {"estado": "vivo"}
```

Tres líneas de contenido, y cada una merece explicación.

**El decorador** declara método y ruta. Es lo que reemplaza el parseo manual de
`scope["path"]` y `scope["method"]` de la sección anterior.

**`async def`** no es opcional en este proyecto: es EA-01. Y conviene entender por
qué la regla existe, porque el marco de trabajo **admite** handlers sincrónicos: si
se declara uno con `def`, lo ejecuta en un hilo aparte para no bloquear el bucle.
Eso parece una comodidad y es una trampa, y el TPI lo dice sin vueltas al declarar
EA-01: la mezcla —un handler asincrónico que adentro llama a una función
bloqueante— **es peor** que cualquiera de las dos formas puras, porque tiene la
apariencia de lo correcto y el comportamiento de lo incorrecto.

**La anotación de retorno** no es documentación. El marco de trabajo la usa para
serializar la respuesta y para generar la especificación de la sección 1.7. Un tipo
mal declarado produce una especificación que miente, y el frontend —que esta misma
semana está aprendiendo a leer esa especificación— va a escribir su cliente contra
la mentira.

> **⚠️ OJO ACÁ**
> Sobre EA-01 hay algo que te va a tentar y quiero que sepas por qué no.
>
> El marco de trabajo **te deja** escribir un handler con `def` común. Y no falla:
> lo detecta y lo manda a un hilo aparte para no bloquear el bucle. Funciona.
>
> Entonces, ¿por qué el TPI lo prohíbe? Por lo que pasa **en el medio**:
>
> ```python
> @app.get("/productos")
> async def listar():                    # asincrónico...
>     datos = requests.get(URL)          # ...y adentro, una llamada BLOQUEANTE
>     return datos.json()
> ```
>
> Ese código no lo manda a ningún hilo. Es `async`, así que el marco confía en que
> vos sabés lo que hacés, y esa línea **congela el bucle de eventos entero** el
> tiempo que tarde la respuesta. Todos los demás usuarios esperan.
>
> Por eso el TPI dice que **la mezcla es peor que cualquiera de las dos formas
> puras**: un handler sincrónico completo al menos va a un hilo. Uno asincrónico con
> una línea bloqueante adentro tiene la pinta de estar bien y el comportamiento de
> estar mal.
>
> La clase 3 le dedica el capítulo entero a esto.

Los parámetros se declaran como parámetros de la función, y el marco de trabajo
deduce de dónde sacarlos:

```python
@app.get("/productos/{producto_id}")
async def obtener_producto(
    producto_id: int,                    # de la ruta: aparece en el path
    incluir_ingredientes: bool = False,  # de la consulta: no aparece en el path
) -> ProductoResponse:
    ...
```

La regla es simple y vale la pena tenerla clara: **si el nombre del parámetro
aparece en la ruta declarada, viene de la ruta; si no, viene de la cadena de
consulta.** Y en los dos casos **el tipo se valida**: pedir `/productos/abc` con
`producto_id: int` devuelve un `422` sin que nadie escriba una línea de validación.

*(Ver Figura 1.2: el recorrido de una petición del lado del servidor.)*

> **📌 NOTA**
> Fijate en lo que acaba de pasar, porque es la idea central del marco de trabajo y
> conviene que la veas ahora y no dentro de tres clases:
>
> **Las anotaciones de tipo dejaron de ser documentación y pasaron a ser
> comportamiento.**
>
> En las actividades de POO, un `def sumar(a: int, b: int) -> int` era una ayuda
> para vos y para el editor. Python no verificaba nada: le pasabas dos strings y se
> las arreglaba como podía.
>
> Acá el mismo `producto_id: int` hace tres cosas reales: **valida** la entrada,
> **convierte** el texto de la URL a entero, y **documenta** el endpoint en la
> especificación. Un solo lugar, tres efectos.
>
> Y ojo con la contracara, que es de las que más tiempo hacen perder: **si el tipo
> está mal, las tres cosas están mal a la vez.** Declarás `total: float` en vez de
> `Decimal` y no sólo guardás mal el número — también le decís al frontend, en la
> especificación, que espere un número. Y el frontend te va a creer.

---

## 1.6. Cuerpo de la petición

Para lo que viaja en el cuerpo, el parámetro se declara con un modelo:

```python
from pydantic import BaseModel, Field

class ProductoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    precio: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    categoria_id: int

@app.post("/productos", status_code=201)
async def crear_producto(datos: ProductoCreate) -> ProductoResponse:
    ...
```

El marco de trabajo lee el cuerpo, lo parsea, **lo valida contra el modelo**, y si
algo no cumple devuelve un `422` con el detalle de qué campo falló y por qué. El
handler recibe un objeto ya validado, y por lo tanto **no tiene que verificar nada**
sobre su forma.

Ese es el mecanismo que la sección 7 del TPI especifica endpoint por endpoint, y es
el tema completo de la clase 2, que es la que sigue. Por ahora alcanza con retener
tres cosas.

La validación es **declarativa**: las restricciones se enuncian en el modelo, no se
programan en el handler. La validación ocurre **antes** de que el handler corra, así
que dentro del handler los datos ya son confiables. Y el modelo de entrada **no es
el mismo** que el modelo de la tabla: la clase 4 estudia el segundo, y confundirlos
es uno de los errores que la clase 2 documenta.

Nótese además el `Decimal` del ejemplo. Es la decisión que el módulo de frontend
estudia como RN-F08 desde el otro lado: el importe se guarda con un tipo decimal
exacto y **viaja como cadena** para que el cliente no lo convierta a punto flotante.
Acá se ve la mitad de arriba de esa regla.

---

## 1.7. La documentación que no se desactualiza

De todo lo anterior se deduce algo que el marco de trabajo hace solo: como los
tipos, las rutas y los modelos están declarados en el código, **la especificación de
la API se puede generar a partir de él**. Y eso es exactamente lo que ocurre.

Levantando el proyecto queda disponible una especificación en formato OpenAPI, más
dos interfaces navegables que la presentan: una permite además **ejecutar los
endpoints desde el navegador**, con los parámetros cargados a mano.

*(Ver Figura 1.5: la documentación automática y la ejecución de un endpoint.)*

Vale la pena entender por qué esto importa más de lo que parece, y no es por
comodidad.

**El TPI especifica setenta endpoints** en su sección 6, y dos equipos trabajan
contra esa especificación al mismo tiempo. Una especificación escrita a mano se
desactualiza el día que alguien cambia un campo y se olvida de actualizarla, y a
partir de ese momento **miente sin avisar**: el frontend implementa contra un
documento que ya no describe al servidor, y el error aparece en integración,
cuando corregirlo cuesta diez veces más.

Una especificación derivada del código no puede desactualizarse, porque no existe
separada del código. **Eso no es una comodidad: es la eliminación de una clase
entera de errores.**

> **🧪 EXPERIMENTO**
> Hacelo en la primera clase, porque es el que mejor muestra de qué se trata este
> marco de trabajo.
>
> 1. Levantá el proyecto con un endpoint que reciba un `producto_id: int`.
> 2. Abrí la documentación interactiva en el navegador y **ejecutá el endpoint desde
>    ahí**. Anda: no hiciste ningún cliente.
> 3. Ahora probá mandarle `abc` donde va el entero. Mirá el `422` y **leé el cuerpo
>    del error**: te dice qué campo, qué esperaba y qué recibió.
> 4. Volvé al código y cambiá el tipo de retorno del handler. Recargá la
>    documentación.
>
> **Cambió sola.** No tocaste ningún archivo de documentación, porque no hay ninguno.
>
> 5. Último paso, y es el que importa: pedile la especificación en crudo —el JSON de
>    OpenAPI— y mirá lo que tiene adentro.
>
> **Ese archivo es el contrato.** Es lo que la sección 6 del TPI describe en tablas,
> y es lo que tus compañeros del turno de frontend van a leer para escribir su
> cliente. Si tu tipo está mal, ese archivo miente, y ellos no tienen forma de
> saberlo.

---

## 1.8. Inyección de dependencias

Acá se cobra la actividad 8, y conviene plantear el problema antes de mostrar la
solución.

Un endpoint casi nunca trabaja solo: necesita una sesión de base de datos, el
usuario autenticado, tal vez un cliente de caché. La forma directa es construir eso
adentro del handler:

```python
@app.get("/pedidos/{pedido_id}")
async def obtener_pedido(pedido_id: int):
    session = AsyncSession(engine)        # el handler construye lo que necesita
    uow = UnitOfWork(session)
    ...
```

Eso funciona, y tiene exactamente los tres problemas que la actividad 8 nombró como
propios de la **dependencia de creación**:

**No se puede sustituir.** Para probar ese handler hay que tener una base de datos
real, porque la sesión se construye adentro y no hay forma de darle otra.

**Se repite.** Los setenta endpoints del TPI necesitan lo mismo, así que las mismas
líneas aparecen setenta veces, y el día que cambia la forma de construir la sesión
hay que tocar setenta lugares.

**Nadie limpia.** Esa sesión hay que cerrarla, y si el handler falla en el medio, no
se cierra.

La **dependencia de uso** invierte eso: el handler no construye, **recibe**. Y el
marco de trabajo ofrece el mecanismo para que reciba:

```python
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session                      # lo de arriba es preparación

async def get_uow(session: AsyncSession = Depends(get_session)) -> UnitOfWork:
    return UnitOfWork(session)

@app.get("/pedidos/{pedido_id}")
async def obtener_pedido(
    pedido_id: int,
    uow: UnitOfWork = Depends(get_uow),    # lo recibe, no lo construye
) -> PedidoResponse:
    return await PedidoService.obtener(uow, pedido_id)
```

Cuatro propiedades del mecanismo, cada una resolviendo algo:

**Se resuelve por la firma.** El marco de trabajo mira los parámetros, ve los
`Depends`, y arma el orden de resolución solo.

**Las dependencias se anidan.** `get_uow` depende de `get_session`, y eso se declara
igual que en el handler. Se forma un grafo que se resuelve de abajo hacia arriba.

**Se cachean por petición.** Si tres dependencias distintas piden la sesión, se
construye **una sola vez** y se comparte. Eso no es una optimización: es lo que
garantiza que las tres trabajen en la **misma transacción**, que es el tema de la
clase 6.

**Se limpian solas.** Una dependencia declarada con `yield` ejecuta lo de arriba
antes del handler y **lo de abajo después de que la respuesta salió**, incluso si el
handler lanzó una excepción.

Y con eso se llega a la regla del TPI que abrió el capítulo. El Router **recibe** el
Unit of Work y lo **transporta** al Service. No lo construye, no lo abre, no lo usa.

> **💡 PARA ENTENDER**
> Esto es el corazón de la clase, así que vale la pena verlo desde donde venís.
>
> En la actividad 8 el ejemplo era más o menos así:
>
> ```python
> class Servicio:
>     def __init__(self):
>         self.repo = RepositorioSQL()      # dependencia de CREACIÓN
>
> class Servicio:
>     def __init__(self, repo: RepositorioProtocol):
>         self.repo = repo                  # dependencia de USO
> ```
>
> Y la conclusión era que la segunda se puede probar con un repositorio falso, y la
> primera no.
>
> **`Depends()` es eso mismo, resuelto por el marco de trabajo.** Vos declarás qué
> necesitás; alguien más decide qué darte. En producción te da la sesión real; en
> un test le decís que te dé otra cosa, sin tocar el handler.
>
> Lo único que cambió es quién arma el objeto. **El principio es idéntico al que ya
> viste**, y por eso esta clase te resulta más fácil de lo que debería: ya sabías la
> parte difícil.

---

## 1.9. Recursos y ciclo de vida

Hay recursos que **no** se crean por petición: el pool de conexiones a la base de
datos, el cliente de Redis, el broker de la cola. Crearlos en cada petición sería
absurdo —el costo de establecer una conexión es justamente lo que un pool
existe para evitar—.

Esos se crean **una vez al arrancar la aplicación y se cierran una vez al
terminar**, en lo que el marco de trabajo llama el ciclo de vida:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.engine = create_async_engine(settings.DATABASE_URL)
    app.state.redis = redis.from_url(settings.REDIS_URL)
    yield                                   # acá vive la aplicación
    await app.state.redis.aclose()
    await app.state.engine.dispose()

app = FastAPI(lifespan=lifespan)
```

Esto es la octava regla de ejecución asincrónica del TPI, que la clase 3 desarrolla:

> **EA-08.** El pool de conexiones y el cliente de Redis se crean en el lifespan de
> la aplicación y se cierran ahí. **No se crean por petición ni a nivel de módulo.**

La prohibición de crearlos "a nivel de módulo" merece un comentario, porque es el
error que más se comete. Un cliente creado como variable global se construye **al
importar el archivo**, que es un momento en el que puede no haber un bucle de
eventos corriendo todavía. Los síntomas son desconcertantes: funciona al levantar
el servidor y falla en los tests, o al revés.

Y hay una consecuencia práctica que el TPI declara en su stack: como esos recursos
se crean en el ciclo de vida, **la suite de tests tiene que dispararlo**, y por eso
el stack incluye una herramienta específica para eso.

> **⚠️ OJO ACÁ**
> El error de crear el cliente a nivel de módulo es de los peores que te pueden
> tocar, porque **el síntoma no señala la causa.**
>
> ```python
> # arriba de todo del archivo, fuera de cualquier función
> redis_client = redis.from_url(REDIS_URL)     # se ejecuta al IMPORTAR
> ```
>
> Eso corre cuando Python lee el archivo, que es antes de que exista un bucle de
> eventos. A veces anda igual, a veces te tira un error sobre bucles distintos, y a
> veces —lo peor— **anda al levantar el servidor y falla en los tests**.
>
> Y ahí empieza la búsqueda en el lugar equivocado: mirás el test, mirás la
> configuración del test, mirás la fixture. **El problema está en una línea de un
> archivo que ni abriste**, que se ejecutó sola cuando alguien lo importó.
>
> Por eso EA-08 no dice "conviene": dice **no se crean por petición ni a nivel de
> módulo**. Van en el `lifespan`, y punto.

---

## 1.10. Las capas del backend

Acá está lo que hay que llevarse de esta clase para las siete que siguen. El TPI
declara en su sección 2.1 un flujo de dependencias estricto:

> **Router → Service → UoW → Repository → Model.** Ninguna capa puede importar la
> capa superior.

*(Ver Figura 1.3: las capas y la dirección de las dependencias.)*

Las responsabilidades, tal como el TPI las define:

| Capa | Archivo | Responsabilidad | Conoce a |
| --- | --- | --- | --- |
| **Router** | `router.py` | HTTP puro: parsea, valida el schema, resuelve dependencias, delega y serializa. **No traduce excepciones** | Service y el *tipo* UnitOfWork |
| **Task** | `tasks.py` | Punto de entrada del worker. Resuelve su UoW, invoca al Service. **Sin lógica propia** | Service y UnitOfWork |
| **Service** | `service.py` | La lógica de negocio. Sin estado y asincrónico. Recibe UoW y actor por parámetro. **Lanza excepciones de dominio, nunca HTTP** | UoW y los puertos |
| **Unit of Work** | `core/uow.py` | La transacción: sesión, repositorios, commit o rollback al salir. **No cierra la sesión** | Repository y sesión |
| **Repository** | `repository.py` | Acceso a datos, sin lógica de negocio, todo con `await`. Declara la precarga de relaciones | Model y sesión |
| **Model** | `model.py` | Tablas y relaciones. **Sin imports de capas superiores** | Nada de arriba |

Tres observaciones sobre esa tabla, porque cada una es una decisión y no una
descripción.

**El Router no traduce excepciones.** No hay `try`/`except` que convierta un error
de dominio en un código HTTP. De eso se ocupa un manejador global, que la clase 8
estudia. La razón es la de siempre: si cada router traduce, hay setenta traducciones
y basta con que una difiera.

**El Service es asincrónico y sin estado, y recibe el actor por parámetro.** No hay
un "usuario actual" guardado en ningún lado: quien llama dice de parte de quién
llama. Eso es lo que permite que **la misma función la invoque un Router y una
tarea del worker**, que es la observación siguiente.

**La capa Task no es una capa.** El TPI es explícito: es un **cliente** de Service,
igual que el Router. Una tarea resuelve su propio Unit of Work y llama al mismo
Service. Y da la razón: si existiera lógica que vive sólo en una tarea, **no se
podría ejercitar desde la API ni probar sin worker.**

> **💡 PARA ENTENDER**
> De esa tabla hay una fila que conviene que veas ahora, porque explica cómo está
> pensado el sistema entero:
>
> **El Service no sabe quién lo llamó.**
>
> Recibe el Unit of Work y recibe el actor, los dos por parámetro. No busca el
> usuario en ningún lado, no toca la petición HTTP, no sabe si hay una petición.
>
> ¿Y qué gana con eso? Tres cosas concretas:
>
> - **Lo puede llamar un Router** cuando alguien pide algo por HTTP.
> - **Lo puede llamar una tarea del worker**, donde no hay ninguna petición.
> - **Lo podés llamar vos en un test**, sin levantar el servidor.
>
> Fijate la diferencia con la alternativa. Si el Service leyera el usuario de la
> petición, **sólo lo podría llamar un Router** — y entonces la lógica de avanzar un
> pedido tendría que estar escrita dos veces: una para cuando lo hace una persona y
> otra para cuando lo hace la expiración automática.
>
> **Dos copias de la misma regla de negocio es cómo empiezan los bugs que nadie
> entiende.** Una se corrige, la otra no.

---

## 1.11. Redis no es una capa: es un adaptador

Esta sección es la más importante del capítulo después de la anterior, y es donde
la actividad 4 —duck typing y `Protocol`— se cobra entera.

El TPI lo declara así:

> **Redis no es una capa: es un adaptador.** El Service nunca importa
> `redis.asyncio`. Consume dos puertos declarados en `core/ports.py` —`CachePort` y
> `EventPort`— cuyas implementaciones de Redis viven en `core/adapters/`.

Y —esto es lo que lo vuelve una lección y no una convención— **da la razón**:

> La sección 4.3 exige que el sistema siga funcionando con Redis caído, y eso se
> escribe como una implementación alternativa del puerto —`NullCache`— que la
> aplicación instala cuando el healthcheck de Redis falla. **Con el cliente
> importado directamente en el Service, la degradación se escribiría como un
> `try`/`except` repetido en veinte lugares.**

Vale la pena desarmar ese razonamiento, porque es exactamente el que la actividad 4
enseñó en abstracto.

El requisito es de negocio: si Redis se cae, el sistema debe seguir aceptando
pedidos. Sin puerto, cumplir ese requisito significa rodear **cada** uso de Redis
con un `try`/`except` que decida qué hacer si falla. Veinte usos, veinte bloques,
veinte oportunidades de que uno quede mal.

Con puerto, el requisito se cumple **una sola vez**: se escribe una implementación
que no hace nada —guardar en ella no guarda, y leer siempre devuelve vacío— y se
instala esa en lugar de la real. El Service no se entera. Ni una línea suya cambia.

```python
class CachePort(Protocol):                    # actividad 4: duck typing tipado
    async def get(self, clave: str) -> bytes | None: ...
    async def set(self, clave: str, valor: bytes, ttl: int) -> None: ...

class RedisCache:                             # la implementación real
    async def get(self, clave): ...
    async def set(self, clave, valor, ttl): ...

class NullCache:                              # la degradación, completa
    async def get(self, clave): return None
    async def set(self, clave, valor, ttl): return None
```

Nótese que ninguna de las dos implementaciones **declara** que implementa el puerto.
Eso es duck typing: alcanza con tener la forma. Es exactamente lo que la actividad 4
señaló como "el regalo que Java no tiene".

> **💡 PARA ENTENDER**
> Guardate este razonamiento, porque es el que separa un diseño de una colección de
> parches:
>
> **El requisito no era "usá puertos". El requisito era "si Redis se cae, el sistema
> tiene que seguir vendiendo".**
>
> El puerto es la única forma de cumplir eso sin ensuciar veinte lugares. Fijate en
> las dos versiones del mismo requisito:
>
> ```python
> # Sin puerto: esto, repetido en veinte lugares
> try:
>     valor = await redis.get(clave)
> except RedisError:
>     valor = None
>
> # Con puerto: esto, una vez, en el arranque
> cache = RedisCache(...) if redis_disponible else NullCache()
> ```
>
> ¿Y qué pasa con la primera versión en la práctica? Que a las dos de la mañana
> antes de entregar, alguien agrega el uso número veintiuno y **se olvida del
> `try`**. Y eso no falla en la demo: falla el día que Redis se cae, que es
> justamente el día en que el sistema tenía que seguir andando.
>
> Es la misma lección que el módulo de frontend saca de sus once reglas: **las
> reglas que dependen de que alguien se acuerde, fallan.**

---

## 1.12. Los ocho servicios

El TPI declara en su sección 2.2 que el sistema se despliega como **ocho procesos**,
cada uno con su comando, su cardinalidad y su comportamiento ante la caída:

| Servicio | Instancias | Si se cae |
| --- | --- | --- |
| **migrador** | Corre una vez y termina | Ningún otro proceso debe arrancar |
| **seed** | Corre una vez y termina | La API arranca sin catálogos y el healthcheck lo detecta |
| **api** | N, tras un balanceador | Se pierden sus conexiones de eventos; el cliente reconecta |
| **worker** | N | La API sigue; se detiene el trabajo diferido y los eventos se acumulan |
| **scheduler** | **Exactamente una** | Deja de encolarse el trabajo periódico |
| **web** | N | No hay aplicación para el usuario aunque la API atienda |
| **postgres** | Una | El sistema no funciona. **No hay degradación posible** |
| **redis** | Una | El sistema **degrada** según la sección 4.3 y sigue siendo correcto |

*(Ver Figura 1.4: los ocho servicios y su orden de arranque.)*

Tres filas de esa tabla enseñan más que el resto.

**El migrador y el seed son trabajos, no servicios.** Corren, terminan y no vuelven.
Confundir eso lleva a orquestaciones donde el migrador se reinicia en bucle.

**El planificador corre en exactamente una instancia**, y el TPI explica por qué:
dos instancias simultáneas **encolan cada tarea dos veces**. De ahí sale la regla
TB-02 —toda tarea debe ser idempotente—, que la clase 8 desarrolla.

**PostgreSQL y Redis fallan distinto, a propósito.** Si se cae la base, el sistema
no funciona y lo dice con un `503`; no hay degradación posible ni se pretende que la
haya. Si se cae Redis, el sistema **sigue siendo correcto** con menos rendimiento y
sin tiempo real. Esa asimetría es la que da sentido a la distinción del TPI entre
"único almacén durable" y "almacén efímero".

> **📌 NOTA**
> Fijate en la última fila y en la anteúltima, porque juntas dicen algo que vale
> para cualquier sistema que armes:
>
> **Cada dependencia tiene declarado qué pasa si se cae.** Y no todas responden
> igual: una tira todo abajo, la otra degrada.
>
> Eso no es un detalle de operaciones, es una **decisión de diseño**. Decidir que
> Redis puede caerse sin que el sistema deje de vender obliga a escribir el código
> de otra manera —con puertos, como viste en la sección 1.11—. Decidir que Postgres
> no puede caerse te ahorra escribir un montón de código que nunca iba a funcionar
> bien igual.
>
> La pregunta que te tenés que hacer con cada dependencia que agregues a cualquier
> proyecto es esta: **¿qué pasa si esto no está?** Si no tenés respuesta, todavía no
> terminaste de diseñar.

---

## 1.13. Los doce módulos

El TPI organiza el código **por funcionalidad**, no por tipo de archivo. Cada
módulo vive en `app/modules/<nombre>/` y contiene sus propios `router.py`,
`service.py`, `repository.py`, `model.py` y `tasks.py`.

Los doce: `auth`, `usuarios`, `direcciones`, `categorias`, `productos`,
`ingredientes`, `stock`, `pedidos`, `catalogos`, `estadisticas`, `eventos` y
`operacion`.

Dos de esos módulos merecen mención desde ahora porque son especiales.

**`stock` es el dueño del stock**, y expone `aplicar_movimiento()` como **único
camino admitido** para modificarlo. Ningún otro módulo escribe stock directamente.
La clase 7 estudia por qué.

**`eventos` es el único que publica hacia el canal en tiempo real**, y la clase 8 lo
desarrolla.

*(Ver Figura 1.6: la estructura de un módulo y sus cinco archivos.)*

Esa organización es, por si no se notó, **la misma decisión que el módulo de
frontend toma en su octava clase** con Feature-Sliced Design: agrupar por dominio y
declarar una dirección para las dependencias. Los dos lados del sistema resuelven
el mismo problema de la misma manera, con vocabulario distinto.

> **📌 NOTA**
> Vale la pena que veas por qué se organiza así y no por tipo de archivo, porque es
> la alternativa que casi todos los tutoriales usan:
>
> ```
> routers/     productos.py  pedidos.py  usuarios.py  ...
> services/    productos.py  pedidos.py  usuarios.py  ...
> models/      productos.py  pedidos.py  usuarios.py  ...
> ```
>
> Eso anda bien con cinco módulos. **Con doce, cada cambio te obliga a abrir cinco
> carpetas**, y ninguna te dice cuáles archivos son del mismo módulo.
>
> Con la organización por funcionalidad, todo lo de pedidos vive junto: si querés
> entender pedidos, abrís una carpeta. Si querés borrar un módulo, borrás una
> carpeta y el intérprete te avisa quién lo extrañaba.
>
> Y hay algo lindo acá: **tus compañeros del turno de frontend van a llegar a esta
> misma conclusión en su última clase**, por su propio camino y con otro nombre. Es
> una buena señal cuando dos equipos que resuelven problemas distintos terminan
> ordenando el código igual.

---

## 1.14. Herramientas de diagnóstico

**La documentación interactiva** es la primera herramienta y la más subutilizada:
permite ejecutar cualquier endpoint sin escribir un cliente, lo que separa "el
backend está mal" de "mi cliente está mal" en diez segundos.

**La especificación en crudo** —el JSON de OpenAPI— es lo que hay que mirar cuando
el frontend reporta que algo no coincide. Es el contrato, y la discusión se resuelve
ahí y no por chat.

**Los registros de uvicorn** muestran cada petición con su método, ruta, código de
estado y duración. Conviene mirarlos desde el primer día para acostumbrarse a
distinguir un `422` —que es validación, o sea el cliente mandó mal— de un `500`, que
es una excepción no controlada.

**`curl` y `httpx`** desde la línea de comandos aíslan el backend del frontend
completo. El TPI declara `httpx` en su stack porque es también el cliente que se usa
en los tests: lo que se prueba a mano con él es lo mismo que después se automatiza.

**Y el diagnóstico más útil de todos, para este capítulo: seguir un import.** Si un
archivo de una capa importa algo de una capa superior, la regla de la sección 1.10
está rota. Es una verificación que se hace leyendo la cabecera del archivo, y en la
clase 8 se automatiza.

---

## 1.15. Seguridad y evolución

Tres consideraciones cierran el capítulo.

**La documentación automática expone el contrato completo.** Eso es deseable en
desarrollo y discutible en producción: publica qué endpoints existen, qué reciben y
qué devuelven. Es información valiosa para quien quiera atacar el sistema, y por eso
suele deshabilitarse en producción o exigir autenticación.

**Un mensaje de error puede filtrar más de lo que debería.** Una excepción no
controlada que devuelve la traza completa entrega nombres de archivos, rutas y a
veces fragmentos de consultas. De ahí que el TPI use un manejador global, que la
clase 8 estudia.

**Toda validación que importa ocurre en el servidor.** El frontend valida para dar
buena experiencia; el servidor valida porque es el único que puede. Esa es
exactamente la regla RN-F04 que la otra mitad de la cursada estudia, vista desde
acá: **sus garantes son tres casos de prueba que le pegan al backend salteándose la
interfaz.**

Sobre la evolución, dos observaciones. La primera es que el bloqueo global del
intérprete —el argumento histórico a favor de la asincronía en Python— está siendo
revisado: hay una modalidad experimental sin él desde Python 3.13. Eso no cambia
nada de este módulo, porque **el modelo asincrónico no se eligió sólo por el
bloqueo**, sino por lo que dice la sección 1.2: un servidor pasa su tiempo
esperando, y esperar no necesita un hilo por espera.

La segunda es que el contrato ASGI habilitó cosas que WSGI no podía expresar, y el
TPI usa una de ellas —el flujo de eventos de la sección 11—. Elegir un contrato más
expresivo abrió posibilidades que no eran el objetivo original.

---

## 1.16. Verificación

1. Escribir una aplicación ASGI sin marco de trabajo que responda un JSON, y
   **nombrar las tres piezas** que recibe.
2. Levantar un proyecto con tres endpoints y verificar que los tres aparecen en la
   documentación automática.
3. Provocar un `422` mandando un tipo equivocado en un parámetro de ruta, y **leer
   el cuerpo del error** identificando qué campo falló.
4. Cambiar el tipo de retorno de un handler y verificar que **la especificación
   cambió sola**.
5. Escribir una dependencia con `yield` que registre en consola antes y después, y
   **verificar el orden** respecto de la respuesta.
6. Declarar una dependencia usada por otras dos y comprobar que **se construye una
   sola vez** por petición.
7. Ubicar cinco archivos del backend del TPI en su capa y **justificar qué puede
   importar cada uno**.
8. Explicar por qué el Router no traduce excepciones y quién lo hace.
9. Escribir un puerto con `Protocol` y dos implementaciones, y **cambiar de una a
   otra sin tocar el código que lo consume**.

---

## 1.17. Errores frecuentes

**Declarar un handler con `def` en lugar de `async def`.** Funciona —el marco de
trabajo lo manda a un hilo— y viola EA-01. La mezcla es peor que cualquiera de las
dos formas puras (sección 1.5).

**Construir la sesión dentro del handler.** Es dependencia de creación: no se puede
sustituir en un test, se repite en cada endpoint y nadie la cierra (sección 1.8).

**Crear el cliente de Redis o el motor a nivel de módulo.** Se construyen al
importar, cuando puede no haber bucle de eventos. Viola EA-08 y produce fallos que
aparecen sólo en los tests (sección 1.9).

**Importar `redis.asyncio` desde un Service.** Impide la degradación de la sección
4.3 sin repetir manejo de errores en veinte lugares (sección 1.11).

**Traducir excepciones en el Router.** Produce setenta traducciones donde debería
haber una (sección 1.10).

**Poner lógica de negocio en una tarea.** No se puede ejercitar desde la API ni
probar sin worker (sección 1.10).

**Confundir el modelo de entrada con el modelo de la tabla.** Son cosas distintas, y
usar el segundo como schema expone campos que no deberían viajar (sección 1.6).

**Declarar mal un tipo de retorno.** Rompe tres cosas a la vez: la validación, la
serialización y la especificación que el frontend va a leer (sección 1.5).

**Tratar al migrador como un servicio de larga vida.** Corre una vez y termina; si
se lo reinicia en bucle, la orquestación nunca converge (sección 1.12).

---

## 1.18. Actividades

1. **ASGI a mano.** Escribir una aplicación ASGI sin dependencias que responda dos
   rutas distintas parseando `scope["path"]`, y documentar cuánto código hizo falta.
   Reescribirla después con el marco de trabajo y comparar.

2. **El contrato es código.** Implementar tres endpoints del módulo `catalogos` del
   TPI con sus tipos correctos, exportar la especificación de OpenAPI y **compararla
   con la tabla de la sección 6.10 del TPI**, campo por campo.

3. **Creación contra uso.** Escribir un endpoint que construya su propia sesión y
   otro que la reciba por `Depends`. Escribir un test para cada uno y documentar qué
   hizo falta en cada caso. Relacionar con la actividad 8 de POO.

4. **El grafo de dependencias.** Declarar una cadena de tres dependencias anidadas
   donde la última es usada por dos, agregar registros en consola, y **documentar el
   orden de construcción y de limpieza**, y cuántas veces se construyó cada una.

5. **El puerto y su alternativa.** Implementar `CachePort` como `Protocol` con dos
   implementaciones —una real y una que no hace nada—, y un servicio que la consuma.
   Demostrar que el servicio funciona con las dos **sin ningún cambio**, y relacionar
   con la sección 4.3 del TPI.

6. **Exploración: las capas auditadas.** Tomar la tabla de la sección 1.10 y, sobre
   un proyecto propio o de ejemplo, revisar las cabeceras de import de cada archivo
   buscando violaciones de la regla de dependencias. Documentar cada una y proponer
   cómo se corrige. Relacionar lo observado con lo que la sección 2.1 del TPI declara
   sobre qué conoce cada capa.

7. **Exploración: los dos lados de la misma petición.** Junto con alguien del turno
   de frontend, tomar **un endpoint concreto** de la sección 6 del TPI. Implementarlo
   de este lado y consumirlo del otro. Documentar qué información hizo falta que no
   estaba en la tabla, y proponer cómo la especificación de OpenAPI la habría
   aportado. *(Requiere coordinar con la otra mitad de la cursada.)*

---

## 1.19. Síntesis

1. Un servidor web pasa la mayor parte del tiempo **esperando, no calculando**. De
   esa observación se deducen las tres respuestas históricas al problema de atender
   a muchos, y por qué ganó el bucle de eventos.

2. El modelo de un proceso o un hilo por conexión **no escala**: el problema tuvo
   nombre propio en 1999, y la salida fue **un solo hilo que multiplexa esperas**.

3. El bloqueo global del intérprete no impide ese modelo: **se libera mientras se
   espera**, y esperar es lo que un servidor hace casi siempre.

4. WSGI no podía expresar asincronía ni conexiones largas **por la forma de su
   contrato**, no por descuido. ASGI cambió el contrato: la aplicación es una
   corrutina, y **la concurrencia pasó a ser problema de la aplicación.**

5. Las anotaciones de tipo **dejaron de ser documentación y pasaron a ser
   comportamiento**: validan, convierten y documentan. Un tipo mal declarado rompe
   las tres cosas a la vez.

6. Una especificación derivada del código **no puede desactualizarse**, y eso
   elimina una clase entera de errores en un proyecto con dos equipos y setenta
   endpoints.

7. `Depends()` **es la actividad 8**: la diferencia entre construir lo que se
   necesita y recibirlo. El TPI lo exige explícitamente —el Router no construye el
   Unit of Work— y de ahí sale que el código sea probable.

8. Las dependencias se **cachean por petición**, y eso no es una optimización: es lo
   que garantiza que todo el manejo de una petición ocurra en **la misma
   transacción**.

9. Las capas tienen **una sola dirección**: Router → Service → UoW → Repository →
   Model. Y la capa Task **no es una capa**: es otro cliente de Service, porque
   ninguna lógica puede vivir donde no se la pueda probar.

10. **Redis no es una capa, es un adaptador.** El puerto no está por elegancia: es la
    única forma de cumplir el requisito de degradación sin repetir manejo de errores
    en veinte lugares. Es la actividad 4 aplicada.

11. **Cada dependencia declara qué pasa si se cae**, y no todas responden igual: una
    tira el sistema abajo, la otra degrada. Esa asimetría es una decisión de diseño,
    no un detalle de operaciones.

---

## 1.20. Referencias y lecturas complementarias

Las fuentes normativas de este capítulo son las especificaciones de los dos
contratos entre servidor y aplicación. **WSGI** está definido en el **PEP 333**
(2003) y su revisión **PEP 3333** (2010), y su lectura muestra con claridad por qué
un contrato sincrónico no podía extenderse a conexiones largas. **ASGI** se
documenta en `asgi.readthedocs.io`, con su especificación de eventos HTTP y
WebSocket, y conviene leer al menos la sección de mensajes HTTP para reconocer lo
que la sección 1.4 muestra. El modelo asincrónico del lenguaje corresponde al **PEP
3156**, que introdujo `asyncio`, y al **PEP 492**, que agregó `async` y `await`; el
piso de versión que el TPI fija se explica por el **PEP 654**, que introdujo los
grupos de excepciones. El formato de la especificación de la API que el marco de
trabajo genera es **OpenAPI 3.1**, mantenido por la OpenAPI Initiative.

El artículo de Dan Kegel sobre **el problema C10K** (1999, actualizado hasta 2014)
sigue disponible en `kegel.com/c10k.html` y es la mejor fuente sobre el límite del
modelo de un hilo por conexión y sobre los mecanismos de multiplexación que lo
resolvieron. Como bibliografía de estudio, la documentación oficial de FastAPI en
`fastapi.tiangolo.com` es inusualmente buena para ser documentación de producto: su
tutorial sobre dependencias explica el mecanismo de la sección 1.8 con más ejemplos
de los que caben acá. Para el fundamento de la inyección de dependencias, el
artículo de Martin Fowler *Inversion of Control Containers and the Dependency
Injection Pattern* (2004) es el texto donde el patrón quedó nombrado, y su lectura
conecta directamente con lo trabajado en la octava actividad de POO. Y para el
diseño de puertos y adaptadores de la sección 1.11, la formulación original de
Alistair Cockburn (2005) sigue siendo la referencia; conviene notar que la otra
mitad de la cursada llega al mismo texto por otro camino, al estudiar la
arquitectura de su propio lado.

Del TPI, este capítulo se apoya en tres secciones que conviene leer enteras: la
**2.1**, con el flujo de dependencias y la responsabilidad de cada capa; la **2.2**,
con los ocho servicios y su comportamiento ante la caída; y la **2.3**, con los doce
módulos. La sección **1.4**, que declara las ocho reglas de ejecución asincrónica,
es el tema completo de la clase 3 y por ahora sólo se anticipa.

---

**Continúa en:** Capítulo 2 — Contratos: schemas, validación y CRUD, donde los
modelos de la sección 1.6 se convierten en el contrato completo que la otra mitad de
la cursada va a consumir, y donde aparece la primera decisión incómoda: por qué el
importe se declara con un tipo decimal exacto y viaja como cadena de texto.
