# Capítulo 4 — Persistencia: SQLModel, PostgreSQL y el modelo de datos

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 4.1. Alcance de la clase

Los tres capítulos anteriores construyeron un servicio que responde, valida y no
bloquea. Le falta lo único que importa a largo plazo: **recordar**. Este capítulo
introduce el almacenamiento durable, y con él aparece la primera decisión
verdaderamente difícil del módulo.

Esa decisión no es técnica sino de traducción. Las actividades 5 y 6 de POO
establecieron un vocabulario preciso —asociación, agregación, composición— para
describir cómo se relacionan los objetos. Una base relacional **no tiene ninguna de
esas tres cosas**: tiene tablas, filas y claves foráneas. Traducir de un modelo al
otro exige tomar decisiones que ningún diagrama resuelve solo, y equivocarse ahí
cuesta más caro que en cualquier otra parte del sistema, porque **los datos
sobreviven al código.**

El capítulo también cobra dos deudas de la clase anterior. **EA-04** —la sesión que
no expira sus objetos al confirmar— y **EA-05** —la carga perezosa prohibida— dejan
de ser advertencias sobre una excepción con nombre raro y pasan a ser **dos líneas
de código concretas**, con su motivo a la vista.

Y hay una sección que este capítulo trata con especial cuidado porque contradice lo
que se enseña habitualmente. Todo curso de bases de datos enseña a **normalizar**:
que un dato viva en un solo lugar. El TPI declara **cinco redundancias
deliberadas**, y las justifica una por una. Entender por qué a veces copiar un dato
es lo correcto —y qué hay que hacer para que esa copia no se convierta en una
mentira— es lo que separa aplicar una regla de tomar una decisión.

El criterio con el que el TPI resuelve eso vale como enunciado de todo el capítulo:

> **Ninguna redundancia queda sostenida sólo por la disciplina del Service.**

Al finalizar la clase, el alumno debe poder **traducir un diagrama de clases a un
esquema relacional** justificando cada decisión, escribir los modelos con su carga
anticipada declarada, y generar y **leer** una migración antes de aplicarla.

**Contenidos**

1. Origen y objetivos de diseño de la persistencia relacional.
2. El desajuste objeto-relacional y qué esconde un ORM.
3. De la asociación, la agregación y la composición al esquema.
4. SQLModel: qué une y por qué.
5. El motor y la sesión asincrónicos.
6. Relaciones y carga anticipada.
7. Los tres dominios del sistema.
8. Normalización y las cinco redundancias declaradas.
9. Borrado lógico: una enumeración taxativa.
10. Índices y restricciones de unicidad.
11. Migraciones como código versionado.
12. Herramientas de diagnóstico.

---

## 4.2. Por qué relacional: origen y diseño

El modelo relacional es de 1970 y nació de un artículo de Edgar Codd que proponía
algo entonces radical: **separar cómo se guardan los datos de cómo se consultan.**
Los sistemas de la época obligaban al programa a conocer la estructura física del
almacenamiento —punteros, orden de los registros— y por lo tanto cualquier cambio en
esa estructura rompía todos los programas.

La propuesta de Codd fue describir los datos como **relaciones** —conjuntos de
tuplas— y consultarlos con un lenguaje declarativo donde uno dice **qué quiere**, no
cómo obtenerlo. El motor decide el cómo. Esa separación es la razón por la que un
esquema puede reorganizarse, agregar índices o cambiar su almacenamiento sin que las
consultas cambien.

Sobre eso se construyeron dos garantías que el resto de este módulo da por
sentadas: las **restricciones declaradas** —una clave foránea, una unicidad, una
comprobación— que el motor impone sin que ningún programa colabore, y las
**transacciones**, que la clase 6 estudia.

**El desajuste.** Cuando los lenguajes orientados a objetos se volvieron dominantes,
apareció un problema que se conoció como *desajuste de impedancia objeto-relacional*,
y conviene enunciarlo con precisión porque explica todo lo que sigue:

| En objetos | En relacional |
| --- | --- |
| Un objeto tiene **identidad** propia | Una fila se identifica por su **clave** |
| Las referencias son **punteros en memoria** | Las referencias son **valores de clave foránea** |
| Hay **herencia** | No hay herencia |
| Una colección es un **atributo del objeto** | Una relación uno a muchos vive **en la tabla hija** |
| Un objeto se **navega** libremente | Cada navegación es **una consulta** |

*(Ver Figura 4.2: las cinco diferencias del desajuste.)*

La última fila es la que más consecuencias tiene en este proyecto, y es donde EA-05
va a aparecer.

**Los mapeadores.** Un ORM traduce entre los dos modelos. Hibernate lo popularizó en
Java a partir de 2001, y SQLAlchemy hizo lo propio en Python desde 2006. La promesa
es escribir objetos y que alguien más se ocupe del SQL.

Y acá va la advertencia que este capítulo sostiene entero: **un ORM no elimina el
desajuste, lo esconde.** Todo lo de la tabla anterior sigue ahí abajo. Quien no lo
sabe escribe código que parece correcto y emite ciento una consultas donde debía
emitir dos, o que modifica un objeto y no entiende por qué eso disparó cinco
sentencias.

De ese recorrido salen las cuatro decisiones de diseño del capítulo.

**Primera: el almacén durable es uno solo.** El TPI lo declara: PostgreSQL es el
único almacén durable, y Redis es efímero. Ningún dato de negocio vive sólo en
Redis.

**Segunda: las garantías se declaran en la base cuando se puede.** Una restricción
que el motor impone no depende de que ningún programa se acuerde.

**Tercera: lo que la base no puede garantizar, lo garantiza una prueba.** Es la
frase del TPI sobre las redundancias, y la sección 4.9 la desarrolla.

**Cuarta: el esquema es código versionado.** Las migraciones viven en el
repositorio, se revisan y se aplican en orden. La sección 4.12 lo trata.

> **💡 PARA ENTENDER**
> De la tabla del desajuste, quedate con la última fila, porque es la que te va a
> morder de verdad:
>
> **En objetos, navegar es gratis. En la base, cada navegación es una consulta.**
>
> Cuando escribís `pedido.usuario.direccion.calle`, en memoria son tres saltos de
> puntero: nanosegundos. Contra una base son **tres consultas**, con red de por medio
> cada vez.
>
> Un ORM hace que las dos cosas se escriban igual. **Y ahí está el peligro**: el código
> se ve idéntico y el costo es cuatro órdenes de magnitud distinto.
>
> Por eso EA-05 existe. No es una manía del TPI: es que **el ORM te deja escribir algo
> barato que resulta carísimo**, y la única defensa es declarar de antemano qué vas a
> navegar.

---

## 4.3. De las actividades 5 y 6 al esquema

Acá se cobra lo que ya saben. Las tres relaciones que estudiaron en POO tienen
traducción al esquema, y **la diferencia entre ellas no está en la clave foránea
sino en qué pasa al borrar.**

**Asociación uno a muchos.** Un pedido pertenece a un usuario; un usuario tiene
muchos pedidos. La clave foránea vive **en el lado "muchos"**, que es lo que
sorprende a quien viene de objetos: en el objeto, la colección es un atributo del
usuario; en la tabla, la referencia está en el pedido.

```python
class Pedido(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")   # la FK vive acá
```

**Asociación uno a uno.** Se expresa como una foránea con una restricción de
unicidad. Sin esa unicidad no es uno a uno: es uno a muchos con un solo elemento
por casualidad.

**Muchos a muchos.** No se puede expresar directamente: exige una **tabla
intermedia**. Y esa tabla, que parece pura mecánica, suele ser una entidad con
sentido propio. En el TPI, `ProductoIngrediente` no es sólo un vínculo: **lleva la
cantidad de la receta**, y esa cantidad no pertenece ni al producto ni al
ingrediente sino a la relación entre ambos.

**Agregación y composición** son las que se traducen distinto, y el criterio es el
que la actividad 6 estableció: **si la parte puede existir sin el todo.**

| Relación | Ejemplo del TPI | Al borrar el padre |
| --- | --- | --- |
| **Agregación** | Producto y Categoría | La categoría **sigue existiendo** |
| **Composición** | Pedido y sus líneas de detalle | Las líneas **no tienen sentido solas** |

*(Ver Figura 4.1: las tres relaciones traducidas al esquema.)*

En el esquema eso se declara con el comportamiento del borrado: la composición lleva
borrado en cascada, la agregación restringe o anula. Pero **en este sistema hay una
vuelta de tuerca**, y es la que la sección 4.10 desarrolla: los pedidos **no se
borran nunca**, así que esa cascada no se ejecuta jamás en producción. Está
declarada igual, porque describe la intención del modelo.

> **📌 NOTA**
> Un detalle que confunde a todo el que viene de objetos, y conviene verlo ahora:
>
> **La clave foránea va del lado "muchos", que es el contrario al que uno esperaría.**
>
> En tu cabeza —y en el diagrama de clases— el usuario *tiene* una lista de pedidos.
> Parece que la relación viviera en el usuario.
>
> En la base es al revés: **cada pedido guarda a quién pertenece.** La tabla de
> usuarios no sabe nada de pedidos.
>
> ¿Y por qué? Porque una columna guarda **un** valor, no una lista. Para que el
> usuario "tuviera" sus pedidos habría que guardar una cantidad variable de
> referencias en una fila, y eso el modelo relacional no lo hace.
>
> El ORM después te deja escribir `usuario.pedidos` y parece que la lista estuviera
> ahí. **No está: es una consulta** que va a buscar los pedidos cuyo `usuario_id`
> coincide. Y por eso hay que declararla — otra vez EA-05."""

---

## 4.4. SQLModel: qué une

El Capítulo 2 declaró modelos con Pydantic para validar peticiones. Este capítulo
necesita modelos que representen tablas. **SQLModel** —publicado en 2021 por el mismo
autor del marco de trabajo— une las dos cosas: un modelo de SQLModel **es** un modelo
de Pydantic **y** una tabla de SQLAlchemy.

```python
class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=120, index=True)
    precio: Decimal = Field(max_digits=10, decimal_places=2)
    categoria_id: int = Field(foreign_key="categoria.id")
    deleted_at: datetime | None = Field(default=None)
```

El parámetro `table=True` es el que hace la diferencia: sin él, es un modelo de
validación como los del Capítulo 2; con él, además es una tabla.

Y acá conviene una advertencia que evita un error frecuente: **que se puedan unir no
significa que convenga usar el mismo modelo para todo.** El modelo de tabla y los
schemas de entrada y salida siguen siendo cosas distintas, por las tres razones de
la sección 2.5. Lo que SQLModel evita es reescribir los campos comunes, no la
segregación.

La forma habitual de aprovecharlo es una base compartida y tres modelos que la
extienden, uno de los cuales es además la tabla:

```python
class ProductoBase(SQLModel):                    # sin table=True: sólo campos
    nombre: str = Field(max_length=120)
    precio: Decimal = Field(max_digits=10, decimal_places=2)

class Producto(ProductoBase, table=True):        # LA TABLA
    id: int | None = Field(default=None, primary_key=True)
    costo_interno: Decimal                        # sólo en la tabla
    deleted_at: datetime | None = Field(default=None)

class ProductoCreate(ProductoBase):               # entrada
    categoria_id: int

class ProductoPublic(ProductoBase):               # salida
    id: int
```

Nótese qué campo está en cuál. `costo_interno` vive **sólo en la tabla**: no entra
por `ProductoCreate` y no sale por `ProductoPublic`. `deleted_at` tampoco sale.
Y `id` no está en la entrada, porque lo asigna la base.

> **⚠️ OJO ACÁ**
> Esa herencia ahorra tipeo y trae una trampa que conviene ver ahora:
>
> **Si agregás un campo a `ProductoBase`, aparece en los tres lugares a la vez.**
>
> Hoy agregás `costo_proveedor` a la base porque lo necesitás en la tabla. Y sin
> darte cuenta acabás de hacer dos cosas más: **el cliente ahora lo puede mandar**
> —está en `Create`— y **el cliente ahora lo puede ver** —está en `Public`—.
>
> No hay error, no hay advertencia. El campo simplemente empieza a viajar en las dos
> direcciones.
>
> Regla: **a la base van sólo los campos que van en los tres.** Todo lo demás se
> declara en el modelo que corresponde. Si dudás, ponelo en la tabla y agregalo
> después a los schemas donde haga falta — el error de que falte se ve enseguida; el
> de que sobre, no.

---

## 4.5. El motor y la sesión

Acá se cobran dos reglas de la clase anterior, y las dos son una línea de código.

```python
# EA-08: se crean en el ciclo de vida, ni por petición ni a nivel de módulo
engine = create_async_engine(
    settings.DATABASE_URL,          # postgresql+psycopg://...
    pool_size=settings.DB_POOL_SIZE,
    pool_timeout=settings.DB_POOL_TIMEOUT,
)

# EA-04: expire_on_commit=False, y no es una optimización
async_session = async_sessionmaker(engine, expire_on_commit=False,
                                   class_=AsyncSession)
```

Sobre la primera línea, un detalle del TPI que conviene notar: la dirección de la
base declara **el dialecto asincrónico** —`postgresql+psycopg://`—, y a partir de ahí
el motor elige solo la variante correcta. Es EA-03 expresada en configuración.

Sobre `pool_size` y `pool_timeout`, la sección 3.11 ya explicó por qué son variables
declaradas y no valores por defecto: con corrutinas, el techo natural que ponía el
grupo de hilos desapareció, y el pool es el primer recurso que se agota.

Y sobre `expire_on_commit=False`, el TPI es explícito en que **no es una
optimización**. Vale la pena ver el caso concreto que evita:

```python
pedido = await uow.pedidos.crear(datos)
await uow.commit()
return PedidoResponse(id=pedido.id, total=pedido.total)   # ← acá explotaría
```

Con el valor por defecto, el commit marca el objeto como expirado. Esa lectura de
`pedido.id` intentaría ir a buscar el dato de nuevo, **desde una línea común sin
`await`**, y ahí no hay a dónde saltar: es exactamente la situación de la sección
3.8. Con `False`, el objeto conserva sus valores y la lectura es un acceso a memoria.

> **📌 NOTA**
> Vale entender **por qué** el valor por defecto es `True`, porque no es un capricho
> de SQLAlchemy: en un mundo sincrónico tiene todo el sentido.
>
> Después de un commit, otra transacción pudo haber cambiado esos datos. Expirar el
> objeto garantiza que la próxima lectura traiga lo que hay en la base **ahora**, y
> no lo que había antes. Es una decisión conservadora y correcta.
>
> **Lo que cambia en asincrónico no es la conveniencia: es la posibilidad.** Esa
> relectura implícita necesita emitir una consulta, y como ocurre en una línea común
> sin `await`, no tiene desde dónde hacerlo.
>
> O sea: el valor por defecto **no es un error de la biblioteca**. Es una opción
> pensada para otro modelo de ejecución, que en este directamente no funciona.
>
> Y de ahí sale un criterio general que te va a servir: **cuando una biblioteca
> soporta dos modelos de ejecución, sus valores por defecto suelen estar pensados
> para el más viejo.** Revisalos.

---

## 4.6. Relaciones y carga anticipada

Las relaciones se declaran en los dos extremos:

```python
class Pedido(SQLModel, table=True):
    usuario_id: int = Field(foreign_key="usuario.id")
    usuario: "Usuario" = Relationship(back_populates="pedidos")
    detalles: list["DetallePedido"] = Relationship(back_populates="pedido")

class Usuario(SQLModel, table=True):
    pedidos: list["Pedido"] = Relationship(back_populates="usuario")
```

`back_populates` le dice al ORM que esos dos atributos son **los dos lados de la
misma relación**, de modo que agregar un pedido a la lista del usuario también
completa el `usuario` del pedido. Sin eso, los dos lados pueden quedar
inconsistentes en memoria.

Ahora bien: **declarar la relación no la carga.** Y acá aparece EA-05 en código.

```python
# El repositorio DECLARA qué relaciones va a necesitar la respuesta
async def obtener_con_detalles(self, pedido_id: int) -> Pedido | None:
    consulta = (
        select(Pedido)
        .where(Pedido.id == pedido_id)
        .options(
            selectinload(Pedido.detalles),
            selectinload(Pedido.usuario),
        )
    )
    return (await self.session.exec(consulta)).first()
```

Sin esas dos líneas de `selectinload`, acceder a `pedido.detalles` en el Service
lanza la excepción de la sección 3.8. **Con ellas, los datos ya están en memoria.**

*(Ver Figura 4.3: carga perezosa y anticipada, y las consultas que emite cada una.)*

Hay dos estrategias de precarga y conviene saber cuál usar:

| Estrategia | Cómo trae los datos | Cuándo conviene |
| --- | --- | --- |
| `selectinload` | **Dos consultas**: una para el padre, otra con `IN` para los hijos | **Colecciones** —uno a muchos— |
| `joinedload` | **Una consulta** con `JOIN` | Relaciones **a uno** |

La razón de la primera fila es concreta: con `JOIN`, un pedido con veinte líneas
devuelve **veinte filas con los datos del pedido repetidos veinte veces**. Con dos
consultas, se traen los datos del pedido una vez y las veinte líneas aparte. Para
colecciones grandes, la diferencia de datos transferidos es enorme.

El TPI resuelve esto declarándolo: su sección 8.3 incluye **una tabla de precarga**
que indica, endpoint por endpoint, qué relaciones hay que traer. Esa tabla no es una
guía de rendimiento: es **una condición para que el endpoint funcione**.

> **💡 PARA ENTENDER**
> Fijate dónde vive esa declaración, porque es una decisión de arquitectura y no un
> detalle:
>
> **La precarga se declara en el repositorio, no en el Service ni en la vista.**
>
> Y tiene lógica: el repositorio es el único que sabe **cómo** se traen los datos.
> El Service dice *qué* necesita —"dame el pedido con sus líneas"— y el repositorio
> decide cómo lo trae.
>
> Eso tiene una consecuencia práctica que vale oro: **cuando te explota una excepción
> de greenlet, ya sabés dónde mirar.** No es en la vista, no es en el Service: es en
> el método del repositorio que trajo ese objeto, y le falta una línea.
>
> Es el mismo principio de las capas de la clase 1: **cada cosa en el lugar donde se
> sabe lo que hace falta saber.** Si la precarga se declarara en el Service, el
> Service tendría que conocer detalles del acceso a datos, y ahí se rompe el flujo
> `Router → Service → UoW → Repository → Model`.

> **⚠️ OJO ACÁ**
> Esta es la diferencia práctica entre un backend sincrónico y este, y conviene que
> la tengas clarísima antes de escribir tu primer repositorio:
>
> | | Sincrónico | **Este proyecto** |
> | --- | --- | --- |
> | Olvidar la precarga | Funciona. Lento. Nadie se entera | **Excepción en la primera iteración** |
> | Cuándo te enterás | Cuando la tabla creció y alguien se quejó | **Mientras lo estás escribiendo** |
>
> Al principio la segunda columna se siente como un castigo: estás escribiendo un
> endpoint y te explota una excepción con un nombre que no dice nada.
>
> **Dale vuelta la lectura.** El sincrónico no te avisa nunca: te deja mandar a
> producción un endpoint que emite ciento una consultas, y te enterás dentro de seis
> meses cuando ya hay diez mil pedidos y nadie se acuerda de quién escribió eso.
>
> Acá el problema aparece **en tu máquina, con tres registros de prueba, el día que
> lo escribís.** Es el mejor momento posible para enterarse.

---

## 4.7. Los tres dominios

El TPI organiza sus **veintitrés entidades** en tres dominios, y esa división no es
sólo de presentación: agrupa cosas que cambian juntas.

| Dominio | De qué trata | Entidades características |
| --- | --- | --- |
| **Identidad y acceso** | Quién es quién y qué puede hacer | `Usuario`, `UsuarioRol`, `DireccionEntrega`, `IntentoAcceso` |
| **Catálogo y stock** | Qué se vende y cuánto hay | `Categoria`, `Producto`, `Ingrediente`, `MovimientoStock` |
| **Ventas y trazabilidad** | Qué se vendió y qué pasó con eso | `Pedido`, `DetallePedido`, `Pago`, `HistorialEstadoPedido` |

A eso se suman las **cinco tablas catálogo** —roles, estados de pedido, formas de
pago, modalidades de entrega y unidades—, que merecen un comentario porque su
existencia es una decisión.

Un estado de pedido podría ser una columna de texto, o una enumeración del lenguaje.
El TPI lo modela como **una tabla**, y eso permite algo que las otras dos opciones no:
que el estado **tenga atributos propios**. La sección 3.4 aprovecha exactamente eso:
`EstadoPedido` tiene una columna `es_terminal`, y RN-01 dice que un estado terminal
no admite transiciones salientes. Con una enumeración del lenguaje, esa propiedad
tendría que vivir en el código.

> **📌 NOTA**
> La decisión de modelar los catálogos como tablas tiene un costo y un beneficio, y
> conviene tener los dos a la vista:
>
> **El costo:** cada lectura de un pedido necesita también su estado, así que hay una
> relación más que precargar. Y agregar un estado nuevo exige una migración, no un
> cambio de código.
>
> **El beneficio:** el estado **tiene atributos propios**. `es_terminal` es el
> ejemplo del TPI, y de ahí sale RN-01. Con una enumeración del lenguaje, saber si un
> estado es terminal sería un `if` en algún lado, y ese `if` **habría que repetirlo**
> en cada lugar que lo necesite.
>
> El criterio para decidir es una sola pregunta: **¿esto va a necesitar atributos
> además del nombre?** Si la respuesta es sí —o si no estás seguro— va como tabla. Si
> es un conjunto cerrado que sólo necesita distinguirse a sí mismo, una enumeración
> alcanza.
>
> Y ojo: los cinco catálogos del TPI **también aparecen como enumeración en el
> frontend**, porque del otro lado son valores cerrados de una unión literal. Los dos
> lados modelan lo mismo con la herramienta de su mundo.

---

## 4.8. Normalización, y las cinco redundancias declaradas

Todo curso de bases de datos enseña a normalizar: que cada dato viva en un solo
lugar, de modo que no pueda haber dos versiones contradictorias. Es una regla
excelente y este sistema la rompe **cinco veces, a propósito**.

Conviene empezar por el criterio con que el TPI las admite, porque es lo que las
separa de un descuido:

> Cinco redundancias deliberadas. **Cada una tiene un garante**: una restricción de
> la base cuando es expresable, un test de invariante cuando no lo es. **Ninguna
> redundancia queda sostenida sólo por la disciplina del Service.**

Las cinco:

| # | Redundancia | Qué duplica | Garante |
| --- | --- | --- | --- |
| 1 | **Snapshot de línea** | Nombre, precio y subtotal del producto al momento del pedido | RN-04 y dos pruebas |
| 2 | **Snapshot de dirección** | Seis columnas con la dirección de entrega | Comprobación en la base + validación + prueba |
| 3 | **Importes del pedido** | El total en función del subtotal, descuento y envío | Comprobación de consistencia + tres de no negatividad + prueba |
| 4 | **Monto del pago** | El total del pedido | Sólo una prueba: **cruza tablas** |
| 5 | **Portada del producto** | La dirección de la imagen marcada como portada | Índice único para la unicidad + prueba para la igualdad |

*(Ver Figura 4.4: las cinco redundancias y qué sostiene a cada una.)*

**La primera es la más importante de entender**, porque no es una optimización: es
una necesidad del dominio. Un pedido de hace tres meses debe mostrar el precio que
tenía el producto **ese día**, no el de hoy. Si la línea de detalle apuntara al
producto sin copiar nada, cambiar un precio **reescribiría la historia**. De ahí
RN-04:

> El nombre, el precio y el subtotal de cada línea, y el nombre de cada ingrediente
> removido, son **un snapshot inmutable** tomado al crear el pedido.

Las filas 4 y 5 muestran el criterio en acción. El monto del pago duplica el total
del pedido, y esa igualdad **no se puede expresar como una comprobación de la base,
porque cruza dos tablas**: su garante es una prueba, y el TPI lo dice así. En la
portada del producto, la parte que **sí** es expresable —que exista una sola portada
por producto— la impone un índice único; **la parte que cruza tablas —que la
dirección copiada coincida con la original— la sostiene una prueba.**

Y la quinta redundancia viene con su propia justificación, que es un caso de estudio
de cómo se decide esto:

> El listado público de productos es el endpoint **más consultado** del sistema y es
> el que se cachea, y sin la columna cada tarjeta necesitaría su galería precargada
> para saber qué imagen mostrar. Con veinte productos por página eso es **una
> consulta adicional que devuelve cien filas para usar veinte.** La alternativa
> —resolver la portada en el frontend— pondría lógica de negocio en la vista. El
> costo de la redundancia es **un `UPDATE` de una columna cada vez que cambia la
> portada**, que ocurre una vez cada tanto y siempre dentro de la transacción que la
> cambia.

> **💡 PARA ENTENDER**
> Fijate cómo está armada esa justificación, porque es el molde de cualquier decisión
> de diseño que vayas a defender:
>
> 1. **Cuál es el caso**: el listado público, el endpoint más consultado.
> 2. **Qué costaría no hacerlo**: cien filas traídas para usar veinte, en cada página.
> 3. **Qué alternativas se descartaron y por qué**: resolverlo en el frontend metería
>    lógica de negocio en la vista.
> 4. **Cuánto cuesta hacerlo**: un `UPDATE` de una columna, cada tanto, dentro de la
>    transacción.
> 5. **Quién lo garantiza**: una prueba, porque la base no puede.
>
> Cinco puntos. **Eso es una decisión de diseño**; "lo hice así porque es más rápido"
> no lo es.
>
> Y ojo con esto para tu TPI: cuando le pidas a un agente que te desnormalice algo
> "por rendimiento", te va a agregar la columna sin dudar. **Lo que no te va a
> agregar es el garante** — y una redundancia sin garante no es una optimización, es
> una bomba de tiempo que se activa el día que las dos copias dejan de coincidir.

---

## 4.9. Borrado lógico: una enumeración taxativa

El **borrado lógico** consiste en no borrar: marcar la fila con una fecha de
eliminación y filtrarla en las consultas. Se usa cuando el dato tiene valor
histórico o cuando otras filas lo referencian.

Y acá el TPI hace algo que conviene destacar antes que nada, porque es una lección
de honestidad técnica:

> La enumeración de esta sección **es taxativa**. Enunciar que "todas las consultas
> filtran `deleted_at`" **sería falso**.

En lugar de una regla cómoda y mentirosa, el documento enumera. **Cinco entidades**
tienen borrado lógico: usuario, dirección de entrega, categoría, producto e
ingrediente. **Dieciocho no lo tienen**, y **seis admiten borrado físico**, cada una
con su razón:

| Entidad | Por qué se puede borrar de verdad |
| --- | --- |
| `ProductoCategoria`, `ProductoIngrediente` | **Ningún pedido las referencia** |
| `ProductoImagen` | La galería es del producto; nada más la apunta |
| `IntentoAcceso`, `ClaveIdempotencia`, `EventoSalida` | Tienen **purgas de retención declaradas** |

Y una frase que resume la política: **"Las entidades de negocio no se borran nunca,
y `UsuarioRol` tampoco: su baja es una revocación lógica."**

> **💡 PARA ENTENDER**
> Esa frase esconde una distinción que vale para cualquier sistema que hagas:
>
> **Hay datos que describen cómo son las cosas, y datos que registran qué pasó.**
>
> Un producto **describe**: su precio es el de hoy, y si mañana cambia, el de hoy ya
> no importa. Se puede modificar y —con cuidado— se puede dar de baja.
>
> Un pedido **registra**: es el hecho de que alguien compró algo un martes a las
> ocho. Ese hecho ocurrió, y **no hay ninguna operación futura que pueda hacer que no
> haya ocurrido.** Modificarlo no es corregir un dato: es falsificar la historia.
>
> Por eso el TPI no borra pedidos ni movimientos de stock, y por eso RN-03 dice que
> el historial es de **sólo agregado**. Cancelar un pedido no lo borra: **agrega un
> registro que dice que se canceló.**
>
> Cuando modeles algo, la pregunta es esa: **¿esto describe o registra?** Lo que
> registra no se toca. Y si tenés que "corregir" un registro, lo correcto casi
> siempre es agregar otro que lo compense, no editar el que está.

Lo más interesante viene después. El TPI enumera **cinco excepciones de lectura**
—también taxativas—: casos donde una consulta **no filtra** las filas borradas. Tres
merecen comentario porque cada una enseña algo distinto.

**La lectura histórica.** Al abrir un pedido viejo, la resolución del producto de
cada línea **no filtra**: un producto retirado del catálogo **sigue siendo legible
desde un pedido anterior**. Es la contracara de la primera redundancia: el snapshot
conserva el nombre y el precio, y esta excepción permite además llegar al producto.

**La confirmación de pedido.** La revalidación de stock consulta sin filtrar, y el
TPI da la razón: **necesita distinguir "eliminado" de "sin stock"** para devolver el
error correcto. Filtrar haría que un producto borrado se reportara como faltante, y
el usuario recibiría un mensaje equivocado.

**El árbol de categorías.** Esta es la más sutil y vale la pena detenerse. El cálculo
de profundidad de una categoría recorre sus ancestros **sin filtrar**, porque —en
palabras del TPI— *"si filtrara, una rama con un ancestro eliminado parecería más
corta de lo que es y admitiría un nivel de más"*. No es una excepción por comodidad:
**filtrar produciría un resultado incorrecto.**

Y un detalle final que conviene conocer: **ninguna entidad con borrado lógico tiene
endpoint de restauración.** Revertir un borrado accidental es una operación de base
de datos, hecha a mano por quien tenga acceso.

> **⚠️ OJO ACÁ**
> El borrado lógico tiene una trampa que se descubre siempre tarde, y es esta:
>
> **Un índice único común rompe el borrado lógico.**
>
> Pensalo. Tenés `UNIQUE(email)` en usuarios. Alguien se da de baja —su fila queda
> con `deleted_at` cargado— y después quiere volver a registrarse con el mismo
> correo. **La base lo rechaza**, porque para el índice único esa fila sigue estando.
>
> Y el mensaje que te llega es *"el email ya existe"*, cuando en la aplicación ese
> usuario no existe. Vas a buscarlo, no aparece en ningún listado, y no entendés nada.
>
> La solución es un **índice único parcial**, que PostgreSQL sí soporta:
>
> ```sql
> CREATE UNIQUE INDEX ux_usuario_email_activo
>   ON usuario (email) WHERE deleted_at IS NULL;
> ```
>
> Así la unicidad aplica **sólo entre los vivos**. Por eso el TPI declara que usa
> índices únicos parciales, y por eso ese detalle está en el stack: **no es un lujo,
> es lo que hace que el borrado lógico funcione.**

---

## 4.10. Índices y restricciones

Un índice es una estructura auxiliar que permite encontrar filas sin recorrer la
tabla entera. El TPI declara **treinta y uno**, cada uno con su motivo, y esa
enumeración explícita es coherente con el resto del documento: **un índice sin motivo
declarado es un costo sin beneficio conocido**, porque cada índice hace más lentas
las escrituras.

Los tres criterios que justifican la mayoría:

**Las claves foráneas se indexan.** Sin índice, buscar los pedidos de un usuario
recorre la tabla de pedidos completa. PostgreSQL **no crea ese índice
automáticamente**, a diferencia de otros motores.

**Lo que se filtra u ordena seguido se indexa.** Si el listado de productos ordena
por fecha de creación, esa columna necesita índice.

**La unicidad de negocio se declara como restricción.** Que un correo no se repita no
es algo que el Service deba verificar: es algo que la base debe impedir. Verificar en
el Service **deja una ventana** entre la comprobación y la inserción, y en esa
ventana otra petición puede insertar el mismo valor.

Y las **comprobaciones** —los `CHECK`— son el otro mecanismo declarativo, el que la
sección 4.8 usa como garante de tres de las cinco redundancias. Una comprobación de
que el total es igual al subtotal menos el descuento más el envío **se cumple
siempre**, venga la escritura de donde venga. Su límite es el que el TPI señala: **no
puede cruzar tablas.**

---

## 4.11. Migraciones

El esquema de la base cambia con el tiempo, y ese cambio necesita las mismas
garantías que el código: quedar registrado, revisarse, aplicarse en orden y poder
reproducirse en otra máquina.

**Alembic** resuelve eso con migraciones versionadas: cada cambio es un archivo con
su función de aplicación y su función de reversión, y cada uno declara a cuál sigue.
El TPI exige inicializarlo con la plantilla asincrónica, coherente con EA-03.

Alembic puede **generar** una migración comparando los modelos con el esquema
actual. Y acá va la advertencia que el TPI convierte en práctica obligatoria:

**Una migración generada se lee antes de aplicarse.** Siempre. La comparación
automática es buena y no es perfecta: no detecta bien los renombres —los ve como
borrar una columna y crear otra, **lo que pierde los datos**—, ni los cambios de
tipo que exigen conversión, ni las restricciones parciales de la sección 4.9.

El TPI ubica al migrador como el **primero de sus ocho servicios**, con una regla
que la clase 1 ya mencionó: corre una vez, termina, y **si falla, ningún otro
proceso debe arrancar**.

*(Ver Figura 4.6: una migración generada, con lo que hay que revisar señalado.)*

> **🧪 EXPERIMENTO**
> Este experimento demuestra por qué una migración se lee antes de aplicarse, y es
> mejor comerse el susto acá que en producción.
>
> 1. Creá un modelo con un campo `nombre` y generá la migración. Aplicala.
> 2. Insertá tres filas con datos.
> 3. Ahora **renombrá** el campo a `nombre_completo` en el modelo y generá la
>    migración de nuevo.
> 4. **Abrí el archivo generado y leelo antes de aplicar nada.**
>
> Vas a ver `drop_column('nombre')` seguido de `add_column('nombre_completo')`.
>
> Eso no es un renombre: **es borrar los datos y crear una columna vacía.** Si lo
> aplicás, tus tres filas pierden el nombre para siempre.
>
> 5. Corregí la migración a mano por `alter_column` con `new_column_name`, aplicala,
>    y verificá que los datos siguen.
>
> La herramienta no se equivocó: **comparó dos esquemas y no puede adivinar tu
> intención.** Vos sabés que renombraste; ella ve una columna que ya no está y otra
> que apareció.

---

## 4.12. Herramientas de diagnóstico

**El registro de sentencias del motor** es la herramienta central de este capítulo.
Activándolo se ve **cada consulta que el ORM emite**, y eso responde la pregunta que
un ORM vuelve difícil: qué SQL produjo realmente el código que se escribió. Es la
forma de verificar que una consulta con precarga emite dos sentencias y no ciento
una.

**El plan de ejecución** —lo que devuelve `EXPLAIN ANALYZE`— muestra cómo el motor
resolvió una consulta: si usó un índice o recorrió la tabla entera, y cuánto tardó
cada paso. Es lo que hay que mirar cuando una consulta es lenta, antes de agregar
índices a ciegas.

**El estado del pool** dice cuántas conexiones están en uso. Si está lleno de forma
sostenida, el problema es el de la sección 3.11.

**Un cliente de base de datos** —cualquiera que muestre el esquema— sirve para
verificar que una migración hizo lo que se esperaba: que el índice existe, que la
comprobación está declarada, que el tipo es el correcto.

*(Ver Figura 4.5: el esquema de un dominio visto desde un cliente.)*

Y una verificación específica de este capítulo: **contar las consultas de un
endpoint.** Con el registro activado, pedir un listado de veinte elementos y contar
las sentencias emitidas. Si son dos o tres, la precarga está bien declarada. Si son
veintiuna, falta.

---

## 4.13. Seguridad y evolución

Tres consideraciones cierran el capítulo.

**Los dos roles de base de datos.** El TPI declara que el sistema usa **dos roles**:
un propietario, que es el único que aplica migraciones y puede alterar el esquema, y
un rol de aplicación, que sólo puede leer y escribir datos. Esa separación tiene una
consecuencia concreta: **aunque el código de la aplicación sea comprometido, no puede
alterar el esquema ni borrar tablas.** Y es además uno de los dos mecanismos que
garantizan las tablas de sólo agregado de RN-03: el rol de aplicación **no tiene
permiso** de actualizar ni borrar sobre ellas.

**Los datos personales tienen requisitos propios.** Un correo, una dirección y un
teléfono son datos personales, y el borrado lógico de la sección 4.9 **conserva esos
datos**. Es una decisión legítima —hay razones de trazabilidad— y conviene saber que
existe una tensión con las normativas de protección de datos, que en general
reconocen un derecho a la supresión.

**El esquema es una superficie de ataque indirecta.** Un mensaje de error que revela
nombres de tablas y columnas le entrega a un atacante el mapa del sistema. Es otra
razón del manejador global de errores que la clase 8 estudia.

Sobre la evolución, dos observaciones. La primera es que **el modelo relacional lleva
más de cincuenta años** y las alternativas que iban a reemplazarlo terminaron
conviviendo con él. La razón es la de la sección 4.2: las garantías declaradas —las
restricciones y las transacciones— son difíciles de reponer en la aplicación, y casi
siempre se reponen peor.

La segunda es que PostgreSQL viene incorporando capacidades que antes obligaban a
sumar otro motor: documentos JSON con índices, búsqueda de texto, tipos geométricos.
Eso hace más defendible la decisión del TPI de tener **un solo almacén durable**, que
es siempre más simple de operar que dos.

---

## 4.14. Verificación

1. Traducir un diagrama con las tres relaciones de POO a un esquema, **justificando
   dónde va cada clave foránea** y qué comportamiento de borrado corresponde.
2. Declarar una relación uno a uno y **verificar que sin la restricción de unicidad
   no lo es**.
3. Provocar la excepción de la sección 3.8 olvidando la precarga, y corregirla.
4. Contar con el registro de sentencias las consultas que emite un listado de veinte
   elementos, **con y sin precarga**.
5. Comparar `selectinload` y `joinedload` en una colección, y **contar las filas
   transferidas** por cada uno.
6. Quitar `expire_on_commit=False` y **reproducir el error** que EA-04 previene.
7. Identificar en el TPI las cinco redundancias y **nombrar el garante de cada una**.
8. Crear un usuario, darlo de baja lógicamente, e intentar registrar el mismo correo.
   **Corregirlo con un índice único parcial.**
9. Generar la migración de un renombre y **encontrar el problema antes de aplicarla**.

---

## 4.15. Errores frecuentes

**Poner la clave foránea del lado equivocado.** En una relación uno a muchos vive en
el lado "muchos", al revés de lo que sugiere el diagrama de clases (sección 4.3).

**Declarar uno a uno sin restricción de unicidad.** Sin ella es uno a muchos con un
solo elemento por casualidad (sección 4.3).

**Usar el modelo de tabla como schema de entrada y de salida.** Son cosas distintas
por las tres razones de la clase 2 (sección 4.4).

**Olvidar `expire_on_commit=False`.** El objeto queda expirado tras el commit y la
primera lectura falla. Viola EA-04 (sección 4.5).

**Declarar la relación y no precargarla.** Declarar no es cargar: acceder lanza la
excepción de greenlet. Viola EA-05 (sección 4.6).

**Usar `joinedload` para una colección grande.** Devuelve los datos del padre
repetidos una vez por hijo (sección 4.6).

**Desnormalizar sin garante.** Una redundancia sin restricción ni prueba es una
inconsistencia esperando ocurrir (sección 4.8).

**Suponer que todas las consultas filtran el borrado lógico.** El TPI enumera cinco
excepciones taxativas, y tres de ellas son de corrección y no de comodidad (sección
4.9).

**Declarar un índice único común sobre una tabla con borrado lógico.** Impide reusar
un valor de una fila dada de baja. Corresponde un índice parcial (sección 4.9).

**Verificar la unicidad en el Service.** Deja una ventana entre la comprobación y la
inserción (sección 4.10).

**Aplicar una migración generada sin leerla.** La comparación automática ve un
renombre como borrar y crear, **lo que pierde los datos** (sección 4.11).

**Olvidar el índice de una clave foránea.** PostgreSQL no lo crea solo (sección
4.10).

---

## 4.16. Actividades

1. **Del diagrama al esquema.** Tomar el dominio de catálogo del TPI —producto,
   categoría, ingrediente y sus vínculos— y escribir sus modelos completos con
   relaciones, comportamiento de borrado e índices. Justificar cada decisión contra
   las actividades 5 y 6 de POO.

2. **Las consultas contadas.** Implementar un endpoint que liste pedidos con su
   usuario y sus líneas. Medir con el registro de sentencias cuántas emite sin
   precarga, con `selectinload` y con `joinedload`, y **documentar además las filas
   transferidas** en cada caso.

3. **Las cinco redundancias.** Para cada una de las cinco que el TPI declara,
   documentar qué duplica, qué la garantiza, y **qué pasaría si esa garantía no
   existiera**. Proponer para la cuarta —el monto del pago— una forma de detectar la
   inconsistencia si la prueba no existiera.

4. **El índice parcial.** Implementar borrado lógico sobre usuarios con unicidad de
   correo. Demostrar el problema con un índice único común y resolverlo con uno
   parcial. Verificar los dos casos: registrar un correo dado de baja, y no poder
   duplicar uno activo.

5. **Migraciones que se leen.** Generar tres migraciones —agregar columna, renombrar
   columna y cambiar un tipo con conversión— y documentar para cada una qué generó la
   herramienta, qué hacía falta corregir y por qué.

6. **Exploración: qué esconde el ORM.** Escribir cinco operaciones habituales
   —insertar, actualizar, borrar, listar con filtro y navegar una relación— y
   capturar el SQL que cada una emite. Documentar los casos donde el SQL sorprendió,
   y relacionar lo observado con la afirmación de la sección 4.2 sobre que el ORM no
   elimina el desajuste sino que lo esconde.

7. **Exploración: el plan de ejecución.** Sobre una tabla con varios miles de filas
   de prueba, ejecutar una consulta filtrada por una columna sin índice y capturar su
   plan. Agregar el índice, repetir, y comparar. Documentar qué cambió en el plan y
   cuánto en el tiempo, y explicar por qué el TPI declara el motivo de cada uno de sus
   treinta y un índices. *(Requiere una base con datos de prueba.)*

---

## 4.17. Síntesis

1. El modelo relacional separó **cómo se guardan los datos de cómo se consultan**, y
   de esa separación salen las garantías que el resto del módulo da por sentadas: las
   restricciones declaradas y las transacciones.

2. **Un ORM no elimina el desajuste objeto-relacional: lo esconde.** La diferencia
   más costosa es que en objetos navegar es gratis y contra una base **cada
   navegación es una consulta**.

3. La clave foránea vive **del lado "muchos"**, al revés de lo que sugiere el
   diagrama de clases, porque una columna guarda un valor y no una lista.

4. **La diferencia entre agregación y composición no está en la clave foránea sino en
   qué pasa al borrar**, y en este sistema esa cascada casi nunca se ejecuta porque
   las entidades de negocio no se borran.

5. `expire_on_commit=False` **no es una optimización**: sin él, la primera lectura
   después del commit intenta emitir entrada y salida donde no puede.

6. **Declarar una relación no la carga.** La precarga se declara por consulta, y la
   tabla del TPI es una condición para que el endpoint funcione, no una guía de
   rendimiento.

7. Normalizar es la regla, y el TPI la rompe **cinco veces con criterio declarado**.
   Lo que separa una redundancia de un descuido es que **ninguna queda sostenida sólo
   por la disciplina del Service**: cada una tiene una restricción o una prueba.

8. El **snapshot de línea** no es una optimización sino una necesidad del dominio: sin
   él, cambiar un precio reescribiría la historia.

9. El TPI **enumera** en vez de generalizar, y lo dice: afirmar que "todas las
   consultas filtran el borrado lógico" **sería falso**. Tres de sus cinco excepciones
   son de corrección, no de comodidad.

10. **Un índice único común rompe el borrado lógico.** El índice parcial es lo que
    hace que las dos cosas convivan.

11. **Una migración generada se lee antes de aplicarse**: la comparación automática
    ve un renombre como borrar y crear, y eso pierde los datos.

---

## 4.18. Referencias y lecturas complementarias

La fuente fundacional del modelo relacional es el artículo de E. F. Codd *A
Relational Model of Data for Large Shared Data Banks* (Communications of the ACM,
1970), de lectura sorprendentemente accesible y que muestra con claridad qué problema
se estaba resolviendo. El lenguaje de consulta está normado en **ISO/IEC 9075**, aunque
en la práctica la referencia útil es la documentación del motor: la de **PostgreSQL**,
en `postgresql.org/docs`, es de las mejores de su categoría y sus capítulos sobre
índices, restricciones y niveles de aislamiento cubren todo lo de las secciones 4.9 y
4.10, además de anticipar la clase 6.

Para las herramientas, la documentación de **SQLAlchemy** sobre estrategias de carga
de relaciones es la fuente directa de la sección 4.6, y explica en detalle cuándo
conviene cada estrategia y por qué. La de **SQLModel** en `sqlmodel.tiangolo.com`
cubre la unión de los dos mundos de la sección 4.4, y la de **Alembic** documenta las
limitaciones de la comparación automática que la sección 4.11 convierte en práctica
obligatoria.

Como bibliografía de estudio, Fowler, *Patterns of Enterprise Application
Architecture* (Addison-Wesley, 2002) es donde quedaron nombrados los patrones de
acceso a datos que la clase 6 va a usar, y su capítulo sobre mapeo objeto-relacional
enuncia el desajuste de la sección 4.2 con más rigor que la mayoría de los textos
posteriores. Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017)
dedica su segundo capítulo a la comparación entre modelos de datos y responde con
honestidad por qué el relacional sobrevivió a sus reemplazos anunciados. Y para la
práctica cotidiana de escribir consultas que el motor pueda optimizar, Winand, *SQL
Performance Explained* (2012, con contenido libre en `use-the-index-luke.com`) es la
mejor introducción a los índices que existe, y explica los planes de ejecución de la
sección 4.12 desde el problema y no desde la herramienta.

Del TPI, este capítulo se apoya en la sección **3** completa —sus nueve subsecciones,
de las que la **3.7** y la **3.8** son las que más discusión merecen en clase—, en la
**8.3** por su tabla de precarga, y en la **16.1** por las variables de conexión que
la sección 4.5 usa.

---

**Continúa en:** Capítulo 5 — Autenticación y autorización, donde el token que la
otra mitad de la cursada aprende a guardar esa misma semana se emite y se verifica de
este lado, y donde bcrypt obliga a aplicar EA-02 y EA-06 sobre un caso real.
