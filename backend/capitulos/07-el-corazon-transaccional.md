# Capítulo 7 — El corazón transaccional: pedidos, stock, concurrencia e idempotencia

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 7.1. Alcance de la clase

Esta es la clase más difícil del módulo, y conviene decirlo de entrada porque la
dificultad no está donde suele estar. No hay tecnología nueva: todo lo que se usa
acá ya apareció. Lo que hay es **una operación que puede ocurrir dos veces al mismo
tiempo**, y eso rompe suposiciones que el resto del módulo pudo dar por buenas.

El caso concreto es el que ordena el capítulo entero. Dos personas confirman un
pedido del último producto **en el mismo segundo**. Las dos consultas leen que queda
uno. Las dos descuentan uno. **La base termina en menos uno**, y dos clientes
recibieron la confirmación de algo que no existe.

Ninguna de las dos operaciones hizo nada mal. Cada una, aislada, es correcta. El
problema aparece sólo cuando ocurren juntas, y por eso es tan difícil de encontrar:
**no se reproduce probando a mano.**

El capítulo cubre además la regla que el módulo viene anticipando desde la clase
6, donde apareció un ordenamiento escondido dentro de un método sin explicación.
**RN-18** es esa explicación, y tiene una sutileza que la vuelve una de las mejores
reglas del TPI: ordenar dentro de cada familia **no alcanza**, y el documento dice
exactamente por qué.

Y cierra el arco que la otra mitad de la cursada abrió en su primera clase, cuando
estableció que `POST` no es idempotente según la norma. **Acá se ve qué hace el
servidor con esa clave que el cliente genera**, y resulta que el mecanismo tiene dos
niveles y tres desenlaces posibles.

Al finalizar la clase, el alumno debe poder **provocar deliberadamente una
actualización perdida y un interbloqueo**, explicar qué mecanismo previene cada uno,
y justificar por qué el stock del sistema tiene un único punto de escritura.

**Contenidos**

1. Los cuatro fenómenos de concurrencia.
2. La génesis: bloqueo en dos fases y los límites del estándar.
3. Niveles de aislamiento y por qué el predeterminado no alcanza.
4. Bloqueo optimista y pesimista: qué resigna cada uno.
5. Los siete mecanismos de control de concurrencia.
6. Anatomía de un bloqueo: modo, objeto, dueño y plazo.
7. El orden de bloqueo entre familias.
8. La máquina de estados declarada como datos.
9. El flujo de confirmación, paso a paso.
10. El punto único de escritura del stock y la conversión de unidades.
11. Idempotencia del lado del servidor: dos niveles, tres desenlaces.
12. Herramientas de diagnóstico.
13. Seguridad y evolución.

---

## 7.2. Los fenómenos de concurrencia

Cuando dos transacciones se ejecutan a la vez sobre los mismos datos, pueden
aparecer cuatro comportamientos indeseables. Se los estudia desde los años ochenta
y tienen nombre propio; conviene verlos con un caso del dominio cada uno, porque
así dejan de ser una lista para memorizar.

| Fenómeno | Qué ocurre | En el dominio |
| --- | --- | --- |
| **Lectura sucia** | Una transacción lee lo que otra escribió y todavía no confirmó | Ver un pedido confirmado que después se revierte |
| **Lectura no repetible** | Leer dos veces lo mismo da resultados distintos | El stock cambia entre la verificación y el descuento |
| **Lectura fantasma** | Una consulta con filtro devuelve filas nuevas al repetirse | Aparecen pedidos nuevos a mitad de un informe |
| **Actualización perdida** | Dos transacciones leen, calculan y escriben; **una pisa a la otra** | **El caso de la sección 7.1** |

*(Ver Figura 7.1: los cuatro fenómenos con su caso.)*

El cuarto es el que este capítulo persigue, y conviene verlo en el tiempo:

| Momento | Transacción A | Transacción B | Stock real |
| --- | --- | --- | --- |
| 1 | Lee stock: **1** | | 1 |
| 2 | | Lee stock: **1** | 1 |
| 3 | Verifica: alcanza | | 1 |
| 4 | | Verifica: alcanza | 1 |
| 5 | Escribe stock = 0 | | 0 |
| 6 | | Escribe stock = 0 | **0** |

*(Ver Figura 7.2: la actualización perdida, momento por momento.)*

Se vendieron **dos** unidades y el stock bajó **una**. Las dos transacciones
confirmaron, ninguna falló, y ningún registro dice que algo salió mal.

Y hay una aclaración del TPI que conviene tener desde el principio, porque desarma
una confusión frecuente:

> **La asincronía no cambia nada de esto**: dos corrutinas sobre dos conexiones
> distintas compiten **exactamente igual** que dos hilos.

Es fácil suponer que un solo hilo de ejecución evita este problema. **No lo evita**,
porque la competencia no está en el proceso: está en la base. Dos corrutinas que
ceden el control en su `await` y vuelven, escriben sobre las mismas filas con la
misma superposición que dos hilos.

### La génesis: cómo se descubrió el problema

Los fenómenos de la tabla anterior no se dedujeron: **se encontraron en sistemas
que fallaban**, y su formalización llevó una década.

El punto de partida es el trabajo de **Eswaran, Gray, Lorie y Traiger** en IBM, que
en 1976 publicaron *The Notions of Consistency and Predicate Locks in a Database
System* mientras construían **System R**, el primer motor relacional. Ahí aparece la
formulación del problema y su solución: el **bloqueo en dos fases**.

La idea es de una simplicidad engañosa. Una transacción tiene **una fase de
crecimiento**, en la que adquiere bloqueos y no libera ninguno, y **una fase de
contracción**, en la que libera y no adquiere ninguno más. Con esa disciplina —y
sólo con ella— se demuestra que el resultado de ejecutar transacciones
concurrentemente **equivale a haberlas ejecutado una detrás de otra**.

De ahí sale una consecuencia práctica que hay que retener: **los bloqueos se liberan
al confirmar, no al terminar de usar la fila.** Liberarlos antes rompe la
demostración y devuelve los fenómenos que se querían evitar.

**Jim Gray** llevó esto más lejos en *The Transaction Concept: Virtues and
Limitations* (1981), donde nombró las cuatro propiedades que la clase 6 enumeró y
—esto es lo interesante— **discutió sus límites** desde el principio. El acrónimo que
hoy se recita como si fuera una ley natural nació ya acompañado de la lista de cosas
que no resuelve.

El estándar SQL de 1992 tomó esos hallazgos y definió los cuatro niveles de
aislamiento **en función de qué fenómenos permite cada uno**. Y ahí quedó un problema
que este módulo hereda: la definición del estándar **describe los niveles por lo que
prohíben, no por lo que garantizan**, y eso deja fenómenos afuera. El artículo de
Berenson y otros de 1995 lo demostró con casos concretos, y por eso cada motor
interpreta los niveles a su manera.

**La actualización perdida es exactamente uno de esos casos.** El estándar no la
menciona entre los fenómenos que el nivel de lectura confirmada debe prevenir, y por
lo tanto ese nivel no la previene. No es un defecto del motor: es lo que el estándar
dice.

**Las decisiones de diseño que explican todo lo que sigue** son tres, y quedan
enunciadas acá para que el resto del capítulo se lea con ellas en la mano.

**Primera: el aislamiento se paga donde hace falta, no globalmente.** El TPI no sube
el nivel de la base: agrega bloqueos explícitos en las operaciones que los necesitan.

**Segunda: los bloqueos viven dentro de la transacción.** Por eso ningún mecanismo
externo puede reemplazarlos, y por eso el orden de adquisición importa.

**Tercera: donde una regla se puede hacer cumplir sola, se hace cumplir sola.** El
ordenamiento vive dentro del método, la escritura de stock tiene un único punto, y
las restricciones de la base respaldan lo que el servicio ya validó.

> **📌 NOTA**
> Hay una consecuencia del bloqueo en dos fases que vale la pena que te quede,
> porque explica algo que parece ineficiente y no lo es:
>
> **El bloqueo se libera cuando confirmás la transacción, no cuando terminás de usar
> la fila.**
>
> Te puede parecer un desperdicio. Descontaste el stock en la línea 3 y la
> transacción sigue veinte líneas más, con la fila bloqueada todo ese rato. ¿Por qué
> no liberarla ahí?
>
> Porque si la liberás antes, **otra transacción puede leer un valor que todavía
> podés revertir.** Y si revertís, esa otra tomó una decisión sobre un dato que nunca
> existió.
>
> Eswaran y Gray lo demostraron en 1976: **la garantía sólo se sostiene si ninguna
> transacción libera un bloqueo antes de haber adquirido el último que necesita.**
>
> De ahí sale un consejo muy concreto para tu TPI: **hacé las transacciones cortas.**
> No porque sea elegante, sino porque cada operación lenta adentro de una transacción
> es tiempo con filas bloqueadas. Nunca metas una llamada a un servicio externo entre
> un bloqueo y su confirmación.

---

## 7.3. Los niveles de aislamiento, y por qué el predeterminado no alcanza

La norma define cuatro niveles de aislamiento, y cada uno **permite** ciertos
fenómenos a cambio de rendimiento:

| Nivel | Permite | Cuesta |
| --- | --- | --- |
| Lectura no confirmada | Los cuatro | Nada |
| **Lectura confirmada** | Los tres últimos | Poco — **es el predeterminado de PostgreSQL** |
| Lectura repetible | Las fantasmas | Más |
| Serializable | Ninguno | Más, y puede abortar transacciones |

El TPI es explícito sobre lo que eso implica:

> Sin bloqueo explícito, dos transacciones simultáneas pueden leer el mismo stock,
> restar cada una su cantidad y escribir un valor incorrecto. **El nivel de
> aislamiento por defecto de PostgreSQL no lo evita.**

Vale detenerse en eso, porque es lo que más sorprende. El nivel predeterminado
garantiza que una transacción **no vea escrituras sin confirmar** de otra. Eso
suena a suficiente y no lo es, porque **el problema no está en lo que se leyó**: las
dos leyeron un valor perfectamente confirmado. El problema está en que **entre la
lectura y la escritura, el valor dejó de ser cierto**.

Subir el nivel de aislamiento sería una salida. El TPI elige otra —y la sección 7.5
explica cuál— porque el nivel serializable tiene un costo que conviene conocer:
**puede abortar transacciones** que no hicieron nada mal, obligando a que la
aplicación las reintente. Eso traslada complejidad al código de la aplicación en
todos los casos, para resolver un problema que ocurre en unos pocos.

> **💡 PARA ENTENDER**
> Hay una idea acá que vale para todo lo que sigue:
>
> **El nivel de aislamiento predeterminado no es "el que está mal". Es el que
> equilibra correctamente para el noventa y nueve por ciento de las operaciones.**
>
> Una consulta del catálogo, una lectura de un pedido, un listado de usuarios: en
> todo eso, el nivel predeterminado hace exactamente lo correcto y es el más barato.
>
> El problema es el uno por ciento restante: **las operaciones que leen un valor,
> deciden algo con él, y lo escriben.** Ahí, y sólo ahí, hace falta protección
> adicional.
>
> Y por eso el TPI no sube el nivel global: **paga el costo sólo donde hace falta**,
> con bloqueos explícitos en las operaciones que los necesitan. Es la misma lógica
> que ya viste con la precarga — no hacer siempre lo caro, hacerlo donde
> corresponde.

---

## 7.4. Optimista contra pesimista

Hay dos estrategias para proteger una operación de lectura-decisión-escritura, y se
llaman así por lo que suponen.

**El bloqueo optimista** supone que los conflictos son raros. No bloquea nada:
guarda una versión del dato, y al escribir verifica que nadie la haya cambiado. Si
alguien lo hizo, **falla y hay que reintentar**.

**El bloqueo pesimista** supone que los conflictos son probables. Bloquea la fila
antes de leerla, y quien más la quiera **espera**.

| | Optimista | **Pesimista** |
| --- | --- | --- |
| Supone | Los conflictos son raros | Los conflictos ocurren |
| Costo cuando no hay conflicto | Ninguno | Un bloqueo que nadie disputa |
| Costo cuando hay conflicto | **Reintentar todo** | Esperar |
| Riesgo | Reintentos en cascada bajo carga | **Interbloqueos** |

El TPI usa **pesimista** para el stock, y la elección tiene sentido en este dominio:
en el momento de mayor demanda —cuando queda poco de algo popular— los conflictos
**no son raros**, son exactamente lo que está pasando. Y en ese momento, reintentar
significa que el cliente ve un error mientras el sistema pelea consigo mismo.

Su costo es el riesgo de la última fila, y es el tema de la sección 7.7.

---

## 7.5. Los siete mecanismos

El TPI declara **siete mecanismos** de control de concurrencia. Conviene verlos
juntos antes de desarmarlos, porque cada uno protege algo distinto y **ninguno
reemplaza a otro**:

| # | Mecanismo | Qué protege |
| --- | --- | --- |
| 1 | **Bloqueo de la transición** | Que dos confirmaciones del mismo pedido prosperen |
| 2 | **Bloqueo pesimista del stock** | Que dos operaciones descuenten sobre la misma lectura |
| 3 | **Orden de bloqueo** | Que dos operaciones se traben mutuamente |
| 4 | **Verificación posterior** | Que lo leído antes del bloqueo siga siendo cierto |
| 5 | **Tiempos límite** | Que una transacción colgada bloquee para siempre |
| 6 | **Restricción de respaldo** | Que un error de código deje el stock negativo |
| 7 | **Lo que Redis no hace** | Que alguien intente reemplazar el bloqueo con otra cosa |

*(Ver Figura 7.4: los siete mecanismos y qué protege cada uno.)*

**Uno: bloqueo de la transición.** Antes de evaluar la máquina de estados, el
servicio **bloquea la fila del pedido** y revalida el estado de origen. Es RN-10, y
es lo que impide que dos confirmaciones concurrentes del mismo pedido prosperen: la
segunda espera, y cuando entra, el estado ya no es el que esperaba.

**Dos: bloqueo pesimista del stock.** Antes de descontar o reponer, el servicio
obtiene las filas con bloqueo. Las transacciones concurrentes **esperan hasta la
confirmación**.

**Tres: orden de bloqueo.** Es la sección 7.7.

**Cuatro: verificación posterior.** Esta es la que más se olvida y el TPI la enuncia
sin ambigüedad:

> **Después del bloqueo** se revalidan stock de producto, disponibilidad, borrado y
> stock de cada insumo. Si algo falla se lanza la excepción de dominio
> correspondiente y **la transacción completa hace rollback.**

La palabra clave es *después*. Todo lo que se leyó **antes** de adquirir el bloqueo
pudo haber cambiado mientras se esperaba, y por lo tanto **hay que leerlo de
nuevo**. Verificar antes de bloquear es exactamente el error de la sección 7.2.

**Cinco: tiempos límite.** La sesión declara un plazo para adquirir un bloqueo y
otro para la sentencia completa. Sin eso, una transacción colgada **bloquea las
confirmaciones indefinidamente**. Con eso, el vencimiento se traduce en un `409` que
el cliente **puede reintentar**.

**Seis: restricción de respaldo.** Las comprobaciones de no negatividad sobre las
columnas de stock. Y el TPI aclara su papel con una precisión que conviene retener:

> Actúan como **última línea de defensa, no como mecanismo de validación**: el
> ajuste manual que dejaría el stock negativo **se rechaza en el servicio** con un
> `409`.

Es decir: la restricción **no es la que valida**. Valida el servicio, con un mensaje
que el usuario entiende. La restricción está para el caso en que el servicio tenga
un error, y su mensaje sería incomprensible para un usuario — pero **el dato queda
correcto**.

**Siete: lo que Redis no hace.** El TPI cierra la enumeración descartando una
alternativa que alguien va a proponer:

> Nada de esto pasa por Redis: **un bloqueo distribuido no puede sustituir un bloqueo
> de fila que vive dentro de la transacción que protege.**

La razón es precisa. Un bloqueo en Redis y una transacción en PostgreSQL **son dos
cosas separadas**: el bloqueo se puede liberar —por vencimiento, por una caída de
Redis— mientras la transacción sigue abierta. Un bloqueo de fila **es parte de la
transacción**: existe exactamente mientras ella existe, y se libera cuando ella
termina. Esa coincidencia es lo que lo hace confiable, y es imposible de reproducir
desde afuera.

> **⚠️ OJO ACÁ**
> El mecanismo cuatro es el que más se olvida y el más traicionero, así que fijate
> bien en el orden:
>
> ```python
> # MAL: verifica y después bloquea
> producto = await repo.get_by_id(id)
> if producto.stock < cantidad:
>     raise StockInsuficiente()
> producto = await repo.get_for_update(id)     # ← mientras esperaba, otro descontó
> producto.stock -= cantidad
>
> # BIEN: bloquea y después verifica
> producto = await repo.get_for_update(id)     # ← nadie más puede tocarlo desde acá
> if producto.stock < cantidad:
>     raise StockInsuficiente()
> producto.stock -= cantidad
> ```
>
> La versión de arriba **parece más eficiente** —chequea barato antes de bloquear
> caro— y es exactamente el bug de la sección 7.2 con un paso de más.
>
> Entre el `if` y el `get_for_update` hay una ventana. Es chiquita, de
> milisegundos. **Y es justo la ventana que se abre cuando hay mucha carga**, que es
> cuando queda poco stock, que es cuando importa.
>
> Regla sin excepciones: **primero se bloquea, después se decide.** Todo lo leído
> antes del bloqueo hay que leerlo de nuevo.

---

## 7.6. Anatomía de un bloqueo

Los siete mecanismos hablan de "bloquear" como si fuera una sola cosa. No lo es, y
conviene abrir el artefacto antes de seguir, porque lo que el motor muestra en su
vista de diagnóstico se lee campo por campo.

**Un bloqueo tiene modo.** No todos se excluyen entre sí: dos transacciones pueden
tener el mismo bloqueo compartido sobre la misma fila y ninguna espera. Los tres que
importan acá:

| Modo | Lo toma | Compatible con |
| --- | --- | --- |
| **Compartido de fila** | Una lectura con `FOR SHARE` | Otro compartido |
| **Exclusivo de fila** | Una lectura con `FOR UPDATE`, o un `UPDATE` | **Nada** |
| **Compartido de tabla** | Cualquier consulta común | Todo salvo los exclusivos de tabla |

La fila del medio es la que este capítulo usa. Que sea **incompatible con todo**
—incluso con otro exclusivo— es lo que hace que la segunda transacción espere.

**Un bloqueo tiene objeto.** La vista de diagnóstico del motor lo identifica con tres
datos: el identificador de la base, el de la tabla y el de la fila física. Esos tres
campos son los que permiten responder *"¿quién tiene bloqueado el producto 5?"* sin
adivinar.

**Un bloqueo tiene dueño, y puede tener una espera.** Cada entrada de la vista indica
qué proceso lo pidió y **si fue concedido o no**. Una entrada no concedida es
literalmente una transacción esperando, y cruzarla con la vista de actividad da la
sentencia exacta que está trabada.

Y el atributo que la sección 7.5 usa: **un bloqueo puede tener plazo**. Sin plazo, la
espera es indefinida. Con un plazo declarado, el intento falla después de un tiempo
conocido, y ese fallo se traduce en un `409` reintentable en lugar de una petición
que nunca responde.

> **🧪 EXPERIMENTO**
> Esta es la consulta que te salva el día cuando el sistema "se cuelga" sin dar
> ningún error:
>
> ```sql
> SELECT  bloqueada.pid    AS quien_espera,
>         bloqueada.query  AS sentencia_trabada,
>         bloqueante.pid   AS quien_bloquea,
>         bloqueante.query AS sentencia_que_bloquea
> FROM pg_stat_activity bloqueada
> JOIN pg_stat_activity bloqueante
>   ON bloqueante.pid = ANY(pg_blocking_pids(bloqueada.pid))
> WHERE cardinality(pg_blocking_pids(bloqueada.pid)) > 0;
> ```
>
> Te devuelve, en una tabla, **quién espera a quién y por qué sentencia**. Es la
> diferencia entre "el sistema anda lento" y "el proceso 4312 tiene bloqueado el
> producto 5 desde hace cuarenta segundos con esta sentencia".
>
> Probá esto: abrí una transacción, bloqueá una fila y **no la confirmes**. En otra
> terminal intentá bloquear la misma. En una tercera, corré la consulta de arriba.
>
> Y fijate el detalle que más enseña: `pg_blocking_pids` **devuelve un arreglo**, no
> un valor. Una transacción puede estar esperando a varias a la vez.

---

## 7.7. El orden de bloqueo, y por qué ordenar cada familia no alcanza

Acá está RN-18, la regla que la clase 6 dejó anticipada.

El bloqueo pesimista tiene un riesgo conocido: el **interbloqueo**. Ocurre cuando
dos transacciones esperan la una a la otra en círculo.

| Momento | Transacción A | Transacción B |
| --- | --- | --- |
| 1 | Bloquea el producto **7** | |
| 2 | | Bloquea el producto **3** |
| 3 | Pide el producto **3** → **espera a B** | |
| 4 | | Pide el producto **7** → **espera a A** |

Ninguna puede avanzar. El motor detecta el ciclo y **mata una de las dos**.

La solución clásica es **adquirir siempre los bloqueos en el mismo orden**. Si las
dos transacciones piden primero el 3 y después el 7, la segunda espera a la primera
y ninguna se traba. Por eso `get_many_for_update` ordena los identificadores de
forma ascendente por dentro, como vio la clase 6.

**Y acá viene la sutileza que hace de RN-18 una regla no obvia.** El TPI:

> El orden global de bloqueo es: **primero todas las filas de producto por
> identificador ascendente, después todas las de ingrediente** por identificador
> ascendente. Las dos familias **siempre en ese orden y nunca intercaladas**. **Sin
> un orden entre familias, dos confirmaciones que comparten un producto y un insumo
> pueden trabarse mutuamente aunque cada familia esté ordenada.**

Esa última frase es el punto. Ordenar **dentro** de cada familia no alcanza:

| Momento | Transacción A | Transacción B |
| --- | --- | --- |
| 1 | Bloquea **producto 5** | |
| 2 | | Bloquea **ingrediente 2** |
| 3 | Pide **ingrediente 2** → espera | |
| 4 | | Pide **producto 5** → espera |

Las dos ordenaron perfectamente sus identificadores **dentro** de cada familia. Y
se trabaron igual, porque **empezaron por familias distintas**.

*(Ver Figura 7.3: el interbloqueo entre familias.)*

La regla completa exige las dos cosas: **orden dentro de cada familia, y orden entre
familias.** Productos primero, insumos después, siempre y sin intercalar.

Y hay una extensión de RN-08 que generaliza el criterio más allá del stock:

> La regla de orden ascendente **se extiende a cualquier escritura que afecte a más
> de una fila de la misma tabla.**

> **💡 PARA ENTENDER**
> Esta es de las reglas más lindas del TPI y quiero que veas por qué:
>
> **Es una regla que no hace falta coordinar.**
>
> Pensá lo raro que es esto. Dos transacciones que no se conocen, que corren en
> procesos distintos, escritas quizá por personas distintas, **nunca se van a trabar
> si las dos siguen la misma convención de orden.** No hace falta que se pongan de
> acuerdo, ni que se avisen, ni que exista un coordinador.
>
> Alcanza con que **cada una, por su cuenta, pida las cosas en el mismo orden.**
>
> Y ahora el detalle que hace la diferencia entre saberlo y entenderlo: **ordenar
> dentro de cada familia no alcanza.** El orden tiene que ser total —tiene que
> abarcar todo lo que se bloquea— porque un ciclo de dos elementos se arma con dos
> elementos cualesquiera, aunque cada uno venga de un conjunto ordenado.
>
> Es exactamente el mismo principio de la cola del banco: alcanza con que todos
> respeten el orden de llegada. Nadie tiene que hablar con nadie.

---

## 7.8. El flujo de confirmación

Con los siete mecanismos en la mano, el flujo de confirmación se lee entero. Las
reglas que lo gobiernan son varias, y conviene enunciarlas donde aparecen:

**Se bloquea el pedido y se revalida el estado.** RN-10: la transición se ejecuta
sobre la fila bloqueada, y el estado de origen **se revalida después de adquirir el
bloqueo**.

**Se consulta la matriz de transiciones.** Y acá conviene detenerse, porque la
decisión de diseño es la misma que el módulo viene aplicando y en este caso se ve
con particular claridad.

Una máquina de estados se puede escribir de dos maneras. La primera es una cadena de
condicionales en el servicio: *si está pendiente y el actor es el propietario,
entonces puede cancelar; si está confirmado y el actor es empleado, entonces puede
pasar a preparación*. Funciona, y tiene tres problemas concretos:

- **No se puede consultar.** Responder *"¿qué transiciones admite un pedido
  confirmado?"* exige leer el código y confiar en no haber salteado una rama.
- **No se puede versionar.** Agregar un estado implica desplegar.
- **No se puede auditar.** No hay forma de mostrarle a nadie la matriz completa.

La segunda manera —la del TPI— es **declararla como datos**: una tabla de estados y
una matriz de transiciones que dice, para cada par de estados, **qué roles pueden
hacer esa transición**. El servicio no decide: consulta.

RN-01 agrega la pieza que cierra el diseño: **un estado terminal no admite
transiciones salientes**, y eso es un **atributo de la fila del estado**, no un
condicional en el código. Un pedido entregado o cancelado no puede moverse porque su
estado lo dice, no porque alguien se acordó de escribir el `if`.

La consecuencia práctica aparece en la clase 5 y vale repetirla: **un permiso mal
puesto no sólo deja pasar o no deja pasar — cambia qué error ve el usuario.** Si la
matriz dice que el propietario puede cancelar desde pendiente y alguien agrega una
verificación de rol encima, ese usuario recibe *"no tenés permiso"* para algo que sí
puede hacer.

> **📌 NOTA**
> Este patrón tiene nombre y lo vas a usar toda tu carrera:
>
> **Una máquina de estados se declara como datos, no se programa como condicionales.**
>
> Y fijate cómo cambia lo que podés hacer con ella:
>
> | Con condicionales | Con una matriz declarada |
> | --- | --- |
> | *"¿qué puede hacer un pedido confirmado?"* → leer el código | → **una consulta** |
> | Agregar un estado → desplegar | → **una migración de datos** |
> | Mostrarle la matriz a la cátedra → transcribirla a mano | → **exportarla** |
> | Probar todas las transiciones → escribirlas una por una | → **recorrer la tabla** |
>
> La última fila es la que más vale para tu TPI. Con la matriz declarada, **la prueba
> que verifica que ninguna transición prohibida prospera se escribe una sola vez** y
> recorre todas las combinaciones. Si mañana agregan un estado, la prueba ya lo
> cubre.
>
> Es exactamente el mismo criterio de la clase 4 con las restricciones, y el de esta
> clase con el ordenamiento adentro del método: **poné la regla donde no dependa de
> que alguien se acuerde.**

**Se bloquean los productos y después los insumos.** Es RN-18.

**Se verifica después del bloqueo.** Stock, disponibilidad y borrado de cada uno.

**Se descuenta el stock en la misma transacción.** RN-06: el stock de producto y de
insumos se descuenta al pasar a confirmado, **dentro de la misma transacción que
registra la transición**. No hay un momento en que el pedido esté confirmado y el
stock no descontado.

**El pago acompaña.** RN-09: el pago se crea junto con el pedido, pasa a confirmado
**en la misma transacción** y a anulado en toda cancelación.

Y una regla sutil que merece su propio párrafo, RN-13:

> El stock de producto **se verifica y se descuenta contra la suma de las cantidades
> de todas las líneas del mismo producto, no línea por línea.**

Parece un detalle de implementación y previene un error real: un pedido puede tener
**el mismo producto en dos líneas** —dos milanesas con distinta personalización—.
Verificando línea por línea, con stock 1 y dos líneas de 1, **las dos verificaciones
pasan** y el descuento total es 2. Verificando contra la suma, la operación se
rechaza correctamente.

> **⚠️ OJO ACÁ**
> RN-13 parece un detalle y es de los errores más difíciles de encontrar, porque
> **el código se ve perfectamente razonable**:
>
> ```python
> # MAL: cada línea se verifica contra el stock completo
> for linea in pedido.lineas:
>     producto = productos[linea.producto_id]
>     if producto.stock_cantidad < linea.cantidad:      # ← 1 >= 1 ✓
>         raise StockInsuficiente(linea.producto_id)     #   1 >= 1 ✓ otra vez
>     producto.stock_cantidad -= linea.cantidad          # ← termina en −1
>
> # BIEN: se agrupa primero, se verifica contra la suma
> requerido = defaultdict(int)
> for linea in pedido.lineas:
>     requerido[linea.producto_id] += linea.cantidad     # ← acá está la clave
> for producto_id, cantidad in requerido.items():
>     producto = productos[producto_id]
>     if producto.stock_cantidad < cantidad:
>         raise StockInsuficiente(producto_id)
> ```
>
> ¿Cuándo se rompe? **Cuando el mismo producto aparece en dos líneas del mismo
> pedido**, que en este dominio pasa todo el tiempo: dos milanesas con distinta
> personalización son dos líneas del mismo producto.
>
> Con stock 1 y dos líneas de 1, las dos verificaciones pasan porque **cada una
> compara contra el stock entero.** Y ojo con esto: **el bloqueo no te salva.** No hay
> concurrencia acá — es una sola transacción restando dos veces.
>
> Y por eso el TPI lo escribe como regla en lugar de dejarlo librado al criterio:
> *"se verifica y se descuenta contra la suma de las cantidades de todas las líneas
> del mismo producto, **no línea por línea**"*.

La cancelación es simétrica. RN-07: al cancelar un pedido que estaba confirmado o en
preparación, **el stock se repone en la misma transacción**.

---

## 7.9. El punto único de escritura

La sección 9.3 del TPI declara algo que la clase 1 ya había mencionado y que ahora
se entiende:

> `stock.aplicar_movimiento(...)` es **el único camino admitido** para modificar el
> stock de producto y de insumo. Actualiza la columna **e inserta la fila de
> movimiento en la misma llamada y en la misma transacción.**

*(Ver Figura 7.5: el punto único de escritura y quiénes lo usan.)*

Eso es RN-11, y el TPI agrega una frase que la vuelve verificable:

> El stock actual **debe poder reconstruirse sumando sus movimientos.**

Esa es una propiedad comprobable: si se suman todos los movimientos de un producto
y el resultado no coincide con su columna de stock, **alguien escribió por otro
lado**. No hace falta revisar el código para saberlo: se detecta con una consulta.

Y el TPI no deja lugar a interpretación sobre las alternativas:

> Un `UPDATE` directo sobre una columna de stock desde otro servicio **es un defecto
> de implementación, no una alternativa.**

**La conversión de unidades vive ahí también**, y esa es la parte que sorprende:

> La función es **también el único lugar que convierte unidades**: recibe la cantidad
> en la unidad que el llamador tenga a mano, **valida que su dimensión coincida** con
> la del insumo, la multiplica por el factor y persiste el resultado en la unidad
> base. **Ningún servicio convierte por su cuenta.**

> **💡 PARA ENTENDER**
> Frená un segundo acá, porque esto ya lo hiciste en POO y quizás no lo estás
> conectando.
>
> **`aplicar_movimiento` es una fachada, y la razón de que exista es la misma por la
> que en la actividad 6 pusiste el comportamiento adentro del objeto que compone.**
>
> Acordate del criterio de encapsulamiento: **un atributo no se modifica desde
> afuera**. Se expone un método que lo modifica **manteniendo las invariantes de la
> clase**, y el atributo queda privado. Si cualquiera puede escribir `objeto.saldo =
> 500`, la clase no garantiza nada.
>
> Acá pasa exactamente lo mismo, un nivel más arriba:
>
> | En POO | En el TPI |
> | --- | --- |
> | El atributo privado | La columna de stock |
> | El método que lo modifica | `aplicar_movimiento()` |
> | La invariante que mantiene | El movimiento registrado y la unidad convertida |
> | Escribir el atributo desde afuera | **Un `UPDATE` directo** |
>
> Y fijate la fila de abajo: el TPI dice que ese `UPDATE` directo **es un defecto de
> implementación, no una alternativa.** Es la misma frase que le dirías a alguien que
> te toca un atributo privado.
>
> La diferencia es el mecanismo. En POO, el lenguaje te ayuda con la convención del
> guion bajo. Acá **no hay nada que lo impida técnicamente**: la columna está ahí y
> cualquier repositorio puede escribirla. Por eso la garantía es otra —la
> reconstrucción por movimientos, que **detecta la violación aunque no pueda
> prevenirla**.

Que la conversión esté en el mismo lugar que la escritura no es casualidad: **son la
misma decisión.** Si la conversión viviera afuera, habría tantas conversiones como
llamadores, y bastaría con que una estuviera mal —o que alguien olvidara verificar
que las dimensiones coinciden, y sumara litros a kilos— para corromper el stock de
un insumo sin que nada falle.

> **📌 NOTA**
> Fijate en la frase *"el stock actual debe poder reconstruirse sumando sus
> movimientos"*, porque es de las mejores del TPI y describe un patrón que se usa en
> muchísimos sistemas serios.
>
> **La columna de stock es una conveniencia. Los movimientos son la verdad.**
>
> Podrías no tener la columna: cada vez que necesitás el stock, sumás los
> movimientos. Sería correcto y lentísimo. La columna existe para no hacer esa suma
> en cada consulta — **es exactamente una desnormalización**, de las que viste en la
> clase 4.
>
> Y como toda desnormalización, **necesita un garante.** Acá el garante es doble: el
> punto único de escritura (RN-11) que hace imposible desincronizarlas, y la
> propiedad de reconstrucción, que **permite verificarlo con una consulta.**
>
> Ese patrón —guardar los hechos y derivar el estado— es la base de los sistemas
> contables desde hace siglos. Un balance no se edita: se agregan asientos. Es la
> misma distinción de la clase 4 entre lo que describe y lo que registra.

---

## 7.10. Idempotencia: dos niveles y tres desenlaces

Acá cierra el arco más largo de los dos módulos. La otra mitad de la cursada
estableció en su primera clase que **`POST` no es idempotente según la norma**, y en
la última implementa RN-F07: el cliente genera una clave antes de confirmar y la
manda en un encabezado.

Este capítulo muestra qué hace el servidor con esa clave, y el mecanismo tiene **dos
niveles**.

**Nivel uno: la marca en Redis.** Antes de abrir ninguna transacción, el servicio
intenta poner una marca con la clave, que **sólo se escribe si no existía**. Si ya
estaba, responde de inmediato con un `409` que indica que esa clave está en curso
**sin haber tocado la base**.

Es un atajo barato para el caso más común —un doble clic, dos peticiones con
milisegundos de diferencia— y tiene una propiedad importante que lo hace
descartable: **con Redis caído, el paso se saltea.** No es la autoridad.

**Nivel dos: la fila en la tabla.** Ya dentro de la transacción, el servicio inserta
una fila con la clave, el estado **en curso**, y —esto es lo importante— **una huella
del cuerpo de la petición**.

Esa huella es lo que permite distinguir las dos situaciones que parecen iguales:

- **El mismo pedido reenviado**: misma clave, mismo cuerpo, misma huella.
- **Una clave reciclada**: misma clave, **cuerpo distinto**, huella distinta.

Si la inserción viola la unicidad de la clave, el servicio revierte, relee la fila
que ya estaba, y ramifica en **tres desenlaces**:

| Situación | Respuesta | Por qué |
| --- | --- | --- |
| Huella **coincide** y estado **completada** | **`200`** con el pedido ya creado | Es un reenvío legítimo: se devuelve lo que se creó |
| Huella **coincide** y estado **en curso** | `409`, reintentable | La primera todavía está trabajando |
| Huella **no coincide** | **`422`** | La clave se reutilizó para otro cuerpo |

Y al terminar bien, la fila se actualiza a **completada**, guardando el código de
respuesta y el identificador del pedido creado — que es lo que permite devolver ese
mismo `200` si el cliente vuelve a preguntar.

> **💡 PARA ENTENDER**
> Fijate la primera fila de esa tabla, porque tiene un detalle que casi nadie
> implementa bien:
>
> **Un reenvío legítimo responde `200`, no `201`.**
>
> El `201` significa "creé algo". La segunda vez **no se creó nada**: se está
> devolviendo lo que ya existía. Responder `201` otra vez sería mentir sobre lo que
> pasó.
>
> Y ahora lo importante para tu TPI: **el cliente ve exactamente el mismo pedido en
> los dos casos.** Nunca se entera de si el suyo fue el que lo creó o si llegó
> segundo. Desde su punto de vista, mandó una petición y obtuvo su pedido.
>
> **Eso es lo que significa idempotencia**: no que la operación se ejecute una sola
> vez, sino que **ejecutarla varias veces tenga el mismo efecto observable que
> ejecutarla una.**
>
> Y fijate la división de trabajo entre los dos niveles: **Redis es el atajo, la
> tabla es la autoridad.** Si Redis se cae, el sistema es más lento en rechazar
> duplicados y **sigue siendo correcto**. Esa asimetría vas a volver a verla en la
> clase 8, donde es una regla con nombre propio.

---

## 7.11. Herramientas de diagnóstico

**Provocar la condición de carrera** es la primera herramienta, y no es trivial:
estos problemas **no se reproducen probando a mano.** La forma de forzarlos es
lanzar peticiones concurrentes desde un script, o abrir dos sesiones de base de
datos y ejecutar los pasos manualmente en el orden de las tablas de la sección 7.2.

**Las dos sesiones a mano** son la mejor herramienta didáctica de todo el capítulo:
en una terminal se abre una transacción y se bloquea una fila; en la otra se intenta
bloquear la misma y **se ve la espera**. Después se confirma la primera y se ve
cómo la segunda avanza.

**Los registros del motor** informan los interbloqueos con detalle: qué dos
transacciones, qué recursos, y cuál fue elegida como víctima. Es la forma de
diagnosticar la sección 7.7 cuando ocurre en producción.

*(Ver Figura 7.6: un interbloqueo en los registros del motor.)*

**La vista de bloqueos** del motor muestra en tiempo real quién tiene qué bloqueado
y quién está esperando. Es lo que hay que mirar cuando el sistema "se cuelga" sin
errores.

**La verificación de reconstrucción del stock** es la comprobación de la sección
7.8: sumar los movimientos de cada producto y compararlos con su columna. **Si no
coinciden, hay un camino de escritura que no debería existir.**

> **🧪 EXPERIMENTO**
> Este es el experimento más importante del módulo y hay que hacerlo con dos
> terminales abiertas.
>
> **Parte 1 — ver la actualización perdida.**
> 1. Abrí dos clientes de base de datos contra la misma base.
> 2. En los dos, empezá una transacción y leé el stock del mismo producto. Los dos
>    ven, digamos, 1.
> 3. En los dos, escribí `stock = 0`. Confirmá los dos.
> 4. **Vendiste dos y descontaste una.** Sin error, sin aviso.
>
> **Parte 2 — ver el bloqueo funcionando.**
> 5. Repetí, pero leyendo con `SELECT ... FOR UPDATE` en los dos.
> 6. El segundo **se queda esperando**. No falla: espera.
> 7. Confirmá el primero. Mirá cómo el segundo avanza **y lee el valor nuevo**.
>
> **Parte 3 — provocar un interbloqueo.**
> 8. En la sesión A bloqueá el producto 7. En la B, el producto 3.
> 9. Ahora en A pedí el 3, y en B pedí el 7.
> 10. **Una de las dos muere**, y el motor te dice cuál y por qué en su registro.
>
> Esos diez pasos son las tres cosas que este capítulo explica en veinte páginas. Y
> el paso 4 es el que más impresiona: **no hay ningún error en ninguna parte.**

---

## 7.12. Seguridad y evolución

Cuatro consideraciones cierran el capítulo.

**Una condición de carrera es explotable.** Si un descuento de saldo o un canje de
cupón no está protegido, alguien que envía peticiones simultáneas puede canjear el
mismo cupón varias veces. No hace falta ninguna herramienta sofisticada: alcanza con
un script que dispare veinte peticiones a la vez. **Es una de las vulnerabilidades
más frecuentes y menos buscadas.**

**Un interbloqueo repetido es una denegación de servicio.** Si un endpoint se traba
consigo mismo bajo carga, cada intento mata una transacción y el sistema deja de
avanzar justo cuando más se lo necesita. Por eso RN-18 no es una recomendación de
rendimiento sino de disponibilidad.

**Un bloqueo sin plazo es una espera infinita.** Los tiempos límite del quinto
mecanismo convierten un problema indefinido en un error concreto y reintentable, y
esa es la diferencia entre un sistema que degrada y uno que se cuelga.

**El punto único de escritura es también una decisión de auditoría.** Si el stock se
puede modificar desde cinco lugares, **auditar quién lo cambió exige revisar
cinco.** Con un único punto y su registro de movimientos, la respuesta a "quién
descontó estas tres unidades y por qué" es una consulta.

Sobre la evolución, dos observaciones. La primera es que estos problemas **no
dependen del lenguaje ni del marco de trabajo**: son propiedades de acceder
concurrentemente a un recurso compartido, y aparecen igual en cualquier tecnología.
Lo aprendido acá se traslada entero.

Y la segunda es que **el bloqueo pesimista no escala indefinidamente.** En sistemas
de mucha mayor escala se usan otras estrategias —reservas con vencimiento, colas por
producto, particionado— que resignan simplicidad a cambio de concurrencia. Para el
tamaño de este sistema, el bloqueo es la respuesta correcta, y conviene saber que
existe un punto donde deja de serlo.

---

## 7.13. Verificación

1. **Provocar una actualización perdida** con dos sesiones y documentar que ninguna
   falló.
2. Repetir con bloqueo y **observar la espera** de la segunda.
3. **Provocar un interbloqueo** y leer el informe del motor: qué transacciones, qué
   recursos, cuál murió.
4. Escribir la versión incorrecta del orden verificar-bloquear y **explicar dónde
   está la ventana**.
5. Demostrar que **ordenar dentro de cada familia no alcanza**, con dos
   transacciones que empiecen por familias distintas.
6. Explicar por qué la revalidación ocurre **después** del bloqueo y no antes.
7. Verificar que el stock **se reconstruye sumando sus movimientos**.
8. Provocar un pedido con el mismo producto en dos líneas y verificar que **se
   valida contra la suma** (RN-13).
9. Reenviar la misma petición de creación con la misma clave y verificar que
   responde **`200` y no `201`**.
10. Reenviar la misma clave con un cuerpo distinto y verificar el **`422`**.

---

## 7.14. Errores frecuentes

**Verificar antes de bloquear.** Deja una ventana entre la comprobación y el
bloqueo, y esa ventana se abre justo bajo carga (sección 7.5).

**Suponer que la asincronía evita las condiciones de carrera.** Dos corrutinas sobre
dos conexiones compiten igual que dos hilos (sección 7.2).

**Suponer que el nivel de aislamiento predeterminado alcanza.** No evita la
actualización perdida: las dos transacciones leyeron un valor confirmado (sección
7.3).

**Bloquear sin un orden.** Dos transacciones que piden lo mismo en orden distinto se
traban (sección 7.7).

**Ordenar dentro de cada familia y no entre familias.** Sigue habiendo interbloqueo
si dos operaciones empiezan por familias distintas. Es la parte de RN-18 que se pasa
por alto (sección 7.7).

**Descontar el stock fuera de la transacción de la transición.** Deja un momento en
que el pedido está confirmado y el stock no descontado (sección 7.8).

**Verificar el stock línea por línea.** Un pedido con el mismo producto en dos
líneas pasa dos verificaciones que individualmente alcanzan. Viola RN-13 (sección
7.7).

**Escribir stock con un `UPDATE` directo.** El TPI lo declara **un defecto de
implementación, no una alternativa**. Rompe la reconstrucción por movimientos
(sección 7.9).

**Convertir unidades fuera del punto único.** Habría tantas conversiones como
llamadores, y basta una mal hecha (sección 7.9).

**Bloquear sin plazo límite.** Una transacción colgada bloquea las confirmaciones
indefinidamente (sección 7.5).

**Usar un bloqueo en Redis en lugar de uno de fila.** Se puede liberar mientras la
transacción sigue abierta: son dos cosas separadas (sección 7.5).

**Responder `201` a un reenvío idempotente.** La segunda vez no se creó nada
(sección 7.10).

---

## 7.15. Actividades

1. **Los cuatro fenómenos, provocados.** Con dos sesiones de base de datos, provocar
   al menos tres de los cuatro fenómenos de la sección 7.2 y documentar la secuencia
   exacta de pasos de cada uno.

2. **El bloqueo, medido.** Implementar el descuento de stock con y sin bloqueo, y
   lanzar cincuenta confirmaciones concurrentes del mismo producto con stock 10.
   Documentar cuántas prosperaron y cómo quedó el stock en cada caso.

3. **El interbloqueo entre familias.** Escribir dos operaciones que bloqueen un
   producto y un insumo en orden distinto entre familias —cada una ordenada
   internamente—, provocar el interbloqueo y capturar el informe del motor.
   Corregirlo aplicando RN-18 completa y verificar que desaparece.

4. **La reconstrucción del stock.** Escribir la consulta que suma los movimientos de
   cada producto y los compara con su columna. Provocar deliberadamente una escritura
   directa que la rompa, y verificar que la consulta la detecta.

5. **Los tres desenlaces.** Implementar la idempotencia de dos niveles y provocar los
   tres casos: reenvío legítimo, petición en curso y clave reutilizada. Documentar la
   respuesta de cada uno y por qué el código de estado es el que es.

6. **Exploración: el costo del aislamiento.** Ejecutar la misma operación bajo los
   cuatro niveles de aislamiento y documentar qué fenómenos aparecen en cada uno y
   qué transacciones aborta el nivel serializable. Relacionar lo observado con la
   decisión del TPI de la sección 7.3 de no subir el nivel global.

7. **Exploración: los dos lados de la clave.** Junto con alguien del turno de
   frontend, seguir una clave de idempotencia completa: dónde se genera, cuándo se
   persiste, cómo viaja, qué hace el servidor con ella, y cuándo se descarta.
   Provocar los tres desenlaces desde el cliente real y documentar qué ve el usuario
   en cada caso. *(Requiere coordinar con la otra mitad de la cursada.)*

---

## 7.16. Síntesis

1. El problema de este capítulo **no se reproduce probando a mano**: cada operación
   aislada es correcta, y el error aparece sólo cuando ocurren juntas.

2. **La asincronía no evita las condiciones de carrera.** La competencia no está en
   el proceso sino en la base: dos corrutinas compiten igual que dos hilos.

3. **El nivel de aislamiento predeterminado no evita la actualización perdida**,
   porque las dos transacciones leyeron un valor confirmado. El problema no es lo que
   se leyó sino que dejó de ser cierto antes de escribir.

4. El TPI usa **bloqueo pesimista** porque en este dominio los conflictos ocurren
   justo cuando importa, y **paga el costo sólo donde hace falta** en lugar de subir
   el nivel global.

5. **Primero se bloquea, después se decide.** Todo lo leído antes del bloqueo hay que
   leerlo de nuevo: ese es el cuarto mecanismo y el que más se olvida.

6. **Ordenar dentro de cada familia no alcanza.** Dos operaciones que empiezan por
   familias distintas se traban aunque cada una esté ordenada. RN-18 exige un orden
   total.

7. El orden de bloqueo es **una regla que no hace falta coordinar**: alcanza con que
   cada transacción, por su cuenta, pida las cosas en el mismo orden.

8. Las restricciones de la base son **última línea de defensa, no mecanismo de
   validación**. Valida el servicio, con un mensaje que el usuario entiende.

9. **Un bloqueo distribuido no reemplaza a uno de fila**, porque el de fila vive
   dentro de la transacción que protege y se libera exactamente con ella.

10. **La columna de stock es una conveniencia; los movimientos son la verdad.** Que
    el stock se pueda reconstruir sumando movimientos convierte una regla en algo
    verificable con una consulta.

11. La idempotencia tiene **dos niveles y tres desenlaces**: Redis como atajo
    descartable, la tabla con huella como autoridad, y un `200` —no un `201`— para el
    reenvío legítimo.

12. **Idempotencia no significa que la operación se ejecute una vez**, sino que
    ejecutarla varias tenga el mismo efecto observable que ejecutarla una.

---

## 7.17. Referencias y lecturas complementarias

Los fenómenos de concurrencia y los niveles de aislamiento están definidos en la
norma **ISO/IEC 9075**, pero la referencia útil es la documentación de **PostgreSQL**
sobre control de concurrencia, que los explica con precisión y —lo más valioso—
documenta **en qué se aparta del estándar**. Su capítulo sobre bloqueos explícitos
cubre los modos que la sección 7.5 usa, y su sección sobre interbloqueos describe el
mecanismo de detección y el criterio con que el motor elige la víctima. El artículo
de Berenson y otros *A Critique of ANSI SQL Isolation Levels* (SIGMOD, 1995) es la
mejor discusión sobre por qué los niveles del estándar están mal definidos y qué
fenómenos deja fuera; su lectura explica por qué cada motor los interpreta distinto.

Como bibliografía de estudio, el séptimo capítulo de Kleppmann, *Designing
Data-Intensive Applications* (O'Reilly, 2017) es la mejor explicación disponible de
por qué el aislamiento es difícil, y su tratamiento de la actualización perdida y de
la escritura sesgada cubre exactamente el problema de la sección 7.2. Bernstein y
Newcomer, *Principles of Transaction Processing* (2.ª edición, Morgan Kaufmann,
2009) trata el bloqueo en dos fases y el orden de adquisición con la formalidad que
la sección 7.7 aplica de manera intuitiva. Y para la idempotencia en interfaces
web, la especificación de **Idempotency-Key** en curso en el IETF documenta el
patrón de la sección 7.9 y las decisiones que otros sistemas tomaron sobre los
mismos tres desenlaces.

Del TPI, este capítulo se apoya en la sección **9** completa —con su **9.2** como
núcleo—, en la **8.1** por el flujo de creación y sus dos niveles de idempotencia,
en la **8.2** por el avance de estado, y en las **3.4** y **3.5** por la máquina de
estados y su matriz. Las reglas involucradas son **RN-01**, **RN-06** a **RN-13** y
**RN-18**.

---

**Continúa en:** Capítulo 8 — Robustez y más allá de la petición, donde lo que no
puede ocurrir dentro de la transacción encuentra su lugar, la asimetría entre Redis
y PostgreSQL se convierte en una regla con nombre propio, y el módulo cierra con lo
que lo motivó: dirigir a un agente de IA sobre una base que uno entiende.
