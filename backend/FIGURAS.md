# Catálogo de figuras — Backend desde POO

Toda figura del módulo se declara acá antes de referenciarse en un capítulo.
Regla del material: si un esquema necesita cajas y flechas, **es una figura**, no
arte ASCII (ver [`CLAUDE.md`](CLAUDE.md) §4).

Columna **Origen**: `diagrama` (Mermaid, en [`DIAGRAMAS.md`](DIAGRAMAS.md)) o
`captura` (la toma el docente sobre pantalla real).

---

## Capítulo 1 — Del objeto al servicio

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 1.1 | Del proceso por petición al bucle de eventos | Las tres respuestas históricas al problema de atender a muchos, cada una con **su costo anotado**: un proceso por petición (caro de crear), un hilo por conexión (1 MB de pila y cambio de contexto), un hilo multiplexando (nada puede bloquear). El problema C10K marcado como el punto de quiebre | diagrama | ⬜ pendiente |
| 1.2 | El recorrido de una petición del lado del servidor | De uvicorn al handler y de vuelta: ASGI, ruteo, validación del schema, resolución de dependencias, Service, y serialización. Debe verse **dónde se valida** y dónde el handler recibe datos ya confiables | diagrama | ⬜ pendiente |
| 1.3 | Las capas y la dirección de las dependencias | Router → Service → UoW → Repository → Model, con las flechas en un solo sentido. La capa **Task va al costado**, como segundo cliente de Service y no como capa nueva. Los puertos de caché y eventos aparte, marcados como adaptadores | diagrama | ⬜ pendiente |
| 1.4 | Los ocho servicios y su orden de arranque | migrador → seed → api/worker/scheduler/web, sobre postgres y redis. Cada uno con su cardinalidad, y **el scheduler marcado con "exactamente 1"**. Postgres y Redis con distinto color según si su caída degrada o detiene | diagrama | ⬜ pendiente |
| 1.5 | La documentación automática | Captura de la interfaz interactiva con un endpoint desplegado y ejecutado desde el navegador, mostrando la respuesta. Idealmente al lado del `422` con el detalle de validación | captura | ⬜ pendiente |
| 1.6 | La estructura de un módulo | Los cinco archivos de un módulo (`router.py`, `service.py`, `repository.py`, `model.py`, `tasks.py`) y qué capa es cada uno. Puede ser captura del árbol real del proyecto o diagrama | captura | ⬜ pendiente |

## Capítulo 2 — Contratos: schemas, validación y CRUD

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 2.1 | Del contrato generado al contrato derivado | Las tres etapas con **lo que resignó cada una**: SOAP/WSDL (nada se desajusta, nada se mueve), REST sin contrato (todo se mueve, nada garantiza), OpenAPI (derivado del código). El eje debe ser el intercambio, no la cronología | diagrama | ⬜ pendiente |
| 2.2 | Los cuatro pasos de la validación | Parseo → coerción → validación → construcción, con el `422` saliendo de los pasos 1 a 3 y **el handler recibiendo sólo datos ya confiables**. Debe verse que el handler nunca corre con entrada inválida | diagrama | ⬜ pendiente |
| 2.3 | Los tres modelos segregados | `Create`, `Update` y `Public` sobre la misma entidad, con una fila por campo y una marca por modelo. Los campos que **sólo** están en `Public` (id, creado_en) y el que no está en ninguno (costo interno) son el contenido de la figura | diagrama | ⬜ pendiente |
| 2.4 | El importe de la base al cliente | `DECIMAL(10,2)` en Postgres → `Decimal` en el modelo → **cadena `"1234.50"`** en el JSON → `string` en TypeScript. Debe verse marcado **dónde NO se convierte a punto flotante**, que es todo el recorrido | diagrama | ⬜ pendiente |
| 2.5 | Un `422` en la documentación interactiva | Captura de la interfaz interactiva tras enviar un cuerpo inválido, con el detalle desplegado mostrando `loc`, `type`, `msg` e `input`. Idealmente con **dos errores a la vez**, para que se vea que es una lista | captura | ⬜ pendiente |
| 2.6 | El schema en la especificación | Captura del fragmento de OpenAPI correspondiente a un modelo, mostrando cómo cada restricción declarada aparece traducida. Es la evidencia de que el contrato se deriva del código | captura | ⬜ pendiente |

## Capítulo 3 — El bucle de eventos del servidor

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 3.1 | Concurrencia frente a paralelismo | Dos líneas de tiempo: arriba, un hilo alternando entre tres tareas (concurrente, no paralelo); abajo, tres núcleos ejecutando a la vez. Debe verse que **la de arriba también termina las tres**, sólo que sin superposición real | diagrama | ⬜ pendiente |
| 3.2 | Cómo una petición cede el control y vuelve | Los cuatro pasos del bucle, con una petición que cede en cada `await` mientras otras se atienden en el hueco. Los `await` marcados como **los únicos puntos de cesión** | diagrama | ⬜ pendiente |
| 3.3 | Qué pasa cuando una línea bloquea | Los tres casos lado a lado: handler `def` (bloquea **un hilo** de un grupo), `async` correcto (**nada**), `async` con línea sincrónica (**el proceso entero**). La tercera columna es el punto de la figura | diagrama | ⬜ pendiente |
| 3.4 | Dónde el ORM puede saltar al bucle y dónde no | El greenlet con el ORM sincrónico adentro, la flecha de salto al bucle **desde dentro de un `await`**, y las dos situaciones donde no hay a dónde saltar: relación no precargada y objeto expirado tras el commit | diagrama | ⬜ pendiente |
| 3.5 | El techo que desaparece | A la izquierda, el grupo de hilos limitando la concurrencia contra la base sin que nadie lo pida; a la derecha, diez mil corrutinas esperando y **el pool de conexiones como nuevo cuello de botella**. Las dos variables que el TPI declara van anotadas a la derecha | diagrama | ⬜ pendiente |
| 3.6 | Una traza de `MissingGreenlet` | Captura de la traza completa, con dos marcas: **dónde salta** la excepción y **dónde está su causa real** —el acceso al atributo, o el repositorio que no declaró la precarga—. Es la figura que enseña a leerla | captura | ⬜ pendiente |

## Capítulo 4 — Persistencia: SQLModel, PostgreSQL y el modelo de datos

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 4.1 | Las tres relaciones traducidas al esquema | Asociación, agregación y composición del diagrama de clases, y al lado su esquema. Debe verse que **la clave foránea va del lado "muchos"** en los tres casos, y que lo que las diferencia es **el comportamiento al borrar** | diagrama | ⬜ pendiente |
| 4.2 | Las cinco diferencias del desajuste | Objeto contra fila, fila por fila: identidad, referencias, herencia, colecciones y navegación. La última fila destacada: **navegar es gratis en memoria y es una consulta contra la base** | diagrama | ⬜ pendiente |
| 4.3 | Carga perezosa y anticipada | El mismo listado de veinte pedidos con sus líneas: sin precarga (**excepción en la primera iteración**), con `selectinload` (2 consultas) y con `joinedload` (1 consulta, filas repetidas). Debe verse la cantidad de filas transferidas en cada caso | diagrama | ⬜ pendiente |
| 4.4 | Las cinco redundancias y su garante | Una fila por redundancia, con qué duplica y **qué la sostiene**: restricción de la base, índice único, o prueba cuando cruza tablas. La columna de garantes es el punto de la figura | diagrama | ⬜ pendiente |
| 4.5 | El esquema de un dominio | Captura de un cliente de base de datos mostrando las tablas de un dominio con sus claves foráneas, índices y restricciones. Idealmente el dominio de ventas, que tiene las redundancias | captura | ⬜ pendiente |
| 4.6 | Una migración generada | Captura del archivo de migración de un **renombre**, con `drop_column` y `add_column` señalados y la anotación de que eso **pierde los datos**. Al lado, la versión corregida con `alter_column` | captura | ⬜ pendiente |

## Capítulo 5 — Autenticación y autorización

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 5.1 | Los tres esquemas y qué resigna cada uno | Contraseña en cada petición, sesión en servidor y token firmado, cada uno con **lo que gana y lo que resigna** anotado. El eje es el intercambio: sesión (puede cerrar / no escala) contra token (escala / no puede cerrar) | diagrama | ⬜ pendiente |
| 5.2 | Las tres partes de un token | Encabezado, contenido y firma, con **el contenido marcado como legible por cualquiera** y la firma como lo único que garantiza integridad y autenticidad. La palabra "codificado" y no "cifrado" debe estar destacada | diagrama | ⬜ pendiente |
| 5.3 | El flujo de login paso a paso | Diagrama de secuencia del inicio de sesión, con **el punto donde se decide sin calcular** destacado: el límite de intentos se evalúa antes de tocar bcrypt, y un rechazo cuesta una consulta | diagrama | ⬜ pendiente |
| 5.4 | bcrypt: tres configuraciones | En el bucle (**detiene el proceso 300 ms**), en un hilo sin semáforo (100 hilos compitiendo por los núcleos), y en un hilo con semáforo de cuatro permisos (cuatro núcleos como máximo, el resto responde). Los tres con su consecuencia anotada | diagrama | ⬜ pendiente |
| 5.5 | Los dos routers | El router abierto con los públicos y los cuatro exceptuados, y el protegido con la dependencia. Debe verse **por qué no se resuelve con exclusiones**: las dependencias se suman hacia abajo y no hay forma de restar | diagrama | ⬜ pendiente |
| 5.6 | Un token decodificado | Captura de un token real de desarrollo con sus tres partes decodificadas, mostrando el contenido legible. Advertencia visible: **no usar sitios de terceros con tokens de producción** | captura | ⬜ pendiente |

## Capítulo 6 — Repositorios, Unit of Work y transacciones

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 6.1 | Las cuatro propiedades de una transacción | Atomicidad, consistencia, aislamiento y durabilidad, **cada una con su caso del dominio**. El aislamiento debe verse marcado como el que **tiene grados** y el que la clase 7 va a necesitar entero | diagrama | ⬜ pendiente |
| 6.2 | La operación a medias | El registro de usuario con y sin Unit of Work ante un fallo en el medio. A la izquierda: usuario guardado, rol no, **respuesta de error igual**. A la derecha: nada guardado, misma respuesta. La igualdad de las respuestas es el punto | diagrama | ⬜ pendiente |
| 6.3 | Quién crea, quién abre, quién confirma y quién cierra | Diagrama de secuencia del ciclo completo: la dependencia crea la sesión, otra construye el UoW **sin abrirlo**, el Router lo transporta, el Service lo abre y confirma, y **la dependencia cierra después de la respuesta** | diagrama | ⬜ pendiente |
| 6.4 | Por qué el intento de acceso necesita su propia transacción | Arriba: el registro dentro de la transacción de la petición y el rollback llevándoselo puesto. Abajo: sesión propia que se confirma igual. **La circularidad —lo que se quiere registrar destruye el registro— es el contenido** | diagrama | ⬜ pendiente |
| 6.5 | Las dos jerarquías de repositorio | `BaseRepository[T]` con los dieciocho modelos y `SoftDeleteRepository[T]` con los cinco que tienen borrado lógico, y los métodos que sólo existen en la segunda | diagrama | ⬜ pendiente |
| 6.6 | El registro de una transacción completa | Captura del registro de sentencias mostrando **dónde empieza y dónde termina** una transacción de varias escrituras, con las marcas de inicio y confirmación visibles | captura | ⬜ pendiente |

## Capítulo 7 — El corazón transaccional

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 7.1 | Los cuatro fenómenos de concurrencia | Lectura sucia, no repetible, fantasma y actualización perdida, **cada una con su caso del dominio**. La cuarta va destacada como la que persigue el capítulo, y anotada como la que **el estándar no obliga a prevenir en el nivel predeterminado** | diagrama | ⬜ pendiente |
| 7.2 | La actualización perdida, momento por momento | Línea de tiempo de dos transacciones leyendo 1, verificando, y escribiendo 0 las dos. Lo que la figura tiene que gritar: **se vendieron dos, se descontó una, y ninguna transacción falló** | diagrama | ⬜ pendiente |
| 7.3 | El interbloqueo entre familias | Dos transacciones **con sus identificadores perfectamente ordenados dentro de cada familia**, trabándose igual porque una empezó por producto y la otra por insumo. Al lado, la versión con RN-18 completa. **Es la figura más importante del capítulo** | diagrama | ⬜ pendiente |
| 7.4 | Los siete mecanismos y qué protege cada uno | Los siete de la sección 7.5 con el problema concreto que evita cada uno anotado al lado. Debe verse que **ninguno reemplaza a otro** | diagrama | ⬜ pendiente |
| 7.5 | El punto único de escritura del stock | Los servicios que necesitan mover stock, todos pasando por `aplicar_movimiento()`, que actualiza la columna **e inserta el movimiento en la misma transacción**. Al costado, el `UPDATE` directo tachado, y la propiedad de reconstrucción como verificación | diagrama | ⬜ pendiente |
| 7.6 | Un interbloqueo en los registros del motor | Captura del informe de interbloqueo de PostgreSQL, con las dos transacciones, los recursos disputados y **cuál fue elegida como víctima** visibles | captura | ⬜ pendiente |

## Capítulo 8 — Robustez y más allá de la petición

| Figura | Título | Qué muestra | Origen | Estado |
| --- | --- | --- | --- | --- |
| 8.1 | La escritura dual: los dos órdenes, los dos malos | Publicar antes de confirmar (se anuncia lo que nunca existió) y confirmar antes de publicar (existe y nadie se enteró), con **la muerte del proceso marcada en el medio de cada uno**. Debe verse que el segundo error es **recuperable** y el primero no | diagrama | ⬜ pendiente |
| 8.2 | El camino de un evento, los seis pasos | Del Service que escribe la fila dentro de la transacción hasta la vista que se redibuja. **El paso 2 —el commit— va destacado**: en ese instante el hecho y su anuncio son igual de ciertos. La ventana de la entrega al menos una vez debe verse entre el paso 3 y el 4 | diagrama | ⬜ pendiente |
| 8.3 | El evento con dato contra el evento vacío | Los mismos dos eventos llegando **repetidos y desordenados**, en las dos versiones. Con dato: queda el estado viejo en pantalla. Sin dato: da igual. **Las cuatro filas de la tabla comparativa son el contenido** | diagrama | ⬜ pendiente |
| 8.4 | Las siete reglas del trabajo diferido | TB-01 a TB-07, con **TB-01 en el centro** como la que hace posibles a las otras seis, y de qué protege cada una anotado al lado | diagrama | ⬜ pendiente |
| 8.5 | Los cinco usos de Redis y su política de degradación | R-1 a R-5, cada uno con su política —degradar, fallar abierto, acumular— y **la razón declarada**. Debe verse que las cinco son distintas, y que las dos que degradan lo hacen **porque la copia durable ya existía** | diagrama | ⬜ pendiente |
| 8.6 | La reconexión: por qué suscribirse primero | Los dos órdenes posibles al reconectar, con su riesgo: suscribirse primero **duplica** (tolerable, RN-15 lo declara); consultar primero **pierde** (no tolerable). **Se eligió el orden cuyo error el sistema ya sabe absorber** | diagrama | ⬜ pendiente |
| 8.7 | El buzón drenando después de una caída | Captura de la tabla de eventos de salida con filas acumuladas sin publicar y, al lado, la misma tabla después de reanudar el publicador. **Las marcas de publicación apareciendo son el contenido** | captura | ⬜ pendiente |
