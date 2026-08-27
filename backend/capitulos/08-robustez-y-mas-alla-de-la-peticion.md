# Capítulo 8 — Robustez y más allá de la petición

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 8.1. Alcance de la clase

Los siete capítulos anteriores construyeron un sistema que responde peticiones. Este
trata lo que ese sistema **no puede hacer dentro de una petición**, y las tres
preguntas que aparecen cuando se lo intenta.

La primera es la que ordena el capítulo. Cuando se confirma un pedido, hay que
guardarlo en la base **y** avisarle al panel de cocina que llegó. Lo primero vive en
una transacción. Lo segundo no. Y entre esas dos cosas hay un momento en que una
ocurrió y la otra no.

Si se avisa antes de confirmar, se puede anunciar un pedido que después se revierte.
Si se confirma antes de avisar y el proceso muere en el medio, **el pedido existe y
nadie se enteró.** No hay un orden que resuelva las dos cosas, y ese problema tiene
nombre: **la escritura dual**.

La segunda pregunta es qué pasa cuando el trabajo no entra en el tiempo de una
respuesta. Un correo de confirmación, la limpieza de pedidos vencidos, el drenaje
del buzón de eventos: todo eso tiene que ocurrir, y **nadie puede estar esperando
que ocurra**. Eso trae siete reglas propias, y la primera de ellas —**TB-01**— es la
que hace posibles a las otras seis.

La tercera es qué hace el sistema cuando **una pieza se cae**. Y acá el TPI hace
algo que la mayoría de los proyectos no hace: en lugar de dejarlo librado a lo que
pase, declara **cinco políticas taxativas**, una por cada uso de Redis, y **cada una
es distinta**. No hay una respuesta universal a "¿qué hago si se cae?".

El capítulo cierra los dos módulos, y por eso su última sección no es técnica: es
sobre **dirigir a un agente de IA sobre una base que uno entiende**, que es lo que
motivó los dieciséis capítulos.

Al finalizar la clase, el alumno debe poder **explicar por qué ningún orden resuelve
la escritura dual**, implementar el buzón de salida, y justificar por qué el evento
que viaja no lleva el dato nuevo.

**Contenidos**

1. El problema de la escritura dual y por qué ningún orden lo resuelve.
2. La génesis: confirmación en dos fases y por qué se abandonó.
3. El buzón de salida: los seis pasos del camino de un evento.
4. Anatomía de una fila del buzón, columna por columna.
5. Por qué el evento no lleva el dato nuevo.
6. Las siete reglas del trabajo diferido.
7. Los cinco modos de fallo de una tarea.
8. Redis nunca es autoritativo.
9. Las cinco políticas de degradación, y por qué son distintas entre sí.
10. El objeto nulo: degradar sin condicionales.
11. El disyuntor y por qué no alcanza un `try/except`.
12. El hueco de la reconexión y el error que sí se tolera.
13. Herramientas de diagnóstico.
14. Seguridad y evolución.
15. Cierre: dirigir a un agente sobre una base que uno entiende.

---

## 8.2. El problema de la escritura dual

El caso es concreto y aparece en cuanto un sistema tiene más de un almacén. Hay que
escribir en dos lugares, y **sólo uno de los dos tiene transacciones**.

Hay exactamente dos órdenes posibles, y los dos están mal.

| Orden | Qué pasa si el proceso muere en el medio |
| --- | --- |
| **Publicar y después confirmar** | Se anunció un pedido que **nunca existió** |
| **Confirmar y después publicar** | **El pedido existe y nadie se enteró** |

*(Ver Figura 8.1: los dos órdenes posibles, los dos malos.)*

No hay un tercer orden. Y conviene ver por qué la solución intuitiva —envolver las
dos en algo que las haga atómicas— no está disponible: **PostgreSQL y Redis no
comparten transacción.** Una `PUBLISH` no se revierte cuando la transacción hace
`rollback`, porque no participó de ella.

La reacción natural es elegir el mal menor y seguir. El TPI hace algo mejor: **elige
el orden que falla de forma recuperable**, y arma el mecanismo que lo recupera.

> **💡 PARA ENTENDER**
> Antes de ver la solución, fijate en un detalle de la tabla de arriba porque es la
> clave de todo el capítulo:
>
> **Los dos errores no son igual de graves.**
>
> - "Se anunció algo que no existe" → **el sistema mostró una mentira.** No hay
>   forma de arreglarlo después: alguien ya lo vio.
> - "Existe y nadie se enteró" → **el sistema está atrasado.** Si guardaste en algún
>   lado que faltaba avisar, **se puede avisar más tarde.**
>
> El segundo es recuperable. El primero no.
>
> Y ese es el criterio que vas a ver aplicado tres veces más en este capítulo:
> cuando no podés evitar el error, **elegí cuál de los errores posibles vas a
> tener.** Lo vas a ver de nuevo, casi textual, en la sección 8.10 sobre la
> reconexión.
>
> Esto es lo que separa un diseño pensado de uno improvisado. El improvisado no
> eligió: **le tocó.**

---

## 8.3. La génesis: por qué no se resuelve con una transacción distribuida

El problema de escribir atómicamente en dos sistemas no es nuevo, y tuvo una
respuesta formal antes de tener una práctica.

**Jim Gray** describió en 1978 el protocolo de **confirmación en dos fases**, que
hace exactamente lo que uno querría: un coordinador le pregunta a todos los
participantes *"¿podés confirmar?"*, espera que **todos** digan que sí, y recién ahí
les ordena confirmar. Si alguno dice que no, todos revierten.

Funciona, está demostrado, y **casi nadie lo usa**. La razón la formuló **Dale
Skeen** en 1981 al demostrar que el protocolo es **bloqueante**: si el coordinador
muere entre la pregunta y la orden, **los participantes quedan esperando con sus
recursos bloqueados**, y no pueden decidir por su cuenta sin arriesgarse a divergir.

El costo práctico es el que terminó de matarlo:

| | Confirmación en dos fases | El buzón de salida |
| --- | --- | --- |
| Atomicidad | **Real** | Con un desfasaje |
| Si el coordinador muere | **Todos bloqueados** | Nadie bloqueado |
| Participantes necesarios | Todos deben soportarlo | **Ninguno** |
| Latencia | Dos vueltas a todos | **Una transacción local** |

La cuarta fila es la que decide en este caso: **Redis no soporta el protocolo.** Aun
si se quisiera pagar el costo, no está disponible.

La alternativa que la industria adoptó parte de una idea distinta, formulada en los
trabajos sobre **transacciones de compensación** de Garcia-Molina y Salem (1987) y
popularizada después: **renunciar a la atomicidad entre sistemas, y sostener la
consistencia con el tiempo.**

Y de ahí sale el patrón que este capítulo implementa, hoy conocido como **buzón de
salida**: *si no podés escribir atómicamente en los dos lugares, escribí
atómicamente en **uno solo** —el que tiene transacciones— y que ese uno recuerde lo
que hay que hacer en el otro.*

**Las decisiones de diseño que explican todo lo que sigue** son cuatro.

**Primera: la intención de publicar se guarda como dato, no se ejecuta.** Un evento
es una fila más de la transacción de negocio.

**Segunda: la entrega es al menos una vez, y se declara.** No se intenta lograr
exactamente una: se exige que los consumidores toleren repeticiones.

**Tercera: nada que sea necesario para completar una operación puede vivir en una
tarea.** Es TB-01, y es lo que permite que el encolado falle sin romper nada.

**Cuarta: cada dependencia declara qué pasa cuando se cae, y no todas responden
igual.** Son las cinco políticas de la sección 8.10.

---

## 8.4. El buzón de salida: los seis pasos

El TPI describe el camino de un evento en seis pasos, y dice algo importante sobre
ellos: **"el orden es lo que hace que no se pierda ninguno"**.

*(Ver Figura 8.2: el camino completo de un evento.)*

**Uno.** El servicio, **dentro de la transacción de negocio** —junto a la
actualización del pedido y a la inserción del historial—, escribe una fila en la
tabla de eventos de salida con su tipo, su canal y su contenido. **No publica nada.**
Eso es RN-14.

**Dos.** El Unit of Work confirma. Y acá está la frase que justifica todo el patrón:

> En este instante el hecho y su anuncio **son igual de ciertos** —o están los dos o
> no está ninguno—.

**Tres.** Una tarea del trabajador toma el lote pendiente **con bloqueo y salteando
las filas ya tomadas, ordenado por identificador**, y publica cada evento en su
canal.

**Cuatro.** El trabajador marca los eventos como publicados **dentro de la misma
transacción que los tomó**. Si el proceso muere entre la publicación y la marca, el
evento **se publica de nuevo en el ciclo siguiente**: entrega al menos una vez, que
es RN-15.

**Cinco.** La interfaz, en el manejador del flujo de eventos de cada cliente
conectado, está suscripta al canal: recibe el mensaje, **verifica que ese cliente
pueda verlo**, y lo emite con su identificador.

**Seis.** El cliente recibe el evento e **invalida su clave de caché**; la biblioteca
de datos recarga por la interfaz REST y la vista se redibuja con el dato
autoritativo. Eso es RN-F09, del otro módulo.

Vale detenerse en el paso tres, porque el bloqueo que usa es distinto de los del
capítulo 7. Ahí se bloqueaba **y se esperaba**. Acá se bloquea **y se saltea lo que
ya está tomado**, y esa diferencia es exactamente lo que permite correr varios
trabajadores sobre el mismo buzón sin que se pisen: cada uno toma un lote distinto
**sin coordinarse con los otros**.

> **📌 NOTA**
> El paso dos es el corazón del patrón y quiero que lo veas por lo que elimina, no
> por lo que hace:
>
> **En ese instante desaparece el momento donde una cosa ocurrió y la otra no.**
>
> No hay ventana. No hay "murió justo entre las dos". El hecho y su anuncio son
> **la misma escritura**: si confirmó, están los dos; si revirtió, no está ninguno.
>
> Y fijate qué se hizo para lograrlo: **se cambió una acción por un dato.** En vez
> de *publicar el evento* —que es una acción, y las acciones no se revierten— se
> *escribe la intención de publicarlo*, que es un dato, y **los datos sí se
> revierten**.
>
> Ese movimiento —convertir un efecto en un dato para que participe de una
> transacción— es de las herramientas más potentes que te llevás del módulo. Cada
> vez que tengas que hacer algo irreversible dentro de una transacción, la pregunta
> correcta no es "¿cómo lo revierto?" sino **"¿cómo lo convierto en un dato?"**

---

## 8.5. Anatomía de una fila del buzón

El patrón se entiende mejor abriendo la fila, porque **cada columna existe por una
razón distinta** y varias responden a cosas que ya aparecieron en el capítulo.

| Columna | Para qué está | Qué pasa si falta |
| --- | --- | --- |
| **identificador** | Ordena la publicación y **viaja al cliente como identificador del evento** | La reconexión de la sección 8.11 no tiene desde dónde recuperar |
| **tipo** | Qué clase de hecho ocurrió | El cliente no sabe qué invalidar |
| **canal** | A quiénes les interesa | Habría que decidirlo al publicar, fuera de la transacción |
| **contenido** | La identificación del recurso, **no sus datos** | Sección 8.6 |
| **creado en** | Cuándo ocurrió el hecho | No se puede medir la antigüedad del atraso |
| **publicado en** | Nulo mientras espera | **No se distingue lo pendiente de lo hecho** |
| **intentos** | Cuántas veces se intentó | No se distingue **atraso de fallo** |

Las últimas tres filas son las que hacen el trabajo, y conviene mirarlas juntas.

**La marca de publicación es nula por defecto**, y ese detalle es lo que convierte
la tabla en una cola: *lo pendiente* es una consulta, no un estado que alguien tiene
que mantener. Nadie borra la fila al publicarla —se la marca—, y por eso el buzón es
además **un registro de lo que se anunció**.

**El contador de intentos separa dos diagnósticos que se ven igual desde afuera.**
Un buzón con mil filas pendientes y contadores en cero está **atrasado**: el
publicador viene lento o estuvo detenido. Un buzón con cien filas cerca del máximo
está **fallando**: se intentó publicarlas y no se pudo. El tamaño es el mismo
síntoma; la causa y la respuesta son distintas.

Y **el instante de creación** es lo que permite la observación de la sección 8.12:
mil eventos publicados en un segundo son un pico normal, mientras que **un evento de
hace una hora es un problema**, aunque sea uno solo.

Una observación sobre el conjunto: **ninguna de estas columnas describe el negocio.**
Un evento de salida no es una entidad del dominio —no es un pedido ni un producto—,
es **infraestructura persistida**. Y esa es la razón de que viva en la base y no en
Redis: no está ahí por ser un dato de negocio, sino **por necesitar la transacción**.

> **📌 NOTA**
> Fijate en la primera fila de la tabla, porque hace algo que no es obvio:
>
> **El identificador de la fila del buzón es el mismo que el cliente usa para
> reconectar.**
>
> No hay dos numeraciones. Cuando el navegador dice *"lo último que recibí fue el
> evento 8.412"*, ese número **es una clave primaria de tu base**, y por eso el
> servidor puede responder la pregunta *"¿qué me perdí?"* con un simple `WHERE id >
> 8412`.
>
> Si el identificador del evento fuera otra cosa —un valor aleatorio, una marca de
> tiempo— **esa consulta no existiría**, y habría que mantener una correspondencia
> entre dos numeraciones. Un dato más que puede quedar mal.
>
> Es el mismo criterio que venís viendo hace ocho capítulos: **cuando una cosa puede
> servir para dos, que sea la misma cosa.** Menos piezas, menos formas de
> desincronizarse.

---

## 8.6. Por qué el evento no lleva el dato nuevo

Esta es una de las mejores decisiones del TPI, porque **la opción rápida es la
equivocada** y el documento explica exactamente por qué.

Sería más rápido mandar el pedido completo en el contenido del evento: el cliente lo
recibe y lo muestra, sin volver a pedir nada. El TPI no lo hace, **por dos razones
que no tienen nada que ver entre sí**.

**La primera es de autorización.** El mismo evento va a un canal que miran **el
propietario del pedido y el personal**, y esos dos no pueden ver los mismos campos.
Mandar el objeto obligaría a filtrarlo por rol **en el momento de emitir**, que es
—en palabras del TPI— *"exactamente la lógica que ya vive en los schemas"*. Se
estaría duplicando la decisión de qué ve cada quien, en un segundo lugar, con la
posibilidad de que las dos versiones se desincronicen.

**La segunda es de orden.** La entrega es al menos una vez y **sin orden garantizado
entre canales**. Dos eventos del mismo pedido que llegan invertidos, **si traen
datos**, dejan la pantalla mostrando el estado anterior. Con el evento vacío no pasa:

> Un evento que solo dice "el pedido 42 cambió" es **idempotente y conmutativo por
> construcción**.

*(Ver Figura 8.3: el evento con dato contra el evento sin dato, ante repetición y
desorden.)*

Esas dos palabras merecen desarmarse porque son el fundamento de la decisión.
**Idempotente**: recibirlo dos veces produce el mismo resultado que recibirlo una —
se invalida una clave que ya estaba invalidada, y no pasa nada. **Conmutativo**:
recibir el evento A y después el B produce el mismo resultado que al revés — las dos
invalidaciones terminan en el mismo pedido a la interfaz.

> **💡 PARA ENTENDER**
> Esto merece que te detengas, porque es el remate de los dos módulos y conecta las
> dos mitades de la cursada:
>
> **El evento no transporta el dato. Transporta la noticia de que el dato cambió.**
>
> Y mirá lo que se gana con esa distinción:
>
> | | Evento con el dato | **Evento vacío** |
> | --- | --- | --- |
> | Si llega dos veces | puede pisar algo más nuevo | **no pasa nada** |
> | Si llegan desordenados | **queda el viejo en pantalla** | da igual el orden |
> | Autorización | filtrar por rol al emitir | **ya la hace la API** |
> | Si se pierde uno | el dato queda mal | el siguiente lo arregla |
>
> Cuatro problemas difíciles, resueltos **por no mandar algo**.
>
> Y acá está el cierre del arco: **el dato autoritativo sale siempre por el mismo
> lugar** —la interfaz REST, con sus modelos de salida y su autorización—. El canal
> de eventos no es una segunda puerta por la que también salen datos. **Es un
> timbre.**
>
> Cuando alguien te proponga "mandemos el objeto en el evento así es más rápido",
> ya sabés las cuatro cosas que se rompen.

---

## 8.7. Las siete reglas del trabajo diferido

El TPI declara siete reglas para las tareas, todas en la sección 10.1. Conviene
verlas juntas porque **la primera es la que hace posibles a las otras seis**.

*(Ver Figura 8.4: las siete reglas y de qué protege cada una.)*

**TB-01 — Ninguna tarea es parte del camino crítico.** Y el TPI da el criterio para
detectar cuándo se está violando:

> Si una operación **no se puede dar por completa** sin que la tarea corra, esa
> operación **está mal partida**: lo que hace la tarea tiene que estar en la
> transacción.

Es una regla de diseño disfrazada de regla operativa. Y su consecuencia es enorme:
**es lo que permite que el encolado pueda fallar sin romper nada.**

**TB-02 — Toda tarea es idempotente.** La razón es mecánica: el intermediario
garantiza entrega **al menos una vez**, y un trabajador que muere **después de hacer
el trabajo y antes de confirmar el mensaje** hace que la tarea se ejecute de nuevo.
El TPI es tajante: *"una tarea que no se puede repetir sin daño es un defecto"*.

**TB-03 — Ninguna tarea recibe objetos como argumento.** Sólo identificadores y
valores primitivos; la tarea **relee lo que necesita**. La razón:

> Un objeto serializado en la cola es **una foto vieja**: para cuando el trabajador
> lo abre, la fila puede haber cambiado.

> **⚠️ OJO ACÁ**
> TB-03 parece una restricción caprichosa hasta que ves el caso, y entonces no lo
> olvidás más:
>
> ```python
> # MAL: el objeto viaja
> await notificar_cambio_estado.kiq(pedido)
>
> # BIEN: viaja el identificador, la tarea relee
> await notificar_cambio_estado.kiq(pedido.id)
> ```
>
> ¿Qué pasa con la primera? El pedido se serializa **con el estado que tenía en ese
> instante**. Entre que entra a la cola y que el trabajador lo abre pueden pasar
> segundos —o minutos, si la cola viene cargada— y en ese rato el pedido **puede
> haber sido cancelado.**
>
> Resultado: **le mandás al cliente un correo diciéndole que su pedido está en
> preparación, cuando ya está cancelado.** Y el correo es correcto respecto de lo
> que la tarea recibió. Simplemente recibió **una foto vieja**.
>
> Es el mismo problema de la sección 7.5 del capítulo anterior —decidir con datos
> leídos antes— pero con una ventana muchísimo más grande: ahí eran milisegundos,
> acá pueden ser minutos.
>
> Y hay un segundo motivo, más prosaico: **un objeto en una cola es un formato.** Si
> mañana le agregás un campo al modelo, los mensajes que ya estaban encolados **no
> lo tienen**, y el trabajador nuevo revienta al abrirlos. Un identificador no tiene
> ese problema: un entero es un entero para siempre.

**TB-04 — Toda tarea abre su propia sesión y su propio Unit of Work, y llama al
mismo servicio que llamaría un enrutador.** Y el cierre de la regla: *"no hay lógica
de negocio que viva sólo en una tarea"*. Esto conecta directo con la clase 6, donde
el actor sintético del sistema existía justamente para esto.

**TB-05 — Toda tarea declara su política de reintento** —cuántas veces y con qué
espera— **y qué hace cuando la agota**. La justificación es de las mejores del
documento:

> Una tarea que falla en silencio para siempre es **peor que una que no existe**,
> porque **nadie sabe que no ocurrió**.

**TB-06 — El identificador de la petición que encoló la tarea viaja con ella** y
aparece en los registros del trabajador. *"Sin eso, un error en el trabajador es
imposible de atar a lo que lo originó."*

**TB-07 — Ninguna tarea publica eventos directamente.** Si produce un hecho que hay
que anunciar, **lo escribe en el buzón como cualquier servicio**. Las tareas no son
una excepción a RN-14.

> **⚠️ OJO ACÁ**
> TB-01 es la regla más importante del capítulo y la que más se viola sin darse
> cuenta. Fijate el caso típico:
>
> ```python
> # MAL: la operación depende de la tarea
> async def registrar_usuario(uow, datos):
>     usuario = await uow.usuarios.create(...)
>     await enviar_mail_verificacion.kiq(usuario.id)   # ← si esto falla…
>     return usuario                                    #   el usuario no puede verificar
>
> # BIEN: la operación se completa sola
> async def registrar_usuario(uow, datos):
>     usuario = await uow.usuarios.create(...)
>     await uow.eventos.create(tipo="usuario_registrado", ...)   # dato, en la transacción
>     return usuario     # el mail sale del buzón; si tarda, el usuario ya existe
> ```
>
> La pregunta que tenés que hacerte en cada tarea que escribas:
>
> **"Si esta tarea NUNCA corre, ¿la operación se completó igual?"**
>
> Si la respuesta es no, **no es una tarea**: es parte de la operación y va en la
> transacción. Y el TPI lo dice sin vueltas: *"esa operación está mal partida"*.
>
> Es un error frecuentísimo porque **se ve como una optimización**: "el mail tarda,
> lo mando aparte y respondo rápido". Y lo que estás haciendo en realidad es
> convertir una operación atómica en dos, **con todo lo del capítulo 7 en el
> medio.**

---

## 8.8. Cuando una tarea falla: los cinco modos

Una tarea no falla de una sola manera, y el TPI enumera **cinco modos distintos, con
una respuesta distinta cada uno**. Esta enumeración es la anatomía del artefacto de
esta clase: no hay que memorizarla, hay que entender por qué cada respuesta es la
que es.

| Modo | Respuesta | Por qué |
| --- | --- | --- |
| **Transitoria** (red, bloqueo, plazo vencido) | Reintento con **espera creciente** | Puede funcionar la próxima |
| **Permanente** (dato inválido, regla de negocio) | **No se reintenta** | Va a fallar igual las diez veces |
| **El trabajador muere a mitad** | Otro toma el mensaje, **desde el principio** | Por eso TB-02 exige idempotencia |
| **La cola crece sin drenar** | Es un **síntoma**, no un fallo | Los trabajadores no dan abasto o están caídos |
| **Redis caído** | Las peticiones **siguen atendiéndose** | TB-01 |

La primera fila tiene un detalle que el TPI justifica y que suele pasarse por alto:
la espera **creciente**. La razón es concreta —*"reintentar de inmediato contra una
base sobrecargada **la sobrecarga más**"*—. Un reintento inmediato ante una falla de
carga no es neutro: **empeora exactamente la condición que causó la falla.**

La segunda fila es la que distingue un sistema pensado de uno que reintenta todo por
las dudas. Reintentar una falla permanente **no la arregla**: consume el presupuesto
de reintentos, llena los registros, y retrasa el momento en que alguien se entera.

La última fila cierra el círculo con TB-01: *"las tareas periódicas no corren; las
peticiones siguen atendiéndose"*. Y el TPI agrega la consecuencia: **al volver, la
siguiente corrida hace el trabajo acumulado**, y las siete tareas están escritas para
tolerar eso.

---

## 8.9. Redis nunca es autoritativo

RN-20 es de las reglas más cortas del TPI y de las que más decisiones gobiernan:

> Redis **nunca es autoritativo**. Toda decisión de negocio —si hay stock, si el
> pedido se puede confirmar, si la clave de idempotencia ya se usó— **se toma contra
> PostgreSQL**. Lo que Redis aporta es **velocidad y una respuesta temprana, nunca la
> última palabra**.

Los tres ejemplos que la regla enumera ya aparecieron, y ahora se leen juntos:

| Decisión | Lo que Redis aporta | Quién decide |
| --- | --- | --- |
| ¿Hay stock? | Nada — el bloqueo es de fila | **PostgreSQL** (cap. 7) |
| ¿Superó los intentos? | Un contador rápido | **La tabla de intentos** (cap. 5) |
| ¿Se usó esta clave? | Un rechazo temprano y barato | **La restricción única** (cap. 7) |

Hay una regla más que muestra hasta dónde llega este criterio. RN-21 dice que un
pedido pendiente cuyo plazo venció **se cancela automáticamente**, y agrega la parte
importante:

> La cancelación es **una transición como cualquier otra**: pasa por el servicio,
> respeta la matriz, exige motivo y deja su fila en el historial, con el actor del
> sistema. **No es una actualización masiva.**

Es la tentación obvia y el TPI la descarta explícitamente. Un `UPDATE` masivo sobre
los pedidos vencidos sería una línea de SQL y **se saltearía todo**: la matriz de
transiciones, el historial, la reposición de stock de RN-07, el evento de salida. Los
pedidos quedarían cancelados **y el stock nunca volvería**.

La tarea periódica, entonces, no hace nada especial: **busca los vencidos y llama al
mismo servicio de cancelación que llamaría un cliente**, uno por uno, con el actor
sintético del sistema. Es TB-04 en acción, y es la razón por la que ese actor existe
desde la clase 5.

Y hay una regla hermana que conviene leer al lado. RN-19: *"ninguna respuesta que
dependa del rol del solicitante o de la propiedad del recurso se cachea. **Solo se
cachea lo público y lo idéntico para todos**"*.

La razón es una clase entera de vulnerabilidad: si se cachea una respuesta que
depende de quién pregunta, **el siguiente que pregunte puede recibir la respuesta del
anterior**. El catálogo es idéntico para todos y se cachea; "mis pedidos" no lo es y
no se cachea nunca.

---

## 8.10. Las cinco políticas de degradación

Acá está lo que distingue al TPI de un proyecto común, y conviene decirlo con todas
las letras: **el documento declara qué hace el sistema con Redis caído, uso por uso,
y las cinco respuestas son distintas.**

La sección es normativa y las políticas son taxativas. La aplicación distingue **dos
situaciones y no hay una tercera**: Redis responde con error o no responde dentro del
plazo, o Redis responde.

*(Ver Figura 8.5: los cinco usos con su política de degradación.)*

**R-1, el límite de intentos: degradar, ni abrir ni cerrar.** El limitador cae a la
consulta sobre la tabla de intentos, con la misma ventana y los mismos umbrales: *"el
login sigue protegido, más lento"*. Y el TPI descarta las dos alternativas obvias con
un argumento cada una:

- **Fallar abierto** dejaría al sistema sin protección contra fuerza bruta **justo
  cuando está degradado, que es cuando un atacante va a probar.**
- **Fallar cerrado** bloquearía a todos los usuarios por la caída de un componente
  que **no es autoritativo**.

Y remata explicando por qué la tercera opción está disponible acá y no siempre:
*"funciona porque **la copia durable ya estaba**: la tabla de intentos no es un
vestigio, **es el plan B**"*.

**R-2, la caché: fallar abierto en lectura, diferir en la invalidación.** El
adaptador se reemplaza por uno vacío —todo es un fallo de caché, toda lectura va a
PostgreSQL, **la respuesta es idéntica y cambia la latencia**—. Y una frase que vale
por toda la sección:

> **Una caché cuya caída produce errores no es una caché: es una dependencia dura
> disfrazada.**

La parte fina es la invalidación. Si una operación de administración invalida el
catálogo mientras el circuito está abierto, esa invalidación **se pierde**; por eso
deja una marca en memoria que se reintenta al cerrarse, y por eso el plazo de
expiración de las tablas de catálogo —una hora— **es la única cota que quedaría si
esa marca también se perdiera.**

> **💡 PARA ENTENDER**
> Pará acá, porque R-2 es **la actividad 4 de POO** funcionando en producción y
> quiero que hagas la conexión.
>
> Acordate del `Protocol` y del duck typing: **definís qué métodos tiene que tener
> algo, y cualquier clase que los tenga sirve.** Sin herencia, sin registrarse en
> ningún lado.
>
> El TPI define un puerto de caché exactamente así:
>
> ```python
> class CachePort(Protocol):
>     async def get(self, clave: str) -> bytes | None: ...
>     async def set(self, clave: str, valor: bytes, ttl: int) -> None: ...
>     async def delete(self, clave: str) -> None: ...
>
> class RedisCache:        # el de todos los días
>     ...
>
> class NullCache:         # el de la degradación
>     async def get(self, clave): return None          # siempre un fallo de caché
>     async def set(self, clave, valor, ttl): pass     # no guarda nada
>     async def delete(self, clave): pass              # no hay nada que borrar
> ```
>
> `NullCache` **cumple el protocolo sin heredar de nada**, y por eso se puede
> intercambiar en caliente cuando el circuito se abre. **El servicio no se entera.**
> No hay un `if hay_redis:` en ninguna parte del código de negocio.
>
> Y fijate lo que eso te da, que es lo mismo que decía la clase 6 sobre los tipos:
> **la degradación no es un caso especial del código, es otro objeto.** Un caso
> especial hay que acordarse de escribirlo en cada lugar; otro objeto se pone una
> vez, en el borde.
>
> Este patrón tiene nombre —**objeto nulo**— y es de los más útiles que vas a usar:
> en vez de devolver `None` y obligar a todos a preguntar, devolvés algo que cumple
> la interfaz **y no hace nada**.

**R-3, los eventos: fallar abierto y acumular.** El publicador no puede publicar y
deja las filas del buzón sin marcar **y sin incrementar su contador de intentos**.
Mientras el circuito esté abierto, **espacia sus ciclos**. Los clientes dejan de
recibir; las vistas siguen actualizándose por el refresco periódico de respaldo que
RN-F11 exige del otro módulo. *"El evento ya está persistido: **nada se pierde, sólo
se atrasa**."*

**R-4, la cola de tareas: fallar abierto en el encolado.** Un servicio que intenta
encolar y no puede **lo registra y sigue**. Y la justificación es literalmente TB-01:
*"si alguna tarea fuera imprescindible para completar una operación, no debería ser
una tarea"*.

**R-5, la idempotencia: degradar al nivel dos.** Se saltea la marca en Redis y **la
unicidad de la clave hace todo el trabajo**. *"Cambia el código de error del caso
concurrente, **no el resultado**."* Y el cierre, que explica por qué el diseño del
capítulo 7 tenía dos niveles:

> El nivel uno es **una optimización declarada**: un mecanismo de corrección que
> depende de una caché **no es un mecanismo de corrección.**

> **📌 NOTA**
> Volvé a leer esas cinco políticas y fijate en lo que tienen en común, porque no es
> la respuesta:
>
> **Ninguna dice "se cae y vemos qué pasa". Las cinco están decididas de antemano, y
> las cinco son distintas.**
>
> Y las tres formas de fallar tienen nombre propio en la industria:
>
> | | Qué hace | Cuándo corresponde |
> | --- | --- | --- |
> | **Fallar abierto** | Dejar pasar | La pieza daba velocidad, no corrección (R-2, R-3, R-4) |
> | **Fallar cerrado** | Rechazar todo | La pieza daba una garantía que no se puede resignar |
> | **Degradar** | Ir al plan B | **Hay una copia durable que ya estaba** (R-1, R-5) |
>
> La tercera es la mejor de las tres **y casi nunca está disponible**, porque exige
> haber diseñado el plan B antes de necesitarlo. En este sistema está disponible dos
> veces, y las dos por la misma razón: la tabla de intentos y la tabla de claves
> **existían por otro motivo** y sirven de respaldo.
>
> Cuando armes tu TPI y agregues una dependencia externa, la pregunta que va antes
> de escribir la primera línea es: **"¿qué hace el sistema cuando esto no responde?"**
> Si no tenés respuesta, todavía no terminaste de diseñar.

---

## 8.11. El disyuntor, y el hueco de la reconexión

Quedan dos piezas, y las dos tienen la misma forma: **una decisión sobre qué error se
tolera.**

**El disyuntor.** El TPI se anticipa a la solución obvia y la descarta: la caída de
Redis **no se detecta con un `try/except` por llamada**. El adaptador lleva un
disyuntor con **tres estados**:

| Estado | Qué hace |
| --- | --- |
| **Cerrado** | Las llamadas pasan |
| **Abierto** | Tras N errores consecutivos, **las llamadas ni se intentan** |
| **Semiabierto** | Deja pasar una llamada de prueba para ver si volvió |

La diferencia con el `try/except` es la fila del medio, y es toda la diferencia. Con
`try/except`, **cada petición sigue esperando el plazo completo** antes de fallar: si
el plazo es de doscientos milisegundos, con Redis caído **todas las peticiones tardan
doscientos milisegundos de más**. Con el circuito abierto, la llamada **no se
intenta** y la degradación es inmediata.

Y hay un cálculo del TPI sobre esto que conviene mirar de cerca, porque muestra el
nivel de detalle que un diseño necesita para ser correcto. Sobre por qué el
publicador de eventos, con el circuito abierto, **no incrementa el contador de
intentos y espacia sus ciclos**:

> Sin estas precisiones, con un ciclo de 500 ms y un máximo de 5 intentos, una caída
> de Redis **agotaría el presupuesto de todo el buzón en dos segundos y medio**,
> treinta **antes de que el disyuntor probara por primera vez**.

**El hueco de la reconexión.** El canal de publicación de Redis **no persiste**: lo
que se publica mientras un cliente no está suscripto, ese cliente no lo recibe. El
TPI lo llama *"la limitación más importante de este diseño"* y agrega cómo se trata:
**"se resuelve del lado del servidor, no ignorándola"**.

Cuando un cliente reconecta, reenvía el identificador del último evento que recibió.
Y acá viene la decisión:

> **El orden importa**: suscribirse primero y consultar después **puede duplicar**
> eventos (tolerable, RN-15 ya lo declara); consultar primero y suscribirse después
> **puede perderlos** (no tolerable).

*(Ver Figura 8.6: los dos órdenes de la reconexión.)*

Y para el cliente que estuvo desconectado mucho tiempo, la recuperación **se acota**:
si el hueco es mayor que lo que el sistema retiene, el servidor emite un evento de
resincronización y el cliente **invalida todas sus claves en lugar de reproducir la
historia**.

> **💡 PARA ENTENDER**
> Volvé a leer la frase del orden en la reconexión, porque es **el mismo razonamiento
> de la sección 8.2** aplicado a otro problema:
>
> | | Suscribirse primero | Consultar primero |
> | --- | --- | --- |
> | Riesgo | **duplicar** eventos | **perder** eventos |
> | ¿Se tolera? | **Sí** — RN-15 ya lo declara | **No** |
>
> No se eligió el orden que no falla. **No existe.** Se eligió el orden **cuyo error
> el sistema ya sabe absorber**.
>
> Y fijate cómo se sostiene toda la cadena: se puede tolerar el duplicado **porque
> los eventos son idempotentes**, y son idempotentes **porque no llevan el dato**
> (sección 8.6), y no llevan el dato **porque el dato autoritativo sale por la
> interfaz REST**.
>
> Cada decisión de este capítulo apoya a la siguiente. Sacá una y se caen tres.
>
> **Eso es arquitectura.** No es elegir tecnologías: es que las decisiones se
> sostengan entre sí.

---

## 8.12. Herramientas de diagnóstico

*(Ver Figura 8.7: el buzón acumulado y el buzón drenando, después de una caída.)*

**La profundidad del buzón** es el primer indicador y el más honesto: contar las
filas sin publicar. Si ese número **crece y no baja**, el publicador está caído o no
da abasto. El TPI expone además un endpoint de operación que lo informa.

**La antigüedad del evento más viejo sin publicar** dice más que la cantidad. Mil
eventos publicados en un segundo son un pico normal; **un evento de hace una hora es
un problema**.

**El contador de intentos por fila** distingue el atraso del fallo. Un buzón grande
con contadores en cero está atrasado; **un buzón con filas cerca del máximo está
fallando**, y son dos diagnósticos distintos.

**El estado del disyuntor** debe ser observable. Un sistema que degradó
correctamente **se ve igual que uno sano desde afuera** —esa es la idea— y por eso
hay que poder preguntarle si está degradado.

**El identificador de petición en los registros del trabajador** es TB-06 en acción:
permite tomar un error del trabajador y encontrar **la petición que lo originó**,
horas después.

**Los mensajes pendientes en el grupo de consumidores** muestran las tareas tomadas y
no confirmadas. Ahí aparecen los trabajadores que murieron a mitad.

> **🧪 EXPERIMENTO**
> Este experimento vale por todo el capítulo y son tres pasos:
>
> **Parte 1 — ver el buzón funcionando.**
> 1. Confirmá un pedido. Antes de que el publicador corra, mirá la tabla de eventos:
>    **la fila está, sin marcar.**
> 2. Dejá correr el publicador. Mirá cómo la fila queda marcada y el cliente recibe.
>
> **Parte 2 — matar Redis.**
> 3. Apagá Redis. **Confirmá otro pedido.**
> 4. La operación **funciona igual**. Fijate en la tabla: el evento está ahí,
>    esperando.
> 5. Mirá el catálogo: **sigue respondiendo**, más lento. Eso es R-2.
> 6. Intentá hacer login: **sigue protegido**. Eso es R-1 cayendo a la tabla.
>
> **Parte 3 — revivirlo.**
> 7. Prendé Redis. **No toques nada más.**
> 8. Mirá cómo el buzón drena solo y los clientes reciben todo lo acumulado.
>
> El paso 4 es el que más enseña: **apagaste una pieza de la arquitectura y el
> sistema siguió aceptando pedidos.** Ninguna operación de negocio falló.
>
> Ahora hacé el contraejemplo: escribí una versión que publique directo en Redis
> dentro del servicio, y repetí el paso 3. **Vas a ver la operación entera fallar
> por no haber podido avisar.**

---

## 8.13. Seguridad y evolución

Cinco consideraciones cierran la parte técnica del módulo.

**Un buzón sin retención crece para siempre.** Los eventos publicados hay que
borrarlos, y el plazo de retención **no es arbitrario**: es lo que acota cuánto atrás
puede recuperar un cliente que reconecta (sección 8.11). Acortarlo ahorra espacio y
**achica la ventana de recuperación**.

**Un evento es un dato que sale del sistema.** Todo lo que se escriba en su contenido
**puede llegar a un cliente**. El diseño de la sección 8.6 lo evita casi por
completo, y esa es una de sus ventajas menos obvias: **un evento que no lleva datos
no puede filtrarlos.**

**Un canal mal autorizado es una fuga.** El paso cinco verifica que el cliente pueda
ver el evento **antes de emitirlo**. Sin esa verificación, suscribirse a un canal
sería una forma de enterarse de la actividad de otros.

**Una tarea que falla en silencio es una promesa incumplida.** Es TB-05, y en
seguridad importa más de lo que parece: si la tarea que revoca accesos o notifica un
cambio de contraseña falla y nadie se entera, **el sistema cree haber hecho algo que
no hizo.**

**Un reintento sin cota es una amplificación.** Una tarea que reintenta
indefinidamente contra un servicio caído **le agrega carga a algo que ya está mal**.
La espera creciente y el máximo de intentos son medidas de protección hacia afuera,
no sólo hacia adentro.

Sobre la evolución, dos observaciones. La primera es que **el buzón de salida no es
específico de Redis ni de este sistema**: es el patrón estándar para integrar una
base transaccional con cualquier cosa que no lo sea. Lo aprendido acá se traslada a
colas, servicios externos y sistemas de terceros.

Y la segunda es que **este diseño tiene un techo conocido**. Un buzón consultado
periódicamente funciona bien hasta cierto volumen; más allá, se reemplaza por lectura
del registro de transacciones de la base, que evita la consulta a costa de acoplarse
al motor. Para el tamaño de este sistema, la consulta periódica es la respuesta
correcta, y conviene saber que existe el punto donde deja de serlo.

---

## 8.14. Cierre: dirigir a un agente sobre una base que uno entiende

Los dieciséis capítulos de los dos módulos existen por esto, así que vale terminar
diciéndolo.

Un agente de IA escribe el código de este capítulo sin dificultad. Si se le pide un
buzón de salida con su publicador, lo escribe. Si se le pide un disyuntor, lo
escribe. **Y va a estar bien escrito.**

Lo que no va a hacer, salvo que se lo pidan, es **preguntar qué pasa cuando Redis se
cae**. Va a elegir una respuesta razonable —probablemente `try/except` y seguir— y no
va a avisar que eligió. Tampoco va a preguntar si el evento debe llevar el dato: va a
mandarlo, porque es lo más común, y las cuatro consecuencias de la sección 8.6 van a
aparecer meses después como errores intermitentes que nadie sabe reproducir.

Y no es que el agente esté mal. **Es que esas preguntas no son de programación: son
de diseño, y las hace quien conoce el dominio.**

De ahí sale lo único que hay que llevarse de los dos módulos:

**No se dirige lo que no se entiende.**

Quien terminó estos dieciséis capítulos no sabe programar mejor que el agente. Pero
sabe **qué preguntarle**, sabe **qué mirar de lo que devuelve**, y sobre todo sabe
**qué no le va a decir**. Puede pedirle un buzón de salida y verificar que la
escritura del evento esté dentro de la transacción. Puede pedirle una tarea y
preguntarle qué pasa si se ejecuta dos veces. Puede leer un diseño y ver el momento
donde una cosa ocurrió y la otra no.

Eso no lo da la herramienta. **Lo dan los conceptos**, que es con lo que empezó el
primer capítulo del primer módulo y con lo que termina el último del segundo.

---

## 8.15. Verificación

1. Explicar **por qué ningún orden resuelve la escritura dual**, con los dos casos
   concretos.
2. Provocar la muerte del proceso **entre la confirmación y la publicación** y
   verificar que el evento sale igual en el ciclo siguiente.
3. Verificar que la escritura del evento ocurre **dentro de la transacción de
   negocio**: revertir la operación y comprobar que no queda evento.
4. Detener el publicador, acumular eventos, y verificar que al reanudarlo **drena en
   orden**.
5. Correr **dos publicadores a la vez** y verificar que no publican los mismos
   eventos.
6. Ejecutar la misma tarea dos veces y verificar que **el resultado es el mismo**
   (TB-02).
7. Apagar Redis y verificar los cinco comportamientos declarados, **uno por uno**.
8. Verificar que **ninguna operación de negocio falla** con Redis caído.
9. Reconectar el flujo de eventos con un identificador previo y verificar que
   **llegan los perdidos, en orden**.
10. Verificar que un evento **no contiene datos del recurso**, sólo su identificación.
11. Tomar un error del trabajador y **encontrar la petición que lo originó** por su
    identificador (TB-06).
12. Provocar una falla permanente y verificar que **no se reintenta**.

---

## 8.16. Errores frecuentes

**Publicar el evento dentro del servicio.** Viola RN-14 y reintroduce la escritura
dual completa: la publicación no se revierte (sección 8.4).

**Publicar después del `commit`, en el mismo servicio.** Parece la solución y es el
segundo caso de la sección 8.2: si el proceso muere ahí, el hecho ocurrió y nadie se
enteró.

**Mandar el objeto en el evento.** Duplica la autorización y deja la pantalla
mostrando el estado anterior cuando dos eventos llegan invertidos (sección 8.6).

**Hacer que una operación dependa de una tarea.** Viola TB-01. El síntoma: la
operación "no está completa" hasta que la tarea corre (sección 8.7).

**Pasarle un objeto a una tarea.** Es una foto vieja: para cuando el trabajador la
abre, la fila puede haber cambiado. Viola TB-03.

**Escribir lógica de negocio dentro de una tarea.** Viola TB-04: la tarea llama al
mismo servicio que llamaría un enrutador.

**Reintentar de inmediato.** Contra una base sobrecargada, **la sobrecarga más**
(sección 8.8).

**Reintentar una falla permanente.** No la arregla, consume el presupuesto de
reintentos y retrasa que alguien se entere (sección 8.8).

**Dejar que una tarea falle en silencio.** Es peor que no tenerla, porque nadie sabe
que no ocurrió. Viola TB-05.

**Tomar una decisión de negocio contra Redis.** Viola RN-20: aporta velocidad, nunca
la última palabra (sección 8.9).

**Cachear una respuesta que depende del rol o de la propiedad.** Viola RN-19 y el
siguiente que pregunte puede recibir la respuesta del anterior (sección 8.9).

**Detectar la caída con `try/except` por llamada.** Cada petición sigue esperando el
plazo completo. Para eso está el disyuntor (sección 8.11).

**Consultar los eventos perdidos antes de suscribirse.** Puede perder eventos, que es
el error **no tolerable** de los dos (sección 8.11).

**No declarar qué pasa cuando una dependencia se cae.** Si no hay respuesta, el
diseño no está terminado (sección 8.10).

---

## 8.17. Actividades

1. **Los dos órdenes, provocados.** Implementar las dos versiones incorrectas de la
   sección 8.2 —publicar antes y publicar después— y matar el proceso en el momento
   exacto para producir cada uno de los dos fallos. Documentar qué queda en el
   sistema en cada caso.

2. **El buzón completo.** Implementar la tabla de eventos, la escritura dentro de la
   transacción y el publicador con toma por lotes. Verificar los seis pasos de la
   sección 8.4 uno por uno, y demostrar que **dos publicadores concurrentes no se
   pisan**.

3. **Las siete reglas, auditadas.** Tomar las tareas del sistema y verificar cuáles
   cumplen cada una de TB-01 a TB-07. Para cada incumplimiento, escribir qué falla
   concretamente y corregirlo.

4. **La degradación completa.** Apagar Redis y documentar, **para los cinco usos**,
   qué hace el sistema y en qué se nota. Comparar lo observado con lo que declara la
   sección 8.9 y señalar cualquier diferencia.

5. **El disyuntor, medido.** Implementar la versión con `try/except` y la versión con
   disyuntor, apagar Redis y **medir la latencia de las peticiones en las dos**.
   Documentar la diferencia y relacionarla con el cálculo de la sección 8.11.

6. **Exploración: el evento con datos.** Implementar la versión que manda el objeto
   en el evento, y provocar deliberadamente los dos problemas de la sección 8.6:
   un evento repetido y dos eventos invertidos. Documentar qué queda en pantalla en
   cada caso y explicar por qué el evento vacío no tiene ninguno de los dos.

7. **Exploración: los dos lados del evento.** Junto con alguien del turno de
   frontend, seguir un evento completo de punta a punta: desde la fila que el
   servicio escribe hasta la vista que se redibuja. Cortar la conexión a mitad de
   camino, reconectar, y verificar que llegan los perdidos. Documentar qué hace cada
   mitad y por qué la del cliente **invalida en lugar de escribir**. *(Requiere
   coordinar con la otra mitad de la cursada.)*

---

## 8.18. Síntesis

1. **La escritura dual no tiene un orden correcto.** Publicar antes anuncia lo que no
   existe; publicar después puede perder el anuncio. Hay que elegir cuál de los dos
   errores tener.

2. **De los dos errores, uno es recuperable y el otro no.** Un sistema atrasado se
   pone al día; un sistema que mostró una mentira, no. Ese criterio se aplica cuatro
   veces en el capítulo.

3. **La confirmación en dos fases resuelve el problema y es bloqueante.** Si el
   coordinador muere, los participantes quedan con sus recursos tomados. Además,
   Redis no la soporta.

4. **El buzón de salida convierte una acción en un dato.** Las acciones no se
   revierten; los datos sí. Por eso el hecho y su anuncio pueden ser la misma
   escritura.

5. **La entrega es al menos una vez, y se declara.** No se busca exactamente una: se
   exige que los consumidores toleren repeticiones.

6. **El evento no lleva el dato: lleva la noticia de que el dato cambió.** Eso lo
   hace idempotente y conmutativo por construcción, y evita duplicar la autorización.

7. **El dato autoritativo sale siempre por el mismo lugar.** El canal de eventos no
   es una segunda puerta por la que también salen datos: es un timbre.

8. **Si una operación no se completa sin que la tarea corra, está mal partida.** Es
   TB-01, y es lo que permite que el encolado falle sin romper nada.

9. **Una tarea que falla en silencio es peor que una que no existe**, porque nadie
   sabe que no ocurrió.

10. **Redis nunca es autoritativo.** Aporta velocidad y una respuesta temprana, nunca
    la última palabra.

11. **Cada dependencia declara qué pasa cuando se cae, y no todas responden igual.**
    Fallar abierto, fallar cerrado y degradar son tres respuestas distintas; la
    tercera exige haber diseñado el plan B antes de necesitarlo.

12. **Una caché cuya caída produce errores no es una caché: es una dependencia dura
    disfrazada.**

13. **Un mecanismo de corrección que depende de una caché no es un mecanismo de
    corrección.** Por eso la idempotencia tiene dos niveles y el segundo es el que
    decide.

14. **Las decisiones del capítulo se sostienen entre sí.** Se tolera el duplicado
    porque los eventos son idempotentes, y lo son porque no llevan el dato, y no lo
    llevan porque el dato sale por la interfaz REST.

15. **No se dirige lo que no se entiende.** El agente escribe el código; las
    preguntas que nadie le hizo son las que definen si el sistema funciona.

---

## 8.19. Referencias y lecturas complementarias

El protocolo de confirmación en dos fases está descripto en el trabajo de **Jim
Gray** *Notes on Data Base Operating Systems* (1978), y su carácter bloqueante fue
demostrado por **Dale Skeen** en *Nonblocking Commit Protocols* (SIGMOD, 1981); leer
los dos en ese orden explica por qué la industria terminó buscando otra cosa. Esa
otra cosa aparece formulada en **Garcia-Molina y Salem**, *Sagas* (SIGMOD, 1987),
donde se propone sostener la consistencia entre sistemas con compensaciones en lugar
de atomicidad. El patrón del buzón de salida en su forma actual está catalogado por
**Chris Richardson** en *Microservices Patterns* (Manning, 2018) junto con las
variantes que este capítulo menciona al final, y el noveno capítulo de **Kleppmann**,
*Designing Data-Intensive Applications* (O'Reilly, 2017), es la mejor discusión
disponible sobre entrega al menos una vez y sobre por qué "exactamente una vez" es
una promesa que conviene mirar con cuidado.

Para las políticas de degradación, el libro de **Michael Nygard** *Release It!* (2.ª
edición, Pragmatic Bookshelf, 2018) es la referencia: el disyuntor de la sección 8.11
aparece ahí con sus tres estados, junto con los demás patrones de estabilidad y —lo
más valioso— con los relatos de los fallos reales que los motivaron. La documentación
de **PostgreSQL** sobre bloqueos explícitos cubre la variante que el publicador usa
para tomar lotes sin coordinarse, y la especificación de **eventos enviados por el
servidor**, parte del estándar HTML, documenta el mecanismo de reconexión con
identificador que la sección 8.11 discute.

Del TPI, este capítulo se apoya en la sección **10** completa —con **10.1** como
núcleo normativo y **10.3** por los modos de fallo—, en la **11** por el camino del
evento y el hueco de la reconexión, y en la **4.3** por las cinco políticas de
degradación. Las reglas involucradas son **RN-14**, **RN-15**, **RN-19**, **RN-20** y
**RN-21**, junto con **TB-01 a TB-07** completas.

---

**Fin del módulo.** Ocho capítulos que van de un objeto de Python a un sistema que
sigue funcionando cuando una de sus piezas se cae. Lo que queda es el trabajo
integrador — y las preguntas que hay que saber hacer para dirigirlo.
