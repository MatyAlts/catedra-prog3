# Backend desde POO — temario del módulo

Módulo de **8 clases de 4 horas** (32 h) que lleva al alumno desde haber terminado
POO en Python hasta poder encarar el backend del **TPI Food Store** trabajando con
agentes de IA.

Se dicta **en paralelo** con el módulo de frontend, dentro de la misma cursada de
Programación III: los alumnos tienen medio día con cada docente. Este temario está
diseñado para que esa simultaneidad sea una ventaja y no una coincidencia — ver
[§ Sincronización](#sincronización-con-el-módulo-de-frontend).

> **Versión 2.** El orden se ajustó a pedido del docente de backend, para adelantar
> los schemas y seguir la línea del temario oficial. Ver
> [§ Relación con el temario oficial](#relación-con-el-temario-oficial).

---

## Punto de partida: lo que ya traen

El módulo arranca donde terminan las ocho actividades de POO en Python, que
hicieron la transición desde Java:

| # | Actividad de POO | Lo que habilita en este módulo |
| --- | --- | --- |
| 1 | El cambio de mentalidad y la tabla de equivalencias | Leer código Python idiomático sin traducirlo mentalmente a Java |
| 2 | La property: del getter preventivo al acceso por atributo | Los modelos de SQLModel y los validadores de Pydantic |
| 3 | Lo que se traduce mal y las trampas que Java no enseña a ver | Los errores propios de Python que el ORM amplifica |
| 4 | Duck typing, `Protocol` y los regalos que Java no tiene | **El repositorio como `Protocol`**, y los puertos de caché y eventos |
| 5 | La clase única y la asociación (1 a 1 y 1 a muchos) | Las claves foráneas y las relaciones del modelo de datos |
| 6 | Agregación y composición | **El Unit of Work compone repositorios**; el pedido compone sus líneas |
| 7 | Clase abstracta y herencia | La clase base de repositorio genérico y la de servicio |
| 8 | Dependencia de uso y de creación; interfaces con ABC y `Protocol` | **La inyección de dependencias de FastAPI.** `Depends()` es esto |

**La octava actividad es el puente.** Lo que ahí se llamó "dependencia de uso
contra dependencia de creación" es, literalmente, la diferencia entre un servicio
que construye su propio repositorio y uno que lo recibe. FastAPI lo resuelve con
`Depends()`, y el TPI lo exige en su sección 2.1: el Router **no construye** el
Unit of Work, lo recibe y lo transporta.

**Lo que no traen y este módulo tiene que enseñar entero:** asincronía, HTTP del
lado del servidor, persistencia relacional, transacciones, concurrencia y testing
asincrónico.

---

## Punto de llegada

Poder leer `docs-tpi/02-backend/`, entender las **37 reglas declaradas** del
backend, y dirigir a un agente de IA para implementarlas sabiendo qué pedir y
—sobre todo— **por qué lo que el agente responda puede estar mal**.

Son tres familias, y conviene tenerlas separadas desde el principio:

| Familia | Cuántas | Dónde las declara el TPI | De qué tratan |
| --- | --- | --- | --- |
| **RN-01 a RN-22** | 22 | Sección 3.9 y a lo largo del documento | Reglas de negocio: qué puede y qué no puede pasar en el dominio |
| **EA-01 a EA-08** | 8 | **Todas en la sección 1.4** | Ejecución asincrónica: qué no se puede hacer dentro de un bucle de eventos |
| **TB-01 a TB-07** | 7 | **Todas en la sección 10.1** | Trabajo diferido: qué debe cumplir una tarea de la cola |

A eso se suman los **50 casos de prueba obligatorios** (TST-01 a TST-50) de la
sección 15.2, que son el garante declarado de buena parte de las reglas.

Para comparar: el módulo de frontend cubre once reglas. **Este cubre treinta y
siete.** No es que el backend sea "más difícil": es que tiene más superficie donde
equivocarse, y el documento lo reconoce declarando cada caso.

## La tensión que ordena el módulo

El TPI pide **FastAPI con todos los handlers asincrónicos, SQLModel sobre
SQLAlchemy 2.0 asincrónico, PostgreSQL como único almacén durable, Redis como
almacén efímero, taskiq para el trabajo diferido y SSE para el tiempo real.**
Diecinueve tecnologías.

Esa decisión tiene una consecuencia que gobierna el módulo entero: **todo es
asincrónico, y en un bucle de eventos una sola llamada bloqueante detiene el
servidor completo.** No lo hace lento: lo detiene, para todos los usuarios a la
vez. La sección 1.4 del TPI le dedica varias páginas, y de ahí sale la exigencia
de la sección 5.5 —bcrypt fuera del bucle— que a primera vista parece un capricho.

Cada tema se enseña respondiendo la misma pregunta que el módulo de frontend:

> ¿Qué problema real apareció, que hizo falta inventar esto?

---

## Recorrido

| # | Clase | Del TPI habilita | Unidad oficial | Reglas |
| --- | --- | --- | --- | --- |
| 1 | Del objeto al servicio: HTTP del lado del servidor y el primer endpoint | 2.1, 2.2, 2.3 | 3.1 | anticipo de EA-01 |
| 2 | **Contratos: schemas, validación y CRUD** | 6.1, 7, 14.1 | 3.2 · 3.3 | — |
| 3 | El bucle de eventos del servidor: asincronía y la regla del greenlet | **1.4**, 5.5 | *(no figura)* | **EA-01 a EA-08** |
| 4 | Persistencia: SQLModel, PostgreSQL y el modelo de datos | 3.1–3.8, 16.1 | 4.1 · 5.1 | RN-02, RN-04; se cobran EA-04, EA-05, EA-08 |
| 5 | Autenticación y autorización: JWT, RBAC y bcrypt | 5.1–5.5 | 8 · 7-bis | se cobra EA-02 y EA-06 |
| 6 | Repositorios, Unit of Work y transacciones | 8.3, 8.4 | *(no figura)* | RN-03 |
| 7 | El corazón transaccional: pedidos, stock, concurrencia e idempotencia | 8.1, 8.2, 9, 3.4, 3.5 | *(no figura)* | RN-01, RN-05 a RN-13, **RN-18** |
| 8 | Robustez y más allá de la petición | 4, **10.1**, 11, 12, 14.2, 15, 16 | 9 | **TB-01 a TB-07**, RN-19 a RN-22 |

Las tres familias quedan cubiertas, y **dos clases concentran una familia entera**:
la clase 3 funda las ocho reglas de ejecución asincrónica —que el TPI declara todas
juntas en su sección 1.4— y la clase 8 funda las siete del trabajo diferido.

**Ninguna regla se enuncia sin haber enseñado antes el problema que la origina.**
EA-05 no se entiende sin haber visto explotar una carga perezosa en contexto
asincrónico; RN-18 no se entiende sin haber provocado un interbloqueo; TB-02 no se
entiende sin haber visto una tarea ejecutarse dos veces. Y **el Unit of Work no se
presenta hasta la clase 6**, cuando el alumno ya escribió operaciones que quedan a
medio aplicar y sabe por qué duele.

---

## Relación con el temario oficial

Este módulo sigue la línea de `Temas-Programación 4-2026.docx`, con tres salvedades
que conviene tener explícitas antes de empezar a escribir. La tercera es la que hay
que conversar con el director: **no son diferencias de criterio entre docentes, sino
dos documentos que describen sistemas distintos.**

### Primera: el orden, que es el cambio pedido

El temario oficial introduce Pydantic en su unidad 3.2, **inmediatamente después
del entorno**, y recién persiste en la unidad 4. Este módulo adopta ese orden: la
clase 2 son los contratos y un CRUD en memoria, y la persistencia llega en la
clase 4.

Es el cambio que pidió el docente de backend, y **además mejora la sincronización
con frontend**: cuando esa mitad de la cursada llega a tipar el contrato en su
semana 6, el contrato lleva cuatro semanas publicado y corriendo.

### Segunda: lo que el temario oficial no cubre y el TPI exige

Tres clases enteras de este módulo no tienen correspondencia en el documento
oficial. No son agregados por gusto: sin ellas, buena parte del TPI queda sin
fundamento.

| Clase | Por qué está igual |
| --- | --- |
| **3 — Asincronía y bucle de eventos** | El TPI declara ocho reglas —EA-01 a EA-08— y exige `async def` en **todos** los handlers. Sin esta clase, las ocho quedan sin fundar |
| **6 — Repositorios y Unit of Work** | Es una capa obligatoria del flujo `Router → Service → UoW → Repository → Model` que declara la sección 2.1 |
| **7 — Stock, concurrencia e idempotencia** | Es la sección 9 completa, más RN-18 y la clave de idempotencia que el frontend genera del otro lado |

### Tercera: tres puntos donde se contradicen

Estos no son matices de énfasis sino **decisiones incompatibles**, y conviene
resolverlos entre los dos docentes antes de escribir el material:

| Punto | Temario oficial | TPI Food Store |
| --- | --- | --- |
| Sesión de base de datos | `Session` sincrónica | **`AsyncSession`** — EA-04 lo declara explícitamente, con `expire_on_commit=False` |
| Cliente de tests | `TestClient` | **`httpx.AsyncClient`** sobre `ASGITransport`. El TPI aclara que **`TestClient` no se puede usar dentro de una función asincrónica** |
| Verbo de actualización | `PUT` | **`PATCH`, y `PUT` no se usa.** La sección 6.1 es explícita: *"PATCH modifica de forma parcial y es el verbo de toda actualización. No se usa PUT: ningún endpoint reemplaza el recurso completo"* |

Este material sigue al **TPI**, porque es el documento contra el que se evalúa el
trabajo integrador. Donde el temario oficial dice `Session`, acá se enseña
`AsyncSession` y se explica por qué.

Conviene que los dos docentes lo sepan, y que el alumno también: **va a ver
`Session` y `TestClient` en tutoriales y en la mitad de internet, y en este
proyecto no se usan.** Decirlo explícitamente evita la confusión de quien busca
ayuda afuera y encuentra ejemplos que acá no aplican.

### Una nota menor sobre el documento

El archivo se titula *Programación 4* y describe una cursada **fullstack
integrada**, donde un mismo docente da las dos mitades —incluye React, TanStack
Query y React Router, que en el TPI están descartados por la regla de "sin
framework de interfaz"—. Su numeración interna tiene además algunos saltos: la
unidad 3 pasa de "3.2" a "4.3", y hay dos unidades numeradas 7.

Para este temario se interpretó **la secuencia de los encabezados**, no los
números, y se tomó únicamente la mitad de backend. Vale confirmarlo con quien lo
redactó.

---

## Sincronización con el módulo de frontend

Los dos módulos se dictan la misma semana. Cinco semanas tienen **encuentro
temático**: el mismo concepto, enseñado de los dos lados del cable, el mismo día.

| Sem | Frontend (mañana) | Backend (tarde) | Encuentro |
| --- | --- | --- | --- |
| **1** | La web como plataforma: HTTP, el navegador y el documento | Del objeto al servicio: HTTP del lado del servidor | **Los dos lados de la misma petición** |
| **2** | CSS: caja, flujo y cascada | **Contratos: schemas, validación y CRUD** | El backend **publica el contrato** que el frontend va a consumir |
| **3** | JavaScript y el bucle de eventos | El bucle de eventos del servidor | **El mismo concepto, dos lenguajes** |
| 4 | El DOM sin framework | Persistencia y modelo de datos | Complementarias |
| **5** | Asincronía y red: `fetch`, errores, SSE | Autenticación: JWT, RBAC, bcrypt | **El token, emitido y consumido** |
| **6** | TypeScript y el contrato de la API | Repositorios, Unit of Work y transacciones | El frontend tipa **contra una API que ya existe** |
| 7 | Herramientas y componentes | Pedidos, stock, concurrencia, idempotencia | Frontend genera la clave, backend la reconoce |
| 8 | Arquitectura: FSD, estado y cierre | Robustez, Redis, tareas, eventos y despliegue | Los dos cierran sobre el sistema completo |

**Semana 1.** El frontend estudia la anatomía de una petición y termina leyendo una
fila de la sección 6 del TPI. El backend construye el endpoint que responde esa
misma fila. **La misma tabla, los dos lados.**

**Semana 2.** El backend define los schemas y publica un CRUD funcionando. Es la
semana en que la especificación de OpenAPI **deja de ser un plan y pasa a ser algo
que se abre en el navegador**. El frontend está en CSS y todavía no la necesita, y
por eso esta es la ubicación correcta: cuando la necesite, va a estar lista hace un
mes.

**Semana 3.** El frontend explica que un solo hilo ejecuta y dibuja, y que
bloquearlo mata la página. El backend explica que un solo bucle de eventos atiende
todas las peticiones, y que bloquearlo mata el servidor **para todos**. Es el mismo
modelo mental, y verlo dos veces el mismo día lo fija de una vez. **Conviene que
los dos docentes usen el mismo dibujo.**

**Semana 5.** El frontend enseña dónde guardar el token, por qué ninguna opción es
gratis y por qué **las guardas de ruta son usabilidad y no seguridad** (RN-F04). El
backend enseña cómo se emite y verifica ese token, y por qué el servidor revalida
siempre. Los garantes de RN-F04 —TST-06, TST-07 y TST-27— **ejercitan el backend
salteándose la interfaz**: esa semana los alumnos ven por qué.

**Semana 6.** El frontend traduce los esquemas de la sección 7 a tipos de
TypeScript. Y acá está el beneficio de haber adelantado los schemas: **cuando el
frontend llega a tipar el contrato, ese contrato lleva cuatro semanas implementado
y corriendo.** No tipa contra una tabla del documento: tipa contra la especificación
real que el backend publica. Si algo no coincide, se descubre esa semana y no en la
integración.

**Una desincronización asumida.** El frontend consume SSE en la semana 5 y el
backend lo produce en la semana 8. No es un problema sino el orden correcto: el
consumidor puede trabajar contra un servidor simulado, y cuando el backend lo
construye, el frontend ya sabe qué esperar. Conviene que los dos docentes lo digan
en voz alta.

---

## Clase 1 — Del objeto al servicio

**Puente con POO.** La actividad 8 —dependencia de uso contra dependencia de
creación, interfaces con ABC y `Protocol`— es la base conceptual de todo lo que
sigue. Un servicio que construye su propio repositorio no se puede probar sin base
de datos; uno que lo recibe, sí. `Depends()` es exactamente eso, y el TPI lo exige:
el Router **no construye** el Unit of Work.

**Génesis.** Por qué un servidor necesita atender a muchos a la vez, y las tres
respuestas históricas: un proceso por conexión, un hilo por conexión —y el problema
C10K de 1999— y un solo hilo con multiplexación. Qué papel juega el bloqueo global
del intérprete. De dónde salen WSGI y ASGI, y por qué hizo falta un contrato nuevo.

**Contenido.** El ciclo petición-respuesta desde el servidor. ASGI: qué recibe y
qué devuelve una aplicación. El primer endpoint con `async def`, la generación
automática de OpenAPI, y por qué una especificación derivada del código no puede
desactualizarse. Parámetros de ruta y de consulta. **Inyección de dependencias con
`Depends()`**, y su relación con la actividad 8. Dependencias con recursos y ciclo
de vida (EA-08). Las capas del TPI y la regla de dependencias de la sección 2.1.
**Por qué Redis no es una capa sino un adaptador.** Los ocho servicios (2.2) y los
doce módulos (2.3).

## Clase 2 — Contratos: schemas, validación y CRUD

**Ubicación.** Esta clase estaba originalmente sexta y **se adelantó a pedido del
docente de backend**, siguiendo la línea del temario oficial y porque adelantarla
mejora la sincronización con el módulo de frontend.

**Génesis.** Qué es un contrato entre dos sistemas y por qué escribirlo aparte del
código lo condena a desactualizarse. De dónde viene la validación declarativa: por
qué conviene enunciar las restricciones antes que programarlas, y qué se gana
cuando esa declaración además genera documentación. Por qué el modelo de entrada y
la tabla no son la misma cosa.

**Contenido.** `BaseModel` para contratos de entrada y de salida. Validaciones:
límites numéricos, longitudes, patrones. Tipado con `Annotated` y `Field`, `Path`,
`Query`; enumeraciones para valores cerrados —lo que del otro lado se llama unión
literal—. **Modelos segregados**: `Create`, `Update` y `Public`, y por qué son tres
y no uno. `response_model` y el control de lo que sale. CRUD completo en memoria,
sin base de datos todavía. Errores con `HTTPException` y códigos de estado
correctos. Las convenciones globales de la sección 6.1 del TPI: versionado,
paginación, ordenamiento y formato de error. El catálogo de la sección 14.1 y por
qué un código estable vale más que un mensaje.

**El dinero, primera aparición.** El importe se declara con un tipo decimal exacto
y **viaja como cadena**. Es la mitad de arriba de RN-F08, que el frontend estudia
desde el otro lado esa misma cursada.

**Seguridad y evolución.** Un modelo de salida mal armado expone campos que no
deberían viajar; un mensaje de error mal armado, también.

## Clase 3 — El bucle de eventos del servidor

**Génesis.** De los callbacks a `asyncio`: qué problema resolvió cada paso.
Corrutinas contra hilos. Por qué `async`/`await` llegó al lenguaje en 3.5 y qué
había antes. `TaskGroup` y `except*` (3.11), que son la razón por la que el TPI
fija Python 3.12 como piso.

**Contenido.** El bucle de eventos: qué hace realmente. Corrutinas, tareas y
`await`. Concurrencia contra paralelismo —la misma distinción que el frontend ve
esa semana—. **Qué bloquea el bucle**: entrada/salida sincrónica, cálculo intensivo,
`time.sleep`. `asyncio.to_thread` y `anyio.to_thread.run_sync`. **La regla del
greenlet** de la sección 1.4: por qué un acceso a un atributo diferido puede
explotar en contexto asincrónico. Anticipo de la sección 5.5: bcrypt está
**diseñado** para consumir procesador, y por eso sale del bucle con un semáforo.

**Las ocho reglas EA.** El TPI las declara juntas en esa misma sección 1.4, y esta
clase las funda todas: handlers siempre asincrónicos (EA-01), nada bloqueante
dentro de una corrutina (EA-02), clientes asincrónicos para toda entrada/salida
(EA-03), la sesión sin expiración al hacer commit (EA-04), la carga perezosa
prohibida (EA-05), nada de trabajo de procesador sin ceder (EA-06), nada de tareas
sueltas con `create_task` (EA-07), y el pool y el cliente creados en el ciclo de
vida (EA-08).

**Seguridad y evolución.** Una operación bloqueante es una denegación de servicio
sin atacante.

## Clase 4 — Persistencia: SQLModel, PostgreSQL y el modelo de datos

**Génesis.** Por qué los datos duraderos viven en un motor relacional y no en
objetos serializados. El **desajuste objeto-relacional**: un objeto tiene
identidad, referencias y herencia; una tabla tiene claves, filas y tipos. Qué
resuelve un ORM y —lo más importante— **qué esconde**. Qué es SQLModel y por qué
une dos cosas que en la clase 2 estaban separadas.

**Contenido.** `create_async_engine` y
`async_sessionmaker(expire_on_commit=False)` —y por qué ese valor **no es una
optimización** sino EA-04—. De las relaciones de las actividades 5 y 6 al esquema:
asociación, agregación y composición traducidas a claves foráneas y borrado en
cascada. `Relationship` y `back_populates`; 1:1, 1:N y N:N. **Carga anticipada con
`selectinload`** y por qué la perezosa está prohibida (EA-05): acá se cobra la
clase 3. Los tres dominios del TPI y sus 23 entidades. Normalización, y las **cinco
desnormalizaciones declaradas** (3.8), cada una con su garante: RN-04 congela
nombre y precio en la línea del pedido, y hay que entender por qué copiar un dato
puede ser lo correcto. Índices y restricciones de unicidad (3.6), incluidos los
únicos parciales. Soft delete y sus excepciones (3.7). **Alembic**: migraciones
como código versionado, plantilla asincrónica, y por qué una migración se lee antes
de aplicarla.

**Seguridad y evolución.** Los dos roles de base de datos del TPI: el propietario
que migra y el de aplicación que sólo opera.

## Clase 5 — Autenticación y autorización

**Génesis.** Del `Basic` al token: por qué mandar la contraseña en cada petición es
inaceptable. Por qué un protocolo sin estado obliga a que cada petición se baste a
sí misma —el frontend ve exactamente esto la misma semana—. Qué es un JWT, qué
garantiza y qué no. Por qué el hashing de contraseñas es deliberadamente lento, y
por qué MD5 y SHA no sirven para esto.

**Contenido.** El flujo completo de la sección 5.1, paso a paso. Emisión y
verificación con PyJWT. **bcrypt con factor de costo 12, fuera del bucle de eventos
y con semáforo** (sección 5.5): acá se cobran EA-02 y EA-06. RBAC: los cuatro
roles, y las asignaciones **con vigencia** (5.3). Cambio obligatorio de contraseña
(5.4). Límite de intentos y el `429` con `Retry-After`. Dependencias de FastAPI
para exigir rol, y por qué **la autorización se evalúa en el servidor siempre**.

**Seguridad y evolución.** Qué pasa cuando se revoca un rol y hay un token vigente.
El backend no puede invalidar un JWT emitido: de ahí las decisiones de vigencia.

## Clase 6 — Repositorios, Unit of Work y transacciones

**Ubicación.** El Unit of Work llega recién acá **a propósito**: en las clases 4 y 5
el alumno escribió servicios que tocan varias tablas con la sesión directa, y ya se
comió al menos una operación que quedó a medio aplicar. El patrón se presenta
cuando el problema ya duele, que es la regla pedagógica del módulo.

**Génesis.** Por qué el patrón repositorio existe: separar "qué datos necesito" de
"cómo se los pido a este motor". Por qué el Unit of Work existe: un cambio de
negocio casi nunca toca una sola tabla, y las mitades no sirven. Origen de ambos en
Fowler (2002), y qué problema tenían los sistemas que no los usaban.

**Contenido.** Transacciones: ACID en cinco minutos, y qué problema concreto
resuelve cada letra. **El repositorio genérico** de la sección 8.3:
`BaseRepository[T]` y `SoftDeleteRepository[T]`, con `Protocol` —que es la
actividad 4 aplicada—. **El Unit of Work** de la sección 8.4: composición de
repositorios (actividad 6), gestor de contexto asincrónico, commit y rollback
automático al salir. Ciclo de vida de la sesión: una por petición, resuelta por
`Depends`, y por qué **el UoW no la cierra**. **RN-03**:
`HistorialEstadoPedido` y `MovimientoStock` son append-only, y ninguna capa puede
emitir `UPDATE` ni `DELETE` sobre ellas.

**Seguridad y evolución.** Los dos mecanismos independientes que el TPI usa para
garantizar append-only (sección 16.4): uno en la aplicación y otro en la base.

## Clase 7 — El corazón transaccional

**Génesis.** Los cuatro fenómenos de concurrencia —lectura sucia, no repetible,
fantasma, actualización perdida— con un ejemplo del dominio cada uno. Bloqueo
optimista contra pesimista: qué resigna cada uno. Por qué la idempotencia es un
problema del servidor y no del cliente.

**Contenido.** El flujo de creación de pedido de la sección 8.1, paso por paso. La
máquina de estados (3.4) y la matriz de autorización de transiciones (3.5). El
audit trail append-only y **RN-02**. **Descuento de stock dentro de la misma
transacción** (RN-06). El punto único de escritura de stock:
`aplicar_movimiento()` (sección 9.3), y por qué existe. Bloqueo pesimista con
`SELECT FOR UPDATE`. **RN-18: el orden de bloqueo entre familias**, que es la regla
que evita el interbloqueo — y que no se entiende sin haber provocado uno.
Idempotencia del lado del servidor: la tabla `ClaveIdempotencia`, y cómo el
servidor distingue un reenvío legítimo de una clave reciclada.

**Seguridad y evolución.** Qué pasa si dos peticiones llegan exactamente a la vez.

## Clase 8 — Robustez y más allá de la petición

**Génesis.** Por qué no todo puede ocurrir dentro de la petición: lo que tarda, lo
que puede fallar y reintentarse, y lo que no debe hacer esperar al usuario. Por qué
existe una cola de tareas. Por qué existe una caché, y por qué **ninguna caché es
la fuente de verdad**.

**Contenido.** **Robustez**: middlewares ASGI —registro, tiempos, identificador de
petición—, el **manejador global de excepciones** de la sección 14.2 y por qué el
Router no traduce errores. **Testing** con pytest, `httpx.AsyncClient` sobre
`ASGITransport` y `asgi-lifespan`; los casos TST obligatorios de la sección 15.
**Redis**: los cinco usos (4.1), claves y TTL (4.2), y el **modo de falla** (4.3)
—qué hace el sistema con Redis caído, que es la pregunta que casi nadie se hace—.
El límite de intentos con script Lua (4.4). Caché de lectura: invalidación por
versión y estampida (4.5). Lo que deliberadamente **no** va a Redis (4.6).
**taskiq y las siete reglas TB** (10.1): ninguna tarea en el camino crítico, toda
tarea idempotente, argumentos primitivos y no objetos, su propio UoW, política de
reintento declarada, el identificador de petición que viaja con ella, y nada de
publicar directo en Redis. Catálogo de tareas (10.2) y qué pasa cuando una falla
(10.3). **SSE con sse-starlette** (sección 11): el patrón outbox, el relay en el
worker, y el hueco de la reconexión. El módulo de estadísticas (12). **Despliegue**
(16): variables de entorno, Docker Compose, healthchecks y secuencia de arranque.

**Cierre del módulo.** Cómo trabajar con agentes de IA sobre esta base: qué pedir,
cómo verificar, y **cuáles de las 37 reglas un agente rompe por defecto** si nadie
se lo impide.

---

## Trazabilidad con el TPI

Cada capítulo cierra citando por número las secciones de `docs-tpi/` que quedan
habilitadas. Esa numeración es la del documento del director y no se altera.

## Estado

- [x] Clase 1 — Del objeto al servicio ✅
- [x] Clase 2 — Contratos: schemas, validación y CRUD ✅
- [x] Clase 3 — El bucle de eventos del servidor ✅
- [x] Clase 4 — Persistencia: SQLModel, PostgreSQL y el modelo de datos ✅
- [x] Clase 5 — Autenticación y autorización ✅
- [x] Clase 6 — Repositorios, Unit of Work y transacciones ✅
- [x] Clase 7 — El corazón transaccional ✅
- [x] Clase 8 — Robustez y más allá de la petición ✅
