# Capítulo 6 — Repositorios, Unit of Work y transacciones

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 6.1. Alcance de la clase

Este capítulo llega sexto **a propósito**, y conviene decir por qué antes de
empezar. En las clases 4 y 5 el alumno escribió servicios que tocan varias tablas
usando la sesión directamente, y en la clase anterior apareció una operación que
el TPI describe con una frase que vale como enunciado de toda esta clase:

> El registro inserta la asignación del rol de cliente **en la misma transacción**
> que crea el usuario. **Sin esa inserción, el usuario recién registrado no puede
> comprar.**

Ahí hay dos escrituras que **no tienen sentido por separado**. Un usuario sin rol
existe, puede iniciar sesión, y no puede hacer absolutamente nada. Es peor que si
no existiera, porque nadie lo va a notar hasta que esa persona intente comprar.

Ese es el problema que este capítulo resuelve, y presentarlo antes —cuando todavía
no dolía— habría convertido el patrón en una ceremonia que se copia sin entender.
**Ahora el problema ya se sintió.**

El capítulo estudia dos patrones que Martin Fowler nombró en 2002 y que el TPI
declara como capas obligatorias de su flujo `Router → Service → UoW → Repository →
Model`. Y estudia también las **dos excepciones declaradas** al ciclo de vida, que
son lo más instructivo de la sección 8.4: una de ellas es **la única operación de
escritura del sistema que no comparte la transacción de su petición**, y la razón
por la que debe escapar es de una elegancia que merece detenerse.

Al finalizar la clase, el alumno debe poder **escribir un repositorio con su
precarga declarada**, componer un Unit of Work, y explicar **quién crea la sesión,
quién la abre, quién confirma y quién cierra** — que son cuatro responsabilidades
distintas y en este sistema están en cuatro lugares distintos.

**Contenidos**

1. Origen y objetivos de diseño de los patrones de acceso a datos.
2. Las cuatro propiedades de una transacción.
3. La operación a medias: qué problema se está resolviendo.
4. El patrón repositorio y sus dos jerarquías.
5. Genéricos que se borran en tiempo de ejecución.
6. La tabla de precarga como parte del contrato.
7. El Unit of Work: qué compone y qué garantiza.
8. Quién crea, quién abre, quién confirma y quién cierra.
9. La firma uniforme del servicio.
10. Las dos excepciones declaradas al ciclo de vida.
11. Sólo agregado: dos mecanismos independientes.
12. Herramientas de diagnóstico.

---

## 6.2. Por qué existen estos patrones: origen y diseño

El problema es tan viejo como las bases de datos y se enuncia en una línea: **una
operación de negocio casi nunca corresponde a una sola escritura, y las escrituras
pueden fallar en el medio.**

La respuesta del motor es la **transacción**: un conjunto de operaciones que se
aplican todas o ninguna. El concepto se formalizó en los años setenta y ochenta —Jim
Gray sentó las bases y el acrónimo que las resume se acuñó en 1983—, y sigue siendo
una de las garantías más valiosas que un motor relacional ofrece, precisamente
porque **es muy difícil de reponer en la aplicación**.

Pero la transacción resuelve el *qué* y deja abierto el *dónde*. ¿Quién decide que
estas cinco escrituras van juntas? ¿Dónde empieza y dónde termina?

La respuesta ingenua es que cada función que escribe abra su propia transacción y
la confirme. **Y eso rompe exactamente lo que se quería garantizar**: si crear el
usuario confirma y después falla la asignación del rol, el usuario ya está
guardado. Cada pieza fue correcta y el conjunto quedó inconsistente.

Martin Fowler nombró en 2002 los dos patrones que resuelven eso, en un libro que
catalogó soluciones que ya se usaban sin nombre:

**El repositorio** separa *"qué datos necesito"* de *"cómo se los pido a este
motor"*. El servicio pide "el pedido con sus líneas"; el repositorio decide con qué
consulta lo trae. Eso vuelve el servicio **probable sin base de datos** —se le puede
pasar otro repositorio— y concentra en un solo lugar las decisiones de acceso.

**El Unit of Work** hace de la transacción **un objeto explícito**: alguien la abre,
las escrituras se acumulan, y al terminar se confirma entera o se descarta entera.
Deja de ser algo implícito que ocurre en algún lado.

De ahí salen las cuatro decisiones de diseño de este capítulo.

**Primera: la transacción es de la operación de negocio, no de cada escritura.**
Quien sabe qué va junto es el servicio, no el repositorio.

**Segunda: el repositorio no tiene lógica de negocio.** Sabe traer y guardar; no
sabe si se puede.

**Tercera: quien crea un recurso lo cierra.** Y en este sistema eso significa que el
Unit of Work **no cierra la sesión**, porque no la creó.

**Cuarta: las excepciones se declaran.** El TPI enumera dos operaciones que se
salen del ciclo de vida general, con su razón y su alcance. La sección 6.9 las
estudia.

> **💡 PARA ENTENDER**
> Antes de seguir, fijate en el problema real, porque no es el que parece:
>
> **No es que las operaciones fallen. Es que fallan por la mitad.**
>
> Si crear un usuario falla entero, no pasa nada: el cliente ve un error y vuelve a
> intentar. **Un fallo limpio es un no-evento.**
>
> Lo grave es lo otro: el usuario se creó y el rol no. Nadie ve un error —la petición
> puede haber respondido `500`, pero el usuario **quedó guardado**—. Y ese usuario
> existe, inicia sesión, y no puede hacer nada. **El sistema quedó en un estado que
> ninguna parte del código contempla.**
>
> Todo este capítulo es sobre eso. La transacción no evita que las cosas fallen:
> **evita que queden a medias.** Es una garantía mucho más modesta y mucho más útil.

---

## 6.3. Las cuatro propiedades

El acrónimo que resume lo que una transacción garantiza tiene cuatro letras, y cada
una responde a un problema distinto. Vale verlas con un ejemplo del dominio, porque
así dejan de ser una definición para memorizar.

| Propiedad | Qué garantiza | En el TPI |
| --- | --- | --- |
| **Atomicidad** | Todo o nada | Crear el usuario **y** asignarle el rol, o ninguna de las dos |
| **Consistencia** | Las restricciones se cumplen al terminar | Un pedido confirmado no puede tener stock negativo |
| **Aislamiento** | Las transacciones concurrentes no se pisan | Dos pedidos del último producto no lo venden dos veces |
| **Durabilidad** | Lo confirmado sobrevive a una caída | Un pedido confirmado sigue ahí si el servidor se reinicia |

*(Ver Figura 6.1: las cuatro propiedades con su caso del dominio.)*

**La atomicidad** es la que este capítulo usa todo el tiempo y la que el Unit of
Work materializa.

**La consistencia** merece una precisión que se pasa por alto: no significa "los
datos tienen sentido", sino algo más acotado y verificable: **las restricciones
declaradas se cumplen al terminar la transacción.** Es la letra que conecta
directamente con la clase 4 — cada comprobación y cada clave foránea que se declara
es una condición que el motor va a exigir.

**El aislamiento** es la más compleja y es de la que menos se habla, porque tiene
grados. Un motor ofrece varios **niveles**, y cada uno permite ciertos fenómenos a
cambio de rendimiento. PostgreSQL usa por defecto un nivel donde una transacción ve
sólo lo confirmado por otras, y eso **no alcanza para el problema del stock**: la
clase 7 estudia por qué y qué hace el TPI al respecto.

**La durabilidad** es la que menos discusión genera y la que explica una decisión de
arquitectura del TPI: por eso PostgreSQL es **el único almacén durable** y Redis es
efímero. Lo que está en Redis puede desaparecer; lo confirmado en PostgreSQL, no.

> **⚠️ OJO ACÁ**
> De las cuatro letras, hay una que **no viene gratis y hay que pedirla**, y es la que
> más problemas causa:
>
> **El aislamiento tiene grados, y el que viene por defecto no alcanza para todo.**
>
> PostgreSQL usa por defecto un nivel donde tu transacción ve sólo lo que otras ya
> confirmaron. Suena suficiente. Y no lo es para esto:
>
> 1. Tu transacción lee que quedan 3 unidades.
> 2. Otra transacción vende 3 y confirma.
> 3. Tu transacción descuenta 3. **Ahora hay −3.**
>
> Ninguna de las dos hizo nada mal. Las dos leyeron un valor confirmado y escribieron
> sobre él. **El aislamiento por defecto permite exactamente eso**, y tiene nombre:
> actualización perdida.
>
> No es un bug del motor: es el grado de aislamiento que elegiste sin saber que
> estabas eligiendo. **La clase 7 es enteramente sobre este párrafo.**

---

## 6.4. El repositorio

### 6.4.1. Qué separa

Un repositorio es una clase que concentra el acceso a datos de una entidad. El
servicio le pide lo que necesita **por su significado**; el repositorio decide **con
qué consulta** lo consigue.

```python
# El Service pide por significado
pedido = await uow.pedidos.get_by_id(pedido_id, cargar=("items", "usuario"))

# El Repository decide cómo
async def get_by_id(self, entity_id: int, cargar: tuple = ()) -> T | None:
    consulta = select(self.model).where(self.model.id == entity_id)
    for relacion in cargar:
        consulta = consulta.options(selectinload(getattr(self.model, relacion)))
    return (await self.session.exec(consulta)).first()
```

Esa separación tiene tres consecuencias, y la tercera es la que más importa en este
proyecto.

**El servicio se puede probar sin base de datos**, pasándole un repositorio
sustituto. Es la actividad 4 de POO aplicada: alcanza con que tenga la misma forma.

**Las decisiones de acceso viven en un solo lugar.** Si hay que agregar un índice o
cambiar una consulta, se toca el repositorio y nada más.

**La precarga se declara donde se sabe cómo se traen los datos.** Y de ahí sale algo
práctico que la clase 4 anticipó: cuando salta la excepción de carga perezosa,
**ya se sabe dónde mirar** — en el método del repositorio que trajo ese objeto.

### 6.4.2. Dos jerarquías, y por qué no una

El TPI declara **dos** clases base, y da la razón:

> Hay dos jerarquías: `BaseRepository[T]` para todos los modelos y
> `SoftDeleteRepository[T]` para los cinco que tienen borrado lógico. **Un único
> genérico que filtrara la columna de borrado produciría un error de SQL sobre las
> tablas que no la tienen.**

*(Ver Figura 6.5: las dos jerarquías y qué modelos hereda cada una.)*

Es una consecuencia directa de la enumeración taxativa de la clase 4: como **sólo
cinco entidades** tienen borrado lógico, un filtro universal rompería sobre las
otras dieciocho. La alternativa —un condicional que verifique si el modelo tiene la
columna— funcionaría y sería peor: mueve a tiempo de ejecución una distinción que el
sistema de tipos puede expresar.

> **📌 NOTA**
> Fijate el criterio, porque se aplica muchísimo más allá de este caso:
>
> **Si una distinción se puede expresar en el tipo, no la resuelvas con un `if`.**
>
> Las dos versiones "funcionan":
>
> ```python
> # Con condicional: la distinción vive en tiempo de ejecución
> if hasattr(self.model, "deleted_at"):
>     consulta = consulta.where(self.model.deleted_at.is_(None))
>
> # Con dos clases: la distinción vive en el tipo
> class SoftDeleteRepository(BaseRepository[T]):   # sólo para los cinco que la tienen
> ```
>
> La segunda gana por tres cosas concretas: el editor te dice qué métodos tenés
> disponibles según con qué repositorio estés trabajando; **`get_by_id_including_deleted`
> no existe donde no tiene sentido**; y no hay una comprobación repitiéndose en cada
> consulta de cada repositorio.
>
> Y hay algo más de fondo: el condicional **oculta** que hay dos casos. Las dos clases
> lo **declaran**. Quien lee el código sabe, sin buscar, que hay entidades que se
> borran lógicamente y entidades que no.

### 6.4.3. Los genéricos que se borran

Hay un detalle de la firma del constructor que el TPI explica y que vale por sí
solo:

> `__init__(session, model: type[T])` — **Recibe la clase del modelo de forma
> explícita: los genéricos de Python se borran en tiempo de ejecución y `select(T)`
> no existe.**

Eso es exactamente el mismo fenómeno que **la otra mitad de la cursada estudió como
borrado de tipos en TypeScript**: la anotación genérica existe para el verificador y
**no llega a la ejecución**. Cuando el código corre, `T` no es nada.

Por eso el repositorio necesita que le pasen la clase real:

```python
class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model          # esto SÍ existe en ejecución
```

> **💡 PARA ENTENDER**
> Este detalle es el mejor puente de todo el módulo con lo que ven tus compañeros
> del otro turno, así que vale la pena verlo junto:
>
> | | TypeScript | **Python** |
> | --- | --- | --- |
> | Los tipos genéricos | se borran al compilar | **se borran en tiempo de ejecución** |
> | Consecuencia | no podés preguntar `if (x is Pedido)` | **no podés escribir `select(T)`** |
> | Salida | pasar el dato explícitamente | **pasar la clase explícitamente** |
>
> **Es el mismo fenómeno, con dos nombres distintos y en dos lenguajes distintos.**
>
> Y la lección general es la que ellos ven en su clase 6: **una anotación de tipo es
> información para la herramienta, no un objeto que exista cuando el programa corre.**
>
> Si alguna vez escribís un genérico y necesitás usar el tipo *de verdad* —para
> construir una consulta, para instanciar algo, para comparar— **vas a tener que
> pasarlo como dato.** No hay forma de recuperarlo del genérico.

### 6.4.4. El catálogo de métodos

El TPI declara los métodos de las dos clases base. Vale la pena leer la tabla
completa porque **cada método esconde una decisión**:

| Método | Qué hace | La decisión que esconde |
| --- | --- | --- |
| `get_by_id(id, cargar)` | Obtiene por clave primaria | El parámetro `cargar` **es la precarga de EA-05** |
| `get_by_id_including_deleted(id)` | Sin filtrar el borrado | Es **la vía de las excepciones 2, 3 y 4** de la sección 3.7 |
| `get_for_update(id)` | Como el anterior, con bloqueo | **Sin filtrar** el borrado: hay que distinguir borrado de sin stock |
| `get_many_for_update(ids)` | Bloquea varias filas | **Ordena los identificadores** antes de emitir. Ver más abajo |
| `list(filters, skip, limit, sort, cargar)` | Listado completo | Lleva la paginación y el orden de la sección 6.1 del TPI |
| `count(filters)` | Cantidad | **Los mismos filtros que `list`**: es el total que respeta filtros de la clase 2 |
| `create` / `update` | Agrega a la sesión | Ejecutan `flush()` y `refresh()`, no `commit()` |
| `soft_delete` / `hard_delete` | Baja lógica o física | El físico **sólo** en tablas pivote, galería y purgas |
| `descendientes` / `ancestros` | Subárbol de categorías | Consultas recursivas del motor |
| `tomar_pendientes(limite)` | Toma eventos del outbox | Usa un mecanismo que la clase 8 estudia |

Dos filas merecen desarrollo inmediato.

**`create` y `update` hacen `flush()`, no `commit()`.** La distinción es central:
`flush()` **emite el SQL** —de modo que la base ya conoce el cambio y asigna
identificadores— pero **no confirma la transacción**. El repositorio escribe; **el
repositorio no decide que la operación terminó**. Esa decisión es del Unit of Work,
y por eso el `commit` no aparece en ningún repositorio.

**`get_many_for_update` ordena los identificadores.** El TPI declara que ordena
internamente de forma ascendente antes de emitir la sentencia, y eso —que parece un
detalle de implementación— **es la regla RN-18**, la que evita los interbloqueos. La
clase 7 explica por qué; por ahora alcanza con notar que **la regla vive dentro del
método**, de modo que quien lo usa la cumple sin saberlo.

> **💡 PARA ENTENDER**
> Ese ordenamiento escondido adentro del método es una de las mejores decisiones de
> diseño del TPI, y todavía no sabés por qué. Fijate igual en la forma:
>
> **La regla no está escrita en ningún lado que alguien tenga que leer. Está adentro
> del único método que puede violarla.**
>
> La alternativa habría sido una nota en la documentación: *"acordate de bloquear las
> filas en orden ascendente de identificador"*. Y esa nota **funciona hasta que
> alguien escribe el bloqueo a mano**, apurado, sin haberla leído.
>
> Poniéndolo adentro de `get_many_for_update`, **quien usa el método cumple la regla
> sin saber que existe.** Y quien no lo usa —quien escribe el bloqueo a mano— es
> exactamente el caso que hay que revisar en el código.
>
> Es el mismo patrón que venís viendo desde el primer capítulo de los dos módulos:
> **la regla que se cumple sola le gana a la regla que hay que recordar.** Acá está
> aplicada a algo que ni siquiera entendés todavía, y va a seguir funcionando igual.

---

## 6.5. La tabla de precarga es parte del contrato

La sección 8.3 del TPI incluye una tabla que indica, endpoint por endpoint, qué
relaciones hay que precargar. Y la introduce con una frase que conviene citar
entera:

> **Esta tabla no es documentación de apoyo: es parte del contrato del endpoint.**
> Omitir una precarga produce **una excepción en tiempo de ejecución** (EA-05), **no
> un N+1 silencioso.**

Algunas de sus filas enseñan a leer un requisito de precarga:

| Endpoint | Precarga | Qué revela la decisión |
| --- | --- | --- |
| `GET /productos` | Sólo la unidad de venta | **No trae categorías ni galería**: no se devuelven en el listado, y la portada viaja en la columna desnormalizada de la clase 4 |
| `GET /productos/{id}` | Unidad, categorías, ingredientes con su unidad, imágenes | El detalle sí las devuelve, así que sí se precargan |
| `GET /pedidos` | Sólo el usuario | El listado no muestra las líneas |
| `GET /pedidos/{id}` | Usuario, ítems con producto e ingredientes, historial con usuario, pago | El detalle completo |
| Confirmación de pedido | **Por cada producto, su receta con ingrediente y unidad** | Sin esto, el descuento **emite una consulta por línea, en el punto más caliente del sistema** |

La primera y la segunda fila muestran algo importante: **la precarga no es del
modelo, es del endpoint.** El mismo `Producto` se trae distinto según qué se vaya a
devolver, y por eso la tabla se organiza por endpoint y no por entidad.

> **⚠️ OJO ACÁ**
> La tentación al escribir esto es enorme y hay que resistirla:
>
> **"Precargo todo siempre y me olvido del problema."**
>
> No funciona, y el listado de productos lo muestra: si `GET /productos` precargara
> categorías y galería como hace el detalle, cada página de veinte productos traería
> **veinte categorías y ochenta imágenes que nadie va a mostrar.**
>
> Y eso es peor de lo que parece, porque ese endpoint es el más consultado del sistema
> y el que se cachea. Estarías multiplicando por cinco el peso de la respuesta más
> pedida **para no tener que pensar.**
>
> La regla es al revés: **precargá exactamente lo que la respuesta va a leer.** Ni más
> ni menos. Y el que te dice cuánto es exactamente, es el modelo de salida del
> Capítulo 2: si un campo no está en el `Public`, no hace falta precargarlo.

La última fila conecta la precarga con la clase 7: el descuento de stock por receta
recorre las líneas del pedido y, por cada una, sus ingredientes. **Sin precarga son
tantas consultas como líneas, dentro de una transacción con filas bloqueadas.** Es
el peor lugar posible para emitir consultas de más.

---

## 6.6. El Unit of Work

El Unit of Work **compone repositorios** —es la actividad 6 de POO— y **gestiona la
transacción**:

```python
class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.usuarios = UsuarioRepository(session, Usuario)
        self.pedidos = PedidoRepository(session, Pedido)
        self.productos = ProductoRepository(session, Producto)
        # ... un repositorio por entidad, todos con LA MISMA sesión

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        # NO cierra la sesión: no la creó
```

Tres cosas de ese código.

**Todos los repositorios comparten la sesión.** Eso no es un detalle de eficiencia:
es lo que hace que **todo lo que escriban esté en la misma transacción**. Si cada
repositorio tuviera su propia sesión, el Unit of Work no garantizaría nada.

**Es un gestor de contexto asincrónico**, y el `async with` marca el límite de la
transacción de manera visible. No hay que acordarse de confirmar: **salir del bloque
confirma**.

**Y no cierra la sesión.** El TPI lo declara con esas palabras: *"`__aexit__` hace
commit o rollback y nada más. El cierre lo hace `get_session()`."*

Con eso, el registro de usuario de la clase anterior se escribe así:

```python
async def registrar(uow: UnitOfWork, datos: RegistroRequest) -> Usuario:
    async with uow:
        usuario = await uow.usuarios.create(Usuario(...))
        await uow.roles.create(UsuarioRol(usuario_id=usuario.id, rol_id=ROL_CLIENT))
        return usuario
    # salir del bloque confirma las DOS escrituras, o ninguna
```

Si la segunda línea falla —por cualquier motivo— la primera **no queda**. El
problema de la sección 6.1 desapareció, y no porque alguien se acuerde de revertir:
**porque salir del bloque con una excepción revierte.**

*(Ver Figura 6.2: la operación a medias, antes y después.)*

> **📌 NOTA**
> Fijate en lo que hace el `async with`, porque es el mismo principio que atraviesa
> los dos módulos de esta cursada:
>
> **La transacción tiene un límite visible en el código, y confirmarla no depende de
> que alguien se acuerde.**
>
> Compará las dos formas:
>
> ```python
> # Confiando en la memoria
> usuario = await crear_usuario(...)
> await asignar_rol(...)
> await session.commit()          # ¿y si alguien lo olvida? ¿y si hay un return antes?
>
> # Con el límite declarado
> async with uow:
>     usuario = await uow.usuarios.create(...)
>     await uow.roles.create(...)
> # salir confirma. Salir con excepción revierte. No hay tercera opción.
> ```
>
> Es exactamente la misma idea que tus compañeros del turno de frontend ven con la
> clase base que da de baja las suscripciones: **el mecanismo hace lo correcto, y
> equivocarse exige salirse del camino.**

---

## 6.7. Quién crea, quién abre, quién confirma y quién cierra

Son **cuatro responsabilidades distintas**, y en este sistema están en cuatro
lugares. El TPI las declara una por una en su sección 8.4, y conviene verlas juntas
porque es lo que más se confunde:

| Responsabilidad | Quién | Detalle |
| --- | --- | --- |
| **Crear la sesión** | `get_session()` | Dependencia asincrónica: la obtiene, la cede y **la cierra en su `finally`** |
| **Construir el UoW** | `get_uow()` | Lo construye con esa sesión y **lo devuelve sin abrirlo** |
| **Transportarlo** | El Router | Lo anota como dependencia y lo pasa al Service. **No lo abre** |
| **Abrirlo y confirmarlo** | El Service | Lo abre con `async with`. **Nunca escribe `UnitOfWork()` directamente** |
| **Cerrar la sesión** | `get_session()` | En su `finally`, después de que la respuesta salió |

*(Ver Figura 6.3: el ciclo completo, de la dependencia a la respuesta.)*

La regla que ordena todo eso es la tercera decisión de la sección 6.2: **quien crea
un recurso lo cierra.** El Unit of Work no creó la sesión, así que no la cierra. Si
la cerrara, la dependencia que sí la creó intentaría cerrarla de nuevo.

Y hay un detalle de la sección 8.4 que muestra la caché de dependencias del
Capítulo 1 haciendo algo concreto:

> Todas las demás dependencias que tocan la base —la del usuario actual y la de
> verificación de rol— **reciben esa misma sesión**; sin esa unificación, **cada
> petición autenticada consumiría dos conexiones del pool.**

Eso conecta tres clases: la caché de dependencias es del Capítulo 1, el pool
limitado es de la clase 3, y acá se ve **para qué servía**. Si la dependencia de
sesión se construyera dos veces por petición, cada petición autenticada tomaría dos
conexiones, y el pool se agotaría **con la mitad de la carga**.

### La firma uniforme del servicio

El TPI declara además una convención que parece cosmética y no lo es:

> Toda función de servicio es una corrutina que recibe **el UoW primero y el actor
> segundo**: `async def crear_pedido(uow, actor, body, clave)`. El actor es un objeto
> con el identificador del usuario y el conjunto de sus roles vigentes, **o el actor
> sintético `SISTEMA` cuando la llamada viene de una tarea.**

La última parte cierra el círculo con la clase 5. Ahí se estableció que `SISTEMA` es
**un dato y no una identidad**; acá se ve dónde vive ese dato: es un valor que se le
pasa al servicio cuando quien llama no es una persona.

Y por eso el servicio **funciona igual** llamado desde un Router o desde una tarea
del worker: recibe lo mismo, no averigua nada por su cuenta.

### Una prohibición explícita

El TPI declara además un caso donde **no** poner una verificación de rol, y la razón
enseña:

> La ruta de avance de estado de un pedido **no lleva verificación de rol**. Ponerla
> contradiría la matriz —**el propietario puede cancelar desde pendiente**— e
> **invertiría el orden de errores.**

Vale desarmar la segunda mitad. Con una verificación de rol en la ruta, un cliente
que intenta cancelar su propio pedido recibiría un `403` **antes** de que nadie
evalúe si la transición es válida. El mensaje diría "no tenés permiso" cuando en
realidad **sí lo tiene**, por ser el propietario.

El orden correcto es al revés: primero se resuelve quién es y qué relación tiene con
el recurso, y **después** la matriz decide si esa transición está permitida para ese
actor. Poner el filtro antes **cambia qué error ve el usuario**, y un error
equivocado es peor que ninguno.

---

## 6.8. Las dos excepciones declaradas

Acá está lo más instructivo de la sección 8.4. El TPI enumera **dos operaciones que
se salen del ciclo de vida general**, y las declara con su razón y su alcance en
lugar de dejarlas como rarezas del código.

### 6.8.1. El intento de acceso que debe sobrevivir al rollback

> El registro del intento de acceso usa **una sesión y una transacción propias, que
> se confirman siempre**. Es **la única operación de escritura del sistema que no
> comparte la transacción de su petición**, y existe porque **el fallo que se quiere
> contar es el mismo que revierte la transacción.**

Esa última frase es la clave, y merece leerse dos veces.

El sistema cuenta los intentos fallidos de inicio de sesión para poder limitarlos.
Un intento falla porque la contraseña no coincide, y esa situación **provoca una
excepción que revierte la transacción de la petición**.

Si el registro del intento viviera en esa misma transacción, **el rollback lo
borraría**. El sistema intentaría contar los fallos y **no contaría ninguno**,
porque cada fallo se lleva puesta su propia anotación.

*(Ver Figura 6.4: por qué el intento necesita su propia transacción.)*

Es una situación circular preciosa: **lo que se quiere registrar es exactamente lo
que destruye el registro.** La única salida es que ese registro no participe de esa
transacción.

Y el TPI no se queda ahí. Declara también el costo:

> El **estado externo** que la excepción introduce está enumerado en la sección 15.1,
> con su procedimiento de limpieza.

Porque una escritura que se confirma siempre, aunque la petición falle, **deja datos
que las pruebas tienen que limpiar**. La excepción no sólo se declara: se declara
también qué complica.

> **💡 PARA ENTENDER**
> Esta excepción es de lo mejor que tiene el TPI, así que quedate con el
> razonamiento completo:
>
> **Quiero contar los fallos → el fallo revierte la transacción → si cuento adentro
> de la transacción, el conteo se revierte con el fallo → nunca cuento nada.**
>
> No es un capricho ni una optimización: **la operación es lógicamente incompatible
> con la transacción de la que forma parte.**
>
> Y ahora lo que más me interesa que veas, que es el método y no el caso: **el TPI
> declara la excepción, su razón, y lo que complica.** No dice "usá una sesión
> aparte acá". Dice por qué, y dice qué precio se paga —estado externo que hay que
> limpiar en los tests—.
>
> Eso es lo que separa una excepción legítima de un parche: **un parche no explica
> por qué es necesario ni qué rompe.** Cuando en tu TPI tengas que salirte de una
> regla, escribí las tres cosas. Si no podés escribir la segunda, probablemente no
> era una excepción.

### 6.8.2. Las cuatro sesiones del panel

La segunda excepción es de lectura y su justificación es de otro tipo:

> El resumen de indicadores lanza sus **cuatro consultas concurrentemente sobre
> cuatro sesiones del pool**. Es **la única lectura del sistema que usa más de una
> conexión por petición**; aceptable porque el panel lo consulta **un puñado de
> administradores.**

Acá no hay una imposibilidad lógica: hay un intercambio medido. Cuatro consultas
independientes en paralelo responden mucho más rápido que en serie —es exactamente
lo que la clase 3 mostró con los grupos de tareas—, y el costo es **cuatro conexiones
del pool en lugar de una**.

Lo que vuelve aceptable ese costo es **quién usa el endpoint**: unos pocos
administradores, no todos los clientes. Si el catálogo público hiciera lo mismo, el
pool se agotaría con la carga normal.

> **📌 NOTA**
> Comparar las dos excepciones enseña más que cada una por separado:
>
> | | El intento de acceso | El panel de indicadores |
> | --- | --- | --- |
> | Tipo de razón | **Lógica**: es imposible de otra forma | **Medida**: es un intercambio |
> | Qué pasa si no se hace | El sistema **no funciona** | El panel es más lento |
> | Qué la vuelve aceptable | No hay alternativa | **Quién y cuántos lo usan** |
>
> Las dos son excepciones válidas y **no se justifican igual**. La primera se defiende
> con un razonamiento; la segunda, con un dato sobre el uso real.
>
> Cuando propongas una excepción a una regla de tu proyecto, fijate de cuál de los dos
> tipos es. Si es del segundo, **necesitás el dato**: quién lo usa, cuántas veces, qué
> cuesta. "Es más rápido" no alcanza — más rápido siempre es más rápido, la pregunta
> es a cambio de qué y para cuántos.

---

## 6.9. Sólo agregado: dos mecanismos independientes

La regla RN-03 del TPI establece algo que ninguna capa puede violar:

> `HistorialEstadoPedido` y `MovimientoStock` son de **sólo agregado**; ninguna capa
> puede emitir una modificación ni un borrado sobre esas tablas. La garantía la
> imponen **dos mecanismos independientes**: un disparador de la base y **los
> permisos del rol de aplicación.**

Lo interesante es que sean **dos**, y que sean **independientes**.

**El disparador** vive en la base y rechaza la operación venga de donde venga.
**Los permisos del rol** —los dos roles de base de datos que la clase 4 mencionó—
hacen que el usuario con el que la aplicación se conecta **directamente no tenga
permiso** de modificar ni borrar esas tablas.

Cualquiera de los dos alcanzaría. Tener los dos significa que **el fallo de uno no
deja el sistema desprotegido**: si alguien reemplaza el disparador en una migración
mal revisada, los permisos siguen; si alguien despliega con el rol equivocado, el
disparador sigue.

Y hay algo más que conviene notar: **ninguno de los dos mecanismos está en el código
de la aplicación.** RN-03 no depende de que ningún repositorio se comporte bien.
Aunque alguien escribiera un método que intente actualizar el historial, **la
operación fallaría igual.**

Es el mismo criterio de la clase 4 sobre las redundancias —que ninguna quede
sostenida sólo por la disciplina del servicio— aplicado a una regla de negocio.

> **💡 PARA ENTENDER**
> Hay una idea acá que vale para cualquier sistema serio y que casi nunca se enseña:
>
> **Defensa en profundidad: dos mecanismos independientes para la misma garantía.**
>
> No es desconfianza ni paranoia. Es reconocer que **cada mecanismo tiene su propia
> forma de fallar**, y que si las dos formas son distintas, es muy improbable que
> fallen juntas:
>
> - El disparador falla si alguien lo elimina en una migración mal revisada.
> - Los permisos fallan si alguien despliega con el rol equivocado.
>
> **Son dos errores humanos completamente distintos**, cometidos por personas
> distintas en momentos distintos. Que ocurran los dos a la vez es mucho menos
> probable que cualquiera de ellos por separado.
>
> Y fijate lo más importante, que ya viste en la clase 4 con las redundancias:
> **ninguno de los dos está en el código de la aplicación.** Podés escribir un
> repositorio que intente actualizar el historial y **la operación va a fallar
> igual.** La regla no depende de que tu código se porte bien.

---

## 6.10. Herramientas de diagnóstico

**El registro de sentencias** vuelve a ser la herramienta central, y en este capítulo
sirve para algo específico: **ver dónde empieza y dónde termina cada transacción.**
Con el registro activado se ven las marcas de inicio y de confirmación, y eso
responde la pregunta de si dos escrituras fueron juntas o separadas.

*(Ver Figura 6.6: el registro de una transacción completa, con sus límites.)*

**Verificar que no hay confirmaciones en los repositorios** es una comprobación de
texto: buscar la palabra en la capa de repositorio no debería devolver nada. Es del
mismo tipo que la de EA-03 en la clase 3, y por lo tanto se puede automatizar.

**Contar las conexiones en uso durante una petición** verifica lo de la sección 6.7:
una petición autenticada debería tomar **una** conexión, no dos. Si toma dos, la
unificación de la sesión no está funcionando.

**Provocar un fallo en medio de una operación de varias escrituras** y verificar que
**ninguna quedó** es la prueba directa de que el Unit of Work hace su trabajo. Es la
verificación más simple del capítulo y la que más tranquilidad da.

> **🧪 EXPERIMENTO**
> Este es el experimento que hace visible por qué existe todo este capítulo.
>
> 1. Escribí el registro de usuario **sin** Unit of Work: crear el usuario, confirmar,
>    asignar el rol, confirmar.
> 2. Provocá un fallo entre las dos confirmaciones —lanzá una excepción a mano—.
> 3. Mirá la base. **El usuario está. El rol no.**
> 4. Intentá iniciar sesión con ese usuario. **Funciona.** Ahora intentá comprar
>    algo. No podés, y el error no dice nada útil.
>
> Ese usuario va a estar ahí para siempre, y nadie lo va a notar hasta que esa
> persona escriba preguntando por qué no puede hacer un pedido.
>
> 5. Ahora envolvé las dos escrituras en `async with uow:` y repetí el fallo.
> 6. Mirá la base. **No hay nada.**
>
> Fijate el detalle que importa: **en los dos casos la petición respondió con un
> error.** Desde afuera se ven iguales. La diferencia está en lo que quedó adentro, y
> es exactamente la diferencia entre un fallo limpio y un dato corrupto que nadie
> sabe que existe.

---

## 6.11. Seguridad y evolución

Tres consideraciones cierran el capítulo.

**Una transacción abierta demasiado tiempo es un problema.** Mientras dura, mantiene
bloqueos y ocupa una conexión del pool. Una operación que abre la transacción y
después hace una llamada a un servicio externo puede tener la transacción abierta
segundos, y con suficiente concurrencia eso agota el pool. **El trabajo lento va
fuera de la transacción**, y esa es una de las razones de la cola de tareas que la
clase 8 estudia.

**El rollback no revierte lo que ocurrió afuera.** Si una operación escribió en
Redis, envió un correo o llamó a otro servicio, **eso no vuelve atrás**. Es
exactamente el problema que el patrón de la clase 8 resuelve, y es también la razón
por la que la excepción de la sección 6.8.1 tiene que declarar el estado externo que
introduce.

**Las restricciones de la base son la última línea de defensa.** Un servicio que
verifica y después escribe deja una ventana entre las dos cosas, y en esa ventana
otra petición puede haber cambiado el estado. La verificación en el código evita el
noventa y nueve por ciento de los casos; **la restricción declarada evita el resto**,
que es el que ocurre bajo concurrencia. La clase 7 estudia ese uno por ciento.

Sobre la evolución, dos observaciones. La primera es que **estos patrones tienen más
de veinte años y siguen siendo la respuesta correcta**. Se los ha declarado
innecesarios varias veces —porque el ORM ya hace algo parecido, porque agregan una
capa— y vuelven, porque lo que resuelven no desaparece: alguien tiene que decidir
qué escrituras van juntas, y ese alguien no puede ser cada escritura por su cuenta.

La segunda es que el nombre importa menos que la responsabilidad. Hay marcos donde
el equivalente del Unit of Work es un decorador, o un gestor de contexto de la
propia biblioteca. **Lo que no cambia es la pregunta**: ¿dónde empieza y dónde
termina esta transacción, y quién lo decide?

---

## 6.12. Verificación

1. Escribir una operación de dos escrituras **sin** Unit of Work, provocar un fallo
   en el medio, y **documentar qué quedó en la base**.
2. Repetir con Unit of Work y verificar que no quedó nada.
3. Ubicar en el registro de sentencias **dónde empieza y dónde termina** una
   transacción.
4. Verificar que **ningún repositorio confirma**: buscar la palabra en esa capa.
5. Explicar la diferencia entre emitir el SQL y confirmar, y **por qué el repositorio
   hace lo primero y no lo segundo**.
6. Contar las conexiones que toma una petición autenticada y **verificar que es una**.
7. Escribir un repositorio genérico y **explicar por qué recibe la clase del modelo**.
8. Justificar por qué hay dos jerarquías de repositorio y no una.
9. Explicar por qué el registro del intento de acceso **no puede** estar en la
   transacción de su petición.

---

## 6.13. Errores frecuentes

**Confirmar dentro del repositorio.** El repositorio escribe; quien decide que la
operación terminó es el Unit of Work (sección 6.4.4).

**Abrir una transacción por escritura.** Cada pieza queda correcta y el conjunto
inconsistente: es el problema que el capítulo entero resuelve (sección 6.2).

**Que el Unit of Work cierre la sesión.** No la creó. Quien la creó la cierra
(sección 6.7).

**Construir el Unit of Work dentro del Service.** El Service lo recibe y lo abre;
nunca lo construye. Es la regla de la sección 2.1 del TPI (sección 6.7).

**Darle a cada repositorio su propia sesión.** Entonces el Unit of Work no garantiza
nada: cada uno escribe en su propia transacción (sección 6.6).

**No unificar la sesión entre dependencias.** Cada petición autenticada consume dos
conexiones del pool en lugar de una (sección 6.7).

**Olvidar la precarga declarada.** No es un `N+1` silencioso: es una excepción en
tiempo de ejecución (sección 6.5).

**Precargar por entidad en lugar de por endpoint.** El mismo modelo se trae distinto
según qué se vaya a devolver (sección 6.5).

**Poner una verificación de rol donde la matriz decide.** Invierte el orden de
errores: el usuario recibe "no tenés permiso" cuando sí lo tiene (sección 6.7).

**Hacer trabajo lento con la transacción abierta.** Mantiene bloqueos y ocupa una
conexión; con concurrencia agota el pool (sección 6.11).

**Suponer que el rollback revierte lo que pasó afuera.** Lo escrito en Redis o
enviado por correo no vuelve (sección 6.11).

---

## 6.14. Actividades

1. **El problema, medido.** Implementar el registro de usuario de las dos formas y
   documentar el estado de la base tras un fallo en cada caso. Explicar por qué las
   dos respuestas HTTP son indistinguibles desde afuera.

2. **El repositorio genérico.** Implementar `BaseRepository[T]` y
   `SoftDeleteRepository[T]` con al menos seis de los métodos que el TPI declara.
   Justificar por qué son dos clases y **verificar el error** que produciría una sola.

3. **La precarga por endpoint.** Tomar tres filas de la tabla de precarga del TPI e
   implementarlas. Para cada una, ejecutar el endpoint **sin** la precarga y
   documentar la excepción; después contar las consultas con la precarga puesta.

4. **Los cuatro roles del ciclo de vida.** Implementar la cadena completa —dependencia
   de sesión, dependencia de UoW, Router, Service— y agregar registros que muestren
   **el orden exacto** en que ocurre cada paso, incluido el cierre después de la
   respuesta.

5. **La excepción del intento fallido.** Implementar el registro del intento dentro
   de la transacción de la petición y demostrar que **no queda ninguno**.
   Corregirlo con una sesión propia y verificar que ahora sí. Documentar además el
   estado externo que eso introduce.

6. **Exploración: los límites de la transacción.** Con el registro de sentencias
   activado, capturar el ciclo completo de tres operaciones distintas —una lectura,
   una escritura simple y una de varias escrituras— y documentar dónde empieza y
   termina la transacción en cada caso. Relacionar lo observado con la tabla de
   responsabilidades de la sección 6.7.

7. **Exploración: los tipos que se borran, en dos lenguajes.** Junto con alguien del
   turno de frontend, comparar el borrado de genéricos de Python con el borrado de
   tipos de TypeScript. Escribir en cada lenguaje un caso donde el tipo genérico
   haga falta en ejecución, documentar cómo lo resuelve cada uno, y explicar por qué
   los dos llegan a la misma solución. *(Requiere coordinar con la otra mitad de la
   cursada.)*

---

## 6.15. Síntesis

1. El problema no es que las operaciones fallen sino que **fallen por la mitad**. Un
   fallo limpio es un no-evento; un dato a medias es un estado que ninguna parte del
   código contempla.

2. La transacción resuelve el *qué* y deja abierto el *dónde*. **Quien sabe qué
   escrituras van juntas es el servicio**, no cada escritura por su cuenta.

3. El repositorio separa **"qué datos necesito" de "cómo se los pido"**, y por eso la
   precarga se declara ahí: es el único que sabe cómo se traen.

4. Hay **dos jerarquías de repositorio** porque sólo cinco entidades tienen borrado
   lógico: un filtro universal fallaría sobre las otras dieciocho.

5. **Los genéricos de Python se borran en tiempo de ejecución**, igual que los tipos
   de TypeScript. Por eso el repositorio recibe la clase del modelo como dato: `T` no
   existe cuando el programa corre.

6. `create` y `update` **emiten el SQL pero no confirman**. El repositorio escribe;
   quien decide que la operación terminó es el Unit of Work.

7. La tabla de precarga **es parte del contrato del endpoint**, no documentación de
   apoyo. Y se organiza por endpoint y no por entidad, porque el mismo modelo se trae
   distinto según qué se devuelva.

8. **Cuatro responsabilidades, cuatro lugares**: la dependencia crea y cierra la
   sesión, otra construye el Unit of Work sin abrirlo, el Router lo transporta, y el
   Service lo abre y lo confirma.

9. **Quien crea un recurso lo cierra.** Por eso el Unit of Work no cierra la sesión.

10. Una verificación de rol puesta donde la matriz decide **invierte el orden de
    errores**: el usuario recibe "no tenés permiso" cuando en realidad lo tiene.

11. La excepción del intento de acceso es lógicamente necesaria: **lo que se quiere
    registrar es exactamente lo que destruye el registro.** Y el TPI declara además
    qué complica, que es lo que separa una excepción de un parche.

12. RN-03 se garantiza con **dos mecanismos independientes y ninguno está en el
    código de la aplicación**. La regla se cumple aunque alguien escriba código que
    intente violarla.

---

## 6.16. Referencias y lecturas complementarias

La fuente donde estos dos patrones quedaron nombrados es Fowler, *Patterns of
Enterprise Application Architecture* (Addison-Wesley, 2002); sus entradas sobre
*Repository* y *Unit of Work* son breves y conviene leerlas completas, porque
enuncian las responsabilidades con más precisión de la que suele circular. Las
propiedades de la sección 6.3 fueron formalizadas por Härder y Reuter en *Principles
of Transaction-Oriented Database Recovery* (ACM Computing Surveys, 1983), que acuñó
el acrónimo sobre el trabajo previo de Jim Gray; su lectura muestra que las cuatro
letras no son igual de fundamentales y que el aislamiento es la que más grados
admite.

Para la implementación, la documentación de **SQLAlchemy** sobre la sesión y su
ciclo de vida es la referencia directa de las secciones 6.6 y 6.7, y su discusión
sobre cuándo emitir y cuándo confirmar cubre exactamente la distinción de la sección
6.4.4. La documentación de **PostgreSQL** sobre control de concurrencia detalla los
niveles de aislamiento que la sección 6.3 apenas menciona y que la clase 7 va a
necesitar enteros.

Como bibliografía de estudio, Kleppmann, *Designing Data-Intensive Applications*
(O'Reilly, 2017) dedica su séptimo capítulo a las transacciones y es la mejor
explicación disponible de por qué el aislamiento es difícil; su tratamiento de los
fenómenos de concurrencia es la preparación ideal para la clase siguiente. Y para el
diseño de capas de acceso a datos, el capítulo correspondiente de Evans,
*Domain-Driven Design* (Addison-Wesley, 2003) explica por qué el repositorio
devuelve objetos del dominio y no filas, que es la distinción que vuelve al servicio
independiente del motor.

Del TPI, este capítulo se apoya en la sección **8.3** —con su catálogo de métodos y
su tabla de precarga— y en la **8.4**, que declara el ciclo de vida completo y las
dos excepciones de la sección 6.8. Toca además la **16.4**, por los dos mecanismos
que garantizan RN-03, y anticipa la **9.2**, donde el bloqueo que aparece en
`get_many_for_update` encuentra su explicación.

---

**Continúa en:** Capítulo 7 — El corazón transaccional, donde el aislamiento que
esta clase apenas nombró se vuelve el problema principal, y donde el ordenamiento de
identificadores que `get_many_for_update` hace por dentro revela para qué era: evitar
que dos pedidos simultáneos se queden esperando el uno al otro para siempre.
